# Copyright (c) 2018 SwiftStack, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
import mimetypes
import os
import socket

from swift import gettext_ as _

from eventlet import Timeout

from swift import __canonical_version__ as swift_version
from swift.common import constraints
from swift.common.storage_policy import POLICIES
from swift.common import swob, utils, bufferedhttp
from swift.common.utils import cache_from_env, get_logger, \
    get_remote_client, split_path, config_true_value, generate_trans_id, \
    list_from_csv, \
    register_swift_info
from swift.proxy.controllers import InfoController
from swift.common.swob import HTTPBadRequest, HTTPForbidden, \
    HTTPMethodNotAllowed, HTTPNotFound, HTTPPreconditionFailed, \
    HTTPException, Request
from swift.common.exceptions import APIVersionError

from .utils import (
    ClosingResourceIterable, filter_hop_by_hop_headers)
from swift.proxy.controllers.base import Controller
from urlparse import urlsplit

required_filters = []


def forward_raw_swift_req(swift_baseurl, req, logger, object_chunk_size):
    # logger.info('swift_baseurl: %s' % swift_baseurl)
    scheme, netloc, _, _, _ = urlsplit(swift_baseurl)
    ssl = (scheme == 'https')
    swift_host, swift_port = utils.parse_socket_string(netloc,
                                                       443 if ssl else 80)
    swift_port = int(swift_port)
    if ssl:
        conn = bufferedhttp.HTTPSConnection(swift_host, port=swift_port)
    else:
        conn = bufferedhttp.BufferedHTTPConnection(swift_host, port=swift_port)
    conn.path = req.path_qs
    conn.putrequest(req.method, req.path_qs, skip_host=True)
    proxy_satellite_host = ''
    for header, value in filter_hop_by_hop_headers(req.headers.items()):
        if header.lower() == 'host':
            proxy_satellite_host = value
            continue
        conn.putheader(header, str(value))
    conn.putheader('Host', str(swift_host))
    conn.endheaders()

    content_length = int(req.headers.get('content-length', '0'))
    if content_length != 0:
        chunk = req.body_file.read(object_chunk_size)
        while chunk:
            conn.send(chunk)
            chunk = req.body_file.read(object_chunk_size)

    resp = conn.getresponse()
    headers = dict(filter_hop_by_hop_headers(resp.getheaders()))
    if 'x-storage-url' in headers:
        swift_scheme, swift_netloc, swift_path, _, _ = \
            urlsplit(headers['x-storage-url'])
        headers['x-storage-url'] = \
            swift_scheme+"://"+proxy_satellite_host+swift_path
    body_len = 0 if req.method == 'HEAD' \
        else int(headers.get('content-length', "0"))
    app_iter = ClosingResourceIterable(
        resource=conn, data_src=resp,
        length=body_len)
    return swob.Response(app_iter=app_iter, status=resp.status,
                         headers=headers, request=req)


class ProxySatelliteController(Controller):
    server_type = 'proxysatellite'

    def __init__(self, app, version, account_name,
                 container_name, object_name):
        super(ProxySatelliteController, self).__init__(app)

    def GETorHEADorPUTorPOSTorDELETE(self, req):
        return forward_raw_swift_req(self.app.swift_baseurl,
                                     req,
                                     self.app.logger,
                                     self.app.object_chunk_size)

    @utils.public
    def GET(self, req):
        return self.GETorHEADorPUTorPOSTorDELETE(req)

    @utils.public
    def HEAD(self, req):
        return self.GETorHEADorPUTorPOSTorDELETE(req)

    @utils.public
    def PUT(self, req):
        return self.GETorHEADorPUTorPOSTorDELETE(req)

    @utils.public
    def POST(self, req):
        return self.GETorHEADorPUTorPOSTorDELETE(req)

    @utils.public
    def DELETE(self, req):
        return self.GETorHEADorPUTorPOSTorDELETE(req)


