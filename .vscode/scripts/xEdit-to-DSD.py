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

			# If the line starts with '_RECORD_', it indicates the start of a new entry
			if line.startswith('_RECORD_'):
				if current_data:
					parsed_data.append(current_data)
					current_data = {}
				continue

			# Split each line into key and value
			key, value = line.split(": ", 1)

			# Store key-value pairs in the current data dictionary
			current_data[key] = value

		# Add the last entry if any
		if current_data:
			parsed_data.append(current_data)

	return parsed_data

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
	source_path = config.get('XEDIT_TO_DSD', 'SOURCE')
	source_path = source_path.replace(root_var, ROOT_PATH)
	# print(source_path)
	
	output_path = config.get('XEDIT_TO_DSD', 'OUTPUT')
	output_path = output_path.replace(root_var, ROOT_PATH)
	# print(output_path)

	# Example usage
	file_path = os.path.join(source_path)  # Replace with the path to your file
	parsed_data = parse_data(file_path)
	for entry in parsed_data:
		print(entry)

if __name__ == "__main__":
	main()
