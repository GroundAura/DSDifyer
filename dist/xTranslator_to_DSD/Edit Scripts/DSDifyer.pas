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
    if not Assigned(m) then m := e;
    //if not Assigned(m) then Exit;

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
    AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'FULL');
    AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DESC');
    if sSignature = 'ACTI' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'RNAM');
    end else
    if sSignature = 'BOOK' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'CNAM');
    end else
    if sSignature = 'FLOR' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'RNAM');
    end else
    if sSignature = 'GMST' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DATA\Name');
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DATA\Int');
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'DATA\Bool');
    end else
    if sSignature = 'INFO' then begin
        // "Responses" > i "Response" > "NAM1 - Response Text"
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'NAM1');
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'RNAM');
    end else
    if sSignature = 'MESG' then begin
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
    if sSignature = 'NPC_' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'SHRT');
    end else
    //if sSignature = 'PERK' then begin
        // "Effects (sorted) > i "Effect" > "Function Parameters" > "EPFD - Data" > "Text"
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'EPFD');
    //end else
    if sSignature = 'QUST' then begin
        // "Stages (sorted)" > i "Stage" > "Log Entries" > i "Log Entry" > "CNAM - Log Entry"
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'CNAM');
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'NNAM');
    end else
    if sSignature = 'REGN' then begin
        // "Region Data Entries (sorted)" > "Region Data Entry" > "RDMP - Map Name"
        //AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'RDMP');
    end else
    if sSignature = 'WOOP' then begin
        AddDataByPath(e, m, s, sCurrentPlugin, sMasterPlugin, sEditorID, sSignature, 'TNAM');
    end
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
