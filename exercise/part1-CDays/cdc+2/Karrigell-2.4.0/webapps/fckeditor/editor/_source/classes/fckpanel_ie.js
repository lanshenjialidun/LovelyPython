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
 * File Name: fckpanel_ie.js
 * 	FCKPanel Class: this is the IE version of the base class used to implement
 * 	"Panel" classes.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-27 15:55:23
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKPanel = function()
{}

FCKPanel.prototype.Create = function()
{
	// Create the Popup that will hold the panel.
	this._Popup = window.createPopup() ;
	this._Popup.document.createStyleSheet( FCKConfig.SkinPath + 'fck_contextmenu.css' ) ;
	this._Popup.document.oncontextmenu = function() { return false ; }

	// Create the main DIV that is used as the panel base.
	this.PanelDiv = this._Popup.document.createElement('DIV') ;
	this.PanelDiv.className = 'FCK_Panel' ;

	// Put the main DIV inside the Popup.
	this._Popup.document.body.appendChild(this.PanelDiv) ;
	
	// It calls a method that must be defined on classes that inherit the 
	// FCKPanel class.
	if ( this.CreatePanelBody )
		this.CreatePanelBody( this._Popup.document, this.PanelDiv ) ;
	
	this._Popup.document.close() ;
	
	this.Created = true ;
}

FCKPanel.prototype.Show = function( panelX, panelY )
{
	if ( ! this.Created )
		this.Create() ;

	// The offsetWidth and offsetHeight properties are not available if the 
	// element is not visible. So we must "show" the popup with no size to
	// be able to use that values in the second call.
	this._Popup.show( panelX, panelY, 0, 0 ) ;

	// Second call: Show the Popup at the specified location.
	this._Popup.show( panelX, panelY, this.PanelDiv.offsetWidth, this.PanelDiv.offsetHeight ) ;
}

FCKPanel.prototype.Hide = function()
{
	if ( this._Popup )
		this._Popup.hide() ;
}