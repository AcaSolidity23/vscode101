import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import win32com.client as win32
import pythoncom
import os

class OutlookEvents:
    def OnNewMailEx(self, receivedItemsIDs):
        namespace = outlook.GetNamespace("MAPI")
        for ID in receivedItemsIDs.split(","):
            mail = namespace.GetItemFromID(ID)
            if "NOSTRO" in mail.Subject:
                print(f"New email received from {mail.SenderEmailAddress} with subject: {mail.Subject}")
                print(f"Received on: {mail.ReceivedTime}")
                attachments = mail.Attachments
                for attachment in attachments:
                    if "NOSTRO LIQUIDITY"in attachment.FileName:
                        # Get today's date in the format _DD_MM_YY
                        today_date = datetime.now().strftime("_%d_%m_%y")
                        new_file_name = os.path.splitext(attachment.FileName)[0] + today_date + os.path.splitext(attachment.FileName)[1]
                        attachment.SaveAsFile(os.path.join(r'C:\Users\alazarevic\Desktop', new_file_name))
                        print(f"Attachment {attachment.FileName} saved.")
                        # Process the downloaded Excel file to create XML
                        process_excel_to_xml(file_path)

def process_excel_to_xml(file_path):
    # Read the Excel file
    xls = pd.ExcelFile(file_path)

    # Create the root element
    root = ET.Element("Root")

    # Add XML schema
    schema = ET.Element("xs:schema", attrib={
        "xmlns:xs": "http://www.w3.org/2001/XMLSchema",
        "elementFormDefault": "qualified"
    })
    root.append(schema)

# Define the structure of the XML
element = ET.SubElement(schema, "xs:element", attrib={"name": "Root"})
complex_type = ET.SubElement(element, "xs:complexType")
sequence = ET.SubElement(complex_type, "xs:sequence")
bank_name_element = ET.SubElement(sequence, "xs:element", attrib={"name": "BankName", "type": "xs:string"})

# Define the structure for the lower branch
row_element = ET.SubElement(sequence, "xs:element", attrib={"name": "Row"})
row_complex_type = ET.SubElement(row_element, "xs:complexType")
row_sequence = ET.SubElement(row_complex_type, "xs:sequence")

# Add columns to the schema
columns = {
    "datum knjizenja": "xs:date",
    "valuta": "xs:date",
    "debit": "xs:decimal",
    "credit": "xs:decimal",
    "stanje": "xs:decimal",
    "client": "xs:string"
}

for col_name, col_type in columns.items():
    ET.SubElement(row_sequence, "xs:element", attrib={"name": col_name, "type": col_type})

# Iterate over the sheets
for sheet_name in xls.sheet_names:
    sheet_element = ET.SubElement(root, "BankName", attrib={"name": sheet_name})

    # Read the sheet into a dataframe
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Add sheet data to the XML
    for i, row in df.iterrows():
        row_elem = ET.SubElement(sheet_element, "Row")
        for col_name in df.columns:
            col_name_str = str(col_name)
            col_elem = ET.SubElement(row_elem, col_name_str)
            cell_value = row[col_name]
            if isinstance(cell_value, datetime):
                # Format the date to dd-mm-yyyy
                cell_value = cell_value.strftime('%d-%m-%Y')
            elif col_name_str.lower() in ["debit", "credit", "stanje"]:
                    # Round to two decimal places
                    cell_value = round(float(cell_value), 2)
            col_elem.text = str(cell_value)

# Create a tree from the root element
tree = ET.ElementTree(root)

# Write the tree to an XML file
    xml_file_path = file_path.replace('.xlsx', '.xml')
    with open(xml_file_path, 'wb') as xml_file:
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    print(f"XML file created at {xml_file_path}")

# Connect to Outlook session
outlook = win32.DispatchWithEvents("Outlook.Application", OutlookEvents)

# Keep the script running to monitor incoming emails
while True:
    pythoncom.PumpWaitingMessages()
