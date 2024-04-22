import configparser
import os

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config

def format_formid(formid_dec, plugin):
	formid_dec = int(formid_dec)
	#print(f"TRACE: FormID (dec): "{formid_dec}".")
	formid = hex(formid_dec)[2:]
	#print(f"TRACE: FormID (hex): "{formid}".")
	if len(formid) <= 6:
		while len(formid) < 8:
			formid = "0" + formid
		formid = "0x" + formid + "|" + plugin
		return formid
	elif len(formid) == 7:
		if any(formid.startswith(prefix) for prefix in ("1", "2", "3", "4")):
			formid = "0x0" + formid + "|" + plugin
		else:
			formid = formid[1:]
			while len(formid) > 1 and formid.startswith("0"):
				formid = formid[1:]
			formid = "0x" + formid + "|" + plugin
		return formid
	elif len(formid) == 8:
		if any(formid.startswith(prefix) for prefix in ("fe", "FE")):
			formid = formid[5:]
			while len(formid) > 1 and formid.startswith("0"):
				formid = formid[1:]
			formid = "0x" + formid + "|" + plugin
		else:
			formid = formid[2:]
			while len(formid) > 1 and formid.startswith("0"):
				formid = formid[1:]
			formid = "0x" + formid + "|" + plugin
		return formid
	else:
		print(f"ERROR: FormID '{formid}' longer than expected.")
		return

def format_string(string):
	escape_mapping = {
		"\\": "\\\\",
		"\"": "\\\"",
		"\b": "\\b",
		"\f": "\\f",
		"\n": "\\n",
		"\r": "\\r",
		"\t": "\\t"
	}
	formatted_string = ""
	for char in string:
		formatted_string += escape_mapping.get(char, char)
	return formatted_string

def parse_data(file_path):
	parsed_data = []
	current_data = {}
	key_mapping = {
		"Current Plugin": "origin_plugin",
		"Master Plugin": "master_plugin",
		"EditorID": "editor_id",
		"FormID": "form_id",
		"Record Type": "RecordType",
		"Data Type": "DataType",
		"Index": "index",
		"Master Value": "original",
		"Current Value": "string"
	}
	with open(file_path, "r", encoding="utf-8-sig") as f:
		for line in f:
			#line = line.strip()
			line = line.replace("\n", "")
			if line.startswith("[STRING]"):
				if current_data:
					parsed_data.append(current_data)
					current_data = {}
				continue
			key_value_pair = line.split(": ", 1)
			#print(f"TRACE: 'key_value_pair': '{key_value_pair}'.")
			if len(key_value_pair) == 2:
				key, value = key_value_pair
				key = key_mapping.get(key, key)
				if key == "form_id":
					value = format_formid(value, current_data.get("master_plugin"))
				elif key == "DataType":
					key = "type"
					value.replace("DATA\\Name", "DATA")
					value.replace("EPFD\\Text", "EPFD")
					value = current_data.pop("RecordType") + " " + value
				elif key == "index":
					value = "null" if value in ("", "-1") else value
				elif key in ("original", "string"):
					value = format_string(value)
				#print(f"TRACE: ('key', 'value'): '{key, value}'.")
				current_data[key] = value
		if current_data:
			parsed_data.append(current_data)
	#print(f"TRACE: Parsed data: '{parsed_data}'.")
	return parsed_data

