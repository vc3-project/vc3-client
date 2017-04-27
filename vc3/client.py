__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

#
# Abstract client library
#

import logging

from entities import User, Project, Resource, Allocation, Request, Cluster, Application
from vc3 import infoclient

class VC3ClientAPI(object):
    def __init__(self, config):
        self.config = config
        self.ic = infoclient.InfoClient(self.config)
        self.log = logging.getLogger() 

    def createUser(self,   
                   name,
                   first,
                   last,
                   email,
                   institution):           
        '''
         
        '''
        u = User( name, first, last, email, institution)
        self.log.debug("Creating user: %s " % u)
        
        
    def updateUser(self, name, ):
        '''
        
        '''

    def listUsers(self):
        doc = self.ic.getdocument('users')
        

        print(out)
       
    def updateUser(self):
        pass
    
    def createProject(self):
        pass
    
    def updateProject(self):
        pass
        
    def createResource(self):
        pass
    
    def ListResources(self):
        pass
    
    def createAllocation(self):
        pass

    def listAllocations(self):
        pass
    
    def createCluster(self):
        pass
    
    def listClusters(self):
        pass
    
    
class EntityExistsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    

