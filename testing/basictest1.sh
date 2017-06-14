#!/bin/bash
DEBUG='-d'
echo vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL jhover
echo vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-create --firstname Angus --lastname MacGuyver --email angus@bnl.gov --institution BNL angus
echo vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover
vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-create --firstname John --lastname Hover --email jhover@bnl.gov --institution BNL adminjhover

echo vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-list
vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf user-list

echo vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf project-create --owner jhover --members jhover  jhoverproject
vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf project-create --owner jhover --members jhover  jhoverproject
echo vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf project-adduser jhoverproject angus
vc3client/clientcli.py -c ~/git/vc3-client/etc/vc3-client.conf project-adduser jhoverproject angus

echo vc3client/clientcli.py -c /home/jhover/git/vc3-client/etc/vc3-client.conf project-list jhoverproject
vc3client/clientcli.py -c /home/jhover/git/vc3-client/etc/vc3-client.conf project-list jhoverproject


