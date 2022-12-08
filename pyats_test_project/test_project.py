'''
my_test_project.py

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
# from pyats.easypy import runtime
# runtime.runinfo.runinfo_dir 

# create a logger for this module
logger = logging.getLogger(__name__)

############################### COMMON SETUP SECTION ###############################

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def load_testbed(self, testbed):
        # Convert pyATS testbed to Genie Testbed
        logger.info(
            "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
        )
        testbed = load(testbed)
        print(self.parent.parameters)
        self.parent.parameters.update(testbed=testbed)
        
    # @aetest.subsection
    # def connect(self, testbed):
    #     '''
    #     establishes connection to all your testbed devices.
    #     '''
    #     # make sure testbed is provided
    #     assert testbed, 'Testbed is not provided!'
    #     print(testbed.devices.keys())
    #     # connect to all testbed devices
    #     try:
    #         # testbed.connect(log_stdout=False,
    #         #                 logfile=f'./logs/{testbed.devices.keys()}')
    #         testbed.connect(log_stdout=False,
    #                         logfile='/dev/null') 
                       
    #     except (TimeoutError, StateMachineError, ConnectionError):
    #         logger.error("Unable to connect to all devices")

    @aetest.subsection
    def connect(self, testbed):
        '''
        Establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        device_list = []

        for device in testbed.devices.values():
            logger.info(banner(
                "Connecting to device '{d}'".format(d=device.name)))
            try:
                device.connect(log_stdout=False,
                               logfile=f'./logs/{device.name}-{time.strftime("%Y-%m-%d-%H:%M:%S")}.log')
                
            except Exception as e:
                self.failed("Failed to establish connection to '{}'".format(
                    device.name))

            device_list.append(device)

        # Pass list of devices the to testcases
        self.parent.parameters.update(dev=device_list)
        print(device_list)
############################### TESTCASES SECTION ###############################

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


class routeCount(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """ Count the number of the routes.
            Pass or fail the test based on the 
            desired number of routes are present
        """
        self.routes = {}
        for device_name, device in testbed.devices.items():
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
                         self.passed()
                else:
                         self.failed()

class pingTest(aetest.Testcase):
    @aetest.setup
    def setup(self, testbed):
        """ Make sure devices can ping a list of addresses. """
        # List of addresses to ping:
        ping_list = ['8.8.8.8']
        self.ping_results = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to ping on supported network operation systems
            if device.os in ("iosxe", "nxos"):
            # if device.os in ("ios", "iosxe", "iosxr", "nxos"):
                logger.info(f"{device_name} connected status: {device.connected}")
                self.ping_results[device_name] = {}
                for ip in ping_list:
                    logger.info(f"Pinging {ip} from {device_name}")
                    try:
                        ping = device.ping(ip)
                        pingSuccessRate = ping[(ping.find('percent')-4):ping.find('percent')].strip()
                        try:
                            self.ping_results[device_name][ip] = int(pingSuccessRate)
                        except:
                            self.ping_results[device_name][ip] = 0
                    except:
                        self.ping_results[device_name][ip] = 0

    @aetest.test
    def test(self, steps):
        # Loop over every ping result
        for device_name, ips in self.ping_results.items():
            with steps.start(
                f"Looking for ping failures {device_name}", continue_=True
            ) as device_step:
                # Loop over every ping result
                for ip in ips:
                    with device_step.start(
                        f"Checking Ping from {device_name} to {ip}", continue_=True
                    ) as ping_step:
                        if ips[ip] < 100:
                            device_step.failed(
                            f'Device {device_name} had {ips[ip]}% success pinging {ip}')
                            
############################### COMMON CLEANUP SECTION ###############################

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

    # $ python test_project.py --testbed testbed.yaml
