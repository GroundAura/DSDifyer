import configparser
import os
import shutil
#from fileinput import FileInput
#from pathlib import Path
#from pathlib2 import Path

print("Beginning preparing repository.")

# VARIABLES

print("Setting Variables: Starting...")

def read_config(file_path, section_header):
    config = configparser.ConfigParser(comment_prefixes=(";", "#", "//"), inline_comment_prefixes=(";", "#", "//"))
    config.read(file_path)
    return config[section_header]

config_path = './.vscode/variables.ini'
config_values_ids = read_config(config_path, 'IDs')
config_values_license = read_config(config_path, 'License')
config_values_name = read_config(config_path, 'Name')
config_values_paths = read_config(config_path, 'Paths')
config_values_socials = read_config(config_path, 'Socials')

# Old Text:
old_author_display = "{AuthorName}"
old_author_github = "{GitHubAccount}"
old_contact_info = "{ContactInfo}"
old_discord_server = "{DiscordServer}"
old_id_github = "{RepositoryName}"
old_id_nexus = "{NexusID}"
old_kofi_account = "{KofiAccount}"
old_license_holder = "{LicensorName}"
old_license_year = "{LicenseYear}"
old_linktree_account = "{LinktreeAccount}"
old_name_folder = "{FolderName}"
old_name_mo2_release = "{MO2ModName}"
old_name_mo2_test = "{MO2ModNameTest}"
old_name_plugin = "{PluginName}"
old_name_plugin_short = "{PluginNameShort}"
old_name_zip = "{ZipName}"
old_nexus_account_id = "{NexusAccountID}"
old_path_7Zip = "{Path7Zip}"
old_path_md2nexus = "C:\Games\Skyrim\Tools\md2nexus"
old_path_MO2Downloads = "{PathMO2Downloads}"
old_path_MO2Mods = "{PathMO2Mods}"
old_path_PapyrusCK = "{PathCKSource}"
old_path_PapyrusMCMHelper = "{PathMCMHelperSource}"
old_path_PapyrusSKSE = "{PathSKSESource}"
old_title = "{TitleName}"
old_title_short = "{TitleNameShort}"
old_title_xml = "{TitleNameXML}"
old_title_xml_short = "{TitleNameXMLShort}"

# New Text:
new_author_display = config_values_name["AuthorName"]
new_author_github = config_values_ids["GitHubAccount"]
new_contact_info = config_values_socials["ContactInfo"]
new_discord_server = config_values_socials["DiscordServer"]
new_id_github = config_values_ids["RepositoryName"]
new_id_nexus = config_values_ids["NexusID"]
new_kofi_account = config_values_socials["KofiAccount"]
new_license_holder = config_values_license["LicensorName"]
new_license_year = config_values_license["LicenseYear"]
new_linktree_account = config_values_socials["LinktreeAccount"]
new_name_folder = config_values_name["FolderName"]
new_name_mo2_release = config_values_name["MO2ModName"]
new_name_mo2_test = config_values_name["MO2ModNameTest"]
new_name_plugin = config_values_name["PluginName"]
new_name_plugin_short = config_values_name["PluginNameShort"]
new_name_zip = config_values_name["ZipName"]
new_nexus_account_id = config_values_socials["NexusAccountID"]
new_path_7Zip = config_values_paths["Path7Zip"]
new_path_md2nexus = config_values_paths["Pathmd2nexus"]
new_path_MO2Downloads = config_values_paths["PathMO2Downloads"]
new_path_MO2Mods = config_values_paths["PathMO2Mods"]
new_path_PapyrusCK = config_values_paths["PathCKSource"]
new_path_PapyrusMCMHelper = config_values_paths["PathMCMHelperSource"]
new_path_PapyrusSKSE = config_values_paths["PathSKSESource"]
new_title = config_values_name["TitleName"]
new_title_xml = config_values_name["TitleNameXML"]
new_title_short = config_values_name["TitleNameShort"]
new_title_short_xml = config_values_name["TitleNameXMLShort"]

print("Setting Variables: Complete!")



# REPLACE TEXT

print("Replacing Text: Starting...")
print(os.getcwd())

os.chdir("./_root")
print(os.getcwd())

with open(r'CODE_OF_CONDUCT.md', 'r') as file:
	data = file.read()
	data = data.replace(old_contact_info, new_contact_info)
with open(r'CODE_OF_CONDUCT.md', 'w') as file:
	file.write(data)

