echo $1
b="$1.bak"
echo $b
md5backup=$(md5sum $b | sed -e 's/\s.*$//')
echo "${md5backup}"
md5current=$(md5sum $1 | sed -e 's/\s.*$//')
echo $md5current
if [ $md5backup == $md5current ]; then
  exit
fi

filemtime=`stat -c %Y $1`
echo $filemtime
currtime=`date +%s`
echo $currtime
diff=$(( (currtime - filemtime)  ))
echo $diff
fivemin=300
if [ $diff -gt $fivemin ]; then
  echo "$1 has change more then 5 min"
  echo "copy $b to $1"
  cp $b $1
  echo "restart proxy-server"
  systemctl restart ssswift-proxy.service
fi

