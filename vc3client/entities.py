#!/bin/env python

__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

'''

    + User
    Users always get a default Project, containing them as owner and member. 
    Users may add other users to projects they own.   
    User creates one or more Projects
    
    Projects contain users as members.
    
    + Resources     
       Admin users can define new Resources
       
    + Allocation
        Users can add their own Allocations on a given Resource. 

'''
import logging


class VC3Entity(object):
    '''
    Template for VC3 information entities. Common functions. 
    
    '''
    def __repr__(self):
        s = "%s(" % self.__class__.__name__
        for a in self.__class__.vc3attributes:
            s+="%s=%s " % (a, getattr(self, a, None)) 
        s += ")"
        return s    

    def makeDictObject(self):
        '''
        Converts this Python object to attribute dictionary suitable for addition to existing dict 
        intended to be converted back to JSON. Uses <obj>.name as key:
        
        '''
        d = {}
        d[self.name] = {}
        for attrname in self.vc3attributes:
            d[self.name][attrname] = getattr(self, attrname)
        self.log.debug("Returning dict: %s" % d)
        return d    

    @classmethod
    def objectFromDict(cls, dict):
        '''
        Returns an initialized Entity object from dictionary. 
        Input: Dict:
        { <name> : 
            {
                "name" : "<name>",
                "att1" : "<val1>"  
            }
        }
        '''
        name = dict.keys()[0]
        d = dict[name]
        args = {}
        for key in cls.vc3attributes:
            args[key] = d[key]
        eo = cls(**args)
        return eo
    

class User(VC3Entity):
    '''
    Represents a VC3 user account.
    As policy, name, email, and institution must be set.  

JSON representation:
{
    "user" : {
        "johnrhover": {
            "name"  : "johnrhover",
            "first" : "John",
            "last"  : "Hover",
            "email" : "jhover@bnl.gov",
            "institution" : "Brookhaven National Laboratory",
        },
    }
}
    '''
    vc3attributes = ['name',
                     'first',
                     'last',
                     'email',
                     'institution'] 
    
    def __init__(self, 
                   name,
                   first,
                   last,
                   email,
                   institution):
        '''
        Defines a new User object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 username of this user
        :param str first: User's first name
        :param str last: User's last name
        :param str email: User's email address
        :param str institution: User's intitutional affiliation or employer
        :return: User:  A valid User object      
        :rtype: User
        '''
        self.log = logging.getLogger()
        self.name = name
        self.first = first
        self.last = last
        self.email = email
        self.institution = institution
        self.log.debug("User object created: %s" % self)


    def store(self, infoclient):
        '''
        Stores this user in the provided infoclient info tree. 
        '''
        users = infoclient.getdocumentobject(key='user')
        du = self.makeDictObject()
        self.log.debug("Dict obj: %s" % du)
        infoclient.storedocumentobject(du, key='user')
                

class Project(VC3Entity):
    '''
    Represents a VC3 Project.
    '''
    
    vc3attributes = ['name',
                     'owner',
                     'members', 
                     'allocations',
                     'blueprints']
    
    
    def __init__(self, 
                   name,
                   owner,
                   members,
                   allocations=None, 
                   blueprints=None):
        '''
        Defines a new Project object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this project
        :param str owner: VC3 username of project owner. 
        :param 
        :return: User:  A valid Project objext. 
       
        :rtype: Project
        '''  
        self.log = logging.getLogger()
        self.name = name
        self.owner = owner
        self.members = []
        self.members.append(owner)
        if members is not None:
            for m in members:
                if m not in self.members:
                    self.members.append(m)
        self.allocations = allocations
        self.blueprints = blueprints
        self.log.debug("Project object created: %s" % self)

    def addUser(self, user):
        '''
            Adds provided user (string label) to this project.
        '''
        self.log.debug("Adding user %s to project" % user)
        if user not in self.members:
            self.members.append(user)
        self.log.debug("Members now %s" % self.members)
        

    def store(self, infoclient):
        '''
        Stores this project in the provided infoclient info tree. 
        '''
        projects = infoclient.getdocumentobject(key='project')
        dp = self.makeDictObject()
        self.log.debug("Dict obj: %s" % dp)
        infoclient.storedocumentobject(dp, key='project')
    
   


