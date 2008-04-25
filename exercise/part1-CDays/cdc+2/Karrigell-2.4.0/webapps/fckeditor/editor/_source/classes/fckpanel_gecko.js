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
 * File Name: fckpanel_gecko.js
 * 	FCKPanel Class: this is the IE version of the base class used to implement
 * 	"Panel" classes.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-20 16:32:56
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

// The Panel Styles where already liaded in the parent window by the Context Menu scripts.
// (They are included in the fck_contextmenu CSS)

var FCKPanel = function()
{}

FCKPanel.prototype.Create = function()
{
	// Create the main DIV that is used as the panel base.
	this.PanelDiv = window.parent.document.createElement('DIV') ;
	this.PanelDiv.style.visibility	= 'hidden' ;
	this.PanelDiv.className = 'FCK_Panel' ;
	this.PanelDiv.style.zIndex = 10000 ;
	this.PanelDiv.oncontextmenu = function() { return false ; }

	// Put the main DIV inside the parent document.
	window.parent.document.body.appendChild( this.PanelDiv );
	
	// It calls a method that must be defined on classes that inherit the 
	// FCKPanel class.
	if ( this.CreatePanelBody )
		this.CreatePanelBody( window.parent.document, this.PanelDiv ) ;

	this.Created = true ;
}

FCKPanel.prototype.Show = function( panelX, panelY )
{
	if ( ! this.Created )
		this.Create() ;

	// Set the context menu DIV in the specified location.
	this.PanelDiv.style.left	= panelX + 'px' ;
	this.PanelDiv.style.top		= panelY + 'px' ;

	// Watch the "OnClick" event for all windows to close the Context Menu.
	var oActualWindow = FCK.EditorWindow ;
	while ( oActualWindow )
	{
		oActualWindow.document.addEventListener( 'click', this._OnDocumentClick, false ) ;
		if ( oActualWindow != oActualWindow.parent )
			oActualWindow = oActualWindow.parent ;
		else if ( oActualWindow.opener == null ) 
			oActualWindow = oActualWindow.opener ;
		else
			break ;
	}

	// Show it.
	this.PanelDiv.style.visibility	= '' ;
	FCK.ActivePanel = this ;
}

FCKPanel.prototype._OnDocumentClick = function( event )
{
	if ( ! FCK.ActivePanel ) return ;
	
	var e = event.target ;
	while ( e )
	{
		if ( e == FCK.ActivePanel.PanelDiv ) return ;
		e = e.parentNode ;
	}
	FCK.ActivePanel.Hide() ;
}

FCKPanel.prototype.Hide = function()
{
	this.PanelDiv.style.visibility = 'hidden' ;
	this.PanelDiv.style.left = this.PanelDiv.style.top = '1px' ;
	
	delete FCK.ActivePanel ;
}