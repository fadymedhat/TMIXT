import os
import re
import glob
import xml.etree.ElementTree as ET

"""

extract the printed lines transcriptions from the xml file 
and generate raw text file for each xml file

"""

#print(root.tag)

#print(root.attrib)
xml_files_path = './iamdb_original_xml'
raw_files_path = "printed_raw_text_files"
filename_list = os.listdir(xml_files_path)
filename_list = [os.path.basename(file_name) for file_name in glob.glob(xml_files_path+"/*.xml")]
print(filename_list)
for file in filename_list:
    print(file)
    tree = ET.parse(os.path.join(xml_files_path,file))
    root = tree.getroot()
    with open(os.path.join(raw_files_path, file.replace(".xml",".txt")), "a") as myfile:
        for child in root:
            #print(child.tag, child.attrib)
            if child.tag == 'machine-printed-part':
                for grand in child:
                    if 'text' in grand.attrib :
                        print(grand.attrib['text'])
                        myfile.write(re.sub('&amp;','&', re.sub('&quot;','"',grand.attrib['text']))+'\n')