def data_to_dsd(data, required_elements_only, include_identical_strings):
	combined_content = ""
	template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"index\": \"[index_number]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\"\n\t}"
	values_fid = ("FULL", "DESC", "NPC_ SHRT", "WOOP TNAM", "INFO RNAM", "BOOK CNAM", "MGEF DNAM", "REGN RDMP")
	values_fid_index = ("QUST NNAM", "INFO NAM1", "MESG ITXT", "PERK EPF2", "PERK EPFD")
	values_fid_orig = ("ACTI RNAM", "FLOR RNAM", "QUST CNAM")
	values_fid_edid = ("GMST DATA")
	#values_edid = ()
	#values_edid_index = ()
	#values_orig = ()
	for entry in data:
		entry_content = ""
		new_string = entry["string"]
		original_string = entry["original"]
		if not original_string == new_string or include_identical_strings == True:
			record_type = entry["type"]
			if required_elements_only:
				if record_type.endswith(values_fid):
					form_id = entry["form_id"]
					#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\",\n\t}"
					entry_content += template
					entry_content = entry_content.replace("[form_id]", form_id)
					entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
					entry_content = entry_content.replace("[record_type]", record_type)
					entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
					entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
					entry_content = entry_content.replace("[new_string]", new_string)
				elif record_type.endswith(values_fid_index):
					form_id = entry["form_id"]
					index_number = entry["index"]
					#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"index\": \"[index_number]\",\n\t\t\"string\": \"[new_string]\"\n\t}"
					entry_content += template
					entry_content = entry_content.replace("[form_id]", form_id)
					entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
					entry_content = entry_content.replace("[record_type]", record_type)
					if index_number in ("-1", "", "null"):
						entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
					else:
						entry_content = entry_content.replace("[index_number]", index_number)
					entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
					entry_content = entry_content.replace("[new_string]", new_string)
				elif record_type.endswith(values_fid_orig):
					form_id = entry["form_id"]
					#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\",\n\t}"
					entry_content += template
					entry_content = entry_content.replace("[form_id]", form_id)
					entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
					entry_content = entry_content.replace("[record_type]", record_type)
					entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
					entry_content = entry_content.replace("[original_string]", original_string)
					entry_content = entry_content.replace("[new_string]", new_string)
				elif record_type.endswith(values_fid_edid):
					form_id = entry["form_id"]
					editor_id = entry["editor_id"]
					#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\",\n\t}"
					entry_content += template
					entry_content = entry_content.replace("[form_id]", form_id)
					entry_content = entry_content.replace("[editor_id]", editor_id)
					entry_content = entry_content.replace("[record_type]", record_type)
					entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
					entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
					entry_content = entry_content.replace("[new_string]", new_string)
				#elif record_type.endswith(values_edid):
				#	editor_id = entry["editor_id"]
				#	#template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\"\n\t}"
				#	entry_content += template
				#	entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				#	entry_content = entry_content.replace("[editor_id]", editor_id)
				#	entry_content = entry_content.replace("[record_type]", record_type)
				#	entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				#	entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				#	entry_content = entry_content.replace("[new_string]", new_string)
				#elif record_type.endswith(values_edid_index):
				#	editor_id = entry["editor_id"]
				#	index_number = entry["index"]
				#	#template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"index\": \"[index_number]\",\n\t\t\"string\": \"[new_string]\"\n\t}"
				#	entry_content += template
				#	entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				#	entry_content = entry_content.replace("[editor_id]", editor_id)
				#	entry_content = entry_content.replace("[record_type]", record_type)
				#	if index_number in ("-1", "", "null"):
				#		entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				#	else:
				#		entry_content = entry_content.replace("[index_number]", index_number)
				#	entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				#	entry_content = entry_content.replace("[new_string]", new_string)
				#elif record_type.endswith(values_orig):
				#	#template = "\t{\n\t\t\"type\": \"[record_type]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\"\n\t}"
				#	entry_content += template
				#	entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				#	entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
				#	entry_content = entry_content.replace("[record_type]", record_type)
				#	entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				#	entry_content = entry_content.replace("[original_string]", original_string)
				#	entry_content = entry_content.replace("[new_string]", new_string)
				else:
					print(f"ERROR: Record type '{record_type}' is not supported by this script.")
					#return
			else:
				form_id = entry["form_id"]
				editor_id = entry["editor_id"]
				index_number = entry["index"]
				entry_content += template
				entry_content = entry_content.replace("[form_id]", form_id)
				entry_content = entry_content.replace("[editor_id]", editor_id)
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("[index_number]", index_number)
				entry_content = entry_content.replace("[original_string]", original_string)
				entry_content = entry_content.replace("[new_string]", new_string)
		#print (f"TRACE: Entry content: '{entry_content}'.")
		combined_content += entry_content
	#print (f"TRACE: Combined content: '{combined_content}'.")
	return combined_content

