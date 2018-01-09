"""
Unit tests for testing user policies as implemented in the vc3 client code
"""

import unittest
import ConfigParser
import sys
import os

import vc3client.client


vc3_client = None


def setupModule():
    """
    Create
    :return:
    """
    global vc3_client

    c = ConfigParser.SafeConfigParser()
    if 'VC3_CLIENT_CONFIG' in os.environ:
        c.readfp(open(os.environ['VC3_CLIENT_CONFIG']))
    else:
        c.readfp(open('./vc3-client.ini'))

    try:
        vc3_client = vc3client.client.VC3ClientAPI.VC3ClientAPI(c)
    except Exception as e:
        sys.stderr.write("Couldn't get vc3 client: {0}".format(e))
        raise e


class TestUserPolicy(unittest.TestCase):
    """
    Class to test policy related to user operations
    """

    def testViewProfile(self):
        """
        Test viewing profile operations
        :return:  None
        """
        new_user = vc3_client.defineUser(identity_id='test_id',
                                         name='vc3name1',
                                         first='First',
                                         last='Last',
                                         email='test@test.edu',
                                         organization='Computation Institute',
                                         displayname='test1')

        vc3_client.storeUser(new_user)

        new_user2 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')


class TestAllocationPolicy(unittest.TestCase):
    """
    Class to test policy related to allocation operations
    """

    def setUp(self):
        """
        Setup vc3 client for subsequent tests
        :return:  None
        """

        new_user = vc3_client.defineUser(identity_id='test_id',
                                         name='vc3name1',
                                         first='First',
                                         last='Last',
                                         email='test@test.edu',
                                         organization='Computation Institute',
                                         displayname='test1')

        vc3_client.storeUser(new_user)
        self.__stored_user = new_user

        new_user2 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')
        self.__unstored_user = new_user2

        resource = vc3_client.defineResource(name='resource',
                                             owner=new_user.name,
                                             accesstype='remote-batch',
                                             accessmethod='ssh',
                                             accessflavor='slurm',
                                             accesshost='login.host',
                                             accessport='3890',
                                             gridresource='gridresource',
                                             cloudspotprice='spotprice',
                                             cloudinstancetype='instance_type',
                                             mfa='mfa',
                                             description='testresource',
                                             displayname='displayname',
                                             url='url',
                                             docurl='docurl',
                                             organization='Computation Institute',
                                             )
        vc3_client.storeResource(resource)
        self.__resource = resource

    def tearDown(self):
        """
        Remove entities created for tests
        :return:
        """

        vc3_client.deleteUser(self.__stored_user)
        vc3_client.deleteResource(self.__resource)

    def testAllocationCreation(self):
        """
        Test policies related to allocation creation
        :return: None
        """

        # test allocation with user not in infosystem
        test_allocation = vc3_client.defineAllocation(
            name='testallocation1',
            owner=self.__unstored_user.name,
            resource=self.__resource.name,
            accountname='dummy',
            displayname='testalloc1',
            description='test allocation 1')

        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.storeAllocation,
                          [test_allocation],
                          {'policyuser': self.__unstored_user.name})

        # test allocation creation with fake resource
        test_allocation = vc3_client.defineAllocation(
            name='testallocation1',
            owner=self.__stored_user.name,
            resource='fakeresource',
            accountname='dummy',
            displayname='testalloc1',
            description='test allocation 1')
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.storeAllocation,
                          [test_allocation],
                          {'policyuser': self.__stored_user.name})

        # verify allocation can be created with right policies
        test_allocation = vc3_client.defineAllocation(
            name='testallocation1',
            owner=self.__stored_user.name,
            resource=self.__resource.name,
            accountname='dummy',
            displayname='testalloc1',
            description='test allocation 1')
        vc3_client.storeAllocation(test_allocation,
                                   policy_user=self.__stored_user.name)

    def testAllocationEdit(self):
        """
        Test policies related to allocation editing
        :return: None
        """
        # verify allocation can be created with right policies
        test_allocation = vc3_client.defineAllocation(
            name='testallocation2',
            owner=self.__stored_user.name,
            resource=self.__resource.name,
            accountname='dummy',
            displayname='testalloc2',
            description='test allocation 2')
        vc3_client.storeAllocation(test_allocation,
                                   policy_user=self.__stored_user.name)

        # test editing displayname and description
        test_allocation.displayname = 'newtestalloc2'
        test_allocation.description = 'newdescription'
        vc3_client.storeAllocation(test_allocation,
                                   policy_user=self.__stored_user.name)

        # test editing invalid stuff
        test_allocation.name = 'newvc3name'
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.storeAllocation,
                          [test_allocation],
                          {'policyuser': self.__stored_user.name})

    def testAllocationDelete(self):
        """
        Test policies related to allocation deletion
        :return: None
        """

        test_allocation = vc3_client.defineAllocation(
            name='testallocation3',
            owner=self.__stored_user.name,
            resource=self.__resource.name,
            accountname='dummy',
            displayname='testalloc3',
            description='test allocation 3')
        vc3_client.storeAllocation(test_allocation,
                                   policy_user=self.__stored_user.name)

        # test deletion by non-owner
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.deleteAllocation,
                          [test_allocation],
                          {'policyuser': self.__unstored_user.name})

        # test deletion by valid owner
        vc3_client.deleteAllocation(test_allocation,
                                    policy_user=self.__stored_user.name)


