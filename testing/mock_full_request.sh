#! /bin/sh

requestid=MY_REQUEST
owner=${USER}

vc3-client resource-create --owner ${owner} --accesstype batch --accessmethod ssh --accessflavor strawberry --accesshost resource.org --accessport 1234 RESOURCE_1

vc3-client resource-create --owner ${owner} --accesstype batch --accessmethod ssh --accessflavor strawberry --accesshost otherresource.org --accessport 1234 RESOURCE_2

vc3-client allocation-create --owner ${owner} --resource RESOURCE_1 --accountname vc3-${owner} ALLOCATION_1

vc3-client allocation-create --owner ${owner} --resource RESOURCE_2 --accountname vc3-${owner} ALLOCATION_2

vc3-client nodeset-create --owner ${owner} --node_number 1 --app_type APP_TYPE --app_role APP_ROLE NODESET_1

vc3-client cluster-create --owner ${owner} --nodesets NODESET_1 CLUSTER_1

vc3-client request-create --owner ${owner} --cluster CLUSTER_1 --allocations ALLOCATION_1,ALLOCATION_2 --environments cvmfs ${requestid}

vc3-client allocation-list
vc3-client resource-list
vc3-client nodeset-list
vc3-client cluster-list
vc3-client request-list

