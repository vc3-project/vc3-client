#!/bin/env python
__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

import logging
import urllib

from vc3infoservice.core import InfoEntity
   
class User(InfoEntity):
    '''
    Represents a VC3 instance user account.
    As policy, name, email, and organization must be set.  
    
    '''
    infoattributes = ['name',
                     'state',
                     'acl',
                     'first',
                     'last',
                     'email',
                     'organization',
                     'identity_id',
                     'description',
                     'displayname',
                     'url',
                     'docurl'                  
                     ] 
    infokey = 'user'
    validvalues = {}
    intattributes = []
    
    def __init__(self,
                   name,
                   state,
                   acl,
                   first,
                   last,
                   email,
                   organization,
                   identity_id=None,
                   description=None,
                   displayname=None,
                   url=None,
                   docurl=None
                ):
        '''
        Defines a new User object. 
              
        :param str name: The unique VC3 username of this user
        :param str first: User's first name
        :param str last: User's last name
        :param str email: User's email address
        :param str organization: User's institutional affiliation or employer
        :param str description: Long-form description
        :param str displayname: Pretty human-readable name/short description
        :param str url: High-level URL reference for this entity. 
        :param str docurl: Link to how-to/usage documentation for this entity.          
        :return: User:  A valid User object      
        :rtype: User
        
        '''
        self.log = logging.getLogger()
        self.state = state
        self.acl = acl
        self.name = name
        self.first = first
        self.last = last
        self.email = email
        self.organization = organization
        self.identity_id = identity_id
        self.allocations = []
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.log.debug("Entity created: %s" % self)


    def addAllocation(self, allocation):
        '''
            Adds provided allocation (string label) to this allocation.
        '''

        if self.allocations is None:
            self.allocations = []

        self.log.debug("Adding allocation %s to project" % allocation)
        if allocation not in self.allocations:
            self.allocations.append(allocation)
        self.log.debug("Allocations now %s" % self.allocations)
        

    def removeAllocation(self, allocation):
        '''
            Removes provided allocation (string label) to this project.
        '''

        if self.allocations is None:
            self.allocations = []

        self.log.debug("Removing allocation %s to project" % allocation)
        if allocation not in self.allocations:
            self.log.debug("Allocation %s did not belong to project")
        else:
            self.allocations.remove(allocation)
            self.log.debug("Allocations now %s" % self.allocations)


class Project(InfoEntity):
    '''
    Represents a VC3 Project.
    
    '''
    infokey = 'project'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'members', 
                     'allocations',
                     'blueprints',
                     'description',
                     'displayname',
                     'url',
                     'docurl',
                     'organization', 
                     ]
    validvalues = {}
    intattributes = []    
    
    def __init__(self, 
                   name,
                   state,
                   acl,
                   owner,
                   members,   # list
                   allocations=[],  # list of names 
                   blueprints=[],
                   description=None,
                   displayname=None,
                   url=None,
                   docurl=None, 
                   organization = None,
                   ):  # list of names
        '''
        Defines a new Project object. 
              
        :param str name: The unique VC3 name of this project
        :param str owner: VC3 username of project owner. 
        :param str members: List of vc3 usernames
        :param str allocations: List of allocation names. 
        :param str blueprints:  List of blueprint names. 
        :param str description: Long-form description
        :param str displayname: Pretty human-readable name/short description
        :param str url: High-level URL reference for this entity. 
        :param str docurl: Link to how-to/usage documentation for this entity. 
        :param str organization: Name of experiment or institution for this project. 
        :return: Project:  A valid Project objext. 
        :rtype: Project
        
        '''  
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner
        self.members = []
        for m in members:
            if m not in self.members:
                self.members.append(m)
        self.allocations = allocations
        self.blueprints = blueprints
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.organization = organization
        self.log.debug("Entity created: %s" % self)
 
    def addUser(self, user):
        '''
            Adds provided user (string label) to this project.
        '''
        if self.members is None:
            self.members = []

        self.log.debug("Adding user %s to project" % user)
        if user not in self.members:
            ulist = self.members
            ulist.append(user)
            self.members = ulist
        self.log.debug("Members now %s" % self.members)
        

    def removeUser(self, user):
        '''
            Removes provided user (string label) from this project.
        '''
        if self.members is None:
            self.members = []

        self.log.debug("Removing user %s to project" % user)
        if user not in self.members:
            self.log.debug("User %s did not belong to project")
        else:
            ulist = self.members
            ulist.remove(user)
            self.members = ulist
            self.log.debug("Members now %s" % self.members)

    def addAllocation(self, allocation):
        '''
            Adds provided allocation (string label) to this project.
        '''
        if self.allocations is None:
            self.allocations = []

        self.log.debug("Adding allocation %s to project" % allocation)
        if allocation not in self.allocations:
            alist = self.allocations
            alist.append(allocation)
            self.allocations = alist
        self.log.debug("Allocations now %s" % self.allocations)
        

    def removeAllocation(self, allocation):
        '''
            Removes provided allocation (string label) from this project.
        '''
        if self.allocations is None:
            self.allocations = []

        self.log.debug("Removing allocation %s from project" % allocation)
        if allocation not in self.allocations:
            self.log.debug("Allocation %s did not belong to project")
        else:
            alist = self.allocations
            alist.remove(allocation)
            self.allocations = alist
            self.log.debug("Allocations now %s" % self.allocations)