class TestProjectPolicy(unittest.TestCase):
    """
    Class to test policy related to project operations
    """

    def setUp(self):
        """
        Setup vc3 client for subsequent tests
        :return:  None
        """

        new_user = vc3_client.defineUser(identity_id='test_id',
                                         name='vc3name1',
                                         first='First',
                                         last='Last',
                                         email='test@test.edu',
                                         organization='Computation Institute',
                                         displayname='test1')

        vc3_client.storeUser(new_user)
        self.__stored_user = new_user

        new_user2 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')
        vc3_client.storeUser(new_user2)
        self.__stored_user2 = new_user2

        new_user3 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')
        self.__unstored_user = new_user3

        resource = vc3_client.defineResource(name='resource',
                                             owner=new_user.name,
                                             accesstype='remote-batch',
                                             accessmethod='ssh',
                                             accessflavor='slurm',
                                             accesshost='login.host',
                                             accessport='3890',
                                             gridresource='gridresource',
                                             cloudspotprice='spotprice',
                                             cloudinstancetype='instance_type',
                                             mfa='mfa',
                                             description='testresource',
                                             displayname='displayname',
                                             url='url',
                                             docurl='docurl',
                                             organization='Computation Institute',
                                             )
        vc3_client.storeResource(resource)
        self.__resource = resource

        user_allocation = vc3_client.defineAllocation(
            name='testallocation3',
            owner=self.__stored_user.name,
            resource=self.__resource.name,
            accountname='dummy',
            displayname='testalloc3',
            description='test allocation 3')
        self.__user_allocation = user_allocation
        vc3_client.storeAllocation(user_allocation)

    def tearDown(self):
        """
        Remove entities created for tests
        :return:
        """

        vc3_client.deleteUser(self.__stored_user)
        vc3_client.deleteUser(self.__stored_user2)
        vc3_client.deleteResource(self.__resource)
        vc3_client.deleteAllocation(self.__user_allocation)

    def testProjectCreation(self):
        """
        Test policy for creation of projects

        :return: None
        """

        # verify users without allocation can't create
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.defineProject,
                          [],
                          {'name': 'testname',
                           'owner': self.__stored_user2.name,
                           'members': [],
                           'description': 'test description',
                           'displayname': 'displayname',
                           'url': None,
                           'docurl': None,
                           'organization': None,
                           'policyuser': self.__stored_user2.name})

        # verify creation with valid user
        test_proj1 = vc3_client.defineProject(name='testname1',
                                              owner=self.__stored_user.name,
                                              members=[],
                                              description=None,
                                              displayname=None,
                                              url=None,
                                              docurl=None,
                                              organization=None,
                                              policy_user=self.__stored_user.name)
        vc3_client.storeProject(test_proj1,
                                policy_user=self.__stored_user.name)

    def testProjectView(self):
        """
        Test policies for viewing a project

        :return: None
        """

        # verify view with invalid user
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.listProjects,
                          [],
                          {'policyuser': self.__unstored_user.name})

        # verify view with valid user
        vc3_client.listProjects(policy_user=self.__stored_user.name)

    def testProjectEdit(self):
        """
        Test policies for editing a project

        :return: None
        """
        test_proj1 = vc3_client.defineProject(name='testname1',
                                              owner=self.__stored_user.name,
                                              members=[],
                                              description=None,
                                              displayname=None,
                                              url=None,
                                              docurl=None,
                                              organization=None,
                                              policy_user=self.__stored_user.name)

        vc3_client.storeProject(test_proj1,
                                policy_user=self.__stored_user.name)

        # verify non-owner can't edit
        test_proj1.displayname = 'invalidname'
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.storeProjects,
                          [test_proj1],
                          {'policyuser': self.__stored_user.name2})

        # verify that owner can edit
        test_proj1.displayname = 'newname'
        vc3_client.storeProject(test_proj1,
                                policy_user=self.__stored_user.name)

        # verify owner can add members
        vc3_client.addUserToProject(self.__stored_user2.name,
                                    test_proj1,
                                    policy_user=self.__stored_user.name)

        # verify owner can remove members
        vc3_client.removeUserToProject(self.__stored_user2.name,
                                       test_proj1,
                                       policy_user=self.__stored_user.name)

        # verify non-owner can't add members
        self.assertRaises(vc3client.client.PermissionDenied,
                          vc3_client.addUserToProject,
                          [self.__stored_user2.name,
                                           test_proj1],
                          {'policyuser': self.__unstored_user2.name})

        # verify members can remove themselves
        vc3_client.addUserToProject(self.__stored_user2.name,
                                    test_proj1,
                                    policy_user=self.__stored_user.name)
        vc3_client.removeUserToProject(self.__stored_user2.name,
                                       test_proj1,
                                       policy_user=self.__stored_user2.name)

        # verify members can add their allocations
        vc3_client.addAllocationToProject(self.__user_allocation,
                                          test_proj1,
                                          policy_user=self.__stored_user.name)

        # verify members can remove their allocations
        vc3_client.removeAllocationToProject(self.__user_allocation,
                                             test_proj1,
                                             policy_user=self.__stored_user.name)

        def testAllocationDelete(self):
            """
            Test policies related to project deletion
            :return: None
            """

            test_proj1 = vc3_client.defineProject(name='testname1',
                                                  owner=self.__stored_user.name,
                                                  members=[],
                                                  description=None,
                                                  displayname=None,
                                                  url=None,
                                                  docurl=None,
                                                  organization=None,
                                                  policy_user=self.__stored_user.name)

            vc3_client.storeProject(test_proj1,
                                    policy_user=self.__stored_user.name)

            # test deletion by non-owner
            self.assertRaises(vc3client.client.PermissionDenied,
                              vc3_client.deleteProject,
                              [test_proj1],
                              {'policyuser': self.__stored_user2.name})

            # test deletion by valid owner
            vc3_client.deleteProject(test_proj1,
                                     policy_user=self.__stored_user.name)


