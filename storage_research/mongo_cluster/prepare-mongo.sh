docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}]})" | mongo'

docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}]})" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongo'

docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}]})" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongo'

docker exec -it mongors1n1 bash -c 'echo "use someDb" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"someDb\")" | mongo'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"someDb.someCollection\")" | mongo'
docker exec -it mongos1 bash -c 'echo "db.someDb.someCollection.ensureIndex({user_id: 1})" | mongo'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"someDb.someCollection\", {\"user_id\": 1})" | mongo'