class Resource(InfoEntity):
    '''
    Represents a VC3 target resource. 
    
    Intrinsic time limits/preemption flag to distinguish platforms we could run static components on. 
    Network access is also critical for this.    
        
    '''
    infokey = 'resource'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'accesstype', 
                     'accessmethod',
                     'accessflavor',
                     'accesshost',
                     'accessport',
                     'gridresource',
                     'cloudspotprice',
                     'cloudinstancetype',
                     'mfa',
                     'description',
                     'displayname',
                     'url',
                     'docurl',
                     'organization'                      
                     ]
    validvalues = {
        'accesstype' : ['batch','cloud']
        }
    intattributes = []
    
    def __init__(self,
                 name,
                 state,
                 acl,
                 owner,
                 accesstype,   # grid, batch, cloud
                 accessmethod, # ssh, gsissh
                 accessflavor, # condor-ce, slurm, sge, ec2, nova, gce
                 accesshost,   # hostname
                 accessport,   # port
                 gridresource, # http://cldext02.usatlas.bnl.gov:8773/services/Cloud , HTCondor CE hostname[:port]              
                 cloudspotprice=None,
                 cloudinstancetype=None,
                 mfa = False,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None, 
                 organization = None,
                 ):
        '''
    Creates a new Resource object.
        
    :param str description: Long-form description
    :param str displayname: Pretty human-readable name/short description
    :param str url: High-level URL reference for this entity. 
    :param str docurl: Link to how-to/usage documentation for this entity.     
        '''
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner
        
        # Entity-specific attriutes
        self.accesstype = accesstype
        self.accessmethod = accessmethod
        self.accessflavor = accessflavor
        self.accesshost = accesshost
        self.accessport = accessport
        self.gridresource = gridresource
        self.cloudspotprice    = cloudspotprice
        self.cloudinstancetype = cloudinstancetype
        self.mfa = mfa
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.organization = organization
        self.log.debug("Entity created: %s" % self)


class Allocation(InfoEntity):
    '''
    Represents the access granted a VC3 User and a VC3 target Resource.
    Defined by (resource, vc3user, unix_account) triple.   
    
    May or may not contain sub-Allocations.
    
    (Top-level) Allocation names are in the form <vc3username>.<vc3resourcename>.
    Sub-allocation names are in the form <vc3username>.<vc3resourcename>.<suballocationlabel>
            
    '''
    infokey = 'allocation'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'resource',
                     'type',        # unlimited, quota, cumulative
                     'accountname',
                     'quantity',
                     'units',       # corehours, su, nodes, 
                     'sectype',     # ssh-rsa, ssh-dsa, pki, x509, local
                     'pubtoken',    # ssh pubkey, cloud access key
                     'privtoken',   # ssh privkey, cloud secret key, VOMS proxy
                     'description',
                     'displayname',
                     'url',
                     'docurl',
                    ]   
    validvalues = {
        'sectype' : [ None, 'ssh-rsa', 'ssh-dsa' , 'x509' ],
        }
    intattributes = []    
    
    def __init__(self, 
                 name, 
                 state, 
                 acl, 
                 owner,
                 resource, 
                 accountname,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None,  
                 type='unlimited', 
                 quantity=None, 
                 units=None,
                 sectype=None,
                 pubtoken=None,
                 privtoken=None, 
                  ):
        '''
    Creates a new Allocation object. 
            
    :param str description: Long-form description
    :param str displayname: Pretty human-readable name/short description
    :param str url: High-level URL reference for this entity. 
    :param str docurl: Link to how-to/usage documentation for this entity. 
        
        '''
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner
        self.resource = resource
        self.accountname = accountname     # unix username, or cloud tenant, 
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.type = type           # quota | unlimited | limited 
        self.quantity = quantity   # 
        self.units = units         #
        self.sectype = sectype
        self.pubtoken = pubtoken
        self.privtoken = privtoken
        self.log.debug("Entity created: %s" % self)

