#!/bin/bash

source ./standard-common-config.sh

## Users
# Example
#RUN_CHECK_CLIENT user-create --firstname Charlie --lastname Root --email root@localhost.tld --institution BellLabs --identity_id="356E5D96-B058-41F2-AD06-B59FC5BE9931" charlie

RUN_CHECK_CLIENT user-create --firstname Lincoln --lastname Bryant \
                             --email lincolnb@uchicago.edu \ 
                             --displayname "Lincoln Bryant" \  
                             --identity_id c887eb90-d274-11e5-bf28-779c8998e810 \
                             --institution UChicago \
                             lincolnb 
RUN_CHECK_CLIENT user-create --firstname Jeremy --lastname Van \
                             --email jeremyvan@uchicago.edu \
                             --displayname "Jeremy Van" \
                             --identity_id 05e05adf-e9d4-487f-8771-b6b8a25e84d3 \
                             --institution UChicago \
                             rwg
RUN_CHECK_CLIENT user-create --firstname Robert --lastname Gardner  \
                             --email rwg@uchicago.edu \
                             --displayname "Robert Gardner" \
                             --identity_id c456b77c-d274-11e5-b82c-23a245a48997 \
                             --institution UChicago \
                             rwg
RUN_CHECK_CLIENT user-create --firstname Kenyi --lastname Hurtado \
                             --email khurtado@nd.edu \
                             --displayname "Kenyi Hurtado" \
                             --identity_id a877729e-d274-11e5-a5d2-2f448d5a1c26 \
                             --institution "University of Notre Dame" \
                             khurtado
