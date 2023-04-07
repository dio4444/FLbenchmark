#!/bin/bash
CONTAINER_ID=`docker ps -aqf "name=fate_python"`
self.conf=``
sudo docker exec -it ${CONTAINER_ID} bash -c "python /fate/python/fate_flow/fate_flow_client.py -f upload -c ${self.conf}"
