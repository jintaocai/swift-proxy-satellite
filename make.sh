# if swiftstack swift node /opt/ss/bin
# install required binaries
pip install -r requirements.txt
# python setup.py install
python ./setup.py sdist
# pip install ./dist/proxy_satellite-0.0.1.tar.gz --upgrade
pip install ./dist/proxy_satellite-0.0.1.tar.gz
swift-init proxy-server restart
# systemctl restart ssnoded.service
tail -f /var/log/swift/proxy_access.log
