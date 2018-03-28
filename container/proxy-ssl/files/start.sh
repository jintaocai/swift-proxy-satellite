#!/bin/bash

#service supervisor restart
# Start supervisord
echo "start rsyslog"
/etc/init.d/rsyslog start
echo "Starting supervisord..."
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
echo "start proxy server"
swift-init start proxy-server
echo "start hitch"
service hitch start
