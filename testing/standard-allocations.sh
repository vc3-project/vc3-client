#!/bin/bash

source ./standard-common-config.sh

# Create allocation
RUN_CHECK_CLIENT allocation-create --owner lincolnb --resource uchicago-midway --accountname lincolnb lincolnb.uchicago-midway
RUN_CHECK_CLIENT allocation-create --owner lincolnb --resource uchicago-coreos --accountname lincolnb lincolnb.uchicago-coreos
RUN_CHECK_CLIENT allocation-create --owner lincolnb --resource nersc-cori      --accountname briedel  briedel.nersc-cori

