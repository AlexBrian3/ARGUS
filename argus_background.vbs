' Silent background launcher for ARGUS (runs with zero visible command prompt windows)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
currentDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Run python daemon in background silently
WshShell.Run "python -m brain.daemon --continuous", 0, False
