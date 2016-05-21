#!/usr/bin/env python
import requests # Method of getting the XML information from PAN.
import xml.etree.ElementTree as ET # Difficult to use but good XML parser.
import xlsxwriter # Creates an Excel Spreadsheet.
import argparse

class Spreadsheet(object):
    """Create a spreadsheet from the XML document."""
    def __init__(self):
        self.name = None
        self.nattype = None
        self.src_zone = ""
        self.dst_zone = ""
        self.dst_interface = ""
        self.orig_source = ""
        self.orig_dst = ""
        self.service = ""
        self.src_translation = ""
        self.dst_translation = ""
        self.description = None
        self.disabled = "no" # Set to no since the PAN might return nothing for permit.

    def writeRowHeaders(self):
        """Write the header row of the spreadsheet."""
        titles = ["Rule Name", "NAT Type", "Src Zone", "Dst Zone", "Dst Interface", "Orig Src Address", "Orig Dst Address", "Service", "Src Translation", "Dst Translation", "Description", "Disabled"]
        i = 0
        for title in titles:
            worksheet.write(0, i, title, bold)
            i += 1

    def setName(self, name):
        """Populate the firewall rule description."""
        self.name = name

    def setNattype(self, nattype):
        """Set firewall nat type."""
        self.nattype = nattype

    def setSrc_zone(self, src_zone):
        """Set firewall src_zone."""
        if not self.src_zone == "": # If there are multiple entries add a comma to separate.
            self.src_zone += chr(10)
        self.src_zone +=str(src_zone) # Concatenate each entry.

    def setDst_zone(self, dst_zone):
        """Set firewall  dst_zone."""
        if not self.dst_zone == "": # If there are multiple entries add a comma to separate.
            self.dst_zone += chr(10)
        self.dst_zone +=str(dst_zone) # Concatenate each entry.

    def setDst_interface(self, dst_interface):
        """Set firewall dst_interface."""
        self.dst_interface = dst_interface

    def setOrig_source(self, orig_source):
        """Set firewall orig_source."""
        if not self.orig_source == "": # If there are multiple entries add a comma to separate.
            self.orig_source += chr(10)
        self.orig_source +=str(orig_source) # Concatenate each entry.
  
    def setOrig_dst(self, orig_dst):
        """Set firewall orig_dst."""
        if not self.orig_dst == "": # If there are multiple entries add a comma to separate.
            self.orig_dst += chr(10)
        self.orig_dst +=str(orig_dst) # Concatenate each entry.
    
    def setService(self, service):
        """Set firewall service."""
        if not self.service == "": # If there are multiple entries add a comma to separate.
            self.service += chr(10)
        self.service +=str(service) # Concatenate each entry.
    
    def setSrc_translation(self, src_translation):
        """Set firewall src_translation."""
        if not self.src_translation == "": # If there are multiple entries add a comma to separate.
            self.src_translation += chr(10)
        self.src_translation +=str(src_translation) # Concatenate each entry.
    
    def setDst_translation(self, dst_translation):
        """Set firewall dst_translation."""
        if not self.dst_translation == "": # If there are multiple entries add a comma to separate.
            self.dst_translation += chr(10)
        self.dst_translation +=str(dst_translation) # Concatenate each entry.

    def setDescription(self, description):
        """Populate the firewall description."""
        self.description = description

    def setDisabled(self, disabled):
        """Populate the firewall rule action."""
        self.disabled = disabled


    def writeRow(self, row):
        """Writes row to Excel workbook"""
        # Insert validation later
        worksheet.write(row, 0, self.name, dataformat)
        worksheet.write(row, 1, self.nattype, dataformat)
        worksheet.write(row, 2, self.src_zone, dataformat)
        worksheet.write(row, 3, self.dst_zone, dataformat)
        worksheet.write(row, 4, self.dst_interface, dataformat)
        worksheet.write(row, 5, self.orig_source, dataformat)
        worksheet.write(row, 6, self.orig_dst, dataformat)
        worksheet.write(row, 7, self.service, dataformat)
        worksheet.write(row, 8, self.src_translation, dataformat)
        worksheet.write(row, 9, self.dst_translation, dataformat)
        worksheet.write(row, 10, self.description, dataformat)
        worksheet.write(row, 11, self.disabled, dataformat)
        print "name: ", self.name
        print "nattype: ", self.nattype
        print "src_zone: ", self.src_zone
        print "dst_zone: ", self.dst_zone
        print "dst_interface: ", self.dst_interface
        print "orig_source: ", self.orig_source
        print "orig_dst: ", self.orig_dst
        print "service: ", self.service
        print "src_translation: ", self.src_translation
        print "dst_translation: ", self.dst_translation
        print "description: ", self.description
        print "disabled: ", self.disabled
        print "\n"
        
    def newRow(self):
        """Prepares for new row by clearing variables in class"""
        excelobj.__init__()

