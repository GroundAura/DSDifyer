import configparser
import os
#from pathlib import Path

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
					#if current_data["original"] != current_data["string"]:
					#	current_data["status"] = "TranslationComplete"
					#else:
					#	current_data["status"] = "TranslationRequired"
					#current_data = {"status": "TranslationComplete" if current_data["original"] != current_data["string"] else "TranslationRequired"}
					#current_data["status"] = "TranslationComplete"
					#current_data["status"] = "TranslationRequired"
					#current_data["status"] = "null"
					parsed_data.append(current_data)
					current_data = {}
				continue
			key_value_pair = line.split(": ", 1)
			#print(f"TRACE: 'key_value_pair': '{key_value_pair}'.")
			if len(key_value_pair) == 2:
				key, value = key_value_pair
				key = key_mapping.get(key, key)
				value = "null" if value in ("", "-1") else value
				if key == "form_id":
					value = format_formid(value, current_data.get("master_plugin"))
				if key == "DataType":
					key = "type"
					value = current_data.pop("RecordType") + " " + value
				#print(f"TRACE: ('key', 'value'): '{key, value}'.")
				current_data[key] = value
		if current_data:
			#if current_data["original"] != current_data["string"]:
			#	current_data["status"] = "TranslationComplete"
			#else:
			#	current_data["status"] = "TranslationRequired"
			#current_data = {"status": "TranslationComplete" if current_data["original"] != current_data["string"] else "TranslationRequired"}
			#current_data["status"] = "TranslationComplete"
			#current_data["status"] = "TranslationRequired"
			#current_data["status"] = "null"
			parsed_data.append(current_data)
	#print(f"TRACE: Parsed data: '{parsed_data}'.")
	return parsed_data

def json_formatting(data):
	data = data.replace("\\\\", "\\\\\\\\")
	data = data.replace("\"", "\\\"")
	data = data.replace("\b", "\\b")
	data = data.replace("\f", "\\f")
	data = data.replace("\n", "\\n")
	data = data.replace("\r", "\\r")
	data = data.replace("\t", "\\t")
	#data = data.replace("’", "'")
	return data

#def dict_to_json(dict_list):
#	#key_mapping = {"Current Plugin": "Current Plugin", "Master Plugin": "Master Plugin", "EditorID": "editor_id", "FormID": "form_id", "Record Type": "record_type_pt1", "Data Type": "record_type_pt2", "Index": "index_number", "Master Value": "original", "Current Value": "string"}
#	dict_list = dict_list
#	for dict in dict_list:
#		#dict = {key_mapping.get(key, key): value for key, value in dict.items()}
#		for key in dict:
#			if dict[key] in ("", "-1"):
#				dict[key] = "null"
#			record_type = dict.pop("Record Type") + " " + dict.pop("Data Type")
#			dict['record_type'] = record_type
#	print(f"TRACE: Formatted data: {dict_list}")
#	return dict_list

def create_text_file(file_path, content):
	try:
		with open(file_path, "w", encoding="utf-8") as f:
			f.write(content)
		print(f"INFO: File '{file_path}' created successfully.")
	except Exception as e:
		print(f"ERROR: Error creating file '{file_path}': {e}")