with open(r'LICENSE.txt', 'r') as file:
	data = file.read()
	data = data.replace(old_license_holder, new_license_holder)
	data = data.replace(old_license_year, new_license_year)
with open(r'LICENSE.txt', 'w') as file:
	file.write(data)

with open(r'README.md', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
	data = data.replace(old_author_display, new_author_display)
	data = data.replace(old_id_nexus, new_id_nexus)
	data = data.replace(old_author_github, new_author_github)
	data = data.replace(old_id_github, new_id_github)
with open(r'README.md', 'w') as file:
	file.write(data)

os.chdir("..")
print(os.getcwd())


#os.chdir("./.github")
#print(os.getcwd())
#
#os.chdir("..")
#print(os.getcwd())


#os.chdir("./.github/workflows")
#print(os.getcwd())
#
#os.chdir("../..")
#print(os.getcwd())


#os.chdir("./.idea")
#print(os.getcwd())
#
#os.chdir("..")
#print(os.getcwd())


#os.chdir("./.idea/general")
#print(os.getcwd())
#
#os.chdir("../..")
#print(os.getcwd())


#os.chdir("./.vscode")
#print(os.getcwd())
#
#os.chdir("..")
#print(os.getcwd())


os.chdir("./.vscode/papyrus")
print(os.getcwd())

with open(r'README.md', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
with open(r'README.md', 'w') as file:
	file.write(data)

with open(r'debug.ppj', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
	data = data.replace(old_path_MO2Mods, new_path_MO2Mods)
	data = data.replace(old_path_PapyrusCK, new_path_PapyrusCK)
	data = data.replace(old_path_PapyrusSKSE, new_path_PapyrusSKSE)
	data = data.replace(old_path_PapyrusMCMHelper, new_path_PapyrusMCMHelper)
with open(r'debug.ppj', 'w') as file:
	file.write(data)

with open(r'release.ppj', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
	data = data.replace(old_path_MO2Mods, new_path_MO2Mods)
	data = data.replace(old_path_PapyrusCK, new_path_PapyrusCK)
	data = data.replace(old_path_PapyrusSKSE, new_path_PapyrusSKSE)
	data = data.replace(old_path_PapyrusMCMHelper, new_path_PapyrusMCMHelper)
with open(r'release.ppj', 'w') as file:
	file.write(data)

os.chdir("../..")
print(os.getcwd())


os.chdir("./.vscode/scripts")
print(os.getcwd())

with open(r'copy-img.bat', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
with open(r'copy-img.bat', 'w') as file:
	file.write(data)

with open(r'copy-pex.bat', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
with open(r'copy-pex.bat', 'w') as file:
	file.write(data)

with open(r'md2nexus.bat', 'r') as file:
	data = file.read()
	data = data.replace(old_path_md2nexus, new_path_md2nexus)
with open(r'md2nexus.bat', 'w') as file:
	file.write(data)

with open(r'mo2-downloads.bat', 'r') as file:
	data = file.read()
	data = data.replace(old_name_zip, new_name_zip)
	data = data.replace(old_path_MO2Downloads, new_path_MO2Downloads)
with open(r'mo2-downloads.bat', 'w') as file:
	file.write(data)

with open(r'mo2-mod.bat', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
	data = data.replace(old_name_mo2_test, new_name_mo2_test)
	data = data.replace(old_path_MO2Mods, new_path_MO2Mods)
with open(r'mo2-mod.bat', 'w') as file:
	file.write(data)

with open(r'zip.bat', 'r') as file:
	data = file.read()
	data = data.replace(old_name_folder, new_name_folder)
	data = data.replace(old_name_zip, new_name_zip)
	data = data.replace(old_path_7Zip, new_path_7Zip)
with open(r'zip.bat', 'w') as file:
	file.write(data)

os.chdir("../..")
print(os.getcwd())


#os.chdir("./build")
#print(os.getcwd())
#
#os.chdir("..")
#print(os.getcwd())


os.chdir("./build/MO2")
print(os.getcwd())

with open(r'' + old_name_zip + '.zip.meta', 'r') as file:
	data = file.read()
	data = data.replace(old_name_mo2_test, new_name_mo2_test)
	data = data.replace(old_title, new_title)
with open(r'' + old_name_zip + '.zip.meta', 'w') as file:
	file.write(data)

os.chdir("../..")
print(os.getcwd())


#os.chdir("./dist/" + old_name_folder)
#print(os.getcwd())
#
#os.chdir("../..")
#print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/Base")
#print(os.getcwd())
#
#os.chdir("../../..")
#print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/Base/interface")
#print(os.getcwd())
#
#os.chdir("../../../..")
#print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Base/interface/translations")
print(os.getcwd())

with open(r'' + old_name_plugin + '_ENGLISH.txt', 'r', encoding='utf-16-le') as file:
	data = file.read()
	data = data.replace(old_name_plugin_short, new_name_plugin_short)
	data = data.replace(old_title, new_title)
with open(r'' + old_name_plugin + '_ENGLISH.txt', 'w', encoding='utf-16-le') as file:
	file.write(data)

os.chdir("../../../../..")
print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/Base/MCM")
#print(os.getcwd())
#
#os.chdir("../../../..")
#print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/Base/MCM/Config")
#print(os.getcwd())
#
#os.chdir("../../../../..")
#print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Base/MCM/Config/" + old_name_plugin)
print(os.getcwd())

with open(r'config.json', 'r') as file:
	data = file.read()
	data = data.replace(old_name_plugin, new_name_plugin)
	data = data.replace(old_name_plugin_short, new_name_plugin_short)
with open(r'config.json', 'w') as file:
	file.write(data)

os.chdir("../../../../../..")
print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/Base/scripts")
#print(os.getcwd())
#
#os.chdir("../../../..")
#print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/fomod")
print(os.getcwd())

with open(r'info.xml', 'r', encoding='utf-16-le') as file:
	data = file.read()
	data = data.replace(old_title_xml, new_title_xml)
	data = data.replace(old_author_display, new_author_display)
	data = data.replace(old_id_nexus, new_id_nexus)
with open(r'info.xml', 'w', encoding='utf-16-le') as file:
	file.write(data)

with open(r'ModuleConfig.xml', 'r', encoding='utf-16-le') as file:
	data = file.read()
	data = data.replace(old_title_xml, new_title_xml)
with open(r'ModuleConfig.xml', 'w', encoding='utf-16-le') as file:
	file.write(data)

os.chdir("../../..")
print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/fomod/images")
#print(os.getcwd())
#
#os.chdir("../../../..")
#print(os.getcwd())


#os.chdir("./dist/" + old_name_folder + "/Source")
#print(os.getcwd())
#
#os.chdir("../../..")
#print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Source/scripts")
print(os.getcwd())

with open(r'' + old_name_plugin_short + '_MCM.psc', 'r') as file:
	data = file.read()
	data = data.replace(old_name_plugin_short, new_name_plugin_short)
with open(r'' + old_name_plugin_short + '_MCM.psc', 'w') as file:
	file.write(data)

os.chdir("../../../..")
print(os.getcwd())


os.chdir("./docs")
print(os.getcwd())

with open(r'CHANGELOG.md', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
with open(r'CHANGELOG.md', 'w') as file:
	file.write(data)

os.chdir("..")
print(os.getcwd())


os.chdir("./docs/description-md")
print(os.getcwd())

with open(r'description_brief.txt', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
with open(r'description_brief.txt', 'w') as file:
	file.write(data)

with open(r'description_detailed.md', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
	data = data.replace(old_title_short, new_title_short)
	data = data.replace(old_author_github, new_author_github)
	data = data.replace(old_id_github, new_id_github)
	data = data.replace(old_linktree_account, new_linktree_account)
	data = data.replace(old_discord_server, new_discord_server)
	data = data.replace(old_kofi_account, new_kofi_account)
	data = data.replace(old_nexus_account_id, new_nexus_account_id)
with open(r'description_detailed.md', 'w') as file:
	file.write(data)

os.chdir("../..")
print(os.getcwd())


os.chdir("./docs/description-nexus")
print(os.getcwd())

with open(r'description_brief.txt', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
with open(r'description_brief.txt', 'w') as file:
	file.write(data)

with open(r'description_detailed.bbcode', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
	data = data.replace(old_title_short, new_title_short)
	data = data.replace(old_author_github, new_author_github)
	data = data.replace(old_id_github, new_id_github)
	data = data.replace(old_linktree_account, new_linktree_account)
	data = data.replace(old_discord_server, new_discord_server)
	data = data.replace(old_kofi_account, new_kofi_account)
	data = data.replace(old_nexus_account_id, new_nexus_account_id)
with open(r'description_detailed.bbcode', 'w') as file:
	file.write(data)

os.chdir("../..")
print(os.getcwd())


#os.chdir("./docs/images")
#print(os.getcwd())
#
#os.chdir("../..")
#print(os.getcwd())


#os.chdir("./docs/images/brand")
#print(os.getcwd())
#
#os.chdir("../../..")
#print(os.getcwd())


#os.chdir("./docs/images/screenshots")
#print(os.getcwd())
#
#os.chdir("../../..")
#print(os.getcwd())


os.chdir("./docs/wiki")
print(os.getcwd())

with open(r'_Footer.md', 'r') as file:
	data = file.read()
	data = data.replace(old_author_github, new_author_github)
	data = data.replace(old_id_github, new_id_github)
with open(r'_Footer.md', 'w') as file:
	file.write(data)

with open(r'_Sidebar.md', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
	data = data.replace(old_author_github, new_author_github)
	data = data.replace(old_id_github, new_id_github)
with open(r'_Sidebar.md', 'w') as file:
	file.write(data)

with open(r'Home.md', 'r') as file:
	data = file.read()
	data = data.replace(old_title, new_title)
with open(r'Home.md', 'w') as file:
	file.write(data)

os.chdir("../..")
print(os.getcwd())


print("Replacing Text: Complete!")



# RENAME FILES

print("Renaming Files: Starting...")
print(os.getcwd())


os.chdir("./build/MO2")
print(os.getcwd())

if (os.path.isfile(old_name_zip + ".zip.meta")):
	os.rename(old_name_zip + ".zip.meta", new_name_zip + ".zip.meta")

os.chdir("../..")
print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Base")
print(os.getcwd())

if (os.path.isfile(old_name_plugin + ".esl")):
	os.rename(old_name_plugin + ".esl", new_name_plugin + ".esl")
if (os.path.isfile(old_name_plugin + ".esm")):
	os.rename(old_name_plugin + ".esm", new_name_plugin + ".esm")
if (os.path.isfile(old_name_plugin + ".esp")):
	os.rename(old_name_plugin + ".esp", new_name_plugin + ".esp")

os.chdir("../../..")
print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Base/interface/translations")
print(os.getcwd())

if (os.path.isfile(old_name_plugin + "_ENGLISH.txt")):
	os.rename(old_name_plugin + "_ENGLISH.txt", new_name_plugin + "_ENGLISH.txt")

os.chdir("../../../../..")
print(os.getcwd())


## if (os.path.exists("./dist/" + old_name_folder + "/Base/scripts")):
#os.chdir("dist/" + old_name_folder + "/Base/scripts")
#print(os.getcwd())
#
#if (os.path.isfile(old_name_plugin_short + "_MCM.pex")):
#	os.rename(old_name_plugin_short + "_MCM.pex", new_name_plugin_short + "_MCM.pex")
#
#os.chdir("../../..")
#print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Source/scripts")
print(os.getcwd())

if (os.path.isfile(old_name_plugin_short + "_MCM.psc")):
	os.rename(old_name_plugin_short + "_MCM.psc", new_name_plugin_short + "_MCM.psc")

os.chdir("../../../..")
print(os.getcwd())


print("Renaming Files: Complete!")



# RENAME FOLDERS

print("Renaming Directories: Starting...")
print(os.getcwd())


os.chdir("./dist/" + old_name_folder + "/Base/MCM/Config")
print(os.getcwd())

if (os.path.exists(old_name_plugin)):
	shutil.move(old_name_plugin, new_name_plugin)

os.chdir("../../../../..")
print(os.getcwd())


os.chdir("./dist")
print(os.getcwd())

if (os.path.exists(old_name_folder)):
	shutil.move(old_name_folder, new_name_folder)

os.chdir("..")
print(os.getcwd())


print("Renaming Directories: Complete!")



# MOVE FILES

print("Moving Files: Starting...")
print(os.getcwd())

if (os.path.isfile("CODE_OF_CONDUCT.md")):
	os.remove("CODE_OF_CONDUCT.md")
	shutil.move("./_root/CODE_OF_CONDUCT.md", "./CODE_OF_CONDUCT.md")
	print("moved CODE_OF_CONDUCT.md")

if (os.path.isfile("LICENSE.txt")):
	os.remove("LICENSE.txt")
	shutil.move("./_root/LICENSE.txt", "./LICENSE.txt")
	print("moved LICENSE.txt")

if (os.path.isfile("README.md")):
	os.remove("README.md")
	shutil.move("./_root/README.md", "./README.md")
	print("moved README.md")

if (os.path.exists("_root")):
	os.rmdir("_root")
	print("removed _root/")


print("Moving Files: Complete!")



print("Done preparing repository!")


