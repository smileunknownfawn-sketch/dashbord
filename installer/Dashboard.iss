#define AppName "Дашборд розпоряджень"
#define AppVersion "1.0.1"
#define AppExeName "Dashboard_1.0.1.exe"

[Setup]
AppId={{A1D7A0D1-0101-4010-9A01-DASHBOARD2026}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher="В.О.М."
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputDir=output
OutputBaseFilename=Дашборд_розпоряджень_1.0.1_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
Uninstallable=yes

[Files]
Source: "..\dist\Dashboard_1.0.1.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\sounds\opiat-rabota.mp3"; DestDir: "{app}\sounds"; Flags: ignoreversion
Source: "..\language-russian.jpg"; DestDir: "{app}\assets"; DestName: "language-russian.jpg"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[UninstallDelete]
; Робочі дані навмисно не видаляються. Вони знаходяться поза папкою програми.
Type: filesandordirs; Name: "{app}\sounds"
Type: filesandordirs; Name: "{app}\assets"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Запустити {#AppName}"; Flags: nowait postinstall skipifsilent
