


pyats parse "show version" --testbed-file cml-testbed.yaml --devices cml-dist-rtr01
pyats parse "show ip route bgp" --testbed-file cml-testbed.yaml --devices cml-dist-rtr01

genie parse "show version" --testbed-file cml-testbed.yaml --devices cml-dist-rtr01


pyats parse "show version" --testbed-file cml-testbed.yaml --devices cml-dist-rtr01 --output output_cml-dist-rtr01

device.connect(learn_hostname=True)


pyats learn all --testbed-file mock.yaml --devices uut --output output_folder

##### Creating a project with two tests 'connectivity_checks' and 'bgp_neighbor' with no datafile. This command will create a boiler plate for pyATS AEtests.
```s
pyats create project --name my_test_project --testcases connectivity_checks bgp_neighbor --no-datafile
```

##### To create a testbed file from the excel sheet 'devices.xls' exists in the current directory
```s 
pyats create testbed file --path devices.xls --output testbed.yaml
```

##### To create a tesbed file interactively with encoded passwords
```s
pyats create testbed interactive --output testbed.yaml --encode-password
```

pyats validate testbed testbed.yaml 

pyats shell --testbed-file testbed.yaml

```bash
(main) expert@expert-cws:~/pyats-aetest$ pyats shell --testbed-file testbed.yaml
Welcome to pyATS Interactive Shell
==================================
Python 3.9.10 (main, Jan 15 2022, 18:17:56) 
[GCC 9.3.0]

>>> from pyats.topology.loader import load
>>> testbed = load('testbed.yaml')
-------------------------------------------------------------------------------            
In [1]: 
```

device = testbed.devices['csr1000v-1']
device.connect()
device.disconnect()

device.execute('show version')
device.parse('show version')

device.is_connected()

device.hostname
device.learn('all)
device.learn('interface')
device.learn('bgp')


>>> features = device.learn('all')
>>> for feature in features.keys():
...     print(feature)
... 
acl
arp
bgp
device
dot1x
eigrp
fdb
hsrp
igmp
interface
isis
lag
lisp
lldp
mcast
mld
msdp
nd
ntp
ospf
pim
platform
prefix_list
rip
route_policy
routing
static_routing
stp
vlan
vrf
vxlan
config
>>> 

To parse the output of the raw cli command without connecting to the device 
>>> raw_output = device.execute('show version')
>>> device.parse('show version', output=raw_output) 
{'version': {'xe_version': '17.03.01a', 'version_short': '17.3', 'platform': 'Virtual XE', 'version': '17.3.1a', 'image_id': 'X86_64_LINUX_IOSD-UNIVERSALK9-M', 'label': 'RELEASE SOFTWARE (fc3)', 'os': 'IOS-XE', 'location': 'Amsterdam', 'image_type': 'production image', 'copyright_years': '1986-2020', 'compiled_date': 'Wed 12-Aug-20 00:16', 'compiled_by': 'mcpre', 'rom': 'IOS-XE ROMMON', 'hostname': 'csr1000v-1', 'uptime': '17 hours, 36 minutes', 'uptime_this_cp': '17 hours, 38 minutes', 'returned_to_rom_by': 'reload', 'system_image': 'bootflash:packages.conf', 'last_reload_reason': 'reload', 'license_level': 'ax', 'license_type': 'N/A(Smart License Enabled)', 'next_reload_license_level': 'ax', 'chassis': 'CSR1000V', 'main_mem': '715705', 'processor_type': 'VXE', 'rtr_type': 'CSR1000V', 'chassis_sn': '9ESGOBARV9D', 'router_operating_mode': 'Autonomous', 'number_of_intfs': {'Gigabit Ethernet': '3'}, 'mem_size': {'non-volatile configuration': '32768', 'physical': '3978420'}, 'disks': {'bootflash:.': {'disk_size': '6188032', 'type_of_disk': 'virtual hard disk'}}, 'curr_config_register': '0x2102'}}
>>> 


To get the GigabitEthernet1 IP address 
>>> device.api.get_interface_ipv4_address(interface='GigabitEthernet1')
'10.10.20.48/24'
>>> 

Get current boot variables
>>> device.api.get_boot_variables(boot_var='current')
[]

Get next boot variables
>>> device.api.get_boot_variables(boot_var='next')
[]
>>> 

Get the IOS version 
>>> device.api.get_software_version()
'Cisco IOS Software [Amsterdam], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Experimental Version 17.3.1a RELEASE SOFTWARE (fc3)\nCopyright (c) 1986-2020 by Cisco Systems, Inc.\nCompiled Wed 12-Aug-20 00:16 by mcpre'
>>> 

Get the BGP summay 
>>> device.api.get_bgp_summary(address_family=None, vrf=None, rd=None, all_summary=False)
INFO:genie.libs.sdk.apis.iosxe.bgp.get:Command has not returned any results
{}
>>> 
Ping Parser
>>> device.api.ping(address='8.8.8.8', source='loopback100') 
{'ping': {'repeat': 5, 'data_bytes': 100, 'address': '8.8.8.8', 'timeout_secs': 2, 'source': '172.16.100.1', 'result_per_line': ['.....'], 'statistics': {'success_rate_percent': 0.0, 'received': 0, 'send': 5}}}
>>>
>>> output = device.execute("ping 8.8.8.8 source loopback100")
>>> device.api.ping(address='8.8.8.8', output=output) 
{'ping': {'repeat': 5, 'data_bytes': 100, 'address': '8.8.8.8', 'timeout_secs': 2, 'source': '172.16.100.1', 'result_per_line': ['.....'], 'statistics': {'success_rate_percent': 0.0, 'received': 0, 'send': 5}}}
>>> 



pyats run job jobfile.py --testbed-file "https://<url>/testbed.yaml"

pyats run job ./pyATS_Examples/source-route/job/source_route_job.py --testbed-file ./default_testbed.yaml --configuration ./pyATS_Examples/source-route/easypy_config.yaml --webex-token NmU0O--webex-room Y2lzY29zcGFy 


Default location for pyats log files
~/.pyats/archive
/tmp/


[Creating Testbed YAML File](https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html#creating-testbed-yaml-file)

[Testbed Device Connection](https://pubhub.devnetcloud.com/media/pyats-getting-started/docs/quickstart/manageconnections.html)

[Supported Device Platforms](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/supported_platforms.html)

[Unicon Plugins](https://pubhub.devnetcloud.com/media/unicon/docs/user_guide/introduction.html#installation)

