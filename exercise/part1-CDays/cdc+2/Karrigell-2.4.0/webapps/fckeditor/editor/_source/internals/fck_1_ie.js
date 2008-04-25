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
 * File Name: fck_1_ie.js
 * 	This is the first part of the "FCK" object creation. This is the main
 * 	object that represents an editor instance.
 * 	(IE specific implementations)
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-30 22:48:10
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

FCK.Description = "FCKeditor for Internet Explorer 5.5+" ;

FCK.StartEditor = function()
{
	// Get the editor's window and document (DOM)
	this.EditorWindow	= window.frames[ 'eEditorArea' ] ;
	this.EditorDocument	= this.EditorWindow.document ;
	
	// Set the editor's startup contents
	this.SetHTML( FCKTools.GetLinkedFieldValue() ) ;
	
	// Attach the editor to the form onsubmit event
	FCKTools.AttachToLinkedFieldFormSubmit( this.UpdateLinkedField ) ;

	// Set the focus to the editable area when clicking in the document area.
	// TODO: The cursor must be positioned at the end.
	this.EditorDocument.onmousedown = this.EditorDocument.onmouseup = function()
	{
		FCK.Focus() ;
		
		FCK.EditorWindow.event.cancelBubble	= true ;
		FCK.EditorWindow.event.returnValue	= false ;
	}
	
	// Intercept pasting operations
	this.EditorDocument.body.onpaste = function()
	{
		if ( FCK.Status == FCK_STATUS_COMPLETE )
			return FCK.Events.FireEvent( "OnPaste" ) ;
		else
			return false ;
	}
	
	// Disable Right-Click and shows the context menu.
	this.EditorDocument.oncontextmenu = function()
	{
		var e = this.parentWindow.event ;
		FCK.ShowContextMenu( e.screenX, e.screenY ) ;
		return false ;
	}
	
	// Intercept cursor movements
	this.EditorDocument.onselectionchange = function()
	{
		FCK.Events.FireEvent( "OnSelectionChange" ) ;
	}

	//Enable editing
	this.EditorDocument.body.contentEditable = true ;

	this.SetStatus( FCK_STATUS_ACTIVE ) ;
}

FCK.Focus = function()
{
	if ( FCK.EditMode == FCK_EDITMODE_WYSIWYG )
		FCK.EditorDocument.body.focus() ;
	else
		document.getElementById('eSource').focus() ;
}