class Policy(InfoEntity):
    '''
    Describes the desired resource utilization policy when a Request 
    includes multiple Allocations. 

    '''
    infokey = 'policy'
    infoattributes = ['name',
                     'state',
                     'owner',
                     'acl',
                     'pluginname',
                     'description',
                     'displayname',
                     'url',
                     'docurl', 
                      ]
    validvalues = {}
    intattributes = []
    
    
    def __init__(self, 
                 name, 
                 state, 
                 owner, 
                 acl, 
                 pluginname,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None,  ):
        '''
        Creates a new Policy object. 
        :param str description: Long-form description
        :param str displayname: Pretty human-readable name/short description
        :param str url: High-level URL reference for this entity. 
        :param str docurl: Link to how-to/usage documentation for this entity.             
        
        '''
        self.log = logging.getLogger()
        self.name = name
        self.owner = owner
        self.acl = acl
        self.pluginname = pluginname
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.log.debug("Entity created: %s" % self)


class Nodeset(InfoEntity):
    '''
    Represents a set of equivalently provisioned nodes that are part of a Cluster definition. 

    '''
    infokey = 'nodes'
    infoattributes = ['name',
                     'state',
                     'owner',
                     'acl',
                     
                     'node_number',
                     'app_type',
                     'app_role',
                     
                     'cores',
                     'memory_mb',
                     'storage_mb',
                     'app_host',
                     'app_port',
                     'app_sectoken',            
                     'environment',
                     'description',
                     'displayname',
                     'url',
                     'docurl', 
                     ]
    validvalues = {
        'app_type' : ['htcondor' , 'workqueue' ],
        'app_role' : ['head-node' , 'worker-nodes' ]
        }
    intattributes = [ 'node_number',
                      'cores',
                      'memory_mb',
                      'storage_mb'
                     ]
    
    def __init__(self, name, 
                       state,
                       owner, 
                       acl, 
                       node_number, 
                       app_type, 
                       app_role,
                       resource_type='allocation',   # external, managed, allocation
                       cores=1, 
                       memory_mb=None, 
                       storage_mb=None, 
                       app_host = None, 
                       app_port = None,
                       app_sectoken = None,
                       environment = None,
                       description=None,
                       displayname=None,
                       url=None,
                       docurl=None,  
                       ):
        '''
        Creates a new Nodeset object. 
        
        :param str description: Long-form description
        :param str displayname: Pretty human-readable name/short description
        :param str url: High-level URL reference for this entity. 
        :param str docurl: Link to how-to/usage documentation for this entity.  
        :param str environment:  Environment to preload per job (e.g. a glidein)
            
        '''
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.owner = owner
        self.acl = acl
        self.node_number = node_number
        self.app_type = app_type
        self.app_role = app_role
        self.resource_type = resource_type
        
        self.cores = cores
        self.memory_mb = memory_mb
        self.storage_mb = storage_mb
        self.app_host = app_host
        self.app_port = app_port
        self.app_sectoken = app_sectoken
        self.environment = environment
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.log.debug("Entity created: %s" % self)
        
        
class Cluster(InfoEntity):
    '''
    AKA a Cluster Template
    
    Represents a supported VC3 middleware cluster application, node layout, and all relevant 
    configuration and dependencies to instantiate it. It is focussed on building the virtual 
    *cluster* not the task/job Environment needed to run a particular user's domain application. 
    
    Cluster descriptions should be generic and shareable across Users/Projects. 
    
    '''
    infokey = 'cluster'
    infoattributes = [ 'name',
                        'state',
                        'owner',
                        'acl',
                        'nodesets',
                        'description',
                        'displayname',
                        'url',
                        'docurl',
                      ]
    validvalues = {}
    intattributes = []

    def __init__(self, 
                 name, 
                 state, 
                 owner, 
                 acl, 
                 nodesets,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None ):
        '''
        Creates a new Cluster object. 
        
        :param str description: Long-form description
        :param str displayname: Pretty human-readable name/short description
        :param str url: High-level URL reference for this entity. 
        :param str docurl: Link to how-to/usage documentation for this entity.  
        '''
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.owner = owner
        self.acl = acl
        self.nodesets = nodesets # ordered list of nodeset labels
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.log.debug("Entity created: %s" % self)

    def addNodeset(self, nodesetname ):
        if self.nodesets is None:
            self.nodesets = []

        if nodesetname not in self.nodesets:
            nlist = self.nodesets
            nlist.append(nodesetname)
            self.nodesets = nlist


    def removeNodeset(self, nodesetname):
        if self.nodesets is None:
            self.nodesets = []


        if nodesetname not in self.nodesets:
            self.log.debug("Nodeset %s did not belong to Cluster" % nodesetname)
        else:
            nlist = self.nodesets
            nlist.remove(nodesetname)
            self.nodesets = nlist

        if nodesetname in self.nodesets:
            self.nodesets.remove(nodesetname)

