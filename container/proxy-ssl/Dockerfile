FROM ubuntu:16.04
#CMD /bin/bash
MAINTAINER Johnny Wang <chianingwang@hotmail.com>

# Install repository  for latest version of swift installation
RUN apt-get update && apt-get install -y ntp vim rsyslog ubuntu-cloud-keyring software-properties-common python-pip
#RUN sudo echo "deb http://ubuntu-cloud.archive.canonical.com/ubuntu" "xenial-updates/newton main" > /etc/apt/sources.list.d/cloudarchive-newton.list
RUN add-apt-repository cloud-archive:queens -y
RUN apt-get update && apt-get dist-upgrade -y

# Install supervisor for handling sub-process of swift
RUN apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
ADD files/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Add disperson file for tempauth
# ADD files/dispersion.conf /etc/swift/dispersion.conf

# Install swift packages
RUN mkdir -p /etc/swift
RUN apt-get install -y swift swift-proxy python-swiftclient python-keystoneclient memcached
ADD files/proxy-server.conf /etc/swift/proxy-server.conf
ADD files/swift.conf /etc/swift/swift.conf

# Add logging required configuration files
ADD files/0-swift.conf /etc/rsyslog.d/0-swift.conf
ADD files/50-default.conf /etc/rsyslog.d/50-default.conf
ADD files/rsyslog.conf /etc/rsyslog.conf

# Replace /usr/lib/python2.7/dist-packages/swift/proxy/server.py
ADD files/server.py /usr/lib/python2.7/dist-packages/swift/proxy/server.py

# Add /usr/lib/python2.7/dist-packages/swift/proxy/utili.py
ADD files/utils.py /usr/lib/python2.7/dist-packages/swift/proxy/utils.py


# Add swift-proxy-satellite
COPY files/swift-proxy-satellite /tmp/swift-proxy-satellite
RUN ls /tmp/swift-proxy-satellite && cd /tmp/swift-proxy-satellite && pip install -r requirements.txt && python setup.py sdist
RUN ls /tmp/swift-proxy-satellite/dist && cd /tmp/swift-proxy-satellite/dist && pip install proxy_satellite-0.0.1.tar.gz

# Copy account white list
COPY files/account_list.csv /tmp/account_list.csv

# Build ssl front-end
RUN apt-get install -y git libev-dev libssl-dev automake python-docutils flex bison pkg-config hitch
#RUN git clone https://github.com/varnish/hitch.git
#RUN cd hitch && ./bootstrap && ./configure && make && make install
COPY files/hitch.conf /etc/hitch/hitch.conf
COPY files/ssl.pem /etc/hitch/ssl.pem

# Permission for swift
RUN chown -R swift:swift /etc/swift
RUN service supervisor restart

# Add start.sh
ADD files/start.sh /usr/local/bin/start.sh
RUN chmod 755 /usr/local/bin/start.sh
CMD /usr/local/bin/start.sh

# expose 8081
EXPOSE 8081

ENTRYPOINT ["/bin/sh", "-c" , "echo 192.168.201.153   johnny.swiftstack.org >> /etc/hosts && /usr/local/bin/start.sh && /bin/bash"]
#ENTRYPOINT /usr/local/bin/start.sh && /bin/bash
