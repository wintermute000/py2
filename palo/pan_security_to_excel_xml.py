#!/usr/bin/env python
import requests # Method of getting the XML information from PAN.
import xml.etree.ElementTree as ET # Difficult to use but good XML parser.
import xlsxwriter # Creates an Excel Spreadsheet.
import argparse

#ASSUMES CONFIG FILE IS running-config.xml


class Spreadsheet(object):
    """Create a spreadsheet from the XML document."""
    def __init__(self):
        self.name = None
        self.from_member = ""
        self.to_member = ""
        self.source = ""
        self.destination = ""
        self.application = ""
        self.service = ""
        self.action = None
        self.profile = ""
        self.description = None
        self.disabled = "no" # Set to no since the PAN might return nothing for permit.
        self.expiration = None

    def writeRowHeaders(self):
        """Write the header row of the spreadsheet."""
        titles = ["Rule Name", "From Zone", "To Zone", "Source", "Destination", "Application", "Service", "Action", "Profile", "Description", "Disabled", "Expiration"]
        i = 0
        for title in titles:
            worksheet.write(0, i, title, bold)
            i += 1

    def setName(self, name):
        """Populate the firewall rule description."""
        self.name = name

    def setFromMember(self, from_member):
        """Set firewall from zone."""
        if not self.from_member == "": # If there are multiple entries add a comma to separate.
            self.from_member += chr(10)
        self.from_member +=str(from_member) # Concatenate each entry.

    def setToMember(self, to_member):
        """Set firewall to zone."""
        if not self.to_member == "": # If there are multiple entries add a comma to separate.
            self.to_member += chr(10)
        self.to_member +=str(to_member) # Concatenate each entry.

    def setSource(self, source):
        """Set firewall from source."""
        if not self.source == "": # If there are multiple entries add a comma to separate.
            self.source += chr(10)
        self.source +=str(source) # Concatenate each entry.

    def setDestination(self, destination):
        """Set firewall to destination."""
        if not self.destination == "": # If there are multiple entries add a comma to separate.
            self.destination += chr(10)
        self.destination +=str(destination) # Concatenate each entry.

    def setApplication(self, application):
        """Set firewall to application."""
        if not self.application == "": # If there are multiple entries add a comma to separate.
            self.application += chr(10)
        self.application +=str(application) # Concatenate each entry.

    def setService(self, service):
        """Set firewall to service."""
        if not self.service == "": # If there are multiple entries add a comma to separate.
            self.service += chr(10)
        self.service +=str(service) # Concatenate each entry.

    def setAction(self, action):
        """Populate the firewall rule action."""
        self.action = action

    def setProfile(self, profile):
        """Set firewall to profile."""
        if not self.profile == "": # If there are multiple entries add a comma to separate.
            self.profile += chr(10)
        self.profile +=str(profile) # Concatenate each entry.

    def setDescription(self, description):
        """Populate the firewall rule action."""
        self.description = description

    def setDisabled(self, disabled):
        """Populate the firewall rule action."""
        self.disabled = disabled

    def setExpiration(self, expiration):
        """Populate the firewall rule action."""
        self.expiration = expiration

    def writeRow(self, row):
        """Writes row to Excel workbook"""
        # Insert validation later
        worksheet.write(row, 0, self.name, dataformat)
        worksheet.write(row, 1, self.from_member, dataformat)
        worksheet.write(row, 2, self.to_member, dataformat)
        worksheet.write(row, 3, self.source, dataformat)
        worksheet.write(row, 4, self.destination, dataformat)
        worksheet.write(row, 5, self.application, dataformat)
        worksheet.write(row, 6, self.service, dataformat)
        worksheet.write(row, 7, self.action, dataformat)
        worksheet.write(row, 8, self.profile, dataformat)
        worksheet.write(row, 9, self.description, dataformat)
        worksheet.write(row, 10, self.disabled, dataformat)
        worksheet.write(row, 11, self.expiration, dataformat)

        print "Name: ", self.name
        print "From Zone: ", self.from_member
        print "To Zone: ", self.to_member
        print "Source: ", self.source
        print "Destination: ", self.destination
        print "Application: ", self.application
        print "Service: ", self.service
        print "Action: ", self.action
        print "Profile: ", self.profile
        print "Disabled: ", self.disabled
        print "Description: ", self.description
        print "Expiration: ", self.expiration
        print "\n"

    def newRow(self):
        """Prepares for new row by clearing variables in class"""
        excelobj.__init__()

def commandlineparser():
     global args
     parser = argparse.ArgumentParser(description='Convert Palo Alto Networks Firewall rules from XML to Microsoft Excel.')
     parser.add_argument('-d', '--device', required=True, help='device entry name')
     parser.add_argument('-v', '--vsys', required=True, help='vsys entry name')
     args = parser.parse_args()


