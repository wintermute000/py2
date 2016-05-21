import paramiko
import time
import sys
import cmd
from pprint import pprint
from copy import deepcopy
import sys

if len(sys.argv) != 3:
    # Exit the script
    sys.exit("Usage: ./eigrp-nei-check <.csv file of router to check> <.csv file of neighbor list>")

csv_router = sys.argv[1]
csv_list = sys.argv[2]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#router_parameters is router to check, login, pw supplied in file eigrp-router-to-check.csv in format ip, login, pw
#using list comprehension syntax

router_parameters = {}
with open(csv_router) as eigrp_router_to_check:
        router_parameters = dict(line.strip().split(',') for line in eigrp_router_to_check)

routerip = router_parameters.get('router')
username = router_parameters.get('login')
password = router_parameters.get('pw')
hostname = router_parameters.get('hostname')

cmd = "sh ip eigrp nei"

#calling paramiko to grab output of show ip eigrp neighbor

ssh.connect(routerip,username=username, password=password)
stdin, stdout, stderr = ssh.exec_command(cmd)
show_ip_eigrp_nei_raw = stdout.read()
show_ip_eigrp_nei = (show_ip_eigrp_nei_raw.strip()).decode('ascii')

print("\n")
print ("router to check and credentials defined in file ./eigrp-router-to-check.csv")
print ("SSH to " + routerip + " and executing command 'show ip eigrp neighbor'")
print("\n")
print("###########################################################################################")
print(show_ip_eigrp_nei)
print("###########################################################################################")
print("\n")

#correct_nei is list of EIGRP peers expected supplied in file eigrp-nei-list.csv in format host,ip
#using list comprehension syntax
correct_nei = {}
with open(csv_list) as eigrp_nei_list_csv:
    correct_nei = dict(line.strip().split(',') for line in eigrp_nei_list_csv)

pprint("Checking router defined in " + csv_router + ' against EIGRP adjacency list defined in ' + csv_list)
print("\n")
pprint(correct_nei)
print("\n")
print("Note script does NOT check for extra neighbors, it only checks existence of neighbors in defined list above")
print("\n")

show_ip_eigrp_nei_lines = show_ip_eigrp_nei.split("\n")
down_peers = []
up_peers = []
# duplicate correct_nei as this list is used twice with pop
nei_existence = deepcopy(correct_nei)
nei_upcheck = deepcopy(correct_nei)

# pop each neighbor from nei_existence and iterate through show ip eigrp neighbor, if exist, append to new list up_peers
for x in range(len(nei_existence)):
    next_peer = nei_existence.popitem()[1]

    looping = True
    while looping:
        for y in show_ip_eigrp_nei_lines:
            if next_peer in y:
                if not next_peer in up_peers:
                    up_peers.append(next_peer)
                looping = False
            else:
                looping = False

# pop each neighbor from nei_upcheck and iterate through it comparing with up_peers list, print the status sequentially
for z in range(len(nei_upcheck)):
    next_check_peer = nei_upcheck.popitem()[1]
    if next_check_peer in up_peers:
        print(next_check_peer+" has valid EIGRP adjacency")
    else:
        print (next_check_peer+" is down in EIGRP")
        down_peers.append(next_check_peer)

print('\n')

# if nothing down print result, if peers are down list them

if len(down_peers) > 0:
    print("#######################################################################")
    print('EIGRP Neighbors Down for ' + hostname + ' are \n')
    for a in down_peers:
        for site_name,peer_ip in correct_nei.items():
            if peer_ip == a:
                print (site_name, peer_ip)
    print("#######################################################################")

else:
    print("#######################################################################")
    print('All EIGRP Neighbors Up!')
    print("#######################################################################")