class TestTemplatePolicy(unittest.TestCase):
    """
    Class to test policy related to cluster template operations
    """
    def setUp(self):
        """
        Setup vc3 client for subsequent tests
        :return:  None
        """

        new_user = vc3_client.defineUser(identity_id='test_id',
                                         name='vc3name1',
                                         first='First',
                                         last='Last',
                                         email='test@test.edu',
                                         organization='Computation Institute',
                                         displayname='test1')

        vc3_client.storeUser(new_user)
        self.__stored_user = new_user

        new_user2 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')
        vc3_client.storeUser(new_user2)
        self.__stored_user2 = new_user2

        new_user3 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')
        self.__unstored_user = new_user3

        resource = vc3_client.defineResource(name='resource',
                                             owner=new_user.name,
                                             accesstype='remote-batch',
                                             accessmethod='ssh',
                                             accessflavor='slurm',
                                             accesshost='login.host',
                                             accessport='3890',
                                             gridresource='gridresource',
                                             cloudspotprice='spotprice',
                                             cloudinstancetype='instance_type',
                                             mfa='mfa',
                                             description='testresource',
                                             displayname='displayname',
                                             url='url',
                                             docurl='docurl',
                                             organization='Computation Institute',
                                             )
        vc3_client.storeResource(resource)
        self.__resource = resource

        user_allocation = vc3_client.defineAllocation(
            name='testallocation3',
            owner=self.__stored_user.name,
            resource=self.__resource.name,
            accountname='dummy',
            displayname='testalloc3',
            description='test allocation 3')
        self.__user_allocation = user_allocation
        vc3_client.storeAllocation(user_allocation)


class TestRequestPolicy(unittest.TestCase):
    """
    Class to test policy related to cluster request operations
    """
    def setUp(self):
        """
        Setup vc3 client for subsequent tests
        :return:  None
        """

        new_user = vc3_client.defineUser(identity_id='test_id',
                                         name='vc3name1',
                                         first='First',
                                         last='Last',
                                         email='test@test.edu',
                                         organization='Computation Institute',
                                         displayname='test1')

        vc3_client.storeUser(new_user)
        self.__stored_user = new_user

        new_user2 = vc3_client.defineUser(identity_id='test_id2',
                                          name='vc3name2',
                                          first='First2',
                                          last='Last2',
                                          email='test2@test.edu',
                                          organization='Computation Institute',
                                          displayname='test2')
        self.__unstored_user = new_user2

        resource = vc3_client.defineResource(name='resource',
                                             owner=new_user.name,
                                             accesstype='remote-batch',
                                             accessmethod='ssh',
                                             accessflavor='slurm',
                                             accesshost='login.host',
                                             accessport='3890',
                                             gridresource='gridresource',
                                             cloudspotprice='spotprice',
                                             cloudinstancetype='instance_type',
                                             mfa='mfa',
                                             description='testresource',
                                             displayname='displayname',
                                             url='url',
                                             docurl='docurl',
                                             organization='Computation Institute',
                                             )
        vc3_client.storeResource(resource)
        self.__resource = resource

    def tearDown(self):
        """
        Remove entities created for tests
        :return:
        """

        vc3_client.deleteUser(self.__stored_user)
        vc3_client.deleteUser(self.__stored_user2)
        vc3_client.deleteResource(self.__resource)
        vc3_client.deleteAllocation(self.__user_allocation)
