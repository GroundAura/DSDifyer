import configparser
import os
from pathlib import Path

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config

def generate_folders_from_plugins(source_path, source_type, output_path):
	if source_type == "file":
		with open(source_path, 'r') as f:
			contents = f.read()
			for line in contents.splitlines():
				if line.startswith("*"):
					file_name = line.removeprefix("*")
					folder_path = Path(os.path.join(output_path, "SKSE\\Plugins\\DynamicStringDistributor", file_name))
					folder_path.mkdir(parents=True, exist_ok=True)
					print(f"INFO: Creating directory: '{folder_path}'.")
	elif source_type == "dir":
		plugin_extensions = [".esp", ".esm", ".esl"]
		for _, _, files in os.walk(source_path):
			for file in files:
				for extension in plugin_extensions:
					if file.endswith(extension):
						folder_path = Path(os.path.join(output_path, "SKSE\\Plugins\\DynamicStringDistributor", file))
						folder_path.mkdir(parents=True, exist_ok=True)
						print(f"INFO: Creating directory: '{folder_path}'.")

def main():
	ROOT_PATH = os.getcwd()
	print(f"INFO: Current working directory: '{ROOT_PATH}'.")

	CONFIG_PATH = os.path.join(ROOT_PATH, "xTranslator_to_DSD.ini")
	print(f"Info: trying to read config file from: '{CONFIG_PATH}'")
	config = read_config(CONFIG_PATH, False)
	if not config:
		print("ERROR: Config not found or failed to read.")
		return
	print("INFO: Config found.")
	root_var = "[ROOT]"
	filename_var = "plugins.txt"

	source_path = config.get('CREATE_FOLDERS', 'SOURCE_PATH')
	source_path = source_path.replace(root_var, ROOT_PATH)
	# print(source_path)
	if os.path.isdir(source_path):
		print(f"INFO: Handling SOURCE_PATH ['{source_path}'] as a directory.")
		source_type = "dir"
	elif os.path.isfile(source_path):
		print(f"INFO: Handling SOURCE_PATH ['{source_path}'] as a file.")
		if not source_path.endswith(filename_var):
			print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a directory or a file named {filename_var}.")
			return
		source_type = "file"
	else:
		print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a directory or a file named {filename_var}.")
		return

	output_path = config.get('CREATE_FOLDERS', 'OUTPUT_PATH')
	output_path = output_path.replace(root_var, ROOT_PATH)
	# print(output_path)
	if os.path.isdir(output_path):
		print(f"INFO: Handling OUTPUT_PATH ['{output_path}'] as a directory.")
	else:
		print(f"ERROR: OUTPUT_PATH ['{output_path}'] must be a directory.")
		return

	generate_folders_from_plugins(source_path, source_type, output_path)

if __name__ == "__main__":
	main()
