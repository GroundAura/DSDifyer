# \[center\]![DSDifyer](https://raw.githubusercontent.com/GroundAura/DSDifyer/main/docs/images/brand/Title.png)\[/center\]\[line\]

\[font=Verdana\]**DSDifyer**\[/font\] is a collection of xEdit and Python scripts to assist with creating Dynamic String Distributor mods. This is a modders tool and **not** a playable file.

I mainly made these for English to English changes, but they might be useful for other language translations too.

## \[center\]![Installation](https://raw.githubusercontent.com/GroundAura/Auras-Resources/main/Images/Banners/Skyrim-1/Installation.png)\[/center\]

Download and extract DSDifyer anywhere on your system. Move `DSDifyer.pas` to your `Edit Scripts` folder in your SSEEdit installation.

## \[font=Verdana\]**Requirements**\[/font\]

- [Dynamic String Distributor](https://www.nexusmods.com/skyrimspecialedition/mods/107676) - To use the DSD files in-game.

- [Python](https://www.python.org/downloads/) - To use the Python scripts.

- [SSEEdit](https://www.nexusmods.com/skyrimspecialedition/mods/164) - To use the xEdit to DSD scripts.

- [xTranslator](https://www.nexusmods.com/starfield/mods/313) - To use the xTranslator to DSD script.

## \[font=Verdana\]**Optional Requirements**\[/font\]

- [VS Code](https://code.visualstudio.com/) and its [Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) - To use the build tasks and generally make your life easier.

## \[center\]![Details](https://raw.githubusercontent.com/GroundAura/Auras-Resources/main/Images/Banners/Skyrim-1/Details.png)\[/center\]

## \[font=Verdana\]**xEdit to DSD**\[/font\]

Gets data from xEdit and formats it as DSD files with folders. This is the most finished option with formatting for DSD v1.1.0.

1. Open SSEEdit and load up all the files that have strings you want to replace.

2. Select the plugin(s) or record(s) that have strings you want to replace.

3. Right click. Select '`Apply Script`'. For Script select '`DSDifyer`'. Select '`OK`'.

4. Wait until the xEdit script finishes running. If you selected a large amount of records like the base game ESMs this may take a few minutes.

5. When it prompts you, save the file to '`{install_path}\input\DSDifyer Output.txt`'. If it prompts you to overwrite the file, select '`Yes`'. You can now close xEdit.

6. Open the '`DSDifyer`' folder in VS Code.

7. Press '`Ctrl + Shift + P`' to open the Command Pallete. Type to filter for and select '`Python: Select Interpreter`'. Select one of the options that says something like '`Python 3.12.2 64-bit`'. This should only need to be done once per workspace.

8. Open '`xEdit-to-DSD.ini`' and change any settings if you want.

9. Press '`Ctrl + Shift + B`' to open the Build Task Runner. Select '`Compile DSD from xEdit output`'.

10. Wait until the Python script finishes running. If you selected a large amount of records this may take several minutes or longer. If it's too long it might not finish and you may have to kill the terminal; I'll look into optimizing this.

11. Go to '`{install_path}\output`' to find your DSD files and folders.

## \[font=Verdana\]**xTranslator to DSD**\[/font\]

Gets data from xTranslator and formats it as DSD files. This is slightly outdated as its formatting was made for DSD v1.0.x and xTranslator also doesn't provide all the necessary data for DSD v1.1.0, but it still may be useful so I'll leave it here just in case. **Don't expect this one to work without additional manual work!**

1. Open xTranslator and load up the plugin that has strings you want to replace.

2. Export the data as XML to '`{install_path}\input`'.

3. Repeat steps 1-2 for each plugin that has strings you want to replace. You can then close xTranslator.

4. Open the '`DSDifyer`' folder in VS Code.

5. Press '`Ctrl + Shift + P`' to open the Command Pallete. Type to filter for and select '`Python: Select Interpreter`'. Select one of the options that says something like '`Python 3.12.2 64-bit`'. This should only need to be done once per workspace.

6. Open '`xTranslator-to-DSD.ini`' and change any settings if you want.

7. Press '`Ctrl + Shift + B`' to open the Build Task Runner. Select '`Compile DSD from xTranslator output`'.

8. Wait until the Python script finishes running.

9. Go to '`{install_path}\output`' to find your DSD files.

## \[font=Verdana\]**Generate Folders**\[/font\]

Gets names of plugins from a MO2 `plugins.txt` file or by searching folders for `.esp`/`.esm`/`.esl` files, then creates folders for DSD from that list of plugin names. Should work for any version of DSD and may even have more general uses.

1. Open the '`DSDifyer`' folder in VS Code.

2. Press '`Ctrl + Shift + P`' to open the Command Pallete. Type to filter for and select '`Python: Select Interpreter`'. Select one of the options that says something like '`Python 3.12.2 64-bit`'. This should only need to be done once per workspace.

3. Open '`Generate-Folders.ini`' and change any settings if you want.

4. Press '`Ctrl + Shift + B`' to open the Build Task Runner. Select '`Generate Folders from plugin list`'.

5. Wait until the Python script finishes running.

6. Go to '`{install_path}\output`' to find your DSD folders.

## \[center\]![Recommendations](https://raw.githubusercontent.com/GroundAura/Auras-Resources/main/Images/Banners/Skyrim-1/Recommendations.png)\[/center\]

Other useful tools for working with Dynamic String Distributor.

- [Dynamic String Distributor - Scheme](https://github.com/SkyHorizon3/SSE-Dynamic-String-Distributor/blob/main/doc/Doc.md)

- [Freeformatter (JSON Escape)](https://www.freeformatter.com/json-escape.html#before-output)

- [Freeformatter (JSON Validator)](https://www.freeformatter.com/json-validator.html)

- [SSE Auto Translator](https://www.nexusmods.com/skyrimspecialedition/mods/111491)

- [Simple but easy configuration tool for Dynamic String Distributor](https://www.nexusmods.com/skyrimspecialedition/mods/114077)

## \[center\]![Contributing & Source](https://raw.githubusercontent.com/GroundAura/Auras-Resources/main/Images/Banners/Skyrim-1/Contributing%20%26%20Source.png)\[/center\]

This is one of my first projects working with both Python and xEdit scripting. I'm sure it's not written in the best way possible, but it works. If you have any ideas on how to improve or optimize my script feel free to leave a suggestion or a PR. Same goes for feature ideas, although I can't promise I'll know how to implement them or have the time.

The entire tool is licensed under the [The Clear BSD License](https://choosealicense.com/licenses/bsd-3-clause-clear/) so you're free to use it basically however you want.

[Mirror/Source on GitHub](https://github.com/GroundAura/DSDifyer)

## \[center\]![Thanks](https://raw.githubusercontent.com/GroundAura/Auras-Resources/main/Images/Banners/Skyrim-1/Thanks.png)\[/center\]

- [SkyHorizon](https://www.nexusmods.com/users/124533098) for [Dynamic String Distributor](https://www.nexusmods.com/skyrimspecialedition/mods/107676).

- Jonathan from the xEdit Discord for the initial xEdit script write up and answering my xEdit questions.

- [ChatGPT](https://chat.openai.com/) for answering some of my questions.

\[center\][![linktree](https://i.imgur.com/jOQE4n8.png)](https://linktr.ee/groundaura)[\[font=Verdana\]\[color=#ffffff\]**Find me on Linktree**\[/font\]\[/color\]](https://linktr.ee/groundaura)\[/center\]
\[center\][![discord](https://github.com/doodlum/nexusmods-widgets/blob/main/Discord_40px.png?raw=true)](https://discord.gg/zft8DmbfKv)\[/center\]
\[center\][![kofi](https://github.com/doodlum/nexusmods-widgets/blob/main/Ko-fi_40px_60fps.png?raw=true)](https://ko-fi.com/groundaura)\[/center\]

## \[center\][\[font=Verdana\]\[color=#027f00\]\[u\]**> > > Check Out My Other Mods! < < <**\[/u\]\[/font\]\[/color\]](https://www.nexusmods.com/users/97658973?tab=user+files)\[/center\]
