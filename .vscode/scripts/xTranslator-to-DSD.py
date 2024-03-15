import xml.etree.ElementTree as ET
import json
import os

ROOT_PATH = os.getcwd()

def xml_to_dict(xml_element):
	xml_dict = {}
	if xml_element.attrib:
		xml_dict["@attributes"] = xml_element.attrib
	if xml_element.text:
		xml_dict["text"] = xml_element.text.strip()
	for child in xml_element:
		if child.tag in xml_dict:
			if not isinstance(xml_dict[child.tag], list):
				xml_dict[child.tag] = [xml_dict[child.tag]]
			xml_dict[child.tag].append(xml_to_dict(child))
		else:
			xml_dict[child.tag] = xml_to_dict(child)
	return xml_dict

def xml_to_json(xml_file):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	return json.dumps({root.tag: xml_to_dict(root)}, indent=2, separators=(',', ': '))

def parse_xml(xml_file):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	text = ""
	for element in root:
		print(f'<{element.tag} {element.attrib}></{element.tag}>')
		if element.tag == "Params":
			for element2 in element:
				print(f' <{element2.tag} {element2.attrib}>{element2.text}</{element2.tag}>')
		if element.tag == "Content":
			for element2 in element:
				print(f' <{element2.tag} {element2.attrib}>')
				for element3 in element2:
					print(f'  <{element3.tag} {element3.attrib}>{element3.text}</{element3.tag}>')
				print(f' </{element2.tag}>')
	# text = json.dumps({root.tag: xml_to_dict(root)}, indent=2, separators=(',', ': '))
	print (text)
	return text

def fix_formatting(text):
	text = text.replace("  ", "\t")
	# text = text.replace("ACTI:RNAM", "ACTI RNAM")
	# text = text.replace("FLOR:RNAM", "FLOR RNAM")
	# text = text.replace("REFR:FULL", "REFR FULL")
	# text = text.replace("REGN:RDMP", "REGN RDMP")
	# text = text.replace("DIAL:FULL", "DIAL FULL")
	# text = text.replace("INFO:RNAM", "INFO RNAM")
	# text = text.replace("QUST:CNAM", "QUST CNAM")
	# text = text.replace("QUST:NNAM", "QUST NNAM")
	# text = text.replace("INFO:NAM1", "INFO NAM1")
	text = text.replace("MESG:ITXT", "MESG ITXT")
	text = text.replace("MESG:DESC", "MESG DESC")
	# text = text.replace("", "")
	return text

def main():
	xml_file = os.path.join(ROOT_PATH, "src\\strings\\xml\\_test.xml")
	json_file = os.path.join(ROOT_PATH, "src\\strings\\_test.json")

	output = parse_xml(xml_file)
	output = fix_formatting(output)

	# for string in :
		

	# with open(json_file, 'w') as f:
	# 	f.write(output)

	# print(output)

if __name__ == "__main__":
	main()
