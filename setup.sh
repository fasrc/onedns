DOCKER_MACHINE="default"
DOCKER_MACHINE_STATUS=$(docker-machine status ${DOCKER_MACHINE} 2>/dev/null)
if [ -z ${DOCKER_MACHINE_STATUS} ]; then
  docker-machine create ${DOCKER_MACHINE}
elif [ ${DOCKER_MACHINE_STATUS} != "Running" ]; then
  docker-machine start $DOCKER_MACHINE
fi
eval "$(docker-machine env ${DOCKER_MACHINE})"
DOCKER_HOST_IP=$(docker-machine ip ${DOCKER_MACHINE})
ETCD_PORT=2379
ETCD_SKYDNS_BASEURL="http://${DOCKER_HOST_IP}:${ETCD_PORT}/v2/keys/skydns"
ETCD_SKYDNS_ARPAURL="${ETCD_SKYDNS_BASEURL}/arpa/in-addr"
ETCD_DATA_DIR="/tmp/data"
DNS_PORT=53
docker-machine ssh ${DOCKER_MACHINE} sudo mkdir -p ${ETCD_DATA_DIR}
docker run -d --name etcd -v ${ETCD_DATA_DIR}:/data -p ${ETCD_PORT}:${ETCD_PORT} quay.io/coreos/etcd:v2.3.2 --listen-client-urls http://0.0.0.0:${ETCD_PORT} --advertise-client-urls http://0.0.0.0:${ETCD_PORT} --data-dir /data
docker run -d --name skydns -p ${DNS_PORT}:${DNS_PORT} -p ${DNS_PORT}:${DNS_PORT}/udp --link etcd:etcd skynetservices/skydns:2.5.3a -machines http://etcd:${ETCD_PORT} -addr 0.0.0.0:${DNS_PORT} -no-rec
# skydns configuration
curl -XPUT ${ETCD_SKYDNS_BASEURL}/config -d value='{"domain": "cloud.rc.fas.harvard.edu"}'
# add a test CNAME
curl -XPUT ${ETCD_SKYDNS_BASEURL}/edu/harvard/fas/rc/cloud/test -d value='{"host": "10.242.77.177"}'
# add corresponding PTR
curl -XPUT ${ETCD_SKYDNS_ARPAURL}/10/242/77/177 -d value='{"host": "test.cloud.rc.fas.harvard.edu"}'

nslookup test.cloud.rc.fas.harvard.edu ${DOCKER_HOST_IP}
