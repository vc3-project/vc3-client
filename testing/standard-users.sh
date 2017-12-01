#!/bin/bash

source ./standard-common-config.sh

## Users
RUN_CHECK_CLIENT user-create --firstname Charlie --lastname Root --email root@localhost.tld --institution BellLabs --identity_id="356E5D96-B058-41F2-AD06-B59FC5BE9931" charlie

#RUN_CHECK_CLIENT user-create --firstname Lincoln --lastname Bryant --email lincolnb@uchicago.edu --institution UChicago lincolnb
#
#RUN_CHECK_CLIENT user-create --firstname Benedikt --lastname Riedel --email briedel@uchicago.edu --institution UChicago briedel
#
#RUN_CHECK_CLIENT user-create --firstname Judith --lastname Stephen --email jlstephen@uchicago.edu --institution UChicago jlstephen
#
#RUN_CHECK_CLIENT user-create --firstname Suchandra --lastname Thapa --email ssthapa@uchicago.edu --institution UChicago ssthapa
#
#RUN_CHECK_CLIENT user-create --firstname Jose --lastname Caballero --email caballero@bnl.gov --institution BrookhavenNationalLab caballero
#
#RUN_CHECK_CLIENT user-create --firstname Jeremy --lastname Van --email jeremyvan@uchicago --institution UChicago jeremyvan
#
#RUN_CHECK_CLIENT user-create --firstname Ben --lastname Tovar --email btovar@nd.edu --institution NotreDame btovar
#
#RUN_CHECK_CLIENT user-create --firstname Rob --lastname Gardner --email rwg@uchicago.edu --institution UChicago rwg
#
