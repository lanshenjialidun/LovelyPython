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
 * File Name: fck_1.js
 * 	This is the first part of the "FCK" object creation. This is the main
 * 	object that represents an editor instance.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-05 02:19:46
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

FCK.Events	= new FCKEvents( FCK ) ;
FCK.Toolbar	= null ;

FCK.SetStatus = function( newStatus )
{
	this.Status = newStatus ;
	
	if ( newStatus == FCK_STATUS_ACTIVE )
	{
		// Force the focus in the editor.
		if ( FCKConfig.StartupFocus )
			FCK.Focus() ;
	
	
		
		if ( FCKBrowserInfo.IsIE )
			FCKScriptLoader.AddScript( 'js/fckeditorcode_ie_2.js' ) ;
		else
			FCKScriptLoader.AddScript( 'js/fckeditorcode_gecko_2.js' ) ;
			
	}
	
	this.Events.FireEvent( 'OnStatusChange', newStatus ) ;
	if ( this.OnStatusChange ) this.OnStatusChange( newStatus ) ;
	
}

FCK.SetHTML = function( html, forceWYSIWYG )
{
	if ( forceWYSIWYG || FCK.EditMode == FCK_EDITMODE_WYSIWYG )
	{
		// On Gecko we must disable editing before setting the innerHTML.
		if ( FCKBrowserInfo.IsGecko )
			FCK.EditorDocument.designMode = "off" ;
			
		this.EditorDocument.body.innerHTML = html ;
	
		if ( FCKBrowserInfo.IsGecko )
		{
			// On Gecko we must set the desingMode on again after setting the innerHTML.
			FCK.EditorDocument.designMode = "on" ;
			
			// Tell Gecko to use or not the <SPAN> tag for the bold, italic and underline.
			FCK.EditorDocument.execCommand( "useCSS", false, !FCKConfig.GeckoUseSPAN ) ;
		}
	}
	else
		document.getElementById('eSourceField').value = html ;
}

FCK.GetHTML = function()
{
	if ( FCK.EditMode == FCK_EDITMODE_WYSIWYG )
		return this.EditorDocument.body.innerHTML ;
	else
		return document.getElementById('eSourceField').value ;
}

FCK.GetXHTML = function()
{
	var bSource = ( FCK.EditMode == FCK_EDITMODE_SOURCE ) ;
	
	if ( bSource )
		this.SwitchEditMode() ;
	
	var sXHTML = FCKXHtml.GetXHTML( this.EditorDocument.body ) ;
	
	if ( bSource )
		this.SwitchEditMode() ;
		
	return sXHTML ;
}

FCK.UpdateLinkedField = function()
{
	if ( FCKConfig.EnableXHTML )
		FCKTools.SetLinkedFieldValue( FCK.GetXHTML() ) ;
	else
		FCKTools.SetLinkedFieldValue( FCK.GetHTML() ) ;
}

FCK.ShowContextMenu = function( x, y )
{
	if ( this.Status != FCK_STATUS_COMPLETE ) 
		return ;
		
	FCKContextMenu.Show( x, y ) ;
	this.Events.FireEvent( "OnContextMenu" ) ;
}

