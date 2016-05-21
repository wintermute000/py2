### Reads NX-OS config and looks for all interfaces and static routes under VRF DMZ

from ciscoconfparse import CiscoConfParse
from ciscoconfparse.ccp_util import IPv4Obj
from netaddr import *
import re
from pprint import pprint

parse = CiscoConfParse(config="eb-d63-csw-01-data-config",ignore_blank_lines=False)

INTF_RE = re.compile(r'interface\s\S+')
ADDR_RE = re.compile(r'ip\saddress\s(\S+)')
STATIC_RE = re.compile(r'ip\sroute\s(\S+)')
directly_connected = list()
static_routes = list()
prefixlist_entries = list()

DMZ_interface_objs = parse.find_objects_w_child(parentspec='^interface',childspec='vrf member DMZ')
for obj in DMZ_interface_objs:
    interface_ip_raw = obj.re_match_iter_typed(ADDR_RE, result_type=IPv4Obj)
    interface_network = str(interface_ip_raw.network) + '/' + str(interface_ip_raw.prefixlen)
    directly_connected.append(interface_network)

# vrf_objs = parse.find_objects('^vrf context DMZ')
# for obj in vrf_objs:
#    print (obj.ioscfg)
#    static_raw = obj.re_match_iter_typed(STATIC_RE)
#    print(static_raw)

DMZ_static_list = parse.find_children_w_parents('^vrf context DMZ',STATIC_RE)
for x in DMZ_static_list:
    static_rawlist = x.split()
    static_net = static_rawlist[2]
    static_dst = static_rawlist[3]
    #static_net = IPNetwork(static_raw)
    static_routes.append(str(static_net)+' '+str(static_dst))

DMZ_prefix_list = parse.find_lines('^ip prefix-list DMZ_STATIC.*permit.*')
for y in DMZ_prefix_list:
    prefixlist_rawlist = y.split()
    prefixlist_entry = prefixlist_rawlist[6]
    prefixlist_entries.append(prefixlist_entry)


print("Directly Connected Interface Networks in VRF DMZ")
print '\n'.join(directly_connected)
print("Static routes under VRF DMZ")
print '\n'.join(static_routes)
print("Prefix list networks permitted under DMZ_STATIC")
print '\n'.join(prefixlist_entries)

    #static_raw = static_rawlist[2]
    #print(static_raw)

    #static_route = x.split()
    #print(static_route)