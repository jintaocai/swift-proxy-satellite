echo "===stat account==="
swift -A $1/auth/v1.0 -U test -K test stat -v
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test stat account header error"
    exit 1
fi
echo "===list container==="
swift -A $1/auth/v1.0 -U test -K test list
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test list container error"
    exit 1
fi
echo "===post container==="
swift -A $1/auth/v1.0 -U test -K test post test
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test post container error"
    exit 1
fi
echo "===list container again==="
swift -A $1/auth/v1.0 -U test -K test list
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test list container again error"
    exit 1
fi
echo "===upload text.txt to container test==="
swift -A $1/auth/v1.0 -U test -K test upload test test.txt
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test upload text.txt to container test error"
    exit 1
fi
echo "===list object in test container==="
swift -A $1/auth/v1.0 -U test -K test list test
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test list object in test container error"
    exit 1
fi
echo "===add metadata in object test.txt==="
swift -A $1/auth/v1.0 -U test -K test post test test.txt --meta testkey:testvalue
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test add metadata in object test.txt error"
    exit 1
fi
echo "===show metadata in object==="
swift -A $1/auth/v1.0 -U test -K test stat -v test test.txt
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test show metadata in object error"
    exit 1
fi
echo "===download object test.txt==="
swift -A $1/auth/v1.0 -U test -K test download test test.txt
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test download object test.txt error"
    exit 1
fi
echo "===delete object test.txt in container test==="
swift -A $1/auth/v1.0 -U test -K test delete test test.txt
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete object test.txt in container test error"
    exit 1
fi
echo "===dlo upload bbb_sunflower_1080_2min.mp4"
swift -A $1/auth/v1.0 -U test -K test post test_dlo
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test post dlo container test_dlo error"
    exit 1
fi
swift -A $1/auth/v1.0 -U test -K test upload test_dlo -S 10485760 ./samples/bbb_sunflower_1080_2min.mp4 --object-name bbb_sunflower_1080_2min.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test dlo upload bbb_sunflower_1080_2min.mp4 error"
    exit 1
fi
echo "===list dlo bbb_sunflower_1080_2min.mp4"
swift -A $1/auth/v1.0 -U test -K test list test_dlo
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test list dlo bbb_sunflower_1080_2min.mp4 error"
    exit 1
fi
echo "===list dlo segments bbb_sunflower_1080_2min.mp4"
swift -A $1/auth/v1.0 -U test -K test list test_dlo_segments
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test list dlo segments bbb_sunflower_1080_2min.mp4 error"
    exit 1
fi
echo "===show dlo bbb_sunflower_1080_2min.mp4 metadata"
swift -A $1/auth/v1.0 -U test -K test stat -v test_dlo bbb_sunflower_1080_2min.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test show dlo bbb_sunflower_1080_2min.mp4 metadata error"
    exit 1
fi
echo "===delete dlo bbb_sunflower_1080_2min.mp4 metadata"
swift -A $1/auth/v1.0 -U test -K test delete test_dlo bbb_sunflower_1080_2min.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete dlo bbb_sunflower_1080_2min.mp4 metadata error"
    exit 1
fi
#echo "===check md5sum for bbb_sunflower_1080_2min.mp4"
# beforemd5=$(md5sum ./samples/bbb_sunflower_1080_2min.mp4 | awk '{print $1}')
#beforemd5=$(md5 ./samples/bbb_sunflower_1080_2min.mp4 | awk '{print $4}')
#echo $beforemd5

echo "===preparation create slo and slo_segments containers==="
swift -A $1/auth/v1.0 -U test -K test post slo
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test post slo container slo error"
    exit 1
fi
swift -A $1/auth/v1.0 -U test -K test post slo_segments
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test post slo segment container test_slo error"
    exit 1
fi
echo "===upload test slo 3 segments object==="
swift -A $1/auth/v1.0 -U test -K test upload slo_segments ./samples/bbb_sunflower_1080_2min_001.mp4 --object-name bbb_sunflower_1080_2min_001.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test upload slo 1st segments bbb_sunflower_1080_2min_001.mp4 object error"
    exit 1
fi
swift -A $1/auth/v1.0 -U test -K test upload slo_segments ./samples/bbb_sunflower_1080_2min_002.mp4 --object-name bbb_sunflower_1080_2min_002.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test upload slo 2nd segments bbb_sunflower_1080_2min_002.mp4 object error"
    exit 1
fi
swift -A $1/auth/v1.0 -U test -K test upload slo_segments ./samples/bbb_sunflower_1080_2min_003.mp4 --object-name bbb_sunflower_1080_2min_003.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test upload slo 3rd segments bbb_sunflower_1080_2min_003.mp4 object error"
    exit 1
