a="/etc/swift/proxy-server.conf"
echo $a
b="$a.bak.new"
echo $b
md5backup=$(md5sum $b | sed -e 's/\s.*$//')
echo "${md5backup}"
md5current=$(md5sum $a | sed -e 's/\s.*$//')
echo $md5current
if [ $md5backup == $md5current ]; then
  exit
fi

echo "delete previous proxy-server.conf.bak.new"
rm -rf /etc/swift/proxy-server.conf.bak.new
sleep 2s
echo "prepare a proxy-server.conf.bak.new"
cat /etc/swift/proxy-server.conf | sed 's/\<tempurl swc\>/& proxy_satellite/' >> /etc/swift/proxy-server.conf.bak.new
sleep 2s
echo '' >> /etc/swift/proxy-server.conf.bak.new
echo '[filter:proxy_satellite]' >> /etc/swift/proxy-server.conf.bak.new
echo 'use = egg:proxy_satellite#proxy_satellite' >> /etc/swift/proxy-server.conf.bak.new
echo 'account_list_path = /tmp/account_list.csv' >> /etc/swift/proxy-server.conf.bak.new
echo 'reload_time = 15' >> /etc/swift/proxy-server.conf.bak.new
echo 'proxy-server.conf.bak.new is ready'

sleep 60s
echo "$a has change more then 1 min"
echo "copy $b to $1"
cp $b $a
echo "restart proxy-server"
systemctl restart ssswift-proxy.service
echo "restart incrond"
service incrond restart