if __name__ == '__main__':

    #Get command line arguments
    commandlineparser()

    row = 0 # Used to track which excel row we are on while parsing XML.

    #url = "%s/api/?type=config&action=get&xpath=/config/devices/entry[@name=\'localhost.localdomain\']/device-group/entry[@name=\'%s\']/pre-rulebase/security/rules&key=%s" % (args.panorama, args.firewall, args.apikey)

    xml = ET.parse('running-config.xml')
    document = xml.getroot()

    workbook = xlsxwriter.Workbook(args.device + '.' + args.vsys + "." + "security.policies.xlsx") # Create Excel spreadsheet.
    worksheet = workbook.add_worksheet() # Create new worksheet within the spreadsheet.

    bold = workbook.add_format({'bold': True}) # Cell formatting for row header

    dataformat = workbook.add_format() # Cell Formatting for data.
    dataformat.set_align('top')
    dataformat.set_text_wrap()
    worksheet.set_column(0,15, 20)

    excelobj = Spreadsheet()
    excelobj.writeRowHeaders() # Create friendly row headers in the spreadsheet.

    for root in document.findall("devices"): # Start after root (config)
        xpath_device = "entry[@name='%s']" % args.device
        for device in root.iterfind(xpath_device):
            for vsyssection in device.findall("vsys"):
                xpath_vsys = "entry[@name='%s']" % args.vsys
                for vsys in vsyssection.iterfind(xpath_vsys):
                    for rulebase in vsys.findall("rulebase"):
                        for security in rulebase.findall("security"):
                            for rules in security.findall("rules"):
                                for entries in rules:
                                    row += 1
                                    excelobj.setName(name=entries.attrib.get("name")) # Populate the rule description. Used attrib.get since name is a value within the tag.

                                    for fromzone in entries.findall("from"): # From zone block
                                        for members in fromzone.findall("member"): # From zone block - members block
                                            excelobj.setFromMember(members.text)

                                    for tozone in entries.findall("to"): # To zone block
                                        for members in tozone.findall("member"): # To zone block - members block
                                            excelobj.setToMember(members.text)

                                    for source in entries.findall("source"): # From source block
                                        for members in source.findall("member"): # From source block - members block
                                            excelobj.setSource(members.text)

                                    for destination in entries.findall("destination"): # application block
                                        for members in destination.findall("member"): # application block - members block
                                            excelobj.setDestination(members.text)

                                    for application in entries.findall("application"): # application block
                                        for members in application.findall("member"): # application block - members block
                                            excelobj.setApplication(members.text)

                                    for service in entries.findall("service"): # application block
                                        for members in service.findall("member"): # application block - members block
                                            excelobj.setService(members.text)

                                    for action in entries.findall("action"):
                                        excelobj.setAction(action.text)

                                    for profset in entries.findall("profile-setting"):
                                        for prof in profset.findall("profiles"):
                                            for virus in prof.findall("virus"):
                                                for members in virus.findall("member"):
                                                    excelobj.setProfile(virus.tag + " - " + members.text)
                                            for spyware in prof.findall("spyware"):
                                                for members in spyware.findall("member"):
                                                    excelobj.setProfile(spyware.tag + " - " + members.text)
                                            for vuln in prof.findall("vulnerability"):
                                                for members in vuln.findall("member"):
                                                    excelobj.setProfile(vuln.tag + " - " + members.text)
                                            for url in prof.findall("url-filtering"):
                                                for members in url.findall("member"):
                                                    excelobj.setProfile(url.tag + " - " + members.text)
                                            for file in prof.findall("file-blocking"):
                                                for members in file.findall("member"):
                                                    excelobj.setProfile(file.tag + " - " + members.text)
                                            for group in prof.findall("group"):
                                                for members in file.findall("member"):
                                                    excelobj.setProfile(group.tag + " - " + members.text)

                                    for description in entries.findall("description"):
                                        excelobj.setDescription(description.text)

                                    for disabled in entries.findall("disabled"):
                                        excelobj.setDisabled(disabled.text)

                                    for expiration in entries.findall("schedule"):
                                        excelobj.setExpiration(expiration.text)

                                    excelobj.writeRow(row) # Write each row to the spreadsheet.
                                    excelobj.newRow() # Clear old values and start new row.


    workbook.close() # Close the spreadsheet since we are done with it now.
#
# # XML document structure
# # <repsonse>
# #   <result>
# #       <rules>
# #           <entry>
# #               <from>
# #                   <member>from zone</member>
# #               </from>
# #                <to>
# #                   <member>to zone</member>
# #                </to>
# #               <source>
# #                   <member>source network</member>
# #               </source>
# #               <destination>
# #                   <member>destination network</member>
# #               </destination>
# #               <application>
# #                   <member>application</member>
# #               </application>
# #               <action>
# #                   value
# #               </action>
# #               <description>
# #                   value
# #               </description>
# #               <disabled>
# #                   value
# #               </disabled>
# #           </entry>
# #       </rules>
# #   </result>
# # </repsonse>
