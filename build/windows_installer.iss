[Setup]
AppName=easysnec
AppVersion={#VersionNo}


; DefaultDirName=easysnec
DefaultDirName={autopf}\easysnec
DefaultGroupName=easysnec
OutputBaseFilename=install_easysnec_{#VersionNo}
Compression=lzma
SolidCompression=yes

; [Languages]
; Name: "english"; MessagesFile: "compiler:Default.isl"
[Files]
Source: "..\dist\binary\easysnec-{#VersionNo}.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; https://www.icoconverter.com/ for making more or less-blurry icons
Name: "{group}\easysnec"; Filename: "{app}\easysnec-{#VersionNo}.exe"; IconFilename: "{app}\icon.ico"

[Run]
; Filename: {app}\easysnec-{#VersionNo}.exe; Description: {cm:LaunchProgram,easysnec}; Flags: nowait postinstall skipifsilent
Filename: {app}\easysnec-{#VersionNo}.exe; Flags: nowait
; Name: "{commondesktop}\MyApp"; Filename: "{app}\MyApp.exe"; Tasks: desktopicon
; [Tasks]
; Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons"; Flags: unchecked