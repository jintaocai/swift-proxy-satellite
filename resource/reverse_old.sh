a="/etc/swift/proxy-server.conf"
echo $a
b="$a.bak"
echo $b
md5backup=$(md5sum $b | sed -e 's/\s.*$//')
echo "${md5backup}"
md5current=$(md5sum $a | sed -e 's/\s.*$//')
echo $md5current
if [ $md5backup == $md5current ]; then
  exit
fi

sleep 60s
echo "$a has change more then 1 min"
echo "copy $b to $1"
cp $b $a
echo "restart proxy-server"
systemctl restart ssswift-proxy.service
echo "restart incrond"
service incrond restart
