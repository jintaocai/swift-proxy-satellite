### how to run
```
$ cd swift-proxy-satellite/proxy
$ docker build -t="ss-satellite-ssl:queens" .
```
```
$ docker run -i -t -d --net=host --hostname="ss-satellite-ssl-test" --name="ss-satellite-ssl-test" ss-satellite-ssl:queens
or
$ docker run -i -t -d -p :8081:8081 --hostname="ss-satellite-ssl-test" --name="ss-satellite-ssl-test" ss-satellite-ssl:queens
```
#### option, if services are not starting.
```
$ docker exec -it ss-satellite-ssl-test /bin/bash /usr/local/bin/start.sh
```
### how to test
```
$ cd ../test
$ ./integration-test.sh <your endpoint server and port e.g: https//docker.swiftstack.org>
```

### PS: Dockerfile preparation
 * concate key and crt into pem and move to ./files
 ```
 $ cat ssl.key ssl.crt >> ssl.pem
 ```
 * update dns in /etc/hosts file, replace `192.168.201.153` and `johnny.swiftstack.org` to your swift endpoint ip and hostname.
 ```
 ENTRYPOINT ["/bin/sh", "-c" , "echo 192.168.201.153   johnny.swiftstack.org >> /etc/hosts ...
 ```
 * update ssl endpoint in /etc/swift/proxy-server.conf, replace `https://johnny.swiftstack.org` to your endpoint
 ```
 set swift_baseurl = https://johnny.swiftstack.org
 ```
