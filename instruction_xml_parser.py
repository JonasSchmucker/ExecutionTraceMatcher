# Python code to illustrate parsing of XML files
# importing the required modules
import json
import xml.etree.ElementTree as element_tree
  
  
def parseXML(xmlfile):
  
    # create element tree object
    tree = element_tree.parse(xmlfile)
  
    # get root element
    root = tree.getroot()

    instruction_dict = dict()

    for instruction in root.findall('./extension/instruction'):
        instruction_dict[instruction.attrib['asm']] = instruction.attrib['category']

    with open('instruction_categories.json', 'w') as out_file:
        json.dump(instruction_dict, out_file, indent=4)


def main():
    # parse xml file
    parseXML('instructions.xml')
      
      
if __name__ == "__main__":
  
    # calling main function
    main()