def data_to_dsd(data, include_identical_strings):
	combined_content = ""
	template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"index\": \"[index_number]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
	values_edid = ()
	values_edid_index = ()
	values_fid = ("FULL", "DESC", "NPC_ SHRT", "WOOP TNAM", "INFO RNAM", "BOOK CNAM", "MGEF DNAM", "REGN RDMP")
	values_fid_edid = ("GMST DATA")
	values_fid_orig = ("ACTI RNAM", "FLOR RNAM", "QUST CNAM")
	values_fid_index = ("QUST NNAM", "INFO NAM1", "MESG ITXT", "PERK EPF2", "PERK EPFD")
	values_orig = ()
	for entry in data:
		entry_content = ""
		new_string = entry["string"]
		original_string = entry["original"]
		if not original_string == new_string or include_identical_strings == True:
			record_type = entry["type"]
			#record_type = record_type.replace("DATA\\Bool", "DATA")
			#record_type = record_type.replace("DATA\\Float", "DATA")
			#record_type = record_type.replace("DATA\\Int", "DATA")
			record_type = record_type.replace("DATA\\Name", "DATA")
			record_type = record_type.replace("EPFD\\Text", "EPFD")
			new_string = json_formatting(new_string)
			if record_type in values_edid:
				editor_id = entry["editor_id"]
				#template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				entry_content = entry_content.replace("[editor_id]", editor_id)
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			elif record_type in values_edid_index:
				editor_id = entry["editor_id"]
				index_number = entry["index"]
				#template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"index\": \"[index_number]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				entry_content = entry_content.replace("[editor_id]", editor_id)
				entry_content = entry_content.replace("[record_type]", record_type)
				if index_number in ("-1", "", "null"):
					entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				else:
					entry_content = entry_content.replace("[index_number]", index_number)
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			elif record_type in values_fid:
				form_id = entry["form_id"]
				#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\",\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("[form_id]", form_id)
				entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			elif record_type in values_fid_edid:
				form_id = entry["form_id"]
				editor_id = entry["editor_id"]
				#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\",\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("[form_id]", form_id)
				entry_content = entry_content.replace("[editor_id]", editor_id)
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			elif record_type in values_fid_index:
				form_id = entry["form_id"]
				index_number = entry["index"]
				#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"index\": \"[index_number]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("[form_id]", form_id)
				entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
				entry_content = entry_content.replace("[record_type]", record_type)
				if index_number in ("-1", "", "null"):
					entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				else:
					entry_content = entry_content.replace("[index_number]", index_number)
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			elif record_type in values_fid_orig:
				form_id = entry["form_id"]
				#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\",\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("[form_id]", form_id)
				entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("[original_string]", original_string)
				entry_content = entry_content.replace("[new_string]", new_string)
			elif record_type in values_orig:
				#template = "\t{\n\t\t\"type\": \"[record_type]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
				entry_content += template + "\n"
				original_string = original_string.replace("\\\\", "\\\\\\\\")
				original_string = original_string.replace("\"", "\\" + "\"")
				original_string = original_string.replace("\b", "\\" + "b")
				original_string = original_string.replace("\f", "\\" + "f")
				original_string = original_string.replace("\n", "\\" + "n")
				original_string = original_string.replace("\r", "\\" + "r")
				original_string = original_string.replace("\t", "\\" + "t")
				entry_content += template + "\n"
				entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("[original_string]", original_string)
				entry_content = entry_content.replace("[new_string]", new_string)
			elif entry["DataType"] in values_edid:
				editor_id = entry["editor_id"]
				#template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("\n\t\t\"form_id\": \"[form_id]\",", "")
				entry_content = entry_content.replace("[editor_id]", editor_id)
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			elif entry["DataType"] in values_fid:
				form_id = entry["form_id"]
				#template = "\t{\n\t\t\"form_id\": \"[form_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"string\": \"[new_string]\",\n\t},"
				entry_content += template + "\n"
				entry_content = entry_content.replace("[form_id]", form_id)
				entry_content = entry_content.replace("\n\t\t\"editor_id\": \"[editor_id]\",", "")
				entry_content = entry_content.replace("[record_type]", record_type)
				entry_content = entry_content.replace("\n\t\t\"index\": \"[index_number]\",", "")
				entry_content = entry_content.replace("\n\t\t\"original\": \"[original_string]\",", "")
				entry_content = entry_content.replace("[new_string]", new_string)
			else:
				print(f"ERROR: Record type '{record_type}' is not supported by this script.")
				#return
		#print (entry_content)
		combined_content += entry_content
	#print (combined_content)
	return combined_content

def main():
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

	starting_content = ""
	#starting_content = "[\n"
	parsed_data = parse_data(source_path)
	for entry in parsed_data:
		json_entry = data_to_dsd([entry], include_identical_strings)
		output = ""
		if not json_entry == "":
			new_plugin = entry["origin_plugin"]
			original_plugin = entry["master_plugin"]
			output_folder = os.path.join(output_path, "SKSE\\Plugins\\DynamicStringDistributor", original_plugin)
			if not os.path.exists(output_folder):
				print(f"INFO: Directory '{output_folder}' can't be found, creating directory.")
				os.makedirs(output_folder)
				#folder_path = Path(os.path.join(output_path, "SKSE\\Plugins\\DynamicStringDistributor", original_plugin))
				#folder_path.mkdir(parents=True, exist_ok=True)
			output_file_name = new_plugin[:-3] + "json"
			output_file = os.path.join(output_folder, output_file_name)
			#print(f"TRACE: Trying to read file from '{output_file}'.")
			if os.path.isfile(output_file):
				try:
					with open(output_file, "r", encoding="utf-8") as f:
						output = f.read()
					if output.endswith("]"):
						print(f"INFO: File '{output_file}' already exists, overwriting file.")
						create_text_file(output_file, starting_content)
						with open(output_file, "r") as f:
							output = f.read()
					if output == "":
						output = "[\n"
					output += json_entry
					#print(output)
					with open(output_file, "w", encoding="utf-8") as f:
						f.write(output)
						#print(f"TRACE: Translated entry from '{input_file}' into '{output_file}'.")
				except Exception as e:
					print(f"ERROR: Error reading '{output_file}': {e}")
			else:
				#print(f"ERROR: File '{output_file}' can't be found.")
				print(f"INFO: File '{output_file}' can't be found, creating file.")
				create_text_file(output_file, starting_content)

	for root, _, files in os.walk(output_path):
		for file_name in files:
			output_file = os.path.join(root, file_name)
			#print(f"INFO: Trying to read file from '{output_file}'.")
			if os.path.isfile(output_file):
				try:
					with open(output_file, "r", encoding="utf-8") as f:
						output = f.read()
					if not output.endswith("]"):
						output += "]"
					output = output.replace("\t},\n]", "\t}\n]")
					#output = output.replace("\t", "  ")
					with open(output_file, "w", encoding="utf-8") as f:
						f.write(output)
						print(f"INFO: Finished formatting file: '{output_file}'.")
				except Exception as e:
					print(f"ERROR: Error reading '{output_file}': {e}")

if __name__ == "__main__":
	main()
