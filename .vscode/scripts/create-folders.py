import configparser
import os
from pathlib import Path

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config

def generate_folders_from_plugins(source_path, output_path):
	if source_path.endswith('plugins.txt'):
		with open(source_path, 'r') as f:
			contents = f.read()
			for line in contents.splitlines():
				if line.startswith("*"):
					file = line.removeprefix("*")
					folder_path = Path(os.path.join(output_path, file))
					folder_path.mkdir(parents=True, exist_ok=True)
					print(f"Info: creating directory: '{folder_path}\\'")
	else:
		for _, _, files in os.walk(source_path):
			for file in files:
				if file.endswith('.esp') or file.endswith('.esl') or file.endswith('.esm'):
					folder_path = Path(os.path.join(output_path, file))
					folder_path.mkdir(parents=True, exist_ok=True)
					print(f"Info: creating directory: '{folder_path}\\'")

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
	source_path = config.get('CREATE_FOLDERS', 'SOURCE_FOLDER')
	source_path = source_path.replace(root_var, ROOT_PATH)
	# print(source_path)

	output_path = config.get('CREATE_FOLDERS', 'OUTPUT_FOLDER')
	output_path = output_path.replace(root_var, ROOT_PATH)
	# print(output_path)

	generate_folders_from_plugins(source_path, output_path)

if __name__ == "__main__":
	main()