class Environment(InfoEntity):
    '''
    Represents the node/job-level environment needed to run a given user task. 
    Consists of task requirements like job runtime, disk space, cpucount, gpu
    Consists of job requirements like application software, network access, http cache, CVMFS, etc. 
    
    '''
    infokey = 'environment'
    infoattributes = ['name',
                     'state',
                     'owner',
                     'acl',
                     'packagelist',
                     'envmap',
                     'files',
                     'command',
                     'builder_extra_args',
                     'description',
                     'displayname',
                     'url',
                     'docurl',
                     ]
    validvalues = { }
    intattributes = []

    def __init__(self, 
                 name, 
                 state, 
                 owner, 
                 acl,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None,  
                 packagelist=[], 
                 envmap={}, 
                 files={}, 
                 command = None, 
                 builder_extra_args = None):
        '''
        Defines a new Environment object. 
                  
        :param str name: The unique VC3 label for this environment.
        :param str owner:
        :param List str packagelist:
        :param Dict str->str envmap: 
        :param Dict str->str files: remote-name->contents files. Files to be included in the environment. (Files will be base64 encoded.)
        :param str command: command to execute the environment inside the builder. (e.g., vc3-glidein -c ...)
        :param List builder_extra_args: extra arguments to pass to the builder.
        :param str description: Long-form description
        :param str displayname: Pretty human-readable name/short description
        :param str url: High-level URL reference for this entity. 
        :param str docurl: Link to how-to/usage documentation for this entity. 
        :rtype: Environment
        
        '''  
        self.log = logging.getLogger()
        self.name  = name
        self.state = state
        self.acl   = acl
        self.owner = owner
        self.packagelist = packagelist
        self.envmap = envmap
        self.files = files
        self.command = command
        self.builder_extra_args = builder_extra_args
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.log.debug("Entity created: %s" % self)


