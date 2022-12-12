from genie.conf import Genie
from genie.testbed import load

# Define the testbed filename
testbed_file = "iosxe_testbed.yaml"

commands_list = ["show ip interface brief ",
                "show interface description",
                "show processes cpu",
                "show version",]

# Create a testbed object for the network
# testbed = Genie.init("iosxe_testbed.yaml")
testbed = load(testbed_file)

# # for device in testbed.devices:
# for device in testbed:
#     # Connect to the device
#     # testbed.devices[device].connect()
#     device.connect(learn_hostname=False,
#                    init_exec_commands=[],
#                    init_config_commands=[],
#                    log_stdout=True)
    
#     # Learn all the show commands mentioned in the above commands_list
#     for command in commands_list:
#         # testbed.devices[device].execute(command)
#         device.execute(command)


for device in testbed.devices.values():
    # Connect to the device
    device.connect(learn_hostname=False,
                init_exec_commands=[],
                init_config_commands=[],
                log_stdout=True)
    
    # Learn all pyats features about the devices
    device.learn("all")
    

## To record the output of the above command in binary file 
# python mock_devices.py --record ./devices_record_dir

## To generate 'cml-dist-rtr01' mock device data
# python -m unicon.playback.mock --recorded-data ./devices_record_dir/cml-dist-rtr01 --output ./mocks/cml-dist-rtr01/cml-dist-rtr01.yaml

## To generate 'cml-dist-rtr02' mock device data
# python -m unicon.playback.mock --recorded-data ./devices_record_dir/cml-dist-rtr02 --output ./mocks/cml-dist-rtr02/cml-dist-rtr02.yaml

## To generate 'cml-dist-sw01' mock device data
# python -m unicon.playback.mock --recorded-data ./devices_record_dir/cml-dist-sw01 --output ./mocks/cml-dist-sw01/cml-dist-sw01.yaml

## To generate 'cml-dist-sw02' mock device data
# python -m unicon.playback.mock --recorded-data ./devices_record_dir/cml-dist-sw02 --output ./mocks/cml-dist-sw02/cml-dist-sw02.yaml

## To connect to the mock devices
# mock_device_cli --os iosxe --mock_data_dir  ./mocks/cml-dist-rtr01  --state connect
# mock_device_cli --os iosxe --mock_data_dir  ./mocks/cml-dist-rtr02  --state connect

# mock_device_cli --os nxos --mock_data_dir  ./mocks/cml-dist-sw01  --state connect
# mock_device_cli --os nxos --mock_data_dir  ./mocks/cml-dist-sw02  --state connect

### To disconnect press 'Ctrl + d'
