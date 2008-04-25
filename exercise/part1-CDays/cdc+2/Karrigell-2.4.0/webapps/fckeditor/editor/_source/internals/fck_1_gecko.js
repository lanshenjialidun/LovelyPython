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
 * File Name: fck_1_gecko.js
 * 	This is the first part of the "FCK" object creation. This is the main
 * 	object that represents an editor instance.
 * 	(Gecko specific implementations)
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-30 22:47:52
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

FCK.Description = "FCKeditor for Gecko Browsers" ;

FCK.StartEditor = function()
{
	// Get the editor's window and document (DOM)
	this.EditorWindow	= window.frames[ 'eEditorArea' ] ;
	this.EditorDocument	= this.EditorWindow.document ;
	
	// Sets the editor's startup contents
	this.SetHTML( FCKTools.GetLinkedFieldValue() ) ;

	// Attach the editor to the form onsubmit event
	FCKTools.AttachToLinkedFieldFormSubmit( this.UpdateLinkedField ) ;

	// Disable Right-Click
	var oOnContextMenu = function( e )
	{
		e.preventDefault() ;
		FCK.ShowContextMenu( e.clientX, e.clientY ) ;
	}
	this.EditorDocument.addEventListener( 'contextmenu', oOnContextMenu, true ) ;

	var oOnKeyDown = function( e )
	{
		if ( e.ctrlKey && !e.shiftKey && !e.altKey )
		{
			// Char 86/118 = V/v
			if ( e.which == 86 || e.which == 118 )
			{
				if ( FCK.Status == FCK_STATUS_COMPLETE )
				{
					if ( !FCK.Events.FireEvent( "OnPaste" ) )
						e.preventDefault() ;
				}
				else
					e.preventDefault() ;
			}
		}
	}
	this.EditorDocument.addEventListener( 'keydown', oOnKeyDown, true ) ;
	
	var oOnSelectionChange = function( e )
	{
		/*
		var bIsDifferent = false ;
		var oActualSel = FCK.EditorWindow.getSelection() ;

		if ( FCK.LastSelection )
		{
			if ( FCK.LastSelection.rangeCount != oActualSel.rangeCount )
			{
				bIsDifferent = true ;
			}
			else
			{
				if ( oActualSel.rangeCount == 1 )
				{
					var oRangeA = oActualSel.getRangeAt(0) ;
					var oRangeB = FCK.LastSelection.getRangeAt(0) ;
					
					FCKDebug.Output( 'collapsed: ' + oRangeA.collapsed ) ;
					if ( oRangeA.collapsed )
					{
						FCKDebug.Output( 'startContainerBranch: ' + oRangeA.startContainerBranch + ' == ' + oRangeB.startContainerBranch ) ;
						FCKDebug.Output( 'Container: ' + oRangeA.startContainer.childNodes[ oRangeA.startOffset ] + ' == ' + oRangeB.commonAncestorContainer.parent ) ;
						if 
						( 
							!oRangeB.collapsed ||
							oRangeA.startContainer.childNodes[ oRangeA.startOffset ] != oRangeB.startContainer.childNodes[ oRangeB.startOffset ] ||
							oRangeA.commonAncestorContainer.parent != oRangeB.commonAncestorContainer.parent )
						{
							bIsDifferent = true ;
						}
					}
					else
					{
						bIsDifferent = true ;
					}
				}
				else
				{
					bIsDifferent == true ;
				}
			}
		}
		else
		{
			bIsDifferent = true ;
		}
		
		FCK.LastSelection = oActualSel ;
		
		FCKDebug.Output( 'bIsDifferent: ' + bIsDifferent ) ;
		
		if ( bIsDifferent )
		{*/
			FCK.Events.FireEvent( "OnSelectionChange" ) ;
		//}
	}
	
	this.EditorDocument.addEventListener( 'mouseup', oOnSelectionChange, false ) ;
	this.EditorDocument.addEventListener( 'keyup', oOnSelectionChange, false ) ;

	this.SetStatus( FCK_STATUS_ACTIVE ) ;
}

FCK.Focus = function()
{
	this.EditorWindow.focus() ;
}

