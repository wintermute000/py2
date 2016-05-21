# HOW TO USE - create CSV file with the first row in following format
# name,from,to,source,destination,application,service,action,log-end,profile-setting
# NOTE: Any field with multiple objects entries all entries to be enclosed with "quotes" and separated by a space character
# NOTE: Any field with a single object that has a space requires quotes e.g. "Object One"
# NOTE: log-end HAS to be yes or no (write out word in full)
# NOTE: assumes profile-setting is a group

import csv
import sys

if len(sys.argv) != 4:
    # Exit the script
    sys.exit("Usage: ./pan_csv_to_set.py <.csv file of policy> <device-group> <output-file>")

csv_raw = sys.argv[1]
device_group = sys.argv[2]
output = sys.argv[3]
set_line=""
output = open(output, "a")

with open(csv_raw, 'r') as csv_file:
    csv=csv.DictReader(csv_file)
    for row in csv:
        rule_name = row['name']
        from_zone = row['from']
        to_zone = row['to']
        src = row['source']
        dst = row['destination']
        app = row['application']
        svc = row['service']
        act = row['action']
        log_end = row['log-end']
        profile = row['profile-setting']

        set_line = "set device-group " + device_group + " pre-rulebase security rules " + rule_name + " from [ " + from_zone + " ] to [ " + to_zone + " ] source [ " + src + " ] destination [ " + dst + " ] application [ " + app + " ] service [ " + svc + " ] action " + act + " log-end " + log_end + " profile-setting group " + profile

        output.writelines(set_line)
        output.writelines("\n")
        print(set_line)