class Request(InfoEntity):
    '''
    Represents and contains all information relevant to a concrete virtual cluster. 
    Contains sub-elements that reflect information from other Entities. 
    expiration:  Date or None   Time at which cluster should unconditionally do teardown if 
                                not actively terminated. 
    '''
    infokey = 'request'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'action',        # Command from webportal (run, terminate, etc.)
                     'state_reason',
                     'cluster_state', # State of virtual cluster this Request represents.
                     'cluster_state_reason',
                     'expiration',
                     'queuesconf',    # base64-encoded contents of factory queues.conf sections. 
                     'authconf',      # base64-encoded contents of factory auth.conf sections. 
                     'policy',        # name of policy to use to satisfy request
                     'allocations',   # list of allocations to satisfy this request
                     'environments',  # list of environments to satisfy this request
                     'cluster',       # contains cluster def, which includes nodeset descriptions
                     'statusraw',     # raw dictionary of submissions for all factories+allocations.
                     'statusinfo',    # aggregated submission status
                     'description',
                     'displayname',
                     'url',
                     'docurl',
                     'organization',                     
                     ]
    validvalues = {
                    'state' : ['new', 
                              'validated', 
                              'configured', 
                              'pending', 
                              'growing', 
                              'running', 
                              'shrinking', 
                              'terminating', 
                              'cleanup', 
                              'terminated'],
                     'action' : [ 'new', 'run', 'terminate' ]
                    } 
    intattributes = []
    
    def __init__(self, 
                 name, 
                 state, 
                 acl,
                 owner,
                 action = None,    # run | terminate
                 state_reason = None,
                 cluster_state = "new",
                 cluster_state_reason = None,
                 expiration = None,
                 queuesconf = None,
                 authconf = None, 
                 cluster=None, 
                 policy = None, 
                 allocations  = [],
                 environments = [],
                 statusraw = None,
                 statusinfo = None,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None,
                 organization = None,  
                 ):
        '''
        Creates a new Request object. 
        
        :param str name:          Label for this request. 
        :param str state:         State of request
        :param str state_reason:  Error reporting for state
        :param str action:        Command from webportal (e.g. run, terminate, etc.)
        :param str cluster_state: State of virtual cluster
        :param str cluster_state_reason:  Primarily for error reporting.
        :param str allocations:   List of allocations that the request shoud utilize.
        :param str policy:        Policy for utilizing the allocations. 
        :param str expiration:    Date YYYY-MM-DD,HH:MM:SS when this cluster expires and should be unconditionally terminated.    
                
        '''
        # Common attributes
        self.log = logging.getLogger()
        self.name = name
        self.state = state
        self.acl = acl
        self.owner = owner


        # Request-specific attributes
        self.action = action
        self.state_reason = state_reason
        self.expiration   = expiration
        self.cluster_state = cluster_state
        self.cluster_state_reason = cluster_state_reason
        self.queuesconf = queuesconf
        self.authconf = authconf
        self.statusraw = statusraw
        self.statusinfo = statusinfo
        
        # Composite attributes from other entities. 
        self.cluster = cluster
        self.policy  = policy

        if allocations is None:
            allocations = []
        if environments is None:
            environments = []

        self.allocations  = allocations
        self.environments = environments
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.organization = organization
        self.log.debug("Entity created: %s" % self)


class Provisioner(InfoEntity):
    '''
    Represents a VC3 provisioner component (e.g. vc3-factory, kubernetes?, other?)
        
    '''
    infokey = 'provisioner'
    infoattributes = ['name',
                     'state',
                     'acl',
                     'owner',
                     'type', # autopyfactory, kubernetes
                     'authconfig',
                     'queuesconf',
                     'description',
                     'displayname',
                     'url',
                     'docurl', 
                     ]
    validvalues = {}
    intattributes = []

    def __init__(self, 
                 name, 
                 state, 
                 acl, 
                 provtype='autopyfactory', 
                 authconfig=None, 
                 queuesconfig=None,
                 description=None,
                 displayname=None,
                 url=None,
                 docurl=None, 
                  ):
        '''
        Creates a new Provisioner object. 
              
        :param str name: The unique object name.
        :param str owner:
        :param str type:  What sort of provisioner [autopy/vc3-factory]
        :param str authconfig: (base64encoded) contents of auth.conf for a vc3-factory   
        :param str queuesconfig:  (base64encoded) contents of auth.conf a vc3-factory
        :rtype: Provisioner
        :return: Valid Provisioner object.  
        '''  
        self.log = logging.getLogger()
        self.name  = name  # i.e. factory-id
        self.state = state
        self.acl   = acl
        self.owner = owner
        self.type = provtype
        self.authconfig = authconfig
        self.queuesconfig = queuesconfig
        self.description = description
        self.displayname = displayname
        self.url = url
        self.docurl = docurl
        self.log.debug("Entity created: %s" % self)
                
        
        
if __name__ == '__main__':
    pass
    