class Application(object):
    """WSGI application for the proxy server."""

    def __init__(self, conf, memcache=None, logger=None, account_ring=None,
                 container_ring=None):
        if conf is None:
            conf = {}
        if logger is None:
            self.logger = get_logger(conf, log_route='proxy-server')
        else:
            self.logger = logger

        swift_dir = conf.get('swift_dir', '/etc/swift')
        self.swift_dir = swift_dir
        self.node_timeout = float(conf.get('node_timeout', 10))
        self.recoverable_node_timeout = float(
            conf.get('recoverable_node_timeout', self.node_timeout))
        self.conn_timeout = float(conf.get('conn_timeout', 0.5))
        self.client_timeout = int(conf.get('client_timeout', 60))
        self.put_queue_depth = int(conf.get('put_queue_depth', 10))
        self.object_chunk_size = int(conf.get('object_chunk_size', 65536))
        self.client_chunk_size = int(conf.get('client_chunk_size', 65536))
        self.trans_id_suffix = conf.get('trans_id_suffix', '')
        self.allow_account_management = \
            config_true_value(conf.get('allow_account_management', 'no'))
        self.memcache = memcache
        mimetypes.init(mimetypes.knownfiles +
                       [os.path.join(swift_dir, 'mime.types')])
        self.account_autocreate = \
            config_true_value(conf.get('account_autocreate', 'no'))
        self.deny_host_headers = [
            host.strip() for host in
            conf.get('deny_host_headers', '').split(',') if host.strip()]
        self.strict_cors_mode = config_true_value(
            conf.get('strict_cors_mode', 't'))
        value = conf.get('request_node_count', '2 * replicas').lower().split()
        if len(value) == 1:
            rnc_value = int(value[0])
            self.request_node_count = lambda replicas: rnc_value
        elif len(value) == 3 and value[1] == '*' and value[2] == 'replicas':
            rnc_value = int(value[0])
            self.request_node_count = lambda replicas: rnc_value * replicas
        else:
            raise ValueError(
                'Invalid request_node_count value: %r' % ''.join(value))
        swift_owner_headers = conf.get(
            'swift_owner_headers',
            'x-container-read, x-container-write, '
            'x-container-sync-key, x-container-sync-to, '
            'x-account-meta-temp-url-key, x-account-meta-temp-url-key-2, '
            'x-container-meta-temp-url-key, x-container-meta-temp-url-key-2, '
            'x-account-access-control')
        self.swift_owner_headers = [
            name.strip().title()
            for name in swift_owner_headers.split(',') if name.strip()]
        socket._fileobject.default_bufsize = self.client_chunk_size
        self.expose_info = config_true_value(
            conf.get('expose_info', 'yes'))
        self.disallowed_sections = list_from_csv(
            conf.get('disallowed_sections', 'swift.valid_api_versions'))
        self.admin_key = conf.get('admin_key', None)
        register_swift_info(
            version=swift_version,
            strict_cors_mode=self.strict_cors_mode,
            policies=POLICIES.get_policy_info(),
            allow_account_management=self.allow_account_management,
            account_autocreate=self.account_autocreate,
            **constraints.EFFECTIVE_CONSTRAINTS)
        self.swift_baseurl = conf.get('swift_baseurl')

    def __call__(self, env, start_response):
        """
        WSGI entry point.
        Wraps env in swob.Request object and passes it down.

        :param env: WSGI environment dictionary
        :param start_response: WSGI callable
        """
        try:
            if self.memcache is None:
                self.memcache = cache_from_env(env, True)
            req = self.update_request(Request(env))
            return self.handle_request(req)(env, start_response)
        except UnicodeError:
            err = HTTPPreconditionFailed(
                request=req, body='Invalid UTF8 or contains NULL')
            return err(env, start_response)
        except (Exception, Timeout):
            start_response('500 Server Error',
                           [('Content-Type', 'text/plain')])
            return ['Internal server error.\n']

    def update_request(self, req):
        if 'x-storage-token' in req.headers and \
                'x-auth-token' not in req.headers:
            req.headers['x-auth-token'] = req.headers['x-storage-token']
        return req

    def handle_request(self, req):
        """
        Entry point for proxy server.
        Should return a WSGI-style callable (such as swob.Response).

        :param req: swob.Request object
        """
        try:
            self.logger.set_statsd_prefix('proxy-server')
            try:
                controller, path_parts = self.get_controller(req)
            except APIVersionError:
                self.logger.increment('errors')
                return HTTPBadRequest(request=req)
            except ValueError:
                self.logger.increment('errors')
                return HTTPNotFound(request=req)
            if not controller:
                self.logger.increment('errors')
                return HTTPPreconditionFailed(request=req, body='Bad URL')
            if self.deny_host_headers and \
                    req.host.split(':')[0] in self.deny_host_headers:
                return HTTPForbidden(request=req, body='Invalid host header')

            self.logger.set_statsd_prefix('proxy-server.' +
                                          controller.server_type.lower())
            controller = controller(self, **path_parts)
            if 'swift.trans_id' not in req.environ:
                trans_id_suffix = self.trans_id_suffix
                trans_id_extra = req.headers.get('x-trans-id-extra')
                if trans_id_extra:
                    trans_id_suffix += '-' + trans_id_extra[:32]
                trans_id = generate_trans_id(trans_id_suffix)
                req.environ['swift.trans_id'] = trans_id
                self.logger.txn_id = trans_id
            req.headers['x-trans-id'] = req.environ['swift.trans_id']
            controller.trans_id = req.environ['swift.trans_id']
            self.logger.client_ip = get_remote_client(req)

            if req.method not in controller.allowed_methods:
                return HTTPMethodNotAllowed(request=req, headers={
                    'Allow': ', '.join(controller.allowed_methods)})
            handler = getattr(controller, req.method)

            old_authorize = None
            if 'swift.authorize' in req.environ:
                # We call authorize before the handler, always. If authorized,
                # we remove the swift.authorize hook so isn't ever called
                # again. If not authorized, we return the denial unless the
                # controller's method indicates it'd like to gather more
                # information and try again later.
                resp = req.environ['swift.authorize'](req)
                if not resp:
                    # No resp means authorized, no delayed recheck required.
                    old_authorize = req.environ['swift.authorize']
                else:
                    # Response indicates denial, but we might delay the denial
                    # and recheck later. If not delayed, return the error now.
                    if not getattr(handler, 'delay_denial', None):
                        return resp
            # Save off original request method (GET, POST, etc.) in case it
            # gets mutated during handling.  This way logging can display the
            # method the client actually sent.
            req.environ.setdefault('swift.orig_req_method', req.method)
            try:
                if old_authorize:
                    req.environ.pop('swift.authorize', None)
                return handler(req)
            finally:
                if old_authorize:
                    req.environ['swift.authorize'] = old_authorize
        except HTTPException as error_response:
            return error_response
        except (Exception, Timeout):
            self.logger.exception(_('ERROR Unhandled exception in request'))

    def get_controller(self, req):
        """
        Get the controller to handle a request.

        :param req: the request
        :returns: tuple of (controller class, path dictionary)

        :raises ValueError: (thrown by split_path) if given invalid path
        """
        if req.path == '/info':
            d = dict(version=None,
                     expose_info=self.expose_info,
                     disallowed_sections=self.disallowed_sections,
                     admin_key=self.admin_key)
            return InfoController, d

        version, account, container, obj = split_path(req.path, 1, 4, True)
        d = dict(version=version,
                 account_name=account,
                 container_name=container,
                 object_name=obj)
        return ProxySatelliteController, d


def app_factory(global_conf, **local_conf):
    """paste.deploy app factory for creating WSGI proxy apps."""
    conf = global_conf.copy()
    conf.update(local_conf)
    app = Application(conf)
    return app
