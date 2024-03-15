import xml.etree.ElementTree as ET
# import json
import os

ROOT_PATH = os.getcwd()

# def xml_to_dict(xml_element):
# 	xml_dict = {}
# 	if xml_element.attrib:
# 		xml_dict["@attributes"] = xml_element.attrib
# 	if xml_element.text:
# 		xml_dict["text"] = xml_element.text.strip()
# 	for child in xml_element:
# 		if child.tag in xml_dict:
# 			if not isinstance(xml_dict[child.tag], list):
# 				xml_dict[child.tag] = [xml_dict[child.tag]]
# 			xml_dict[child.tag].append(xml_to_dict(child))
# 		else:
# 			xml_dict[child.tag] = xml_to_dict(child)
# 	return xml_dict

# def xml_to_json(xml_file):
# 	tree = ET.parse(xml_file)
# 	root = tree.getroot()
# 	# test = {root.tag: xml_to_dict(root)}
# 	# print(test)
# 	return json.dumps({root.tag: xml_to_dict(root)}, indent=2, separators=(',', ': '))

def xml_to_json(xml_file, template_file):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	combined_content = "[\n"
	with open(template_file, 'r') as f:
		template = f.read()
	# template = "\t{\n\t\t\"editor_id\": \"[EditorID]\",\n\t\t\"type\": \"[Record type]\",\n\t\t\"original\": \"[original string]\",\n\t\t\"string\": \"[replacement/translation string]\"\n\t}"
	for element in root:
		# print(f'<{element.tag} {element.attrib}></{element.tag}>')
		# if element.tag == "Params":
			# for parameter in element:
				# print(f' <{parameter.tag} {parameter.attrib}>{parameter.text}</{parameter.tag}>')
				# if element.tag == "Addon":
				# 	plugin = parameter.text
				# 	text = text.replace("[Plugin name]", plugin)
		if element.tag == "Content":
			for string in element:
				# print(f' <{string.tag} {string.attrib}>')
				combined_content += template + "\n"
				for string_element in string:
					# print(f'  <{string_element.tag} {string_element.attrib}>{string_element.text}</{string_element.tag}>')
					if string_element.tag == "EDID":
						editor_id = string_element.text
						combined_content = combined_content.replace("[EditorID]", editor_id)
					if string_element.tag == "REC":
						record_type = string_element.text
						record_type = record_type.replace(":", " ")
						combined_content = combined_content.replace("[Record type]", record_type)
					if string_element.tag == "Source":
						original_string = string_element.text
						combined_content = combined_content.replace("[original string]", original_string)
					if string_element.tag == "Dest":
						new_string = string_element.text
						combined_content = combined_content.replace("[replacement/translation string]", new_string)
				# print(f' </{string.tag}>')
	combined_content = combined_content.replace("\t}\n\t{", "\t},\n\t{")
	combined_content += "]"
	# print (combined_content)
	return combined_content

# def fix_formatting(text):
	# text = text.replace("  ", "\t")
	# text = text.replace("\t}\n\t{", "\t},\n\t{")
	# text = text.replace("\t", "  ")
	# text = text.replace("  }\n  {", "  },\n  {")
	# text = text.replace("ACTI:RNAM", "ACTI RNAM")
	# text = text.replace("FLOR:RNAM", "FLOR RNAM")
	# text = text.replace("REFR:FULL", "REFR FULL")
	# text = text.replace("REGN:RDMP", "REGN RDMP")
	# text = text.replace("DIAL:FULL", "DIAL FULL")
	# text = text.replace("INFO:RNAM", "INFO RNAM")
	# text = text.replace("QUST:CNAM", "QUST CNAM")
	# text = text.replace("QUST:NNAM", "QUST NNAM")
	# text = text.replace("INFO:NAM1", "INFO NAM1")
	# text = text.replace("MESG:ITXT", "MESG ITXT")
	# text = text.replace("MESG:DESC", "MESG DESC")
	# text = text.replace("", "")
	# return text

def main():
	source_file = os.path.join(ROOT_PATH, "src\\strings\\xml\\_test.xml")
	template_string = os.path.join(ROOT_PATH, "src\\strings\\templates\\template-string.json")
	output_file = os.path.join(ROOT_PATH, "src\\strings\\_test.json")

	output = xml_to_json(source_file, template_string)
	# output = fix_formatting(output)


	with open(output_file, 'w') as f:
		f.write(output)

	print(output)

if __name__ == "__main__":
	main()
