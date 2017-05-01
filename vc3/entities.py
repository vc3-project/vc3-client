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

class User(object):
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
        self.doc_attributes = ["first",'last','email','institution']
        self.log.debug("User object created: %s" % self)
        
    def __repr__(self):
        s =  "User(name=%s, first=%s, last=%s, email=%s, institution=%s " % (self.name,
            self.first,
            self.last,
            self.email,
            self.institution)
        return s

    def makeDictObject(self):
        '''
        Converts Python object to attribute dictionary suitable for addition to existing dict 
        intended to be converted back to JSON. Uses <obj>.name as key:
        
        '''
        d = {}
        d[self.name] = {}
        for attrname in self.doc_attributes:
            d[self.name][attrname] = getattr(self, attrname)
        self.log.debug("Returning dict: %s" % d)
        return d
        
        
    def store(self, infoclient):
        '''
        Stores this user in the provided infoclient info tree. 
        '''
        users = infoclient.getdocumentobject(key='user')
        du = self.makeDictObject()
        self.log.debug("Dict obj: %s" % du)
        infoclient.storedocumentobject(du, key='user')
                
        
          

class Project(object):
    '''
    Represents a VC3 Project.
    
    
    '''




class Resource(object):
    '''
    Represents a VC3 target resource. 
    
    
    '''

class Allocation(object):
    '''
    Represents the access granted a VC3 User and a VC3 target Resource.
    Defined by (resource, vc3user, unix_account) triple.   
    
    May or may not contain sub-Allocations. 
    
    '''


class Request(object):
    '''
    Represents and contains all information relevant to a concrete virtual cluster. 
    
    
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
    

