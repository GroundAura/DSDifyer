import configparser
import os

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config

# Define a function to parse the data from the file
def parse_data(file_path):
	parsed_data = []
	current_data = {}

	with open(file_path, 'r') as file:
		for line in file:
			# line = line.strip()  # Remove leading and trailing whitespace
			line = line.replace('\n', '') # Remove only trailing line breaks

			# If the line starts with '[STRING]', it indicates the start of a new entry
			if line.startswith('[STRING]'):
				if current_data:
					parsed_data.append(current_data)
					current_data = {}
				continue

			# Split each line into key and value
			key_value_pair = line.split(": ", 1)
			if len(key_value_pair) == 2:
				key, value = key_value_pair
				current_data[key] = value

		# Add the last entry if any
		if current_data:
			parsed_data.append(current_data)

	return parsed_data

def data_to_dsd(data, include_identical_strings):
	combined_content = "[\n"
	template = "\t{\n\t\t\"editor_id\": \"[editor_id]\",\n\t\t\"type\": \"[record_type]\",\n\t\t\"original\": \"[original_string]\",\n\t\t\"string\": \"[new_string]\"\n\t},"
	for entry in data:
		new_plugin = entry['Current Plugin']
		original_plugin = entry['Master Plugin']
		editor_id = entry['EditorID']
		record_type = entry['Record Type'] + " " + entry['Data Type']
		original_string = entry['Master Value']
		new_string = entry['Current Value']

		# print(f"new_plugin: '{new_plugin}'")
		# print(f"original_plugin: '{original_plugin}'")
		# print(f"editor_id: '{editor_id}'")
		# print(f"record_type: '{record_type}'")
		# print(f"original_string: '{original_string}'")
		# print(f"new_string: '{new_string}'")
		# print()

		if not original_string == new_string or include_identical_strings == True:
			record_type = record_type.replace("DATA\\Name", "DATA")
			original_string = original_string.replace("\\\\", "\\\\\\\\")
			original_string = original_string.replace("\"", "\\" + "\"")
			original_string = original_string.replace("\b", "\\" + "b")
			original_string = original_string.replace("\f", "\\" + "f")
			original_string = original_string.replace("\n", "\\" + "n")
			original_string = original_string.replace("\r", "\\" + "r")
			original_string = original_string.replace("\t", "\\" + "t")
			new_string = new_string.replace("\\\\", "\\\\\\\\")
			new_string = new_string.replace("\"", "\\" + "\"")
			new_string = new_string.replace("\b", "\\" + "b")
			new_string = new_string.replace("\f", "\\" + "f")
			new_string = new_string.replace("\n", "\\" + "n")
			new_string = new_string.replace("\r", "\\" + "r")
			new_string = new_string.replace("\t", "\\" + "t")

			combined_content += template + "\n"
			combined_content = combined_content.replace("[editor_id]", editor_id)
			combined_content = combined_content.replace("[record_type]", record_type)
			combined_content = combined_content.replace("[original_string]", original_string)
			combined_content = combined_content.replace("[new_string]", new_string)

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

	root_var = "[ROOT]"
	source_path = config.get('XEDIT_TO_DSD', 'SOURCE_PATH')
	source_path = source_path.replace(root_var, ROOT_PATH)
	# print(source_path)
	if os.path.isfile(source_path):
		source_type = "file"
		print(f"INFO: handling SOURCE_PATH ('{source_path}') as a file")
	elif os.path.isdir(source_path):
		source_type = "dir"
		print(f"INFO: handling SOURCE_PATH ('{source_path}') as a directory")
	else:
		print(f"ERROR: SOURCE_PATH ('{source_path}') cannot be detected as either a file nor directory")
		return
	
	output_path = config.get('XEDIT_TO_DSD', 'OUTPUT_PATH')
	output_path = output_path.replace(root_var, ROOT_PATH)
	# print(output_path)
	if os.path.isfile(output_path):
		output_type = "file"
		print(f"INFO: handling OUTPUT_PATH ('{output_path}') as a directory")
	elif os.path.isdir(output_path):
		output_type = "dir"
		print(f"INFO: handling OUTPUT_PATH ('{output_path}') as a directory")
	else:
		print(f"ERROR: OUTPUT_PATH ('{output_path}') cannot be detected as either a file nor directory")
		return

	if source_type == "file" and output_type == "dir":
		print(f"ERROR: OUTPUT_PATH ('{output_path}') must be a file to match SOURCE_PATH")
		return
	if source_type == "dir" and output_type == "file":
		print(f"ERROR: OUTPUT_PATH ('{output_path}') must be a directory to match SOURCE_PATH")
		return

	include_identical_strings = config.get('XEDIT_TO_DSD', 'Include_Identical_Strings')
	if include_identical_strings == "false" or include_identical_strings == "False" or include_identical_strings == "FALSE" or include_identical_strings == "0":
		include_identical_strings = False
	else:
		include_identical_strings = True

	if source_type == "file":
		input_file = source_path
		parsed_data = parse_data(input_file)
		output = data_to_dsd(parsed_data, include_identical_strings)
		output_file = output_path
		with open(output_file, 'w') as f:
			f.write(output)
			print(f"INFO: translated '{input_file}' to '{output_file}'")
		# print(output)
	else:
		for _, _, files in os.walk(source_path):
			for file in files:
				if file.endswith('.txt'):
					input_file = os.path.join(source_path, file)
					parsed_data = parse_data(input_file)
					output = data_to_dsd(parsed_data, include_identical_strings)
					output_file = os.path.join(output_path, file.removesuffix(".txt") + ".json")
					with open(output_file, 'w') as f:
						f.write(output)
						print(f"INFO: translated '{input_file}' to '{output_file}'")
					# print(output)

if __name__ == "__main__":
	main()
