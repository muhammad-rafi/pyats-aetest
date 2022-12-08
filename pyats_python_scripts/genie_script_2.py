from genie.testbed import load
from rich import print as rprint
from unicon.core.errors import SubCommandFailure 

testbed_file = "testbed.yml"
testbed = load(testbed_file)

# print the testbed in Python dictionary
# rprint(testbed.__dict__['raw_config'])

device = testbed.devices['csr1000v-1']
# device.connect(log_stdout=False)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Connect to the device and run the raw cli commands 

# # Parameters dictionary for connect() 
# conn_param = {'learn_hostname': True, 
#               'learn_os': True, 
#               'init_config_commands': [], 
#               'init_exec_commands': ['terminal length 0', 
#                                      'show version',
#                                      'show ip interface brief'],
#               'log_stdout': 'False'
#               } 

# rprint(device.connect(**conn_param))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Another way to connect to the device and run the raw cli commands 

# List of command 
cmd_list = ['show version', 
            'show platform',
            'show ip interface brief',
            'show banner motd']

# Connect to the testbed device
output = device.connect(learn_hostname=True,
                        learn_os=True,
                        init_config_commands=[],
                        init_exec_commands=cmd_list,
                        log_stdout=False)
# print the output 
rprint(output)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #


# BGP test cases 
# https://github.com/CiscoTestAutomation/genielibs/blob/master/pkgs/conf-pkg/src/genie/libs/conf/bgp/iosxr/tests/test_bgp.py

# >>> from genie.conf import Genie
# >>> from genie.conf.base import Testbed, Device, Link, Interface
# >>> from genie.libs.conf.vrf import Vrf # for VRF
# >>> testbed = Testbed()
# >>> Genie.testbed = Testbed()
# >>> xe_device = Device(name='PE1', os='iosxe')
# >>> vrf = Vrf(name='test', testbed=testbed) # for VRF
# >>> xe_device.add_feature(vrf) # for VRF
# >>> interface = Interface(device=xe_device, name='GigabitEthernet1/0/10')
# >>> interface.vrf = vrf # for VRF
# >>> interface.switchport_enable = False
# >>> interface.shutdown = False
# >>> interface.vrf_downstream = "Staging"
# >>> interface.ipv4 = '200.1.1.2'
# >>> interface.ipv4.netmask = '255.255.255.0'
# >>> # interface.vrf = None
# >>> print(interface.build_config(apply=False))
# interface GigabitEthernet1/0/10
#  vrf forwarding test downstream Staging
#  ip address 200.1.1.2 255.255.255.0
#  no shutdown
#  no switchport
#  exit 


# connected_devices = "list_of_device_objects

# cmd_list = ['show interface',
#             'show interface status',
#             'show interface status | inc ected',
#             'show nothing',             # << invalid command
#             'show version'
#            ]

# def collect_cli_commands(device, cmd_list):
#     dev_details = {}
#     dev_details[device.name] = {}

#     for cmd in cmd_list:
#         dev_details[device.name][cmd] = '' 
#         try:
#             dev_details[device.name][cmd] = device.execute(cmd)
#             logger.info(f"succesfully executed '{cmd}' on device '{device.name}'")
#         except SubCommandFailure:
#             # print(paint("red_i", f"device: {device.name}:  /!\ `{cmd}` invalid command. Skipping."))
#             print(paint("red_i", f"device: {device.name}:  /!\ invalid command: '{cmd}'. Skipping."))
#         except Exception as e:
#             logger.warning(f"device: {device.name}: trying to execute: '{cmd}' causes exception: {str(e)}")
#             logger.debug("EXCEPTION: {e}")

#     return dev_details

# show_cmds = []
# for dev in connected_devices:
#     show_cmds.append(args.show)

# show_output = pcall(collect_cli_commands, device=connected_devices, cmd_list=show_cmds)
