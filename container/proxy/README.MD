### how to run
```
$ cd swift-proxy-satellite/proxy
$ docker build -t="ss-satellite:queens" .
```
```
$ docker run -i -t -d --net=host --hostname="ss-satellite-test" --name="ss-satellite-test" ss-satellite:queens
or
$ docker run -i -t -d -p 8082:8082 --hostname="ss-satellite-test" --name="ss-satellite-test" ss-satellite:queens
```
#### option, if services are not starting.
```
$ docker exec -it ss-satellite-test /bin/bash /usr/local/bin/start.sh
```
### how to test
```
$ cd ../test
$ ./integration-test.sh <your endpoint host and port e.g: http://docker.swiftstack.org:8082>
```
