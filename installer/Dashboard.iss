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
DisableProgramGroupPage=yes

[Languages]
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Files]
Source: "..\dist\Dashboard_1.0.1.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\sounds\opiat-rabota.mp3"; DestDir: "{app}\sounds"; Flags: ignoreversion
Source: "..\language-russian.jpg"; DestDir: "{app}\assets"; DestName: "language-russian.jpg"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\sounds"
Type: filesandordirs; Name: "{app}\assets"

[Run]
Filename: "{app}\{#AppExeName}"; Parameters: "/datafolder=""{code:DataDir}"""; Description: "Запустити {#AppName}"; Flags: nowait postinstall skipifsilent

[Code]
var
  DataDirPage: TInputDirWizardPage;

procedure InitializeWizard;
begin
  DataDirPage := CreateInputDirPage(wpSelectDir,
    'Папка для даних розпоряджень',
    'Оберіть, де зберігати розпорядження та всі пов’язані дані',
    'У цій папці програма створить базу, розпорядження, додатки, відповіді, резервні копії та звіти.',
    False, 'Дашборд розпоряджень');
  DataDirPage.Add('Папка даних:');
  DataDirPage.Values[0] := ExpandConstant('{userdocs}\Дашборд розпоряджень');
end;

function DataDir(Param: String): String;
begin
  Result := DataDirPage.Values[0];
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Marker: String;
begin
  if CurStep = ssPostInstall then
  begin
    Marker := DataDirPage.Values[0];
    ForceDirectories(Marker);
    SaveStringToFile(AddBackslash(ExpandConstant('{app}')) + 'data-folder.txt', Marker + #13#10, False);
  end;
end;