def commandlineparser():
    global args
    parser = argparse.ArgumentParser(description='Convert Palo Alto Networks Firewall rules from Panorama to Microsoft Excel.')
    parser.add_argument('-k', '--apikey', required=True, help='PAN API Token Key')
    parser.add_argument('-f', '--firewall', required=True, help='Firewall Name')
    parser.add_argument('-p', '--panorama', required=True, help='Panorama Managment URL')
    args = parser.parse_args()

if __name__ == '__main__':

    #Get command line arguments
    commandlineparser()

    row = 0 # Used to track which excel row we are on while parsing XML.

    url = "%s/api/?type=config&action=get&xpath=/config/devices/entry[@name=\'localhost.localdomain\']/device-group/entry[@name=\'%s\']/pre-rulebase/nat/rules&key=%s" % (args.panorama, args.firewall, args.apikey)

    xml = requests.get(url, verify=False)
    
    document = ET.fromstring(xml.content) # Parse the page the firewall returned as a string into the document object.
	
	#test code using example xml file
	#tree = ET.parse("nat.xml")
    #document = tree.getroot()
	
    workbook = xlsxwriter.Workbook('NAT_Policies.xlsx') # Create Excel spreadsheet.
    worksheet = workbook.add_worksheet() # Create new worksheet within the spreadsheet.

    bold = workbook.add_format({'bold': True}) # Cell formatting for row header

    dataformat = workbook.add_format() # Cell Formatting for data.
    dataformat.set_align('top')
    dataformat.set_text_wrap()
    worksheet.set_column(0,15, 20)

    excelobj = Spreadsheet()
    excelobj.writeRowHeaders() # Create friendly row headers in the spreadsheet.

    for result in document: # Start after root (result)
        for rules in result: # Start after result (rules)
            for entries in rules: # Start iterating after rules (entries)
                row += 1
                excelobj.setName(name=entries.attrib.get("name")) # Populate the rule description. Used attrib.get since name is a value within the tag.

                for nattype in entries.findall("nat-type"):
                    excelobj.setNattype(nattype.text)

                for src_zone in entries.findall("from"): 
                    for members in src_zone.findall("member"): 
                        excelobj.setSrc_zone(members.text)

                for dst_zone in entries.findall("to"): 
                    for members in dst_zone.findall("member"):
                        excelobj.setDst_zone(members.text)

                for dst_interface in entries.findall("to-interface"):
                    excelobj.setDst_interface(dst_interface.text)
				
                for orig_source in entries.findall("source"): 
                    for members in orig_source.findall("member"): 
                        excelobj.setOrig_source(members.text)

                for orig_dst in entries.findall("destination"):
                    for members in orig_dst.findall("member"):
                        excelobj.setOrig_dst(members.text)

                for service in entries.findall("service"):
                    excelobj.setService(service.text)
					
                for src_translation in entries.findall("source-translation"): 
                    for members in src_translation.findall("dynamic-ip"):
                        excelobj.setSrc_translation(members.tag)
                        for members2 in members.findall("fallback"): 
                            for members3 in members2.findall("interface-address"): 
                                excelobj.setSrc_translation(members3.tag + " " + members3.text)
                            for members3 in members2.findall("translated-address"): 
                                for members4 in members3.findall("member"):
								    excelobj.setSrc_translation(members3.tag + " " + '"'+members4.text+'"')
                        for members2 in members.findall("translated-address"): 
                            excelobj.setSrc_translation(members2.tag + " " + '"'+members2.text+'"')
                    for members in src_translation.findall("dynamic-ip-and-port"): 
                        excelobj.setSrc_translation(members.tag)
                        for members2 in members.findall("interface-address"): 
                            excelobj.setSrc_translation(members2.tag + " " + members2.text)
                        for members2 in members.findall("translated-address"):
                            for members3 in members2.findall("member"):
								excelobj.setSrc_translation(members2.tag + " " + '"'+members3.text+'"')						
                    for members in src_translation.findall("static-ip"): 
                        excelobj.setSrc_translation(members.tag)
                        for members2 in members.findall("bi-directional"): 
                            excelobj.setSrc_translation(members2.tag + " " + members2.text)
                        for members2 in members.findall("translated-address"): 
                            excelobj.setSrc_translation(members2.tag + " " + '"'+members2.text+'"')

                for dst_translation in entries.findall("destination-translation"): 
                    for members in dst_translation.findall("translated-address"): 
                        excelobj.setDst_translation(members.tag + " " + '"'+members.text+'"')
                    for members in dst_translation.findall("translated-port"): 
                        excelobj.setDst_translation(members.tag + " " + members.text)

                for description in entries.findall("description"):
                    excelobj.setDescription(description.text)
					
                for disabled in entries.findall("disabled"):
                    excelobj.setDisabled(disabled.text)

                excelobj.writeRow(row) # Write each row to the spreadsheet.
                excelobj.newRow() # Clear old values and start new row.


    workbook.close() # Close the spreadsheet since we are done with it now.

