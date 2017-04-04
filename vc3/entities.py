

class User(object):
    '''
    Represents a VC3 user account. 
    
    
    
    '''
    pass

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


    

