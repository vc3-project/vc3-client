#!/bin/bash

source ./standard-common-config.sh

RUN_CHECK_CLIENT project-create --owner lincolnb --members lincolnb lincolnb

RUN_CHECK_CLIENT project-create --owner briedel --members briedel briedel

RUN_CHECK_CLIENT project-create --owner jlsteven --members jlsteven jlsteven

RUN_CHECK_CLIENT project-create --owner ssthapa --members ssthapa ssthapa

RUN_CHECK_CLIENT project-create --owner caballero --members caballero caballero

RUN_CHECK_CLIENT project-create --owner jeremyvan --members jeremyvan jeremyvan

RUN_CHECK_CLIENT project-create --owner btovar --members btovar btovar

RUN_CHECK_CLIENT project-create --owner rwg --members rwg rwg

# New group project
RUN_CHECK_CLIENT project-create --owner lincolnb --members lincolnb,briedel SouthPoleTelescope
RUN_CHECK_CLIENT project-create --owner btovar --members btovar,dthain ndccl
RUN_CHECK_CLIENT project-create --owner khurtado --members khurtado lobster