class Resource(VC3Entity):
    '''
    Represents a VC3 target resource. 
    
    "resource" : {
            "uchicago_rcc": {
                "resourcetype" : "remote-batch",  # grid remote-batch local-batch cloud
                "accessmode" : "MFA" # ssh, gsissh, 
                "submithost" : <hostname>,
                "submitport" : <port>,
                "type": "<batch-type>",
                "version": "14.11.11",
                },
            }
    
    intrinsic time limits/preemption flag to distinguish platforms we could run static components on. 
    network access is also critical for this.    
    '''
   
    vc3attributes = ['name',
                     'owner',
                     'accesstype', 
                     'accessmethod',
                     'accessflavor',
                     'gridresource',
                     'attributemap']
    
    
    
    def __init__(self,
                 name,
                 owner,
                 accesstype,   # grid, batch, cloud
                 accessmethod, # ssh, gsissh
                 accessflavor, # condor-ce, slurm, sge, ec2, nova, gce
                 gridresource, # http://cldext02.usatlas.bnl.gov:8773/services/Cloud , HTCodnor CE hostname[:port]              
                 mfa = False,
                 attributemap={}, # Dictionary of other key=value pairs defining resource properties. 
                 ):
        self.log = logging.getLogger()
        self.name = name
        self.owner = owner
        self.accesstype = accesstype
        self.accessmethod = accessmethod
        self.accessflavor = accessflavor
        self.gridresource = gridresource
        self.attributemap = attributemap
        self.log.debug("Project object created: %s" % self)

    def store(self, infoclient):
        '''
        Stores this project in the provided infoclient info tree. 
        '''
        resources = infoclient.getdocumentobject(key='resource')
        dr = self.makeDictObject()
        self.log.debug("Dict obj: %s" % dr)
        infoclient.storedocumentobject(dr, key='resource')


class Allocation(VC3Entity):
    '''
    Represents the access granted a VC3 User and a VC3 target Resource.
    Defined by (resource, vc3user, unix_account) triple.   
    
    May or may not contain sub-Allocations.
    
    (Top-level) Allocation names are in the form <vc3username>.<vc3resourcename>.
    Sub-allocation names are in the form <vc3username>.<vc3resourcename>.<suballocationlabel>
        
    "johnrhover.sdcc-ic." : {
        "acl" : "rw:vc3adminjhover, r:vc3jhover",
        "username": "jhover",
            "security-token" : { 
            "type" : "ssh-keypair",
            "ssh-type" : "ssh-rsa",
            "ssh-pubkey" : "AAAAB3NzaC1...",
            "ssh-privkey" : "XXXXXXXXXXXX...",
            },    
        },
        "johnrhover.amazon-ec2" : {
            "user" : "johnrhover",
            "resource" : "amazon-ec2"
            "acl" : "rw:vc3adminjhover, r:vc3jhover",
            "accountname" : "racf-cloud@rcf.rhic.bnl.gov",
            "security-token" :  {
                "type" : "cloud-tokens",
                "accesskey" : "AAAAB3NzaC1...",
                "privatekey" : "XXXXXXXXXXXX...",
                }
            }
        },
        "johnrhover.bnl-cluster1" : {
            "username": "jhover",
            "security-token" : {
                "type" : "ssh-keypair",
                "ssh-type" : "ssh-rsa",
                "ssh-pubkey" : "AAAAB3NzaC1...",
                "ssh-privkey" : "XXXXXXXXXXXX...",
                }
            }
        }
    '''
    vc3attributes = ['name',
                     'user',
                     'resource',
                     'type',
                     'quantity',
                     'units',
                     'username',
                     'sshprivkey',
                     'sshpubkey',
                     'sslcert',
                     'sslkey',
                     ''
                    ]   

    
    def __init__(self, owner, resource, type):
        '''
        :param str owner:         vc3username of owner of allocation
        :param str resource:      vc3 resource name 
        :param str type:          what sort of allocation (unlimited, limited, quota)
        :param Dict attributemap: Python Dict of other attributes
                
        '''

        self.name = "%s.%s" % (resource, user)

        self.user = user
        self.resource = resource
        self.type = type  # quota | unlimited 
        


