import configparser
import os
import subprocess

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config


def main():
	ROOT_PATH = os.getcwd()
	print(f"INFO: Current working directory: '{ROOT_PATH}'.")

	CONFIG_PATH = os.path.join(ROOT_PATH, "ESP-to-DSD.ini")
	print(f"INFO: Trying to read config file from: '{CONFIG_PATH}'.")
	config = read_config(CONFIG_PATH, False)
	if not config:
		print("ERROR: Config not found or failed to read.")
		return
	print("INFO: Config found.")
	root_var = "[ROOT]"
	false_vars = ["false", "False", "FALSE", "f", "F", "0"]
	plugin_extensions = [".esp", ".esm", ".esl"]

	exe_path = config.get('GENERAL', 'EXE_PATH')
	exe_path = exe_path.replace(root_var, ROOT_PATH)
	#print(exe_path)
	if not exe_path.endswith("esp2dsd.exe"):
		print(f"ERROR: EXE_PATH ['{exe_path}'] must be a path to 'esp2dsd.exe'.")
		return
	else:
		print(f"INFO: EXE_PATH ['{exe_path}'] is valid.")

	output_path = config.get('GENERAL', 'OUTPUT_PATH')
	output_path = output_path.replace(root_var, ROOT_PATH)
	#print(output_path)
	if os.path.isdir(output_path):
		print(f"INFO: OUTPUT_PATH ['{output_path}'] is valid.")
	else:
		print(f"ERROR: OUTPUT_PATH ['{output_path}'] must be a directory.")
		return

	dump_mode = config.get('GENERAL', 'DUMP_MODE')
	if dump_mode in false_vars:
		dump_mode = False
	else:
		dump_mode = True

	if dump_mode and os.path.isfile(source_path):
		print(f"INFO: SOURCE_PATH ['{source_path}'] is valid. Handling SOURCE_PATH as a .esp/.esm/.esl file.")
		source_path = config.get('DUMP_MODE', 'SOURCE_PATH')
		source_path = source_path.replace(root_var, ROOT_PATH)
		#print(source_path)
		if os.path.isfile(source_path):
			#print(f"TRACE: Handling SOURCE_PATH ['{source_path}'] as a file.")
			for extension in plugin_extensions:
				if not source_path.endswith(extension):
					print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a .esp/.esm/.esl file or a directory containing .esp/.esm/.esl files.")
					return
				else:
					print(f"INFO: SOURCE_PATH ['{source_path}'] is valid. Handling SOURCE_PATH as a .esp/.esm/.esl file.")
					command = [exe_path, source_path, output_path]
					try:
						subprocess.run(command, check=True)
					except subprocess.CalledProcessError as e:
						print(f"ERROR: Error running CLI tool: {e}")
		elif os.path.isdir(source_path):
			print(f"INFO: SOURCE_PATH ['{source_path}'] is valid. Handling SOURCE_PATH as a directory.")
		else:
			print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a .esp/.esm/.esl file or a directory containing .esp/.esm/.esl files.")
			return
	
		#include_identical_strings = config.get('GENERAL', 'Include_Identical_Strings')
		#if include_identical_strings in false_vars:
		#	include_identical_strings = False
		#else:
		#	include_identical_strings = True
	else:








if __name__ == "__main__":
	main()
