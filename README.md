# swift-proxy-satellite
This is a repo for filter by account list and convert endpoint FQDN via proxy mc

 * [x] Provide swift proxy satellite for swift RESTful API / Curl Commands.
 * [x] Provide swift proxy satellite for amazon s3 API.

# Setup swift-proxy-satellite via containers
 * proxy server with ssl: https://github.com/swiftstack/swift-proxy-satellite/tree/master/container/proxy-ssl
 * proxy server without ssl: https://github.com/swiftstack/swift-proxy-satellite/tree/master/container/proxy

# Integration Test Swift-Proxy-Satellite Container
 * Setup paco container for taking request - https://github.com/swiftstack/docker-swiftstack-connectors/tree/master/paco-ss
   * default user/password: `test/test`
 * Setup swift-proxy-satellite container - check container/proxy-ssl or container/proxy
 * run integration script
 ```
 $ cd test
 $ ./integration-test.sh https://docker.swiftstack.org
 $ ./integration-test.sh http://docker.swiftstack.org:8082
 ```
 * you can run command as below to jump into containers (paco or swift-proxy-satellite containers) and tail `/var/log/swift/proxy_access.log`
 ```
 e.g
 $ docker exec -it <your container name> /bin/bash
 $ tail -f /var/log/swift/proxy_access.log
 ```

# PS: proxy-satellite white list filter middleware from souce code
 * while list filter code: https://github.com/swiftstack/swift-proxy-satellite/tree/master/proxy_satellite
 * setup is run `pip install -r requirements.txt && python setup.py sdist && pip install dist/proxy_satellite-0.0.1.tar.gz`
