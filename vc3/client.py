#!/bin/env python
__author__ = "John Hover"
__copyright__ = "2017 John Hover"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.1"
__maintainer__ = "John Hover"
__email__ = "jhover@bnl.gov"
__status__ = "Production"

import argparse
import ast
import json
import logging
import os
import yaml

from ConfigParser import ConfigParser

from entities import User, Project, Resource, Allocation, Request, Cluster, Application
from vc3 import infoclient

class VC3ClientAPI(object):
    '''
    Client application programming interface. 
    -- Oriented toward exposing only valid operations to external
    user. 
    -- Direct manipulations of stored information in the infoservice is only done by Entity objects, not
    client user.
        
    -- Store method takes infoclient arg in order to allow multiple infoservice instances in the future. 
    '''
    
    def __init__(self, config):
        self.config = config
        self.ic = infoclient.InfoClient(self.config)
        self.log = logging.getLogger() 


    # User methods

    def defineUser(self,   
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
       :return: User  A valid User object
       
       :rtype: User        
        '''
        u = User( name, first, last, email, institution)
        self.log.debug("Creating user object: %s " % u)
        return u
    
        
    def createUser(self, user):
        '''
        Stores the provided user in the infoservice. 
        
        :param User u:  User to add. 
        :return: None
        '''
        user.store(self.ic)
        
                       
    def updateUser(self, u ):
        '''
        
        '''
        pass
    

    def listUsers(self):
        '''
        Returns list of all valid users as a list of User objects. 

        :return: return description
        :rtype: List of User objects. 
        
        '''
        docobj = self.ic.getdocumentobject('user')
        ulist = []
        try:
            for u in docobj['user'].keys():
                    s = "{ '%s' : %s }" % (u, docobj['user'][u] )
                    nd = {}
                    nd[u] = docobj['user'][u]
                    uo = User.objectFromDict(nd)
                    ulist.append(uo)
                    js = json.dumps(s)
                    ys = yaml.safe_load(js)
                    a = ast.literal_eval(js) 
                    #self.log.debug("dict= %s " % s)
                    #self.log.debug("obj= %s " % uo)
                    #self.log.debug("json = %s" % js)
                    #self.log.debug("yaml = %s" % ys)
                    #self.log.debug("ast = %s" % a)
                    #print(uo)
        except KeyError:
            pass
        return ulist

    def getUser(self, username):
        ulist = self.listUsers()
        for u in ulist:
            if u.name == username:
                return u
    
    # Project methods
    
    def defineProject(self, name, owner, members):
        '''
        Defines a new Project object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this project
        :param str owner:  The VC3 user name of the owner of this project
        :param List str:  List of VC3 user names of members of this project.  
        :return: Project  A valid Project object
        :rtype: Project        
        '''
        p = Project( name, owner, members = None)
        self.log.debug("Creating project object: %s " % p)
        return p
    
    
    def createProject(self, project):
        '''
        Stores the provided project in the infoservice. 
        
        :param Project project:  Project to add. 
        :return: None
        '''
        project.store(self.ic)
    
    
    def updateProject(self):
        pass
    
    def listProjects(self):
        docobj = self.ic.getdocumentobject('project')
        plist = []
        try:
            for p in docobj['project'].keys():
                    s = "{ '%s' : %s }" % (p, docobj['project'][p] )
                    nd = {}
                    nd[p] = docobj['project'][p]
                    po = Project.objectFromDict(nd)
                    plist.append(po)
                    js = json.dumps(s)
                    ys = yaml.safe_load(js)
                    a = ast.literal_eval(js) 
                    #self.log.debug("dict= %s " % s)
                    #self.log.debug("obj= %s " % uo)
                    #self.log.debug("json = %s" % js)
                    #self.log.debug("yaml = %s" % ys)
                    #self.log.debug("ast = %s" % a)
                    #print(uo)
        except KeyError:
            pass
        
        return plist
    
    
    def getProject(self, projectname):
        ulist = self.listProjects()
        for p in plist:
            if p.name == projectname:
                return p
    
        
        # Resource methods    
    def defineResource(self):
        '''
        Defines a new Resource object for usage elsewhere in the API. 
              
        :param str name: The unique VC3 name of this resource
        :param str owner:  The VC3 user name of the owner of this project
        :param str resourcetype,  # grid remote-batch local-batch cloud
        :param str accessmethod,  # ssh, gsissh,  
        :param str accessflavor,  # htcondor-ce, slurm, sge, ec2, nova, gce
        :param gridresource,      # http://cldext02.usatlas.bnl.gov:8773/services/Cloud  | HTCondorCE hostname             
        :param Boolean mfa        # Does site need head-node factory?
        :param Dict attributemap: # Arbitrary attribute dictionary.      
        :return: Resource          A valid Project object
        :rtype: Resource        
        
        '''
        r = Resource( name, owner, attributemap )
        self.log.debug("Creating Resource object: %s " % r)
        return r
    
    
    def createResource(self, resource):
        resource.store(self.ic)
    
    def ListResources(self):
        docobj = self.ic.getdocumentobject('resource')
        rlist = []
        try:
            for p in docobj['resource'].keys():
                    s = "{ '%s' : %s }" % (p, docobj['resource'][p] )
                    nd = {}
                    nd[p] = docobj['project'][p]
                    po = Project.objectFromDict(nd)
                    rlist.append(po)
                    js = json.dumps(s)
                    ys = yaml.safe_load(js)
                    a = ast.literal_eval(js) 
        except KeyError:
            pass
       
        return rlist
    
    def defineAllocation(self):
        pass
    
    
    def createAllocation(self):
        pass

    def listAllocations(self):
        pass
    
    def defineCluster(self):
        pass
    
    def createCluster(self):
        pass
    
    def listClusters(self):
        pass

    def defineRequest(self):
        pass
    
    def createRequest(self):
        pass

    def listRequests(self):
        pass
    
    
class EntityExistsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class VC3ClientCLI(object):
    '''
    
    '''
    def __init__(self):
        self.parseopts()
        self.setuplogging()


    def parseopts(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', '--config', 
                            action="store", 
                            dest='configpath', 
                            default='~/etc/vc3client.conf', 
                            help='configuration file path.')
        
        parser.add_argument('-d', '--debug', 
                            action="store_true", 
                            dest='debug', 
                            help='debug logging')        

        parser.add_argument('-v', '--verbose', 
                            action="store_true", 
                            dest='verbose', 
                            help='verbose/info logging')            
        
        # Init sub-command
        subparsers = parser.add_subparsers( dest="subcommand")

        parser_usercreate = subparsers.add_parser('user-create', 
                                                help='create new vc3 user')
        parser_usercreate.add_argument('username', 
                                     action="store")
        
        parser_usercreate.add_argument('--firstname', 
                                     action="store", 
                                     dest="firstname", 
                                     default='unknown')

        parser_usercreate.add_argument('--lastname', 
                                     action="store", 
                                     dest="lastname", 
                                     default='unknown')

        parser_usercreate.add_argument('--email', 
                                     action="store", 
                                     dest="email", 
                                     default='unknown')

        parser_usercreate.add_argument('--institution', 
                                     action="store", 
                                     dest="institution", 
                                     default='unknown')     
        
        parser_userlist = subparsers.add_parser('user-list', 
                                                help='list vc3 user(s)')
        
        parser_userlist.add_argument('--username', 
                                     action="store")

        parser_projectcreate = subparsers.add_parser('project-create', 
                                                help='create new vc3 project')
        
        parser_projectcreate.add_argument('projectname', 
                                     action="store")

        parser_projectcreate.add_argument('--owner', 
                                     action="store", 
                                     dest="owner", 
                                     default='unknown')

        parser_projectcreate.add_argument('--members', 
                                     action="store", 
                                     dest="members", 
                                     default='unknown')

        parser_projectlist = subparsers.add_parser('project-list', 
                                                help='list vc3 project(s)')

        parser_projectlist.add_argument('--projectname', 
                                     action="store")

        parser_resourcecreate = subparsers.add_parser('resource-create', 
                                                help='create new vc3 resource')
        
        parser_resourcecreate.add_argument('resourcename', 
                                     action="store")

        parser_resourcecreate.add_argument('--owner', 
                                     action="store", 
                                     dest="owner", 
                                     default='unknown')

        parser_resourcecreate.add_argument('--members', 
                                     action="store", 
                                     dest="members", 
                                     default='unknown')
        
        parser_resourcelist = subparsers.add_parser('resource-list', 
                                                help='list vc3 resource(s)')

        parser_resourcelist.add_argument('--projectname', 
                                     action="store")


        parser_allocationcreate = subparsers.add_parser('allocation-create', 
                                                help='create new vc3 allocation')
        
        parser_allocationcreate.add_argument('allocationname', 
                                     action="store")

        parser_allocationcreate.add_argument('--owner', 
                                     action="store", 
                                     dest="owner", 
                                     default='unknown')

        parser_allocationcreate.add_argument('--members', 
                                     action="store", 
                                     dest="members", 
                                     default='unknown')
        
        parser_allocationlist = subparsers.add_parser('allocation-list', 
                                                help='list vc3 allocation(s)')

        parser_allocationlist.add_argument('--projectname', 
                                     action="store")






        self.results= parser.parse_args()



    def setuplogging(self):
        self.log = logging.getLogger()
        FORMAT='%(asctime)s (UTC) [ %(levelname)s ] %(name)s %(filename)s:%(lineno)d %(funcName)s(): %(message)s'
        formatter = logging.Formatter(FORMAT)
        #formatter.converter = time.gmtime  # to convert timestamps to UTC
        logStream = logging.StreamHandler()
        logStream.setFormatter(formatter)
        self.log.addHandler(logStream)
    
        self.log.setLevel(logging.WARN)
        if self.results.debug:
            self.log.setLevel(logging.DEBUG)
        if self.results.verbose:
            self.log.setLevel(logging.INFO)
        self.log.info('Logging initialized.')


    def invoke(self):
        cp = ConfigParser()
        ns = self.results
        self.log.info("Config is %s" % ns.configpath)
        cp.read(os.path.expanduser(ns.configpath))

        capi = VC3ClientAPI(cp)
        
        # User commands
        if ns.subcommand == 'user-create':
            u = capi.defineUser( ns.username,
                             ns.firstname,
                             ns.lastname,
                             ns.email,
                             ns.institution)
            self.log.debug("User is %s" % u)
            capi.createUser(u)
            
        elif ns.subcommand == 'user-list' and ns.username is None:
            ulist = capi.listUsers()
            for u in ulist:
                print(u)
        
        elif ns.subcommand == 'user-list' and ns.username is not None:
            uo = capi.getUser(ns.username)
            print(uo)
        
        # Project commands
        elif ns.subcommand == 'project-create':
            p = capi.defineProject( ns.projectname,
                                    ns.owner,
                                    ns.members)
            self.log.debug("Project is %s" % p)
            capi.createUser(p)    
            
        elif ns.subcommand == 'project-list' and ns.projectname is None:
            plist = capi.listProjects()
            for p in plist:
                print(p)
        
        elif ns.subcommand == 'project-list' and ns.projectname is not None:
            po = capi.getProject(ns.projectname)
            print(po)

        # Resource commands
        elif ns.subcommand == 'resource-create':
            p = capi.defineProject( ns.resourcename,
                                    ns.owner,
                                    ns.members)
            self.log.debug("Project is %s" % p)
            capi.createUser(p)    
            
        elif ns.subcommand == 'resource-list' and ns.resourcename is None:
            plist = capi.listProjects()
            for p in plist:
                print(p)
        
        elif ns.subcommand == 'resource-list' and ns.resourcename is not None:
            po = capi.getProject(ns.resourcename)
            print(po)
        
        # Allocation commands
        elif ns.subcommand == 'allocation-create':
            p = capi.defineProject( ns.allocationname,
                                    ns.owner,
                                    ns.members)
            self.log.debug("Project is %s" % p)
            capi.createUser(p)    
            
        elif ns.subcommand == 'allocation-list' and ns.allocationname is None:
            plist = capi.listProjects()
            for p in plist:
                print(p)
        
        elif ns.subcommand == 'allocation-list' and ns.allocationname is not None:
            po = capi.getProject(ns.allocationname)
            print(po)
        
        
        else:
            self.log.warning('Unrecognized subcommand is %s' % ns.subcommand)
            

if __name__ == '__main__':
    vc3cli = VC3ClientCLI()
    vc3cli.invoke()    
