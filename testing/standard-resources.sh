#!/bin/bash

source ./standard-common-config.sh

# Generic node size:
RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number -1 --app_type generic --app_role worker-nodes --displayname="Generic node size, 1core,1GB,1GB" --cores 4 --memory_mb 1000 --storage_mb 1000  generic-nodesize


# Create resource midway
RUN_CHECK_CLIENT nodeset-create --owner lincolnb --node_number -1 --app_type generic --app_role worker-nodes --displayname="Node size for uchicago-midway (amd partition)" --cores 64 --memory_mb 4000 --storage_mb 10000  uchicago-midway-nodesize

RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost midway-login1.rcc.uchicago.edu --accessport 22 --node uchicago-midway-nodesize --description "Midway cluster at the University of Chicago Research Computing Center (RCC)" --displayname "Midway" --url "https://rcc.uchicago.edu/" --docurl "https://rcc.uchicago.edu/docs/" --organization "University of Chicago Research Computing Center (RCC)" uchicago-midway --public


# Create resource Syracuse
RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor condor --accesshost its-condor-submit.syr.edu --accessport 22 --node generic-nodesize --description "Syracuse OrangeGrid" --displayname "OrangeGrid"  --url "http://researchcomputing.syr.edu/resources/orange-grid/" --docurl "http://researchcomputing.syr.edu/orangegrid-intro/" --organization "Syracuse University" syr-orangegrid


# Create resource CoreOS
RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch  --accessmethod ssh  --accessflavor condor  --accesshost condor.grid.uchicago.edu --accessport 22 --node generic-nodesize --description "CoreOS Cluster"  --displayname "CoreOS"  --url ""  --docurl ""  --organization "University of Chicago" uchicago-coreos --public


# Create resource VC3 test pool
RUN_CHECK_CLIENT resource-create --owner lincolnb  --accesstype batch --accessmethod ssh --accessflavor condor --accesshost pool.virtualclusters.org  --accessport 22 --node generic-nodesize --description "VC3 Test Pool" --displayname "VC3 Test Pool"  --url "http://www.virtualclusters.org/"  --docurl "https://github.com/vc3-project/vc3-user-guide/blob/master/userguide.md" --organization "VC3"  vc3-test-pool --public


# Create resource NERSC Cori
RUN_CHECK_CLIENT nodeset-create --owner lincolnb --node_number -1 --app_type generic --app_role worker-nodes --displayname="Node size for nersc-cori (Haswell partition)" --cores 32 --memory_mb 4000 --storage_mb 10000  nersc-cori-nodesize

RUN_CHECK_CLIENT resource-create  --owner lincolnb  --accesstype batch  --accessmethod ssh --accessflavor slurm   --accesshost cori.nersc.gov  --accessport 22 --node nersc-cori-nodesize --description "Cori Supercomputer at NERSC" --displayname "Cori"  --url "https://www.nersc.gov/users/computational-systems/cori/"  --docurl "http://www.nersc.gov/users/computational-systems/cori/getting-started/" --pubtokendocurl "http://www.nersc.gov/users/connecting-to-nersc/connecting-with-ssh/#toc-anchor-2" --organization "National Energy Research Scientific Computing Center (NERSC)" nersc-cori --public


# Create resource uct2-gk
RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch  --accessmethod ssh  --accessflavor condor  --accesshost uct2-gk.mwt2.org --accessport 22 --node generic-nodesize --description "ATLAS Midwest Tier 2 Center job gateway (UChicago)"  --displayname "MWT2" --url "http://twiki.mwt2.org"  --docurl "http://twiki.mwt2.org"  --organization "Midwest Tier 2" uchicago-mwt2 --public

# Create resource uct3-s1
RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch  --accessmethod ssh  --accessflavor condor  --accesshost uct3-s1.mwt2.org --accessport 22 --node generic-nodesize --description "UChicago ATLAS Tier 3"  --displayname "UCT3" --url "https://hep.uchicago.edu/atlas/"  --docurl "http://twiki.mwt2.org"  --organization "University of Chicago" uchicago-uct3 --public


# Create resource TACC Stampede
RUN_CHECK_CLIENT nodeset-create --owner lincolnb --node_number -1 --app_type generic --app_role worker-nodes --displayname="Node size for tacc-stampede2 (SKX partition)" --cores 96 --memory_mb 2000 --storage_mb 10000  tacc-stampede2-nodesize

RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh  --accessflavor slurm --accesshost login5.stampede2.tacc.utexas.edu --accessport 22 --node tacc-stampede2-nodesize --description "Stampede 2 Super Computer"  --displayname "Stampede 2" --url ""  --docurl ""  --organization "Texas Advanced Computing Center (TACC)" tacc-stampede2 --public


# Create resource ND CCL
RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number -1 --app_type generic --app_role worker-nodes --displayname="Node size for ndccl" --cores 4 --memory_mb 1000 --storage_mb 10000  ndccl-nodesize

RUN_CHECK_CLIENT resource-create --owner btovar --accesstype batch --accessmethod ssh --accessflavor condor --accesshost cclvm05.crc.nd.edu --accessport 22 --node ndccl-nodesize --description "ND-CCL login none" --displayname "ND CCL" --url "https://ccl.cse.nd.edu/" --docurl "https://ccl.cse.nd.edu/" --organization "University of Notre Dame Cooperative Computing Lab" ndccl --public --features singularity


# Create resource UCLA Hoffman2
RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number -1 --app_type generic --app_role worker-nodes --displayname="Node size for ucla-hoffman2" --cores 8 --memory_mb 1000 --storage_mb 10000  ucla-hoffman2-nodesize

RUN_CHECK_CLIENT resource-create --owner briedel --accesstype batch --accessmethod ssh --accessflavor sge --accesshost login1.hoffman2.idre.ucla.edu --accessport 22 --node ucla-hoffman2-nodesize --description "UCLA Hoffman2" --displayname "UCLA Hoffman2" --url "https://idre.ucla.edu/resources/hpc/hoffman2-cluster" --organization "University of California,  Los Angeles" ucla-hoffman2 --public


# Create resource osgconnect
RUN_CHECK_CLIENT resource-create --owner lincolnb --accesstype batch --accessmethod ssh --accessflavor condor --accesshost login03.osgconnect.net --accessport 22 --node generic-nodesize --description "Open Science Grid (SL7)" --displayname "OSG Connect" --url "https://support.opensciencegrid.org" --organization "Open Science Grid" osg-connect --public


# Create resource bridges
RUN_CHECK_CLIENT nodeset-create --owner btovar --node_number -1 --app_type generic --app_role worker-nodes --displayname="Node size for psc-bridges (RMS partition)" --cores 28 --memory_mb 4000 --storage_mb 35000  psc-bridges-nodesize

RUN_CHECK_CLIENT resource-create --owner khurtado --accesstype batch --accessmethod ssh --accessflavor slurm --accesshost bridges.psc.edu --accessport 22 --node psc-bridges-nodesize --description "Bridges Supercomputer at PSC" --displayname "Bridges" --url "https://www.psc.edu/bridges/" --docurl "https://www.psc.edu/bridges/user-guide/running-jobs" --pubtokendocurl "https://www.psc.edu/bridges/user-guide/connecting-to-bridges#keys" --organization "Pittsburgh Supercomputing Center" psc-bridges --public


