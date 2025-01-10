@echo off
mkdir .vscode 2>nul

echo Creating VSCode configuration...
(
echo {
echo     "configurations": [
echo         {
echo             "name": "Win32",
echo             "includePath": [
echo                 "${workspaceFolder}/**",
echo                 "C:/Python313/include",
echo                 "C:/Python313/Lib/site-packages/greenlet/include",
echo                 "${workspaceFolder}/venv/Include",
echo                 "${workspaceFolder}/venv/Include/site/python3.13/greenlet"
echo             ],
echo             "defines": [],
echo             "compilerPath": "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.30.30705/bin/Hostx64/x64/cl.exe",
echo             "cStandard": "c17",
echo             "cppStandard": "c++17",
echo             "intelliSenseMode": "windows-msvc-x64",
echo             "browse": {
echo                 "path": [
echo                     "${workspaceFolder}",
echo                     "C:/Python313/include",
echo                     "C:/Python313/Lib/site-packages/greenlet/include",
echo                     "${workspaceFolder}/venv/Include",
echo                     "${workspaceFolder}/venv/Include/site/python3.13/greenlet"
echo                 ],
echo                 "limitSymbolsToIncludedHeaders": true,
echo                 "databaseFilename": ""
echo             }
echo         }
echo     ],
echo     "version": 4
echo }
) > .vscode\c_cpp_properties.json

echo VSCode configuration created.
echo Please reload VSCode window to apply changes.
pause 