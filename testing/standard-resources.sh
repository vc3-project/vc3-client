#!/bin/bash

source ./standard-common-config.sh


# Create resource
RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost midway-login1.rcc.uchicago.edu --accessport 22 --description "Midway cluster at the University of Chicago Research Computing Center (RCC)" --displayname "Midway" --url "https://rcc.uchicago.edu/" --docurl "https://rcc.uchicago.edu/docs/" --organization "University of Chicago Research Computing Center (RCC)" uchicago-midway

RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor condor --accesshost its-condor-submit.syr.edu --accessport 22 --description "Syracuse OrangeGrid" --displayname "OrangeGrid"  --url "http://researchcomputing.syr.edu/resources/orange-grid/" --docurl "http://researchcomputing.syr.edu/orangegrid-intro/" --organization "Syracuse University" syr-orangegrid

RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch  --accessmethod ssh  --accessflavor condor  --accesshost condor.grid.uchicago.edu --accessport 22 --description "CoreOS Cluster"  --displayname "CoreOS"  --url ""  --docurl ""  --organization "University of Chicago Physical Sciences Division" uchicago-coreos

RUN_CHECK_CLIENT resource-create --owner lincolnb  --accesstype batch --accessmethod ssh --accessflavor condor --accesshost pool.virtualclusters.org  --accessport 22 --description "VC3 Test Pool" --displayname "VC3 Test Pool"  --url "http://www.virtualclusters.org/"  --docurl "https://github.com/vc3-project/vc3-user-guide/blob/master/userguide.md" --organization "VC3"  vc3-test-pool

RUN_CHECK_CLIENT resource-create  --owner lincolnb  --accesstype batch  --accessmethod ssh --accessflavor slurm   --accesshost cori.nersc.gov  --accessport 22 --description "Cori Supercomputer at NERSC" --displayname "Cori"  --url "https://www.nersc.gov/users/computational-systems/cori/"  --docurl "http://www.nersc.gov/users/computational-systems/cori/getting-started/"  --organization "National Energy Research Scientific Computing Center (NERSC)" nersc-cori

RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch  --accessmethod ssh  --accessflavor condor  --accesshost uct2-gk.mwt2.org --accessport 22 --description "University of Chicago Computing Cooperative"  --displayname "UC3" --url ""  --docurl ""  --organization "University of Chicago" uchicago-uc3

RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh  --accessflavor condor  --accesshost stampede-redirect.virtualclusters.org --accessport 22 --description "Stampede 2 Super Computer"  --displayname "Stampede 2" --url ""  --docurl ""  --organization "Texas Advanced Computing Center (TACC)" tacc-stampede2

RUN_CHECK_CLIENT resource-create --owner btovar --accesstype batch --accessmethod ssh --accessflavor condor --accesshost cclvm05.crc.nd.edu --accessport 22 --description "ND-CCL login none" --displayname "ND CCL" --url "" --docurl "" --organization "University of Notre Dame Cooperative Computing Lab" ndccl


