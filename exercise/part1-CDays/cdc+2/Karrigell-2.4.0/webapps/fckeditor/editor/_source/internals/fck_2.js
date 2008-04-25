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
 * File Name: fck_2.js
 * 	This is the second part of the "FCK" object creation. This is the main
 * 	object that represents an editor instance.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-07 01:11:37
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

FCK.ExecuteNamedCommand = function( commandName, commandParameter )
{
	FCK.Focus() ;
	FCK.EditorDocument.execCommand( commandName, false, commandParameter ) ; 
	FCK.Events.FireEvent( 'OnSelectionChange' ) ;
}

FCK.GetNamedCommandState = function( commandName )
{
	try
	{
		if ( !FCK.EditorDocument.queryCommandEnabled( commandName ) )
			return FCK_TRISTATE_DISABLED ;
		else
			return FCK.EditorDocument.queryCommandState( commandName ) ? FCK_TRISTATE_ON : FCK_TRISTATE_OFF ;
	}
	catch ( e )
	{
		return FCK_TRISTATE_OFF ;
	}
}

FCK.GetNamedCommandValue = function( commandName )
{
	var sValue = '' ;
	var eState = FCK.GetNamedCommandState( commandName ) ;
	
	if ( eState == FCK_TRISTATE_DISABLED ) 
		return null ;
	
	try
	{
		sValue = this.EditorDocument.queryCommandValue( commandName ) ;
	}
	catch(e) {}
	
	return sValue ? sValue : '' ;
}

FCK.CreateLink = function( url )
{	
	if ( url.length == 0 )
		FCK.ExecuteNamedCommand( 'Unlink' ) ;
	else
	{
		FCK.ExecuteNamedCommand( 'CreateLink', "javascript:void(0);/*fckeditortemplink*/" ) ;

		var oLinks = this.EditorDocument.links ;
		for ( i = 0 ; i < oLinks.length ; i++ )
		{
			if ( oLinks[i].href == "javascript:void(0);/*fckeditortemplink*/" )
			{
				oLinks[i].href = url ;
				return oLinks[i] ;
			}
		}
	}
}

FCK.CleanAndPaste = function( html )
{
	// Remove all SPAN tags
	html = html.replace(/<\/?SPAN[^>]*>/gi, "" );
	// Remove Class attributes
	html = html.replace(/<(\w[^>]*) class=([^ |>]*)([^>]*)/gi, "<$1$3") ;
	// Remove Style attributes
	html = html.replace(/<(\w[^>]*) style="([^"]*)"([^>]*)/gi, "<$1$3") ;
	// Remove Lang attributes
	html = html.replace(/<(\w[^>]*) lang=([^ |>]*)([^>]*)/gi, "<$1$3") ;
	// Remove XML elements and declarations
	html = html.replace(/<\\?\?xml[^>]*>/gi, "") ;
	// Remove Tags with XML namespace declarations: <o:p></o:p>
	html = html.replace(/<\/?\w+:[^>]*>/gi, "") ;
	// Replace the &nbsp;
	html = html.replace(/&nbsp;/, " " );
	// Transform <P> to <DIV>
	var re = new RegExp("(<P)([^>]*>.*?)(<\/P>)","gi") ;	// Different because of a IE 5.0 error
	html = html.replace( re, "<div$2</div>" ) ;
	
	FCK.InsertHtml( html ) ;
}

FCK.Preview = function()
{
	var oWindow = window.open( '', null, 'toolbar=yes,location=yes,status=yes,menubar=yes,scrollbars=yes,resizable=yes' ) ;
	
	oWindow.document.write( FCK.GetHTML() );
	oWindow.document.close();
		
	// TODO: The CSS of the editor area must be configurable.
	// oWindow.document.createStyleSheet( config.EditorAreaCSS );
}

FCK.SwitchEditMode = function()
{
	// Check if the actual mode is WYSIWYG.
	var bWYSIWYG = ( FCK.EditMode == FCK_EDITMODE_WYSIWYG ) ;
	
	// Display/Hide the TRs.
	document.getElementById('eWysiwyg').style.display	= bWYSIWYG ? "none" : "" ;
	document.getElementById('eSource').style.display	= bWYSIWYG ? "" : "none" ;

	// Update the HTML in the view output to show.
	if ( bWYSIWYG )
		document.getElementById('eSourceField').value = ( FCKConfig.EnableXHTML && FCKConfig.EnableSourceXHTML ? FCK.GetXHTML() : FCK.GetHTML() ) ;
	else
		FCK.SetHTML( FCK.GetHTML(), true ) ;

	// Updates the actual mode status.
	FCK.EditMode = bWYSIWYG ? FCK_EDITMODE_SOURCE : FCK_EDITMODE_WYSIWYG ;
	
	// Set the Focus.
	FCK.Focus() ;
	
	// Update the toolbar.
	FCKToolbarSet.RefreshItemsState() ;
}

