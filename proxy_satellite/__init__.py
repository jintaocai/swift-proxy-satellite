# Copyright (c) 2018 SwiftStack, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
from swift.common.utils import get_logger
from swift.common.wsgi import WSGIContext
from webob import Request
from webob.exc import HTTPUnauthorized
from os.path import getmtime, exists
from time import time


class ProxySatelliteMiddleware(WSGIContext):
    """
    SwiftStack CUD Blocker system.
    Add to your pipeline in proxy-server.conf, such as::
        [pipeline:main]
        pipeline = ... proxy_satellite ... proxy-server
    And add a proxy_satellite filter section, such as::
        [filter:proxy_satellite]
        use = egg:proxy_satellite#proxy_satellite
        account_list_path = /tmp/account_list.csv
        reload_time = 15
    ps: you can deside your ownaccount_list_path 
    """
    def __init__(self, app, conf):
        self.app = app
        self.logger = get_logger(conf, log_route='proxy_satellite')
        self.account_list_path = conf['account_list_path']
        self.reload_time = int(conf.get('reload_time', '15'))
        self._rtime = 0
        self._mtime = 0
        self.account_list = []
        if exists(self.account_list_path):
            # blow up early if account list exists but is invalid
            self._reload(force=True)

    def _load_account_file(self):
        account_list = [line.rstrip('\n') for line in open(
            self.account_list_path)]
        return account_list

    def _has_changed(self):
        """
        Check to see if the account_list on disk m_time is different than
        the current one in memory.
        :returns: True if the account_list on disk has changed, False otherwise
        """
        return getmtime(self.account_list_path) != self._mtime

    def _reload(self, force=False):
        self._rtime = time() + self.reload_time
        if force or self._has_changed():
            self.logger.info('%s changed. Reloading.' % self.account_list_path)
            self._mtime = getmtime(self.account_list_path)
            self.account_list = self._load_account_file()

    def __call__(self, env, start_response):
        if time() > self._rtime:
            self._reload()
        req = Request(env)
        account = env.get('HTTP_X_AUTH_USER')
        token = env.get('HTTP_X_AUTH_TOKEN', env.get('HTTP_X_STORAGE_TOKEN'))

        # check only 1st request
        # 2nd request will use token
        if token is None:
            # if can't get account, then try swift3
            if account is None:
                s = env.get('HTTP_AUTHORIZATION')
                #self.logger.info('s is %' % s)
                x = [x.strip() for x in s.split(':')]
                y = str(x[0]).split(' ')
                #self.logger.info('y[0] is %' % str(y[0]))
                if y[0] == "AWS":
                    account = y[1]
                    #self.logger.info('account for S3 v2 is %' % account)
                elif y[0] == "AWS4-HMAC-SHA256":
                    z = str(y[1].split("Credential=")[1])
                    account = z.split("/")[0]
                    #self.logger.info('account for S3 v4 is %' % str(account))
            if (account not in self.account_list):
                self.logger.info('%s is not allow to get token' % account)
                resp = HTTPUnauthorized(request=req,
                                        body="Account not in list")
                return resp(env, start_response)
            else:
                self.logger.info('%s is in account list and allow to get token' % account)
                return self.app(env, start_response)
        else:
            return self.app(env, start_response)


def filter_factory(global_conf, **local_conf):
    conf = global_conf.copy()
    conf.update(local_conf)

    def proxy_satellite(app):
        return ProxySatelliteMiddleware(app, conf)
    return proxy_satellite
