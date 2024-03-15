import configparser
import os
import xml.etree.ElementTree as ET

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config

def xTranslator_to_DSD(xml_file, replace_original_string, replace_new_string):
	tree = ET.parse(xml_file)
	root = tree.getroot()
	combined_content = "[\n"
	template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
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
						combined_content = combined_content.replace("[editor_id]", editor_id)
					if string_element.tag == "REC":
						record_type = string_element.text
						record_type = record_type.replace(":", " ")
						combined_content = combined_content.replace("[record_type]", record_type)
					if string_element.tag == "Source":
						if replace_original_string:
							original_string = string_element.text
							combined_content = combined_content.replace("[original_string]", original_string)
						else:
							combined_content = combined_content.replace("[original_string]", "")
					if string_element.tag == "Dest":
						if replace_new_string:
							new_string = string_element.text
							combined_content = combined_content.replace("[new_string]", new_string)
						else:
							combined_content = combined_content.replace("[new_string]", "")
				# print(f' </{string.tag}>')
	combined_content += "]"
	combined_content = combined_content.replace("\t},\n]", "\t}\n]")
	# print (combined_content)
	return combined_content

def main():
	ROOT_PATH = os.getcwd()

	CONFIG_PATH = os.path.join(ROOT_PATH, "xTranslator_to_DSD.ini")

	print(f"Info: trying to read config file from: '{CONFIG_PATH}'")
	config = read_config(CONFIG_PATH, False)
	if not config:
		print("Error: config not found or failed to read")
		return
	print("Info: config found")

	source_path = os.path.join(ROOT_PATH, config.get('PATHS', 'SOURCE_FOLDER'))
	output_path = os.path.join(ROOT_PATH, config.get('PATHS', 'OUTPUT_FOLDER'))

	if config.get('GENERAL', 'Forward_Original_String') == "false":
		replace_original_string = False
	else:
		replace_original_string = True

	if config.get('GENERAL', 'Forward_Replacement_String') == "false":
		replace_new_string = False
	else:
		replace_new_string = True

	for _, _, files in os.walk(source_path):
		for file in files:
			if file.endswith('.xml'):
				xml_file = os.path.join(ROOT_PATH, source_path, file)
				output = xTranslator_to_DSD(xml_file, replace_original_string, replace_new_string)
				# print(file)
				# output_file_name = file.removesuffix(".xml") + ".json"
				# print(output_file_name)
				output_file = os.path.join(ROOT_PATH, output_path, file.removesuffix(".xml") + ".json")
				with open(output_file, 'w') as f:
					f.write(output)
					print(f"Info: translated '{xml_file}' to '{output_file}'")
				# print(output)

if __name__ == "__main__":
	main()
