import configparser
import os
from shutil import move as shutil_move
from subprocess import run as cmd
from subprocess import CalledProcessError as cmd_error

def read_config(file_path, case_sensitive):
	config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
	if case_sensitive:
		config.optionxform = lambda option: option
	config.read(file_path)
	return config

def move_file(source, destination):
	try:
		shutil_move(source, destination)
		#print(f"TRACE: File '{source}' moved successfully.")
	except Exception as e:
		print(f"ERROR: Error moving file '{source}': {e}")

def is_bethesda_plugin(file_path):
	plugin_extensions = (".esp", ".esm", ".esl")
	if not os.path.isfile(file_path) or not file_path.endswith(plugin_extensions):
		return False
	return True

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
	false_vars = ("false", "False", "FALSE", "f", "F", "0")

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

	if dump_mode:
		print(f"INFO: Running in DUMP_MODE.")
		source_path = config.get('DUMP_MODE', 'SOURCE_PATH')
		source_path = source_path.replace(root_var, ROOT_PATH)
		#print(source_path)
		if os.path.isdir(source_path):
			print(f"INFO: SOURCE_PATH ['{source_path}'] is valid. Handling SOURCE_PATH as a directory.")
			for root, _, files in os.walk(source_path):
				for file in files:
					source_file_path = os.path.join(root, file)
					if is_bethesda_plugin(source_file_path):
						command = [exe_path, source_file_path, source_file_path]
						try:
							cmd(command, check=True)
						except cmd_error as e:
							print(f"ERROR: Error running CLI tool: {e}")
							return
						json_name = os.path.basename(source_file_path)[:-3] + "json"
						old_path = os.path.join(root, json_name)
						new_path = os.path.join(output_path, json_name)
						move_file(old_path, new_path)
						print(f"INFO: Finished dumping '{source_file_path}' to '{new_path}'.")
		elif is_bethesda_plugin(source_path):
			print(f"INFO: SOURCE_PATH ['{source_path}'] is valid. Handling SOURCE_PATH as a Bethesda plugin.")
			command = [exe_path, source_path, source_path]
			try:
				cmd(command, check=True)
			except cmd_error as e:
				print(f"ERROR: Error running CLI tool: {e}")
				return
			json_name = os.path.basename(source_path)[:-3] + "json"
			old_path = os.path.join(os.path.dirname(source_path), json_name)
			new_path = os.path.join(output_path, json_name)
			move_file(old_path, new_path)
			print(f"INFO: Finished dumping '{source_path}' to '{new_path}'.")
		else:
			print(f"ERROR: SOURCE_PATH ['{source_path}'] must be a Bethesda plugin or a directory containing Bethesda plugins.")
			return
	else:
		print(f"INFO: Running in COMPARE_MODE.")
		origin_plugin_path = config.get('COMPARE_MODE', 'ORIGINAL_PLUGIN_PATH')
		origin_plugin_path = origin_plugin_path.replace(root_var, ROOT_PATH)
		#print(origin_plugin_path)
		if not is_bethesda_plugin(origin_plugin_path):
			print(f"ERROR: ORIGINAL_PLUGIN_PATH ['{origin_plugin_path}'] must be a Bethesda plugin.")
			return
		print(f"INFO: ORIGINAL_PLUGIN_PATH ['{origin_plugin_path}'] is valid.")
		edited_plugin_path = config.get('COMPARE_MODE', 'EDITED_PLUGIN_PATH')
		edited_plugin_path = edited_plugin_path.replace(root_var, ROOT_PATH)
		#print(edited_plugin_path)
		if not is_bethesda_plugin(edited_plugin_path):
			print(f"ERROR: EDITED_PLUGIN_PATH ['{edited_plugin_path}'] must be a Bethesda plugin.")
			return
		print(f"INFO: EDITED_PLUGIN_PATH ['{edited_plugin_path}'] is valid.")
		command = [exe_path, origin_plugin_path, edited_plugin_path]
		try:
			cmd(command, check=True)
		except cmd_error as e:
			print(f"ERROR: Error running CLI tool: {e}")
			return
		json_name = os.path.basename(edited_plugin_path)[:-3] + "json"
		old_path = os.path.join(os.path.dirname(edited_plugin_path), json_name)
		new_path = os.path.join(output_path, json_name)
		move_file(old_path, new_path)
		print(f"INFO: Finished translating '{origin_plugin_path}' to '{new_path}'.")

if __name__ == "__main__":
	main()