class Request(VC3Entity):
    '''
    Represents and contains all information relevant to a concrete virtual cluster. 
    Contains sub-elements that reflect information from other Entities. 
    expiration:  Date or None   Time at which cluster should unconditionally do teardown if 
                                not actively terminated. 
    
    
    "johnrhover-req00001" : {
        "cluster" : "clustername",
        "environment" : {
                    <Environment json>
                },
        "allocations" : {
                    <Allocations>
                    },
        "policy" :  {
                <policy>
            }
        "expiration" : "2017-07-07:1730", 
    }
    

    }
    
    
    '''
    
    
    def getQueuesConf(self):
        pass
    

class Policy(VC3Entity):
    '''
    Describes the desired resource utilization policy when a Request 
    includes multiple Allocations. 
    
    '''
    
    def __init__(self, name, pluginname):
        ''' 
        "static-balanced" : {
                "pluginname" : "StaticBalanced",
            },
 
        "weighted-balanced" : {
                "pluginname" : "WeightedBalanced",
                "weightmap" : "sdcc-ic.johnrhover,.80,bnl-cluster1.johnrhover,.20"
            },
         
        "ordered-fill" : {
                "pluginname" : "OrderedFill",
                "fillorder: "sdcc-ic.johnrhover, bnl-cluster1.johnrhover,amazon-ec2.johnrhover" 
        }
        
        '''


class Cluster(VC3Entity):
    '''
    Represents a supported VC3 middleware cluster application, node layout, and all relevant configuration
    and dependencies to instantiate it. It is focussed on building the virtual *cluster* not the task/job 
    Environment needed to run a particular user's domain application. 
    
    Cluster descriptions should be generic and shareable across Users/Projects. 
    
    e.g. htcondor-managed-cm-schedd
         htcondor-managed-cm-ext-schedd
         workqueue-managed-catalog
         workqueue-ext-catalog
         ?
    
        "htcondor-managed-cm-schedd" : {
            "headnode1" : {
                "node_number" : "1",
                "node_memory_mb" : "4000",
                "node_cores_minimum" : "4",
                "node_storage_minimum_mb" : "50000",
                "app_type" : "htcondor",
                "app_role" : "head-node",
                "app_port" : "9618"
                "app_password" : "XXXXXXX",
            },
            "workers1" : {
                "app_depends" : "headnode1",
                "node_number" : "10",
                "node_cores_minimum" : "8",
                "node_memory_mb" : "4000",
                "node_storage_minimum_mb" : "20000",
                "app_type" : "htcondor",
                "app_role" : "execute",
                "app_host" : "${HEADNODE1}.hostname",
                "app_port" : "9618"
                "app_password" : "XXXXXXX",
            },
        }
    '''

    def __init__(self, name, ):
        '''
        :param str name:   Label for this cluster definition. 
        
        '''
        self.name = name
    
    def addNodeset(self, name, number, cores, memory_mb, storage_mb, app_type, app_role):
        pass




class Environment(VC3Entity):
    '''
    Represents the node/job-level environment needed to run a given user task. 
    Consists of task requirements like job runtime, disk space, cpucount, gpu
    Consists of job requirements like application software, network access, http cache, CVMFS, etc. 
    
    '''

    def __init__(self, name, owner,  packagelist=None, envmap=None ):
        '''
        Defines a new Environment object. 
              
        :param str name: The unique VC3 label for this environment.
        :param str owner:
        :param List str packagelist:
        :param Dict str envmap: 
        
        :return: User:  A valid Environment object
        :rtype: Environment
        '''  
        self.log = logging.getLogger()
        self.vc3attributes = ['name',
                             'owner',
                             'packagelist',
                             'envmap',
                             ]
        self.name = name
        self.owner = owner
        self.packagelist = packagelist
        self.envmap = envmap
        


def runtest():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    log = logging.getLogger()
    u = User(name='vc3jhover', 
             first='John', 
             last='Hover', 
             email='jhover@bnl.gov', 
             institution = 'BNL')
    log.info("User made %s" % u)
    du = u.makeDictObject()
    log.info("Dict made %s" % du)
    #u.store()


if __name__ == '__main__':
    runtest()
    

