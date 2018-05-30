#### refresh deploy update for proxy-sattelite node via bash script + cron
```
$ ./refresh.sh /etc/swift/proxy-server.conf
```

### reverse deploy update for proxy-sattelite node via incron

#### setup incron
First we will need to install incron:
```
$ sudo yum install incron
```

PS if your CentOS can't find the incron repo, try as below.
```
Type the following command as root user to install repo:
# rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm

OR use the following command:
# yum install epel-release.noarch
```

Make sure we set it to start on reboot:
```
$ sudo chkconfig incrond on
```

And now to start incron:
```
$ sudo service incrond start
```

#### configure incron
```
# incrontab -l
no table for root

# vi /etc/incron.conf
Add first systoles
# system_table_dir = /var/spool/incron.systables
system_table_dir = /etc/incron.d/proxy.systable

Add Second editor
# editor = nano
editor = vi
```

#### Adding `reverse.sh` from resource folder in this repo
 * I put the `reverse.sh` under `/opt/ss/support/` 
 * `a` is your proxy-server.conf location and `b` is your `proxy-server.conf.bak` full path.
 * I detect md5 change and wait 60 seconds
```
# vi /opt/ss/support/reverse.sh
a="/etc/swift/proxy-server.conf"
echo $a
b="$a.bak"
echo $b
...
sleep 60s
```

#### Adding incron monitor file and execution script locaiton
```
# incrontab -e for adding the line as below
/etc/swift/proxy-server.conf IN_MODIFY /opt/ss/support/reverse.sh
# incrontab -e
table updated

# incrontab -l
/etc/swift/proxy-server.conf IN_MODIFY /opt/ss/support/reverse.sh
```

#### Trouble Shoot, whenever /etc/swift/proxy-server.conf changes, incron will trigger `/opt/ss/support/reverse.sh`
```
# tail -f /var/log/cron
May 30 11:01:46 JW-swift-demo-proxyonly incrond[24117]: (root) CMD (/opt/ss/support/reverse.sh)
```
