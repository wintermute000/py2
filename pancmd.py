import pan.xapi
import xml.etree.ElementTree as ET
import pprint


xapi_instance = pan.xapi.PanXapi(api_username="o2networks",api_password="4install",api_key="LUFRPT1Xdk0zK2sxV0dGY3FlNmdVZ2dJZjd1eU1JOEU9TmV1NjBqL01EbW5FMHpGMnNpaGMzMUJscjk2M2VKNldsM3hTZHhjcVVNcz0",hostname="10.47.67.65",use_get=True,use_http=True)

panorama_name="localhost.localdomain"
firewall_name="Altona CC"
zone_var = "DMZ"

path="/config/devices/entry[@name=\'%s\']/device-group/entry[@name=\'%s\']" % (panorama_name,firewall_name)

policy_type = ".//pre-rulebase/security/rules"

xapi_instance.show(path)
xml_raw=xapi_instance.xml_document
xml_parsed=ET.fromstring(xml_raw)

xml_rules=xml_parsed.find(policy_type)


for i in xml_rules.iter():
    x=i.text
    if x == zone_var:
        print(ET.dump(i))















