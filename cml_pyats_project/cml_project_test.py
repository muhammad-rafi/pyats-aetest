'''
cml_project_test.py

To run standalone with testbed file 
python cml_project_test.py --testbed cml-testbed.yaml
'''
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

# optional author information
# (update below with your contact information if needed)
__author__ = 'Cisco Systems Inc.'
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'
__contact__ = ['pyats-support-ext@cisco.com']
__credits__ = ['list', 'of', 'credit']
__version__ = 1.0

import logging
import time
from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError
from ats.log.utils import banner
from genie.utils.diff import Diff
from genie.utils import Dq
# from pyats.easypy import runtime
# runtime.runinfo.runinfo_dir 

# create a logger for this module
logger = logging.getLogger(__name__)

####################################################################################
############################### COMMON SETUP SECTION ###############################
####################################################################################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def load_testbed(self, testbed):
        # Convert pyATS testbed to Genie Testbed
        logger.info(
            "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
        )
        testbed = load(testbed)
        # print(self.parent.parameters)
        self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        '''
        Establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        device_list = []

        for device in testbed.devices.values():
            # print(device.name)
            logger.info(banner(
                "Connecting to device '{d}'".format(d=device.name)))
            try:
                device.connect(log_stdout=False,
                               logfile=f'./logs/{device.name}-{time.strftime("%Y-%m-%d-%H:%M:%S")}.log')
                # device.connect(log_stdout=False)
                
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)
        # print(device_list)
        
####################################################################################
################################# TESTCASES SECTION ################################
####################################################################################

class connectivityTest(aetest.Testcase):
    """verify_connected
    Ensure successful connection to all devices in testbed.
    """

    @aetest.test
    def test(self, testbed, steps):
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            with steps.start(f"Test Connection Status of {device_name}", continue_=True) as step:
                # Test "connected" status
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.failed()


class routeCountTest(aetest.Testcase):
    @aetest.test
    def test(self, testbed, steps):
        """ Count the number of the routes.
            Pass or fail the test based on the 
            desired number of routes are present
        """
        self.routes = {}
        for device_name, device in testbed.devices.items():
            with steps.start(f"Total Route Counts for {device_name}", continue_=True) as step:
                # Only attempt to learn details on supported network operation systems
                if device.os in ("iosxe"):
                    logger.info(f"{device_name} connected status: {device.connected}")
                    logger.info(f"Learning route table for {device_name}")
                    routeTable = device.parse("show ip route")
                    self.routes[device_name] = {}
                    self.routes[device_name]['routeTable'] = routeTable
                    
                    logger.info(self.routes[device_name]['routeTable'])
                    logger.info(len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']))
                    # no_of_routes = len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes'])
                    # print(no_of_routes)
                    if len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']) > 5:
                            step.passed()
                    else:
                            step.failed()
                         
class bgpRouteTest(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """ Count the number of the BGP routes.
            Pass or fail the test based on the 
            desired number of routes are present
        """
        self.routes = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("iosxe"):
                logger.info(f"{device_name} connected status: {device.connected}")
                logger.info(f"Learning route table for {device_name}")
                routeTable = device.parse("show ip route bgp")
                self.routes[device_name] = {}
                self.routes[device_name]['routeTable'] = routeTable
                logger.info(self.routes[device_name]['routeTable'])
                logger.info(len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']))
                # no_of_routes = len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes'])
                # print(no_of_routes)
                if len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']) > 0:
                        self.passed()
                else:
                        self.failed()

    @aetest.test
    def test(self, testbed, steps):
        """ Check the BGP routes on iosxe deviece.
            Pass or fail the test based on the 
            difference in the prefixes between 
            two devices BGP routing tables.
        """
        self.routes = {}
        dev_list = []
        missing_prefixes = []
        # with steps.start(f"BGP Routes Difference {device_name}", continue_=True) as step:
        with steps.start(f"BGP Routes Difference Between Devices", continue_=True) as step:
            for device_name, device in testbed.devices.items():
                dev_list.append(device_name)
                logger.info(dev_list)
                # Only attempt to learn details on supported network operation systems
                if device.os in ("iosxe"):
                    logger.info(f"{device_name} connected status: {device.connected}")
                    logger.info(f"Learning route table for {device_name}")
                    routeTable = device.parse("show ip route bgp")
                    self.routes[device_name] = {}
                    self.routes[device_name]['routeTable'] = routeTable
                    # logger.info(self.routes[device_name]['routeTable'])
                    # logger.info(len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']))
                    
                    self.routes[device_name]['bgp_routes'] = routeTable.q.contains('bgp').get_values('routes')
                    # print(routeTable.q.contains('bgp').get_values('routes'))
                    # bgp_routes = self.routes[dev_list[0]]['bgp_routes']
                        
            bgp_routes_dev1 = self.routes[dev_list[0]]['bgp_routes']
            bgp_routes_dev2 = self.routes[dev_list[1]]['bgp_routes']
            
            # print(bgp_routes_dev1)
            # print(bgp_routes_dev2)
            # print('\n')
            
            for i in bgp_routes_dev1:
                if i not in bgp_routes_dev2:
                    # print(i + '\n')
                    missing_prefixes.append(i)
                    logger.info(f"{dev_list[1]} missing {missing_prefixes} bgp prefixes")

            for j in bgp_routes_dev2:
                if j not in bgp_routes_dev1:
                    # print(j + '\n')
                    missing_prefixes.append(j)
                    logger.info(f"{dev_list[0]} missing {missing_prefixes} bgp prefixes")

            # print(missing_prefixes)
            
            if len(missing_prefixes) == 0:
                logger.info(f"{dev_list[0]} and {dev_list[1]} have same bgp prefixes")
                step.passed()
            else:
                logger.info(f"missing_prefixes = {missing_prefixes}")
                step.failed()
            
    # @aetest.test
    # def test(self, testbed, steps):
    #     """ Check the BGP routes on iosxe deviece.
    #         Pass or fail the test based on the 
    #         difference in the BGP routing table.
    #     """
    #     self.routes = {}
    #     dev_list = []
    #     missing_prefixes = []
    #     for device_name, device in testbed.devices.items():
    #         dev_list.append(device_name)
    #         logger.info(dev_list)
    #         with steps.start(f"BGP Routes Difference {device_name}", continue_=True) as step:
    #             # Only attempt to learn details on supported network operation systems
    #             if device.os in ("iosxe"):
    #                 logger.info(f"{device_name} connected status: {device.connected}")
    #                 logger.info(f"Learning route table for {device_name}")
    #                 routeTable = device.parse("show ip route bgp")
    #                 self.routes[device_name] = {}
    #                 self.routes[device_name]['routeTable'] = routeTable
    #                 # logger.info(self.routes[device_name]['routeTable'])
    #                 # logger.info(len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']))
                    
    #                 self.routes[device_name]['bgp_routes'] = routeTable.q.contains('bgp').get_values('routes')
    #                 # print(routeTable.q.contains('bgp').get_values('routes'))
    #                 bgp_routes = self.routes[dev_list[0]]['bgp_routes']
                    
                        
    #     bgp_routes_dev1 = self.routes[dev_list[0]]['bgp_routes']
    #     bgp_routes_dev2 = self.routes[dev_list[1]]['bgp_routes']
        
    #     print(bgp_routes_dev1)
    #     print(bgp_routes_dev2)
    #     print('\n')
        
    #     for i in bgp_routes_dev1:
    #         if i not in bgp_routes_dev2:
    #             print(i + '\n')
    #             missing_prefixes.append(i)

    #     for j in bgp_routes_dev2:
    #         if j not in bgp_routes_dev1:
    #             print(j + '\n')
    #             missing_prefixes.append(j)
        
    #     print(missing_prefixes)
        
    #     if len(missing_prefixes) == 0:
    #         logger.info(f"{dev_list[0]} and {dev_list[1]} have same bgp prefixes")
    #         step.passed()
    #     else:
    #         step.failed()
    #         logger.info(f"missing_prefixes = {missing_prefixes}")

        # ------------------------------------------------------------------------------------------------------------------------- #
            # for i in bgp_routes_dev1:       
                # for j in bgp_routes_dev2:
                #     if i not in j:
                #         print(i)
                        # missing_routes.append(i)
                    # elif j not in i:
            #     print(j)

        # ------------------------------------------------------------------------------------------------------------------------- #
        # Get the common routes 
        # bgp_routes_dev1 = set(self.routes[dev_list[0]]['bgp_routes'])
        # bgp_routes_dev2 = set(self.routes[dev_list[1]]['bgp_routes'])
        # print(bgp_routes_dev1.intersection(bgp_routes_dev2))
        
        # ------------------------------------------------------------------------------------------------------------------------- #
        # Get the devices name
        # logger.info(self.routes.keys())
        # print(self.routes.keys())

        # ------------------------------------------------------------------------------------------------------------------------- #
        #             bgp_routes = self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes'].keys()
        #             self.routes[device_name]['bgp_routes'] = bgp_routes
        #             # logger.info(self.routes[device_name]['bgp_routes'])
        # print(list(self.routes[dev_list[0]]['bgp_routes']))
        
        # ------------------------------------------------------------------------------------------------------------------------- #        
        # Get the routes for both devices defined on the testbed
        # print(self.routes[dev_list[0]]['routeTable']['vrf']['default']['address_family']['ipv4']['routes'])
        # print(self.routes[dev_list[1]]['routeTable']['vrf']['default']['address_family']['ipv4']['routes'])
        # ------------------------------------------------------------------------------------------------------------------------- #
        
        # # diff = Diff(list(self.routes[dev_list[0]]['bgp_routes']), list(self.routes[dev_list[0]]['bgp_routes']))
        # diff = Diff(self.routes[dev_list[0]], self.routes[dev_list[0]])
        # print(str(diff.findDiff()))
                    
                    # if len(self.routes[device_name]['routeTable']['vrf']['default']['address_family']['ipv4']['routes']) > 5:
                    #         step.passed()
                    # else:
                    #         step.failed()
        
        
######################################################################################
############################### COMMON CLEANUP SECTION ###############################
######################################################################################

class CommonCleanup(aetest.CommonCleanup):
    '''CommonCleanup Section

    < common cleanup docstring >

    '''

    # uncomment to add new subsections
    # @aetest.subsection
    # def subsection_cleanup_one(self):
    #     pass

if __name__ == '__main__':
    # for stand-alone execution
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--testbed', dest = 'testbed',
                        help = 'testbed YAML file',
                        type = topology.loader.load,
                        default = None)

    # do the parsing
    args = parser.parse_known_args()[0]
    aetest.main(testbed = args.testbed)
    