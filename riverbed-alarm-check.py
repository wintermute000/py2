import paramiko
import time
import sys
import cmd
from pprint import pprint
from copy import deepcopy
import _collections
import sys
import re
import string



if len(sys.argv) != 2:
    # Exit the script
    sys.exit("Usage: ./riverbed-alarm-check <.csv file of list of riverbeds> ")

csv_list = sys.argv[1]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

username = 'as-monitoring'
password = 'Pr0m31heU$'
cmd1 = "terminal length 0"
cmd2 = "show alarms triggered"


hosts_to_action = {}
with open(csv_list) as hosts_csv:
    hosts_to_action = dict(line.strip().split(',') for line in hosts_csv if not line.startswith("#"))

for hostname,hostip in hosts_to_action.items():
    try:
        #calling paramiko to grab output of show ip eigrp neighbor

        ssh.connect(hostip,username=username, password=password)
        remote_conn = ssh.invoke_shell()
        output = remote_conn.recv(1000) # clear start characters/MOTD etc.
        remote_conn.send("terminal length 0\n")
        remote_conn.send("show alarms triggered\n")
        time.sleep(10)
        output = (remote_conn.recv(5000)).replace("\r","")
        show_alarm_lines = output.split("\n")
        show_alarm = show_alarm_lines[4:-1]
        print("#######################################################################")
        print('Active Alarms for ' + hostname + ':')
        pprint(show_alarm)
        print("\n")
        print("\n")
        ssh.close()
        # stdin, stdout, stderr = ssh.exec_command(cmd1)
        # stdin, stdout, stderr = ssh.exec_command(cmd2)
        # show_alarms_raw = stdout.read()
        # show_alarms = (show_alarms_raw.strip()).decode('ascii')
        #    pprint(show_alarms)

    except Exception as e: # Error handling - put login/pw errors into login-fail.log
        except_file = open("riverbed-fail.log", "a")
        except_output = 'Cannot connect to ' + (hostname) + ',' + (hostip) + ' \n'
        except_file.writelines(except_output)
        print("#######################################################################")
        print("\n")
        print("\n")
        print (except_output)
        print(e)