fi
echo "===get token==="
auth_token=$(swift -A $1/auth/v1.0 -U test -K test auth | grep "export OS_AUTH_TOKEN=" | awk -F"=" '{print $2}')
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test get token error"
    exit 1
fi
echo $auth_token
echo "===upload test slo manifest object==="
curl -H "X-Auth-Token: $auth_token" -v -X PUT $1/v1/AUTH_test/slo/bbb_sunflower_1080_2min.mp4?multipart-manifest=put -d '[{"path":"slo_segments/bbb_sunflower_1080_2min_001.mp4","etag":"07b81cd438af5097d584321ab99cdc06","size_bytes":10485760},{"path":"slo_segments/bbb_sunflower_1080_2min_002.mp4","etag":"ff53521cfdfe801ab1e52d0e7fda4969","size_bytes":10485760},{"path":"slo_segments/bbb_sunflower_1080_2min_003.mp4","etag":"e924eaf1e2171ff355c588fa84da5778","size_bytes":6911647}]'
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test curl pload test slo manifest object bbb_sunflower_1080_2min.mp4?multipart-manifest=put error"
    exit 1
fi
echo "===check slo metadata==="
swift -A $1/auth/v1.0 -U test -K test stat -v slo bbb_sunflower_1080_2min.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test check slo metadata error"
    exit 1
fi
echo "***===trigger slomd5 via GET and ?multipart-manifest=get===***"
curl -H "X-Auth-Token: $auth_token" -v -X GET $1/v1/AUTH_test/slo/bbb_sunflower_1080_2min.mp4?multipart-manifest=get
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test get slo object manifest bbb_sunflower_1080_2min.mp4?multipart-manifest=get error"
    exit 1
fi
echo "\n"

#echo "===check metadata again , has X-Object-Meta-Slomd5==="
#swift -A $1/auth/v1.0 -U test -K test stat -v slo bbb_sunflower_1080_2min.mp4

#echo "===get Slomd5==="
#metamd5=$(swift -A $1/auth/v1.0 -U test -K test stat -v slo bbb_sunflower_1080_2min.mp4 | grep Slomd5 | awk '{print $3}')
#echo $metamd5

echo "===regression test for list the object by account==="
swift -A $1/auth/v1.0 -U test -K test list
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: regression test for list the object by account error"
    exit 1
fi

echo "===regression test for list the objects in slo container==="
swift -A $1/auth/v1.0 -U test -K test list slo
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: regression test for list the objects in slo container error"
    exit 1
fi

echo "===regression test for download the object to name bbb_sunflower_1080_2min.mp4.download==="
swift -A $1/auth/v1.0 -U test -K test download slo bbb_sunflower_1080_2min.mp4 --output bbb_sunflower_1080_2min.mp4.download
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: regression test for download the object to name bbb_sunflower_1080_2min.mp4.download error"
    exit 1
fi

#echo "===check md5sum for bbb_sunflower_1080_2min.mp4.download==="
#aftermd5=$(md5sum ./bbb_sunflower_1080_2min.mp4.download | awk '{print $1}')
#aftermd5=$(md5 ./samples/bbb_sunflower_1080_2min.mp4 | awk '{print $4}')
#echo $aftermd5

echo "===delete the slo object - wipeout manifest and segments objects==="
swift -A $1/auth/v1.0 -U test -K test delete slo bbb_sunflower_1080_2min.mp4
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete the slo object - wipeout manifest and segments objects error"
    exit 1
fi
echo "===delete slo container==="
swift -A $1/auth/v1.0 -U test -K test delete slo
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete slo containe error"
    exit 1
fi
echo "===delete slo_segments container==="
swift -A $1/auth/v1.0 -U test -K test delete slo_segments
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete slo_segments container error"
    exit 1
fi
echo "===delete test dlo container==="
swift -A $1/auth/v1.0 -U test -K test delete test_dlo
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete test dlo container error"
    exit 1
fi
echo "===delete test_dlo_segments container==="
swift -A $1/auth/v1.0 -U test -K test delete test_dlo_segments
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete test_dlo_segments container error"
    exit 1
fi
echo "===delete test container==="
swift -A $1/auth/v1.0 -U test -K test delete test
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete test container error"
    exit 1
fi
echo "===delete download object==="
rm -rf ./bbb_sunflower_1080_2min.mp4.download
result=$?
if [ $result -ne 0 ]; then
    echo "ERROR: test delete download object bbb_sunflower_1080_2min.mp4.download error"
    exit 1
fi
