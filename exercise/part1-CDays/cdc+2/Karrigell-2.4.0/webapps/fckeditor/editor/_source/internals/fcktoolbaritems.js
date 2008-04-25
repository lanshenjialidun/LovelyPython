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
 * File Name: fcktoolbaritems.js
 * 	Toolbar items definitions.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-30 23:24:31
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKToolbarItems = new Object() ;

FCKToolbarItems['Source']		= new FCKToolbarButton( 'Source', 'Source', null, FCK_TOOLBARITEM_ICONTEXT, true ) ;
FCKToolbarItems['Save']			= new FCKToolbarButton( 'Save', null, null, null, true  ) ;
FCKToolbarItems['NewPage']		= new FCKToolbarButton( 'NewPage', null, null, null, true  ) ;
FCKToolbarItems['Preview']		= new FCKToolbarButton( 'Preview', null, null, null, true  ) ;
FCKToolbarItems['About']		= new FCKToolbarButton( 'About', FCKLang.About ) ;

FCKToolbarItems['Cut']			= new FCKToolbarButton( 'Cut', FCKLang.Cut, null, null, true ) ;
FCKToolbarItems['Copy']			= new FCKToolbarButton( 'Copy', FCKLang.Copy, null, null, true ) ;
FCKToolbarItems['Paste']		= new FCKToolbarButton( 'Paste', FCKLang.Paste, null, null, true ) ;
FCKToolbarItems['PasteText']	= new FCKToolbarButton( 'PasteText', FCKLang.PasteText ) ;
FCKToolbarItems['PasteWord']	= new FCKToolbarButton( 'PasteWord', FCKLang.PasteWord ) ;
FCKToolbarItems['Print']		= new FCKToolbarButton( 'Print', null, null, null, true ) ;
FCKToolbarItems['Undo']			= new FCKToolbarButton( 'Undo', null, null, null, true ) ;
FCKToolbarItems['Redo']			= new FCKToolbarButton( 'Redo', null, null, null, true ) ;
FCKToolbarItems['Find']			= new FCKToolbarButton( 'Find', null, null, null, true ) ;
FCKToolbarItems['SelectAll']	= new FCKToolbarButton( 'SelectAll', 'Select All', null, null, true ) ;
FCKToolbarItems['RemoveFormat']	= new FCKToolbarButton( 'RemoveFormat', 'Remove Format' ) ;
FCKToolbarItems['Unlink']		= new FCKToolbarButton( 'Unlink' ) ;

FCKToolbarItems['Bold']			= new FCKToolbarButton( 'Bold' ) ;
FCKToolbarItems['Italic']		= new FCKToolbarButton( 'Italic' ) ;
FCKToolbarItems['Underline']	= new FCKToolbarButton( 'Underline' ) ;
FCKToolbarItems['StrikeThrough']= new FCKToolbarButton( 'StrikeThrough', 'Strike Through' ) ;
FCKToolbarItems['Subscript']	= new FCKToolbarButton( 'Subscript' ) ;
FCKToolbarItems['Superscript']	= new FCKToolbarButton( 'Superscript' ) ;

FCKToolbarItems['OrderedList']	= new FCKToolbarButton( 'InsertOrderedList', 'Ordered List', 'Insert/Remove Ordered List' ) ;
FCKToolbarItems['UnorderedList']= new FCKToolbarButton( 'InsertUnorderedList', 'Unordered List', 'Insert/Remove Unordered List' ) ;
FCKToolbarItems['Outdent']		= new FCKToolbarButton( 'Outdent' ) ;
FCKToolbarItems['Indent']		= new FCKToolbarButton( 'Indent' ) ;

FCKToolbarItems['Link']			= new FCKToolbarButton( 'Link', 'Link', 'Create/Edit Link' ) ;
FCKToolbarItems['Unlink']		= new FCKToolbarButton( 'Unlink', 'Remove Link' ) ;

FCKToolbarItems['Image']		= new FCKToolbarButton( 'Image', 'Image', 'Insert/Edit Image' ) ;
FCKToolbarItems['Table']		= new FCKToolbarButton( 'Table', 'Table', 'Create/Edit Table' ) ;
FCKToolbarItems['SpecialChar']	= new FCKToolbarButton( 'SpecialChar', 'Special Character', 'Insert Special Character' ) ;
FCKToolbarItems['Smiley']		= new FCKToolbarButton( 'Smiley', 'Smiley', 'Insert Smiley' ) ;

FCKToolbarItems['Rule']			= new FCKToolbarButton( 'InsertHorizontalRule', 'Horizontal Rule', 'Insert Horizontal Rule' ) ;

FCKToolbarItems['JustifyLeft']	= new FCKToolbarButton( 'JustifyLeft', 'Align Left' ) ;
FCKToolbarItems['JustifyCenter']= new FCKToolbarButton( 'JustifyCenter', 'Center' ) ;
FCKToolbarItems['JustifyRight']	= new FCKToolbarButton( 'JustifyRight', 'Align Right' ) ;
FCKToolbarItems['JustifyFull']	= new FCKToolbarButton( 'JustifyFull', 'Justify' ) ;

FCKToolbarItems['FontName']		= new FCKToolbarCombo( 'FontName', FCKLang['Font'], FCKConfig.FontNames, FCKConfig.FontNames ) ;
FCKToolbarItems['FontSize']		= new FCKToolbarCombo( 'FontSize', FCKLang['FontSize'], '1;2;3;4;5;6;7', 'xx-small;x-small;small;medium;large;x-large;xx-large' ) ;
FCKToolbarItems['FontFormat']	= new FCKToolbarCombo( 'FontFormat', FCKLang['FontFormat'], '<P>;<DIV>;<H1>;<H2>', 'Normal (P);Normal (DIV);Heading 1;Heading 2' ) ;

FCKToolbarItems['TextColor']	= new FCKToolbarPanelButton( 'TextColor' ) ;
FCKToolbarItems['BGColor']		= new FCKToolbarPanelButton( 'BGColor' ) ;
