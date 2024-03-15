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

def fix_formatting(text):
	# text = text.replace("  ", "\t")
	# text = text.replace("", "")
	return text


def main():
	xml_file = os.path.join(ROOT_PATH, "src\\strings\\Your Own Thoughts\\YOT - Bloodchill Manor_english_english.xml")
	json_file = os.path.join(ROOT_PATH, "src\\strings\\_test\\YOT - Bloodchill Manor_english_english.json")

	output = xml_to_json(xml_file)
	output = fix_formatting(output)
	# print(output)

	with open(json_file, 'w') as f:
		f.write(output)

if __name__ == "__main__":
	main()
