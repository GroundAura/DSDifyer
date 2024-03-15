# Papyrus Compiler

## Dependencies

- Skyrim Special Edition

- Skyrim Special Edition Creation Kit

- Visual Studio Code Papyrus Plugin ([download](https://marketplace.visualstudio.com/items?itemName=joelday.papyrus-lang-vscode))

## Configure

- Ensure that you have opened the Creation Kit at least once and allowed scripts to extract

- Edit the Papyrus plugin settings for Visual Studio Code to set the `papyrus.skyrimSpecialEdition.installPath` to the installation path of your Skyrim and Creation Kit instance

- Edit the `\.vscode\papyrus\debug.ppj` and `\.vscode\papyrus\release.ppj` files to update the import directories to point to your decompiled scripts folder(s)

## Develop

- Create your script files in the `\dist\{FolderName}\Source\scripts\` directory

- Run the build task (`ctrl-shift-b` by default, or `ctrl-shift-p` -> `Run Build Task`) to build both release and debug versions

- To build only one version `ctrl-shift-p` -> `Run Task` -> `Compile Papyrus Scripts <Type>`
