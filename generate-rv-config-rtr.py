import sys
import csv
import pprint
import netaddr
import copy
import pprint
import os

if len(sys.argv) != 3:
    # Exit the script
    sys.exit("Usage: ./generate-rv-config.py <.csv file of parameters> <.txt file of config-template>")

csv_parameters_csv = sys.argv[1]
config_template_csv = sys.argv[2]

config_parameters = []

config_template = str((open(config_template_csv)).read())

#----------------------------------------------------------------------
def csv_reader(file_obj):
    """
    Read a csv file
    """
    reader = csv.reader(file_obj)
    first_row = next(reader)
    for row in reader:
        config_parameters.append(row)
#----------------------------------------------------------------------

if __name__ == "__main__":
    with open(csv_parameters_csv) as parameters_obj:
        csv_reader(parameters_obj)

    os.chdir("./output_configs/")
    for i in config_parameters:
        sitename = i[0]
        site_template = str(copy.copy(config_template))

        area_str = str(i[1])

        loopback = netaddr.IPNetwork(i[2])
        loopback_ip = str(loopback.ip)
        loopback_mask = str(loopback.netmask)

        supernet = netaddr.IPNetwork(i[3])
        supernet_ip = str(supernet.network)
        supernet_mask = str(supernet.netmask)
        supernet_prefix = supernet_ip[0:-3]

        wannet = netaddr.IPNetwork(i[4])
        wannet_ip = str(wannet.network)
        wannet_mask = str(wannet.netmask)
        wan_router_ip_list = list(wannet)
        wan_router_ip = str(wan_router_ip_list[6])

        site_template = site_template.replace("%loopback%",loopback_ip)
        site_template = site_template.replace("%loopback_mask%",loopback_mask)
        site_template = site_template.replace("%area%",area_str)
        site_template = site_template.replace("%supernet%",supernet_ip)
        site_template = site_template.replace("%supernet_mask%",supernet_mask)
        site_template = site_template.replace("%wannet%",wannet_ip)
        site_template = site_template.replace("%wannet_mask%",wannet_mask)
        site_template = site_template.replace("%wan_router_ip%",wan_router_ip)
        site_template = site_template.replace("%supernet_prefix%",supernet_prefix)

        print(site_template)


        site_config = open("RV-DVN2-"+sitename+"-RTR.txt",'w')
        site_config = site_config.write(site_template)












