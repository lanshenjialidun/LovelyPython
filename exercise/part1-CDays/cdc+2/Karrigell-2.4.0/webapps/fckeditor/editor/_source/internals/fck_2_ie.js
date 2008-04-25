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
 * File Name: fck_2_ie.js
 * 	This is the second part of the "FCK" object creation. This is the main
 * 	object that represents an editor instance.
 * 	(IE specific implementations)
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-02 11:40:29
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

FCK.Paste = function()
{
	if ( FCKConfig.ForcePasteAsPlainText )
	{
		FCK.PasteAsPlainText() ;	
		return false ;
	}
	else if ( FCKConfig.AutoDetectPasteFromWord && FCKBrowserInfo.IsIE55OrMore )
	{
		var sHTML = FCK.GetClipboardHTML() ;
		var re = /<\w[^>]* class="?MsoNormal"?/gi ;
		if ( re.test( sHTML ) )
		{
			if ( confirm( FCKLang["PasteWordConfirm"] ) )
			{
				FCK.CleanAndPaste( sHTML ) ;
				return false ;
			}
		}
	}
	else
		return true ;
}

FCK.PasteAsPlainText = function()
{
	// Get the data available in the clipboard and encodes it in HTML.
	var sText = FCKTools.HTMLEncode( clipboardData.getData("Text") ) ;

	// Replace the carriage returns with <BR>
	sText = sText.replace( /\n/g, '<BR>' ) ;
	
	// Insert the resulting data in the editor.
	this.InsertHtml( sText ) ;	
}

FCK.PasteFromWord = function()
{
	FCK.CleanAndPaste( FCK.GetClipboardHTML() ) ;
}

FCK.InsertHtml = function( html )
{
	FCK.Focus() ;
	var oSel = FCKSelection.Delete() ;
	oSel.createRange().pasteHTML( html ) ; 
	
}

FCK.InsertElement = function( element )
{
	FCK.InsertHtml( element.outerHTML ) ;
}

FCK.GetClipboardHTML = function()
{
	var oDiv = document.getElementById( '___FCKHiddenDiv' ) ;
	
	if ( !oDiv )
	{
		var oDiv = document.createElement( 'DIV' ) ;
		oDiv.id = '___FCKHiddenDiv' ;
		oDiv.style.visibility	= 'hidden' ;
		oDiv.style.overflow		= 'hidden' ;
		oDiv.style.position		= 'absolute' ;
		oDiv.style.width		= 1 ;
		oDiv.style.height		= 1 ;
	
		document.body.appendChild( oDiv ) ;
	}
	
	oDiv.innerHTML = '' ;
	
	var oTextRange = document.body.createTextRange() ;
	oTextRange.moveToElementText( oDiv ) ;
	oTextRange.execCommand( 'Paste' ) ;
	
	var sData = oDiv.innerHTML ;
	oDiv.innerHTML = '' ;
	
	return sData ;
}

FCK.AttachToOnSelectionChange = function( functionPointer )
{
	FCK.EditorDocument.attachEvent( 'onselectionchange', functionPointer ) ;
}

