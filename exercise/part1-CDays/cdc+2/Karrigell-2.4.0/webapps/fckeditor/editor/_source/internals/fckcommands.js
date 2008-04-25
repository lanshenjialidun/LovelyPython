/*
 * FCKeditor - The text editor for internet
 * Copyright (C) 2003-2004 Frederico Caldeira Knabben
 * 
 * Licensed under the terms of the GNU Lesser General Public License:
 * 		http://www.opensource.org/licenses/lgpl-license.php
 * 
 * For further information visit:
 * 		http://www.fckeditor.net/
 * 
 * File Name: fckcommands.js
 * 	Define all commands available in the editor.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-02 00:56:46
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKCommands = new Object() ;

/*
Instead of adding a line like this for every named command:
FCKCommands['Bold'] = new FCKNamedCommand( 'Bold' ) ;
... an Array was created to simplify the code (and reduce its size).
*/
var sNamedCommands = [ 
	'Cut','Copy','Paste','Print','Find','SelectAll','RemoveFormat','Unlink','Undo','Redo',
	'Bold','Italic','Underline','StrikeThrough','Subscript','Superscript',
	'JustifyLeft','JustifyCenter','JustifyRight','JustifyFull','Outdent','Indent',
	'InsertOrderedList','InsertUnorderedList','InsertHorizontalRule'] ;

// Loops throw all named items.
for ( i = 0 ; i < sNamedCommands.length ; i++ )
{
	FCKCommands[ sNamedCommands[i] ] = new FCKNamedCommand( sNamedCommands[i] ) ;
}

//### Other Commands.
FCKCommands['Link']			= new FCKDialogCommand( 'Link'			, FCKLang.DlgLnkWindowTitle, 'dialog/fck_link.html'	, 400, 330, FCK.GetNamedCommandState, 'CreateLink' ) ;
FCKCommands['About']		= new FCKDialogCommand( 'About'			, FCKLang.About, 'dialog/fck_about.html'	, 400, 330 ) ;

FCKCommands['Image']		= new FCKDialogCommand( 'Image'			, 'Image Properties', 'dialog/fck_image.html'		, 450, 400, FCK.GetNamedCommandState, 'InsertImage' ) ;
FCKCommands['Table']		= new FCKDialogCommand( 'Table'			, 'Table Properties', 'dialog/fck_table.html'		, 400, 250 ) ;
FCKCommands['TableProp']	= new FCKDialogCommand( 'Table'			, 'Table Properties', 'dialog/fck_table.html?Parent', 400, 250 ) ;
FCKCommands['SpecialChar']	= new FCKDialogCommand( 'SpecialChar'	, 'Select Character', 'dialog/fck_specialchar.html'	, 400, 300, FCK.GetNamedCommandState, 'InsertImage' ) ;
FCKCommands['Smiley']		= new FCKDialogCommand( 'Smiley'		, FCKLang.DlgSmileyTitle, 'dialog/fck_smiley.html'	, FCKConfig.SmileyWindowWidth, FCKConfig.SmileyWindowHeight, FCK.GetNamedCommandState, 'InsertImage' ) ;

FCKCommands['FontName']		= new FCKFontNameCommand() ;
FCKCommands['FontSize']		= new FCKFontSizeCommand() ;
FCKCommands['FontFormat']	= new FCKFormatBlockCommand() ;

FCKCommands['Source']		= new FCKSourceCommand() ;
FCKCommands['Preview']		= new FCKPreviewCommand() ;
FCKCommands['Save']			= new FCKSaveCommand() ;
FCKCommands['NewPage']		= new FCKNewPageCommand() ;

FCKCommands['TextColor']	= new FCKTextColorCommand('ForeColor') ;
FCKCommands['BGColor']		= new FCKTextColorCommand('BackColor') ;

FCKCommands['PasteText']	= new FCKPastePlainTextCommand() ;
FCKCommands['PasteWord']	= new FCKPasteWordCommand() ;

FCKCommands['TableInsertRow']		= new FCKTableCommand('TableInsertRow') ;
FCKCommands['TableDeleteRows']		= new FCKTableCommand('TableDeleteRows') ;
FCKCommands['TableInsertColumn']	= new FCKTableCommand('TableInsertColumn') ;
FCKCommands['TableDeleteColumns']	= new FCKTableCommand('TableDeleteColumns') ;
FCKCommands['TableInsertCell']		= new FCKTableCommand('TableInsertCell') ;
FCKCommands['TableDeleteCells']		= new FCKTableCommand('TableDeleteCells') ;
FCKCommands['TableMergeCells']		= new FCKTableCommand('TableMergeCells') ;
FCKCommands['TableSplitCell']		= new FCKTableCommand('TableSplitCell') ;

// Generic Undefined command (usually used when a command is under development).
FCKCommands['Undefined']	= new FCKUndefinedCommand() ;

