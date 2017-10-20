#!/bin/env python
__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

import ast
import base64
import json
import logging
import os
import sys
import yaml
import StringIO
import ConfigParser

from entities import User, Project, Resource, Allocation, Nodeset, Request, Cluster, Environment
from vc3infoservice import infoclient
from vc3infoservice.core import  InfoMissingPairingException, InfoConnectionFailure, InfoEntityExistsException, InfoEntityMissingException

class VC3ClientAPI(object):
    '''
    Client application programming interface. 
    
    -- DefineX() methods return object. CreateX() stores it to infoservice. The two steps will allow 
    some manipulation of the object by the client, or calling user. 
    
    -- Oriented toward exposing only valid operations to external
    user (portal, resource tool, or admin CLI client). 
    
    -- Direct manipulations of stored information in the infoservice is only done by Entity objects, not
    client user.
        
    -- Store method (inside of storeX methods) takes infoclient arg in order to allow multiple infoservice instances in the future. 
        
    '''
    
    def __init__(self, config):
        self.config = config
        self.ic = infoclient.InfoClient(self.config)
        self.log = logging.getLogger('vc3client') 


    ################################################################################
    #                           User-related calls
    ################################################################################
    def defineUser(self,   
                   name,
                   first,
                   last,
                   email,
                   organization,
                   identity_id = None,
                   description = None,
                   displayname = None,
                   url = None,
                   docurl = None,
                   ):           
        '''
       Defines a new User object for usage elsewhere in the API. 
              
       :param str name: The unique VC3 username of this user
       :param str first: User's first name
       :param str last: User's last name
       :param str email: User's email address
       :param str organization: User's institutional affiliation or employer
       :return: User  A valid User object
       
       :rtype: User        
        '''
        u = User( name=name, 
                  state='new', 
                  acl=None, 
                  first=first, 
                  last=last, 
                  email=email, 
                  organization=organization,
                  identity_id=identity_id,
                  description = description,
                  displayname = displayname,
                  url = url,
                  docurl = docurl
                  )
        u.storenew = True
        self.log.debug("Creating user object: %s " % u)
        return u
    
        
    def storeUser(self, user):
        '''
        Stores the provided user in the infoservice. 
        :param User u:  User to add. 
        :return: None
        '''
        user.store(self.ic)
          

    def listUsers(self):
        '''
        Returns list of all valid users as a list of User objects. 

        :return: return description
        :rtype: List of User objects. 
        
        '''
        return self._listEntities('User')
       
    def getUser(self, username):
        return self.ic.getentity(User , username)
    
    ################################################################################
    #                           Project-related calls
    ################################################################################  
    def defineProject(self, 
                      name, 
                      owner, 
                      members,
                      description = None,
                      displayname = None,
                      url = None,
                      docurl = None,
                      organization = None,                      
                      ):
        '''
        Defines a new Project object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this project
        :param str owner:  The VC3 user name of the owner of this project
        :param List str:  List of VC3 user names of members of this project.  
        :return: Project  A valid Project object
        :rtype: Project        
        '''
        p = Project( name=name, 
                     state='new', 
                     acl=None, 
                     owner=owner, 
                     members=members,
                     allocations=[],
                     blueprints=[],
                     description = description,
                     displayname = displayname,
                     url = url,
                     docurl = docurl,
                     organization = organization                     
                     )
        p.storenew = True
        self.log.debug("Created project object: %s " % p)
        return p
    
    
    def storeProject(self, project):
        '''
        Stores the provided project in the infoservice. 
        
        :param Project project:  Project to add. 
        :return: None
        '''
        self.log.debug("Storing project %s" % project)
        project.store(self.ic)
        self.log.debug("Done.")
    
    
    def addUserToProject(self, user, project):
        '''
        :param str project
        :param str user
        '''
        self.log.debug("Looking up user %s project %s " % (user, project))
        po = self.getProject(project)
        if po is None:
            self.log.warning("Could not find project object %s " % (po,))
        else:
            self.log.debug("Adding user %s to project object %s " % (user, po))
            po.addUser(user)
            self.storeProject(po)        

    def removeUserFromProject(self, user, project):
        '''
        :param str project
        :param str user
        '''
        self.log.debug("Looking up user %s project %s " % (user, project))
        po = self.getProject(project)
        if po is None:
            self.log.warning("Could not find project object %s " % (po,))
        else:
            self.log.debug("Removing user %s from project object %s " % (user, po))
            po.addUser(user)
            self.storeProject(po)        

    def addAllocationToProject(self, allocation, projectname):
        '''
        :param str project
        :param str allocation
        '''
        self.log.debug("Looking up allocation %s project %s " % (allocation, projectname))
        po = self.getProject(projectname)
        if po is None:
            self.log.warning("Could not find project object %s " % (po,))
        else:
            self.log.debug("Adding allocation %s to project object %s " % (allocation, po))
            po.addAllocation(allocation)
            self.storeProject(po)
        
    def removeAllocationFromProject(self, allocation, projectname):
        '''
        :param str project
        :param str allocation
        '''
        self.log.debug("Looking up allocation %s project %s " % (allocation, projectname))
        po = self.getProject(projectname)
        if po is None:
            self.log.warning("Could not find project object %s " % (po,))
        else:
            self.log.debug("Removing allocation %s from project object %s " % (allocation, po))
            po.removeAllocation(allocation)
            self.storeProject(po)

    def listProjects(self):
        return self.ic.listentities(Project)
       
    def getProject(self, projectname):
        return self.ic.getentity(Project, projectname)

    def getProjectsOfOwner(self, ownername):
        projects = self.listProjects()
        filtered = [ p for p in projects if ownername == p.owner ]
        return filtered

    def getProjectsOfUser(self, username):
        projects = self.listProjects()
        filtered = [ p for p in projects if username in p.members ]
        return filtered
    

        
    ################################################################################
    #                           Resource-related calls
    ################################################################################    
    def defineResource(self, 
                       name,
                       owner, 
                       accesstype, 
                       accessmethod, 
                       accessflavor,
                       accesshost, 
                       accessport,  
                       gridresource, 
                       mfa,
                       description = None,
                       displayname = None,
                       url = None,
                       docurl = None,
                       organization = None,
                       ):
        '''
        Defines a new Resource object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this resource
        :param str owner:  The VC3 user name of the owner of this project
        :param str resourcetype,  # grid remote-batch local-batch cloud
        :param str accessmethod,  # ssh, gsissh,  
        :param str accessflavor,  # htcondor-ce, slurm, sge, ec2, nova, gce
        :param str accesshost,    # DNS hostname
        :param str accessport,    # 22 , 6918, 8773
        :param gridresource,      # http://cldext02.usatlas.bnl.gov:8773/services/Cloud  | HTCondorCE hostname             
        :param Boolean mfa        # Does site need head-node factory?     
        :return: Resource          A valid Project object
        :rtype: Resource        
        
        '''
        r = Resource( name, 
                      state='new', 
                      acl=None, 
                      owner=owner, 
                      accesstype=accesstype, 
                      accessmethod=accessmethod, 
                      accessflavor=accessflavor, 
                      accesshost = accesshost,
                      accessport = accessport,
                      gridresource=gridresource, 
                      mfa=mfa,
                      description = description,
                      displayname = displayname,
                      url = url,
                      docurl = docurl,
                      organization = organization                      
                       )
        r.storenew = True
        self.log.debug("Creating Resource object: %s " % r)
        return r
    
    
    def storeResource(self, resource):
        resource.store(self.ic)
    
    def listResources(self):
        return self.ic.listentities(Resource)
       
    def getResource(self, resourcename):
        return self.ic.getentity(Resource, resourcename)

    ################################################################################
    #                           Allocation-related calls
    ################################################################################ 
    def defineAllocation(self, name,
                               owner, 
                               resource, 
                               accountname,
                               description=None,
                               displayname=None,
                               url=None,
                               docurl=None,  
                               ):
        '''
          
        '''
        ao = Allocation(name, 
                        state='new', 
                        acl=None, 
                        owner=owner, 
                        resource=resource, 
                        accountname=accountname,
                        description=description,
                        displayname=displayname,
                        url=url,
                        docurl=docurl, )
        ao.storenew = True
        self.log.debug("Creating Allocation object: %s " % ao)
        return ao
    
    def storeAllocation(self, allocation):
        allocation.store(self.ic)
        
    def listAllocations(self):
        return self.ic.listentities( Allocation )
       
    def getAllocation(self, allocationname):
        return self.ic.getentity( Allocation, allocationname)

    def getAllocationPubToken(self, allocationname):
        alloc = self.getAllocation(allocationname)
        if alloc is None:
            self.log.warning('Could not find allocation object %s' % allocationname)
        else:
            if alloc.pubtoken is not None:
                try:
                    pubstring  = self.decode(alloc.pubtoken)
                    return pubstring
                except Exception, e:
                    self.log.error('Error decoding pubtoken for Allocation %s' % allocationname)                

            
    ################################################################################
    #                        Cluster-related calls
    ################################################################################ 
        '''
        Defines a new Cluster (description) object for usage elsewhere in the API. 
              
        :param str name: The unique name of this cluster description.
        :param str owner:  The user name of the owner of this project
        :param [str]:   List of strings, names of nodesets in this cluster    
        :return: Cluster          A valid Cluster object
        :rtype: Cluster        
        
        '''
    def defineCluster(self, 
                      name, 
                      owner, 
                      nodesets=[],
                      description = None,
                      displayname = None,
                      url = None,
                      docurl = None,                       
                       ): 
        
        c = Cluster(name=name, 
                    state='new',
                    owner=owner,
                    acl=None,
                    nodesets=nodesets, # list of names of nodesets in this cluster definition.
                    description = description,
                    displayname = displayname,
                    url = url,
                    docurl = docurl 
                     )
        c.storenew = True
        return c
                    
    def storeCluster(self, cluster):
        cluster.store(self.ic)
    
    def listClusters(self):
        return self.ic.listentities(Cluster)
       
    def getCluster(self, clustername):
        return self.ic.getentity(Cluster , clustername)

    def addNodesetToCluster(self, nodesetname, clustername):
        co = self.getCluster(clustername)
        if co is None:
            self.log.warning('Could not find cluster object %s', clustername)
        else:
            co.addNodeset(nodesetname)
            self.storeCluster(co)
       
    def removeNodesetFromCluster(self, nodesetname, clustername):
        co = self.getCluster(clustername)
        if co is None:
            self.log.warning('Could not find cluster object %s', clustername)
        else:
            co.removeNodeset(nodesetname)
            self.storeCluster(co)
        

    ################################################################################
    #                        Nodeset-related calls
    ################################################################################ 
    def defineNodeset(self, 
                      name, 
                      owner, 
                      node_number, 
                      app_type, 
                      app_role, 
                      environment,
                      description = None,
                      displayname = None,
                      url = None,
                      docurl = None,                      
                      ):
        ns = Nodeset( name=name, 
                      state='new',
                      owner=owner, 
                      acl=None, 

                      node_number=node_number, 
                      app_type=app_type, 
                      app_role=app_role,
                      cores=1, 
                      memory_mb=None, 
                      storage_mb=None, 
                      app_host = None, 
                      app_port = None,
                      app_sectoken = None,
                      environment = environment,
                      description = description,
                      displayname = displayname,
                      url = url,
                      docurl = docurl
                       )
        ns.storenew = True
        self.log.debug("Created Nodeset object: %s" % ns)
        return ns 
    
    def listNodesets(self):
        return self.ic.listentities(Nodeset)
       
    def getNodeset(self, nodesetname):
        return self.ic.getentity(Nodeset, nodesetname)
    
    def storeNodeset(self, nodeset):
        nodeset.store(self.ic)

    ################################################################################
    #                        Environment-related calls
    ################################################################################ 
    def defineEnvironment(self, 
                          name, 
                          owner, 
                          packagelist = [], 
                          envmap = {}, 
                          files={}, 
                          command = None, 
                          builder_extra_args = None,
                          description = None,
                          displayname = None,
                          url = None,
                          docurl = None,                          
                          ):
        e = Environment(name, 
                        state='new', 
                        acl=None, 
                        owner = owner, 
                        packagelist = packagelist, 
                        envmap = envmap,
                        files = files, 
                        command = command,
                        builder_extra_args = builder_extra_args,
                        description = description,
                        displayname = displayname,
                        url = url,
                        docurl = docurl
                        )
        e.storenew = True
        self.log.debug("Creating Environment object: %s " % e)
        return e
    
    def storeEnvironment(self, environment):
        environment.store(self.ic)
    
    def listEnvironments(self):
        return self.ic.listentities(Environment)
       
    def getEnvironment(self, environmentname):
        return self.ic.getentity('Environment', environmentname)

    ################################################################################
    #                        Request-related calls
    ################################################################################ 
    def defineRequest(self, 
                      name, 
                      owner,
                      cluster,
                      allocations,  
                      environments,
                      policy,
                      expiration,
                      description = None,
                      displayname = None,
                      url = None,
                      docurl = None,
                      organization = None,                       
                       ):
        '''
        
        :return Request
        
        '''
        r = Request(name, 
                    state='new', 
                    acl=None,
                    owner=owner,
                    action='new',
                    state_reason='new',
                    cluster_state='new',          # state of virtual cluster this Request represents 
                    cluster_state_reason='new',
                    cluster = cluster,           # name of abstract cluster specification
                    allocations  = allocations,   # list of allocation names
                    environments = environments,   # list of environments names
                    policy = policy, 
                    expiration = expiration,       # string representation of UTC time when request should be terminated. 
                    description = description,
                    displayname = displayname,
                    url = url,
                    docurl = docurl,
                    organization = organization
                    )
        r.storenew = True
        self.log.debug("Creating Request object: %s " % r)
        return r
    
    def storeRequest(self, request):
        request.store(self.ic)


    def listRequests(self):
        return self._listEntities('Request')
       
    def getRequest(self, requestname):
        return self.ic.getentity( Request, requestname)

    def terminateRequest(self, requestname):
        r = self.ic.getentity( Request, requestname)
        if r is not None:
            self.log.debug("Setting request action to terminate...")
            r.action = 'terminate'
            r.store(self.ic)
            print("Request.action set to terminate.")
        else:
            self.log.info("Request is None.")

    def getRequestStatus(self, requestname):
        r = self.ic.getentity( Request, requestname)
        out = (None, None)
        if r is not None:
            out = (r.statusraw, r.statusinfo)
        return out

    def getRequestState(self, requestname):
        r = self.ic.getentity( Request, requestname)
        out = (None, None)
        if r is not None:
            out = (r.state, r.state_reason)
        return out      

    def saveRequestAsBlueprint(self, requestid, newlabel):
        '''
        Take the specified request and store it as a re-usable blueprint with new label
        '''
        pass
    
    
    ################################################################################
    #                        Infrastructural calls
    ################################################################################ 
    def getQueuesConf(self, requestname, queuename):
        '''
        Get the queues.conf sections for the specified request and queuename
        
        May raise InfoMissingEntityException if Request doesn't exist. 
        
        '''
        r = self.getRequest(requestname)

        if not r.queuesconf:
            raise Exception('Request %s does not have a queues.conf defined' % requestname)

        try:
            buf   = StringIO.StringIO(self.decode(r.queuesconf))
            qconf = ConfigParser.ConfigParser()
            qconf.readfp(buf)

            return qconf.items(queuename)

        except Exception, e:
            self.log.error('Error decoding queues.conf of request %s' % requestname)
            raise e

    def getAuthConf(self, requestname, queuename):
        '''
        Get the auth.conf sections for the specified request and queuename
        '''
        r = self.getRequest(requestname)

        if not r.authconf:
            raise Exception('Request %s does not have a auth.conf defined' % requestname)

        try:
            buf   = StringIO.StringIO(self.decode(r.authconf))
            aconf = ConfigParser.ConfigParser()
            aconf.readfp(buf)

            return aconf.items(queuename)

        except Exception, e:
            self.log.error('Error decoding auth.conf of request %s' % requestname)
            raise e

    def getConfString(self, conftype, requestname ):
        '''
        Return string contents of specified conf type auth|queues
        '''
        r = self.getRequest(requestname)
        cs = ""
        if r:
            if conftype == 'queues':
                buf  = StringIO.StringIO(self.decode(r.queuesconf))
                cs = buf.read()
            elif conftype == 'auth':
                buf   = StringIO.StringIO(self.decode(r.authconf))
                cs = buf.read()
        else:
            self.log.debug("No request with name %s" % requestname)
        return cs


    def requestPairing(self, commonname):
        '''
        Create a request in the VC3 category to create a pairing setup protected by the supplied pairingcode.
        Master will see request, generate keypair, and place in infoservice w/ code. 
         
        '''
        code = self.ic.requestPairing(commonname)
        return code
        
    
    def getPairing(self, pairingcode):
        '''
        One-time only successful call. 
        Can be called unsuccessfully (i.e. during wait for request satisfaction) without harm. 
        Returns tuple of (pubsslkey, privsslkey)
         
        '''
        (cert, key) = self.ic.getPairing(pairingcode)
        return (cert, key)


##############################################
#        External Utility class methods. 
##############################################

    @classmethod
    def encode(self, string):
        return base64.b64encode(string)
    
    @classmethod
    def decode(self, string):
        return base64.b64decode(string)
        

#
# These exceptions in infoclient now. 
#
    
#class EntityExistsException(Exception):
#    def __init__(self, value):
#        self.value = value
#    def __str__(self):
#        return repr(self.value)

#class MissingDependencyException(Exception):
#    '''
#    To be thrown when an API call includes a reference to an entity that doesn't exist. 
#    '''
#    def __init__(self, name, entityclass):
#        self.name        = name
#        self.entityclass = entityclass
#    def __str__(self):
#        return repr(self.name) + '(' + repr(self.entityclass) + ')'

