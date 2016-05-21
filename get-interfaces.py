__author__ = 'jlo2'

from pprint import pprint
from Exscript.util.start import start
from Exscript.util.file  import get_hosts_from_file
from Exscript.util.match import first_match
from Exscript import Account
from Exscript.util.interact import read_login
from Exscript.protocols import SSH2
from Exscript.protocols import Telnet
from Exscript.util.interact import read_login
import Exscript.protocols.drivers
import collections
import socket
import csv

account = read_login()
show_ip_interface_brief = []
show_all_interfaces = []



# Create list of devices to query - uses list comprehension
hosts_to_action = {}
with open("get-interfaces.csv") as hosts_csv:
    hosts_to_action = collections.OrderedDict(line.strip().split(',') for line in hosts_csv if not line.startswith("#"))


# Function to test what port is open
def test_port(ip,port):
    connect = (ip,port)
    try:
        sock = socket.create_connection(connect,4)
        sock.close()
        return 1
    except Exception: return 0

# Function to grab show ip interface brief information off one device
def get_show_interface(ip):
    try:
        interfaces_raw = ""
        interface_lines = []
        interface_lines_raw = []

        # connect via Exscript

        conn.connect(ip)
        conn.login(account)

        conn.execute('terminal length 0')
        conn.execute('show ip interface brief | exclude unassigned')

        # Get output, split into list of lines
        interfaces_raw = repr(conn.response)
        interface_lines = interfaces_raw.split("\\r\\n")
        # Split each list entry into another list and insert hostname at beginning
        for line in interface_lines:
            # Ignore header line
            if 'Interface' in line:
                continue
            line_split = line.split()
            if len(line_split) == 6: #filter out irrelevant lines i.e. those not with 6 columns
                if_name, ip_addr, discard1, discard2, line_status, line_proto = line_split
                show_ip_interface_brief.append((ip, hostname, if_name, ip_addr, line_status, line_proto))
        # Append to master list and close connection
        show_all_interfaces.append(show_ip_interface_brief)

        resultfile = open("SHOW_IP_INTERFACES_BRIEF.CSV",'wb')
        wr = csv.writer(resultfile, dialect='excel')
        wr.writerows(show_ip_interface_brief)

        print('host '+ hostname +' successfully queried')
        conn.send('exit\r')        # Send the "exit" command
        conn.close()               # Wait for the connection to close

    except Exception as e: # Error handling - put login/pw errors into login-fail.log
        out_file = open("login-fail.log", "a")
        output = (hostname) + ',' + (ip) + ' has thrown a login error (password?)\n'
        out_file.writelines(output)
        print (hostname) + ',' + (ip) + " has thrown a login error (password?)"
        print(e)


# Function to iterate through list and call the show_interface function via appropriate mechanism
for hostname,ip in hosts_to_action.items():
    if test_port(ip,'22'):
      print('Querying host '+hostname+' via ssh...')
      conn = SSH2()
      get_show_interface(ip)

    elif test_port(ip,'23'):
      print('Querying host '+hostname+' via telnet...')
      conn = Telnet()
      get_show_interface(ip)

    else: # Error handling - put connectivity errors into connect-fail.log
      out_file = open("connect-fail.log", "a")
      output = (hostname) + ',' + (ip) + ' is not accessible via SSH or Telnet.\n'
      out_file.writelines(output)
      print (hostname) + ',' + (ip) + " is not accessible via SSH or Telnet."
      continue

print ("==============================================================================")
print ("Finished All Hosts - Results Below: Output to SHOW_IP_INTERFACES_BRIEF.CSV")
print ("==============================================================================")
pprint (show_all_interfaces)
print ("==============================================================================")








