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
		#print(f'<{element.tag} {element.attrib}></{element.tag}>')
		#if element.tag == "Params":
			#for parameter in element:
				#print(f' <{parameter.tag} {parameter.attrib}>{parameter.text}</{parameter.tag}>')
				#if element.tag == "Addon":
				#	plugin = parameter.text
				#	text = text.replace("[Plugin name]", plugin)
		if element.tag == "Content":
			for string in element:
				#print(f' <{string.tag} {string.attrib}>')
				combined_content += template + "\n"
				for string_element in string:
					#print(f'  <{string_element.tag} {string_element.attrib}>{string_element.text}</{string_element.tag}>')
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
							original_string = original_string.replace("\\\\", "\\\\\\\\")
							original_string = original_string.replace("\"", "\\" + "\"")
							original_string = original_string.replace("\b", "\\" + "b")
							original_string = original_string.replace("\f", "\\" + "f")
							original_string = original_string.replace("\n", "\\" + "n")
							original_string = original_string.replace("\r", "\\" + "r")
							original_string = original_string.replace("\t", "\\" + "t")
							combined_content = combined_content.replace("[original_string]", original_string)
						else:
							combined_content = combined_content.replace("[original_string]", "")
					if string_element.tag == "Dest":
						if replace_new_string:
							new_string = string_element.text
							new_string = new_string.replace("\\\\", "\\\\\\\\")
							new_string = new_string.replace("\"", "\\" + "\"")
							new_string = new_string.replace("\b", "\\" + "b")
							new_string = new_string.replace("\f", "\\" + "f")
							new_string = new_string.replace("\n", "\\" + "n")
							new_string = new_string.replace("\r", "\\" + "r")
							new_string = new_string.replace("\t", "\\" + "t")
							combined_content = combined_content.replace("[new_string]", new_string)
						else:
							combined_content = combined_content.replace("[new_string]", "")
				#print(f' </{string.tag}>')
	combined_content += "]"
	combined_content = combined_content.replace("\t},\n]", "\t}\n]")
	#print (combined_content)
	return combined_content

def main():
	ROOT_PATH = os.getcwd()
	print(f"INFO: Current working directory: '{ROOT_PATH}'.")

	CONFIG_PATH = os.path.join(ROOT_PATH, "xTranslator-to-DSD.ini")
	print(f"INFO: Trying to read config file from: '{CONFIG_PATH}'.")
	config = read_config(CONFIG_PATH, False)
	if not config:
		print("ERROR: Config not found or failed to read.")
		return
	print("INFO: Config found.")
	root_var = "[ROOT]"
	false_vars = ("false", "False", "FALSE", "f", "F", "0")

	source_path = config.get('GENERAL', 'SOURCE_PATH')
	source_path = source_path.replace(root_var, ROOT_PATH)
	#print(source_path)
	if os.path.isdir(source_path):
		print(f"INFO: SOURCE_PATH ['{source_path}'] is valid.")
	else:
		print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a directory.")
		return
	
	output_path = config.get('GENERAL', 'OUTPUT_PATH')
	output_path = output_path.replace(root_var, ROOT_PATH)
	#print(output_path)
	if os.path.isdir(output_path):
		print(f"INFO: OUTPUT_PATH ['{output_path}'] is valid.")
	else:
		print(f"ERROR: OUTPUT_PATH ['{output_path}'] must be a directory.")
		return

	replace_original_string = config.get('GENERAL', 'Forward_Original_String')
	if replace_original_string in false_vars:
		replace_original_string = False
	else:
		replace_original_string = True

	replace_new_string = config.get('GENERAL', 'Forward_New_String')
	if replace_new_string in false_vars:
		replace_new_string = False
	else:
		replace_new_string = True

	for _, _, files in os.walk(source_path):
		for file in files:
			if file.endswith(".xml"):
				xml_file = os.path.join(source_path, file)
				output = xTranslator_to_DSD(xml_file, replace_original_string, replace_new_string)
				#print(file)
				output_file_name = file.replace(".xml", ".json")
				#print(output_file_name)
				output_file = os.path.join(output_path, output_file_name)
				with open(output_file, 'w') as f:
					f.write(output)
					print(f"INFO: Generated file '{output_file}' from '{xml_file}'.")
				#print(output)

if __name__ == "__main__":
	main()
