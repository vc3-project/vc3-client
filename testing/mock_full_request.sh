#! /bin/sh

requestid=MY_REQUEST
owner=jhover
config=/etc/vc3/vc3-client.conf

echo vc3-client -c ${config} user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
vc3-client -c ${config} user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover

echo vc3-client -c ${config} resource-create --owner ${owner} --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost resource.org --accessport 1234 RESOURCE_1
vc3-client -c ${config} resource-create --owner ${owner} --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost resource.org --accessport 1234 RESOURCE_1

echo vc3-client -c ${config} resource-create --owner ${owner} --accesstype batch --accessmethod ssh --accessflavor sge --accesshost otherresource.org --accessport 1234 RESOURCE_2
vc3-client -c ${config} resource-create --owner ${owner} --accesstype batch --accessmethod ssh --accessflavor sge --accesshost otherresource.org --accessport 1234 RESOURCE_2

echo vc3-client -c ${config} allocation-create --owner ${owner} --resource RESOURCE_1 --accountname vc3-${owner} ALLOCATION_1
vc3-client -c ${config} allocation-create --owner ${owner} --resource RESOURCE_1 --accountname vc3-${owner} ALLOCATION_1

echo vc3-client -c ${config} allocation-create --owner ${owner} --resource RESOURCE_2 --accountname vc3-${owner} ALLOCATION_2
vc3-client -c ${config} allocation-create --owner ${owner} --resource RESOURCE_2 --accountname vc3-${owner} ALLOCATION_2

echo vc3-client -c ${config} nodeset-create --owner ${owner} --node_number 1 --app_type APP_TYPE --app_role APP_ROLE NODESET_1
vc3-client -c ${config} nodeset-create --owner ${owner} --node_number 1 --app_type APP_TYPE --app_role APP_ROLE NODESET_1

echo vc3-client -c ${config} cluster-create --owner ${owner} --nodesets NODESET_1 CLUSTER_1
vc3-client -c ${config} cluster-create --owner ${owner} --nodesets NODESET_1 CLUSTER_1

echo vc3-client -c ${config} request-create --owner ${owner} --cluster CLUSTER_1 --allocations ALLOCATION_1,ALLOCATION_2 --environments cvmfs ${requestid}
vc3-client -c ${config} request-create --owner ${owner} --cluster CLUSTER_1 --allocations ALLOCATION_1,ALLOCATION_2 --environments cvmfs ${requestid}

echo vc3-client -c ${config} allocation-list
vc3-client -c ${config} allocation-list

echo vc3-client -c ${config} resource-list
vc3-client -c ${config} resource-list

echo vc3-client -c ${config} nodeset-list
vc3-client -c ${config} nodeset-list

echo vc3-client -c ${config} cluster-list
vc3-client -c ${config} cluster-list

echo vc3-client -c ${config} request-list
vc3-client -c ${config} request-list


