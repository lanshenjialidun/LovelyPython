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
 * File Name: fck_last.js
 * 	These are the last script lines executed in the editor loading process.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-05-31 23:07:49
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

// This is the last file loaded to complete the editor initialization and activation

// Activate pasting operations.
if ( FCKConfig.ForcePasteAsPlainText )
	FCK.Events.AttachEvent( "OnPaste", FCK.Paste ) ;

// Load the Toolbar
FCKToolbarSet.Name = FCKURLParams['Toolbar'] || 'Default' ;
FCKToolbarSet.Load( FCKToolbarSet.Name ) ;
FCKToolbarSet.Restart() ;

FCK.AttachToOnSelectionChange( FCKToolbarSet.RefreshItemsState ) ;

// Set some object references to the editor instance object (FCK).
FCK.Config		= FCKConfig ;
FCK.ToolbarSet	= FCKToolbarSet ;

FCK.SetStatus( FCK_STATUS_COMPLETE ) ;

// Call the special "FCKeditor_OnComplete" function that should be present in 
// the HTML page where the editor is located.
if ( typeof( window.parent.FCKeditor_OnComplete ) == 'function' )
	window.parent.FCKeditor_OnComplete( FCK ) ;