def main():
	VERSION = "1.2.0"
	print(f"'DSDifyer (xEdit to DSD) v{VERSION}'\nStarted.")

	ROOT_PATH = os.getcwd()
	print(f"INFO: Current working directory: '{ROOT_PATH}'.")

	CONFIG_PATH = os.path.join(ROOT_PATH, "xEdit-to-DSD.ini")
	print(f"INFO: Trying to read config file from: '{CONFIG_PATH}'.")
	config = read_config(CONFIG_PATH, False)
	if not config:
		print("ERROR: Config not found or failed to read.")
		return
	print("INFO: Config found.")
	root_var = "[ROOT]"
	false_vars = ("false", "False", "FALSE", "f", "F", "0")

	source_path = config.get("GENERAL", "SOURCE_PATH")
	source_path = source_path.replace(root_var, ROOT_PATH)
	#print(source_path)
	if os.path.isfile(source_path):
		print(f"INFO: SOURCE_PATH ['{source_path}'] is valid.")
	else:
		print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a file.")
		return

	output_path = config.get("GENERAL", "OUTPUT_PATH")
	output_path = output_path.replace(root_var, ROOT_PATH)
	#print(output_path)
	if os.path.isdir(output_path):
		print(f"INFO: OUTPUT_PATH ['{output_path}'] is valid.")
	else:
		print(f"ERROR: OUTPUT_PATH ['{output_path}'] must be a directory.")
		return

	include_identical_strings = config.get("GENERAL", "Include_Identical_Strings")
	if include_identical_strings in false_vars:
		include_identical_strings = False
	else:
		include_identical_strings = True

	required_elements_only = config.get("GENERAL", "Required_Elements_Only")
	if required_elements_only in false_vars:
		required_elements_only = False
	else:
		required_elements_only = True

	edited_files = 0
	parsed_data = parse_data(source_path)
	if not parsed_data == []:
		all_files_and_contents = []
		#for root, _, files in os.walk(os.path.join(output_path, "SKSE\\Plugins\\DynamicStringDistributor")):
		#	for file_name in files:
		#		file_path = os.path.join(root, file_name)
		#		#print(f"INFO: Trying to read file from '{file_path}'.")
		#		if file_path.endswith(".json"):
		#			try:
		#				with open(file_path, "r", encoding="utf-8") as f:
		#					file_content = f.read()
		#				file_and_content = {"file_path": file_path, "file_content": file_content, "modified": False}
		#				all_files_and_contents.append(file_and_content)
		#			except Exception as e:
		#				print(f"ERROR: Error reading '{file_path}': {e}")
		for entry in parsed_data:
			json_entry = data_to_dsd([entry], required_elements_only, include_identical_strings)
			if not json_entry == "":
				new_plugin = entry["origin_plugin"]
				original_plugin = entry["master_plugin"]
				path_to_match = os.path.join(original_plugin, new_plugin[:-3] + "json")
				for file_and_content in all_files_and_contents:
					#if file_and_content["file_path"].endswith(path_to_match) and json_entry not in file_and_content["file_content"]:
					if file_and_content["file_path"].endswith(path_to_match):
						file_content = file_and_content["file_content"].rstrip("\n]") + ",\n" + json_entry + "\n]"
						file_and_content["file_content"] = file_content
						file_and_content["modified"] = True
						#print(f"TRACE: Adding to existing path: '{path_to_match}'.")
						break
				else:
					file_path = os.path.join(output_path, "SKSE\\Plugins\\DynamicStringDistributor", path_to_match)
					file_content = "[\n" + json_entry + "\n]"
					file_and_content = {"file_path": file_path, "file_content": file_content, "modified": True}
					#print(f"TRACE: Adding to new path: '{path_to_match}'.")
					all_files_and_contents.append(file_and_content)
		for file_and_content in all_files_and_contents:
			if file_and_content["modified"]:
				output_file = file_and_content["file_path"]
				try:
					with open(output_file, "w", encoding="utf-8") as f:
						f.write(file_and_content["file_content"])
					edited_files += 1
					print(f"INFO: Added to file: '{output_file}'.")
				except Exception as e:
					print(f"ERROR: Error writing to '{output_file}': {e}")

	print(f"Finished.\nResults: Files written to: {edited_files}.")

if __name__ == "__main__":
	main()
