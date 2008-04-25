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
 * File Name: fcktextcolorcommand.js
 * 	FCKTextColorCommand Class: represents the text color comand. It shows the
 * 	color selection panel.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-20 22:49:33
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

// FCKTextColorCommand Contructor
//		type: can be 'ForeColor' or 'BackColor'.
var FCKTextColorCommand = function( type )
{
	this.Name = type == 'ForeColor' ? 'TextColor' : 'BGColor' ;
	this.Type = type ;

	// ### BEGIN: This code should be moved to the Execute method but it doesn't work
	// well if placed there.
	
	this._Panel = new FCKColorPanel( this.SetColor ) ;
	this._Panel.Create() ;
	
	// ### END
}

FCKTextColorCommand.prototype.Execute = function( panelX, panelY )
{
	/* It was commented because it is not working well if placed here.
	   It has been moved to the constructor, but it is not the best solution
	   because the Panel should be created only when called.
	
	// Create the Color Panel if needed.
	if ( ! this._Panel )
	{
		this._Panel = new FCKColorPanel( this.SetColor ) ;
		this._Panel.Create() ;
	}
	*/

	// We must "cache" the actual panel type to be used in the SetColor method.
	FCK._ActiveColorPanelType = this.Type ;

	// Show the Color Panel at the desired position.
	this._Panel.Show( panelX, panelY ) ;
}

FCKTextColorCommand.prototype.SetColor = function( color )
{
	if ( FCK._ActiveColorPanelType == 'ForeColor' )
		FCK.ExecuteNamedCommand( 'ForeColor', color ) ;
	else if ( FCKBrowserInfo.IsGecko )
		FCK.ExecuteNamedCommand( 'hilitecolor', color ) ;
	else
		FCK.ExecuteNamedCommand( 'BackColor', color ) ;
	
	// Delete the "cached" active panel type.
	delete FCK._ActiveColorPanelType ;
}

FCKTextColorCommand.prototype.GetState = function()
{
	return FCK_TRISTATE_OFF ;
}