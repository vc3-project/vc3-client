#!/bin/bash

source ./standard-common-config.sh

# Users
RUN_CHECK_CLIENT user-create --firstname Lincoln --lastname Bryant --email lincolnb@uchicago.edu --institution UChicago lincolnb
RUN_CHECK_CLIENT project-create --owner lincolnb --members lincolnb lincolnb

RUN_CHECK_CLIENT user-create --firstname Benedikt --lastname Riedel --email briedel@uchicago.edu --institution UChicago briedel
RUN_CHECK_CLIENT project-create --owner briedel --members briedel briedel

RUN_CHECK_CLIENT user-create --firstname Judith --lastname Stephen --email jlstephen@uchicago.edu --institution UChicago jlstephen
RUN_CHECK_CLIENT project-create --owner jlsteven --members jlsteven jlsteven

RUN_CHECK_CLIENT user-create --firstname Suchandra --lastname Thapa --email ssthapa@uchicago.edu --institution UChicago ssthapa
RUN_CHECK_CLIENT project-create --owner ssthapa --members ssthapa ssthapa

RUN_CHECK_CLIENT user-create --firstname Jose --lastname Caballero --email caballero@bnl.gov --institution BrookhavenNationalLab caballero
RUN_CHECK_CLIENT project-create --owner caballero --members caballero caballero

RUN_CHECK_CLIENT user-create --firstname Jeremy --lastname Van --email jeremyvan@uchicago --institution UChicago jeremyvan
RUN_CHECK_CLIENT project-create --owner jeremyvan --members jeremyvan jeremyvan

RUN_CHECK_CLIENT user-create --firstname Ben --lastname Tovar --email btovar@nd.edu --institution NotreDame btovar
RUN_CHECK_CLIENT project-create --owner btovar --members btovar btovar

RUN_CHECK_CLIENT user-create --firstname Rob --lastname Gardner --email rwg@uchicago.edu --institution UChicago rwg
RUN_CHECK_CLIENT project-create --owner rwg --members rwg rwg


# New group project
RUN_CHECK_CLIENT project-create --owner lincolnb --members lincolnb,briedel SouthPoleTelescope
RUN_CHECK_CLIENT project-create --owner btovar --members btovar,dthain ndccl
RUN_CHECK_CLIENT project-create --owner khurtado --members khurtado lobster

