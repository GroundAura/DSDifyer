{
}
unit userscript;

var
    slData: TStringList;

function Initialize: integer;
begin
    slData := TStringList.Create;
end;

function Process(e: IInterface): integer;
var
    i: integer;
    s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature: string;
    m, menuButtons, menuButton, menuButtons2, menuButton2, subRecord: IInterface;
begin
    // skip item if the selection is the master
    m := Master(e);
    if not Assigned(m) then Exit;

    s := '';

    // the current plugin the processing record exists in
    sCurrentPlugin := GetFileName(e);
    //slData.Add('Current Plugin: ' + sCurrentPlugin);

    // the master of the current record
    sMasterPlugin := GetFileName(MasterOrSelf(e));
    sEditorID := EditorID(MasterOrSelf(e));
    sSignature := Signature(e);
    //slData.Add('Master Plugin: ' + sMasterPlugin);
    //slData.Add('EditorID: ' + sEditorID);
    //slData.Add('Record Type: ' + sSignature);

    // add additional elements here
    if sSignature = 'MESG' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DESC');
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'FULL');
        if ElementExists (e, 'Menu Buttons') then begin
            menuButtons := ElementByName(e, 'Menu Buttons');
            menuButtons2 := ElementByName(m, 'Menu Buttons');
            for i := 0 to ElementCount(menuButtons) - 1 do begin
                menuButton := ElementByIndex(menuButtons, i);
                menuButton2 := ElementByIndex(menuButtons2, i);
                AddDataByPath(menuButton, menuButton2, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'ITXT');
            end;
        end;
    end else
    if sSignature = 'MGEF' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DNAM');
    end else
    if sSignature = 'SPEL' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DESC');
    end else
    if sSignature = 'SHOU' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DESC');
    end else
    if sSignature = 'GMST' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DATA\Name');
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DATA\Int');
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DATA\Bool');
    end;
end;

procedure AddDataByPath(e, m: IInterface; s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, path: string);
begin
    if not ElementExists(e, path) then Exit;
    slData.Add('[STRING]');
    slData.Add('Current Plugin: ' + sCurrentPlugin);
    slData.Add('Master Plugin: ' + sMasterPlugin);
    slData.Add('EditorID: ' + sEditorID);
    slData.Add('Record Type: ' + sSignature);
    slData.Add('Data Type: ' + path);
    s := GetElementEditValues(m, path);
    s := StringReplace(s, #13#10, '\n', [rfReplaceAll]);
    //s := StringReplace(s, #9, '\t', [rfReplaceAll]);
    slData.Add('Master Value: ' + s);
    s := GetElementEditValues(e, path);
    s := StringReplace(s, #13#10, '\n', [rfReplaceAll]);
    //s := StringReplace(s, #9, '\t', [rfReplaceAll]);
    slData.Add('Current Value: ' + s);
    slData.Add('');
end;

function Finalize: integer;
var
    dlgSave: TSaveDialog;
begin
    //AddMessage(slData.Text);
    if (slData.Count > 0) then begin
 
        // ask for file to export to
        dlgSave := TSaveDialog.Create(nil);
        dlgSave.Options := dlgSave.Options + [ofOverwritePrompt];
        dlgSave.Filter := 'Text files (*.txt)|*.txt';
        dlgSave.InitialDir := ProgramPath;
        dlgSave.FileName := 'DSDifyer Output.txt';
        if dlgSave.Execute then
            slData.SaveToFile(dlgSave.FileName);
        dlgSave.Free;
 
    end;
    slData.Free;
end;

end.
