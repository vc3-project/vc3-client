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
        for a in self.vc3attributes:
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


class User(VC3Entity):
    '''
    Represents a VC3 user account.
    As policy, name, email, and institution must be set.  

JSON representation:
{
    "user" : {
        "johnrhover": {
            "first" : "John",
            "last"  : "Hover",
            "email" : "jhover@bnl.gov",
            "institution" : "Brookhaven National Laboratory",
        },
    }
}

    '''
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
        self.vc3attributes = ['name','first','last','email','institution']
        self.log.debug("User object created: %s" % self)

        
    
    @staticmethod
    def objectFromDict(dict):
        '''
        Returns a User object from dictionary. 
        {'vc3jhover': {u'last': u'Last', u'email': u'Email', u'institution': u'BNL', u'first': u'First'}}
        -> User
        
        '''
        name = dict.keys()[0]
        d = dict[name]
        uo = User(name, 
                   d['first'],
                   d['last'],
                   d['email'],
                   d['institution'])
        return uo


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
    def __init__(self, 
                   name,
                   owner,
                   members):
        '''
        Defines a new Project object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this project
        :param str first: User's first name

        :return: User:  A valid Project objext. 
       
        :rtype: Project
        '''  
        self.log = logging.getLogger()
        self.name = name
        self.owner = owner
        self.members = members
        self.vc3attributes = ['name','owner','members']
        self.log.debug("Project object created: %s" % self)

    def store(self, infoclient):
        '''
        Stores this user in the provided infoclient info tree. 
        '''
        users = infoclient.getdocumentobject(key='project')
        dp = self.makeDictObject()
        self.log.debug("Dict obj: %s" % dp)
        infoclient.storedocumentobject(dp, key='project')
    
    
    @staticmethod
    def objectFromDict(dict):
        '''
        Returns a Project object from dictionary. 
        {'vc3jhover': {u'last': u'Last', u'email': u'Email', u'institution': u'BNL', u'first': u'First'}}
        -> User
        '''
        name = dict.keys()[0]
        d = dict[name]
        po = Project(name, 
                   d['owner'],
                   d['members'])
        return po
    


class Resource(object):
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
        
    '''
    def __init__(self,
                 name,
                 owner,
                 resourcetype,   # grid, batch, cloud
                 accessmethod, # ssh, gsissh
                 accessflavor, # condor-ce, slurm, sge, ec2, nova, gce
                 gridresource, # http://cldext02.usatlas.bnl.gov:8773/services/Cloud , HTCodnor CE hostname[:port]              
                 mfa = False,
                 attributemap={}, # Dictionary of other key=value pairs defining resource properties. 
                 ):
        self.log = logging.getLogger()
        self.name = name
        self.owner = owner
        self.resourcetype = accesstype
        self.accessmethod = accessmethod
        self.accessflavor = accessflavor
        self.gridresource = gridresource
        self.attributemap = attributemap
        self.log.debug("Project object created: %s" % self)







class Allocation(object):
    '''
    Represents the access granted a VC3 User and a VC3 target Resource.
    Defined by (resource, vc3user, unix_account) triple.   
    
    May or may not contain sub-Allocations.
    
    (Top-level) Allocation names are in the form <vc3resourcename>.<vc3username>
    
    "sdcc-ic.johnrhover" : {
        "acl" : "rw:vc3adminjhover, r:vc3jhover",
        "username": "jhover",
            "security-token" : { 
            "type" : "ssh-keypair",
            "ssh-type" : "ssh-rsa",
            "ssh-pubkey" : "AAAAB3NzaC1...",
            "ssh-privkey" : "XXXXXXXXXXXX...",
            },    
        },
        "amazon-ec2.johnrhover" : {
            "accountname" : "racf-cloud@rcf.rhic.bnl.gov",
            "security-token" :  {
                "type" : "cloud-tokens",
                "accesskey" : "AAAAB3NzaC1...",
                "privatekey" : "XXXXXXXXXXXX...",
                }
            }
        },
        "bnl-cluster1.johnrhover" : {
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
    
    


class Request(object):
    '''
    Represents and contains all information relevant to a concrete virtual cluster. 
    Contains sub-elements that reflect information from other Entities. 
    
    
    
    
    "johnrhover-req00001" : {
    
    
    }
    
    
    '''


class Cluster(object):
    '''
    Represents a useful collection of computing nodes as used by an Application.
    
    '''



class Policy(object):
    '''
    Describes the desired resource utilization policy when a Request 
    includes multiple Allocations. 
    
    '''


class Application(object):
    '''
    Represents a supported VC3 middleware application and all relevant configuration
    and dependencies to instantiate it. 
    
    '''







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
    

