### setup integration test paco
REF: https://github.com/swiftstack/docker-swiftstack-connectors/tree/master/paco-ss

### how to test
```
$ cd ../test
$ ./integration-test-8081.sh
===stat account===
                     StorageURL: http://127.0.0.1:8081/v1/AUTH_test
                     Auth Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
                        Account: AUTH_test
                     Containers: 0
                        Objects: 0
                          Bytes: 0
Containers in policy "policy-0": 0
   Objects in policy "policy-0": 0
     Bytes in policy "policy-0": 0
                  Accept-Ranges: bytes
                    X-Timestamp: 1520362676.23257
                     X-Trans-Id: txeafb735870fd4a98a267f-005ac3ca55
                   Content-Type: application/json; charset=utf-8
         X-Openstack-Request-Id: txeafb735870fd4a98a267f-005ac3ca55
===list container===
===post container===
===list container again===
test
===upload text.txt to container test===
test.txt
===list object in test container===
test.txt
===add metadata in object test.txt===
===show metadata in object===
                   URL: http://127.0.0.1:8081/v1/AUTH_test/test/test.txt
            Auth Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
               Account: AUTH_test
             Container: test
                Object: test.txt
          Content Type: None
        Content Length: 98
         Last Modified: Tue, 03 Apr 2018 18:39:20 GMT
                  ETag: dc5b4de3752beebcc2d7264af3ee4b11
          Meta Testkey: testvalue
         Accept-Ranges: bytes
           X-Timestamp: 1522780759.95141
            X-Trans-Id: tx9b729a1d775f4b0cb351a-005ac3ca58
X-Openstack-Request-Id: tx9b729a1d775f4b0cb351a-005ac3ca58
===download object test.txt===
test.txt [auth 0.065s, headers 0.078s, total 0.082s, 0.006 MB/s]
===delete object test.txt in container test===
test.txt
===dlo upload bbb_sunflower_1080_2min.mp4
bbb_sunflower_1080_2min.mp4 segment 0
bbb_sunflower_1080_2min.mp4 segment 2
bbb_sunflower_1080_2min.mp4 segment 1
bbb_sunflower_1080_2min.mp4
===list dlo  bbb_sunflower_1080_2min.mp4
bbb_sunflower_1080_2min.mp4
===list dlo segments bbb_sunflower_1080_2min.mp4
bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/00000000
bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/00000001
bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/00000002
===show dlo bbb_sunflower_1080_2min.mp4 metadata
                   URL: http://127.0.0.1:8081/v1/AUTH_test/test_dlo/bbb_sunflower_1080_2min.mp4
            Auth Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
               Account: AUTH_test
             Container: test_dlo
                Object: bbb_sunflower_1080_2min.mp4
          Content Type: video/mp4
        Content Length: 27883167
         Last Modified: Tue, 03 Apr 2018 18:39:23 GMT
                  ETag: "215729ecb16ddc52e240f10d04b7751d"
              Manifest: test_dlo_segments/bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/
            Meta Mtime: 1522445393.000000
         Accept-Ranges: bytes
           X-Timestamp: 1522780762.77258
            X-Trans-Id: tx53d5e203092846c7b4309-005ac3ca5b
X-Openstack-Request-Id: tx53d5e203092846c7b4309-005ac3ca5b
===delete dlo bbb_sunflower_1080_2min.mp4 metadata
test_dlo_segments/bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/00000000
test_dlo_segments/bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/00000002
test_dlo_segments/bbb_sunflower_1080_2min.mp4/1522445393.000000/27883167/10485760/00000001
bbb_sunflower_1080_2min.mp4
===check md5sum for bbb_sunflower_1080_2min.mp4
ee54e072da4a66478a187ba834a0d56a
===preparation create slo and slo_segments containers===
===upload test slo 3 segments object===
bbb_sunflower_1080_2min_001.mp4
bbb_sunflower_1080_2min_002.mp4
bbb_sunflower_1080_2min_003.mp4
===get token===
AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
===upload test slo manifest object===
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8081 (#0)
> PUT /v1/AUTH_test/slo/bbb_sunflower_1080_2min.mp4?multipart-manifest=put HTTP/1.1
> Host: 127.0.0.1:8081
> User-Agent: curl/7.47.0
> Accept: */*
> X-Auth-Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
> Content-Length: 360
> Content-Type: application/x-www-form-urlencoded
>
* upload completely sent off: 360 out of 360 bytes
< HTTP/1.1 201 Created
< Content-Length: 0
< Last-Modified: Tue, 03 Apr 2018 18:39:28 GMT
< Etag: "215729ecb16ddc52e240f10d04b7751d"
< X-Trans-Id: tx4987943d7dcd454d9fb9f-005ac3ca5f
< Date: Tue, 03 Apr 2018 18:39:27 GMT
< Content-Type: text/html; charset=UTF-8
< X-Openstack-Request-Id: tx4987943d7dcd454d9fb9f-005ac3ca5f
<
* Connection #0 to host 127.0.0.1 left intact
===check metadata no X-Object-Meta-Slomd5===
                   URL: http://127.0.0.1:8081/v1/AUTH_test/slo/bbb_sunflower_1080_2min.mp4
            Auth Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
               Account: AUTH_test
             Container: slo
                Object: bbb_sunflower_1080_2min.mp4
### how to run
          Content Type: application/x-www-form-urlencoded
        Content Length: 27883167
         Last Modified: Tue, 03 Apr 2018 18:39:28 GMT
                  ETag: "215729ecb16ddc52e240f10d04b7751d"
         Accept-Ranges: bytes
           X-Timestamp: 1522780767.85552
            X-Trans-Id: txa24c9a3bf5ff44709a5be-005ac3ca60
 X-Static-Large-Object: True
X-Openstack-Request-Id: txa24c9a3bf5ff44709a5be-005ac3ca60
***===trigger slomd5 via GET and ?multipart-manifest=get===***
Note: Unnecessary use of -X or --request, GET is already inferred.
*   Trying 127.0.0.1...
* Connected to 127.0.0.1 (127.0.0.1) port 8081 (#0)
> GET /v1/AUTH_test/slo/bbb_sunflower_1080_2min.mp4?multipart-manifest=get HTTP/1.1
> Host: 127.0.0.1:8081
> User-Agent: curl/7.47.0
> Accept: */*
> X-Auth-Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
>
< HTTP/1.1 200 OK
< Content-Length: 593
< Accept-Ranges: bytes
< Last-Modified: Tue, 03 Apr 2018 18:39:28 GMT
< Etag: ca2e9ecc35b346d18f3fc4a33690e211
< X-Timestamp: 1522780767.85552
< X-Trans-Id: txaaa8b39e6edf4982af665-005ac3ca60
< Date: Tue, 03 Apr 2018 18:39:28 GMT
< X-Static-Large-Object: True
< Content-Type: application/json; charset=utf-8
< X-Openstack-Request-Id: txaaa8b39e6edf4982af665-005ac3ca60
<
* Connection #0 to host 127.0.0.1 left intact
[{"hash": "07b81cd438af5097d584321ab99cdc06", "last_modified": "2018-04-03T18:39:26.000000", "bytes": 10485760, "name": "/slo_segments/bbb_sunflower_1080_2min_001.mp4", "content_type": "video/mp4"}, {"hash": "ff53521cfdfe801ab1e52d0e7fda4969", "last_modified": "2018-04-03T18:39:27.000000", "bytes": 10485760, "name": "/slo_segments/bbb_sunflower_1080_2min_002.mp4", "content_type": "video/mp4"}, {"hash": "e924eaf1e2171ff355c588fa84da5778", "last_modified": "2018-04-03T18:39:28.000000", "bytes": 6911647, "name": "/slo_segments/bbb_sunflower_1080_2min_003.mp4", "content_type": "video/mp4"}]\n
===check metadata again , has X-Object-Meta-Slomd5===
                   URL: http://127.0.0.1:8081/v1/AUTH_test/slo/bbb_sunflower_1080_2min.mp4
            Auth Token: AUTH_tkdb81d51e8b82471ebfc250bd64e23c91
               Account: AUTH_test
             Container: slo
                Object: bbb_sunflower_1080_2min.mp4
          Content Type: application/x-www-form-urlencoded
        Content Length: 27883167
         Last Modified: Tue, 03 Apr 2018 18:39:28 GMT
                  ETag: "215729ecb16ddc52e240f10d04b7751d"
         Accept-Ranges: bytes
           X-Timestamp: 1522780767.85552
            X-Trans-Id: tx9a78605594584b9ea8e15-005ac3ca60
 X-Static-Large-Object: True
X-Openstack-Request-Id: tx9a78605594584b9ea8e15-005ac3ca60
===regression test for list the object by account===
slo
slo_segments
test
test_dlo
test_dlo_segments
===regression test for list the objects in slo container===
bbb_sunflower_1080_2min.mp4
===regression test for download the object to name bbb_sunflower_1080_2min.mp4.download===
bbb_sunflower_1080_2min.mp4 [auth 0.062s, headers 0.084s, total 0.556s, 56.415 MB/s]
===check md5sum for bbb_sunflower_1080_2min.mp4.download===
ee54e072da4a66478a187ba834a0d56a
===delete the object - wipeout manifest and segments objects===
bbb_sunflower_1080_2min.mp4
===delete slo container===
slo
===delete slo_segments container===
slo_segments
===delete test dlo container===
test_dlo
===delete test_dlo_segments container===
test_dlo_segments
===delete test container===
test
===delete the object - wipeout manifest and segments objects===
===delete download object===
```
