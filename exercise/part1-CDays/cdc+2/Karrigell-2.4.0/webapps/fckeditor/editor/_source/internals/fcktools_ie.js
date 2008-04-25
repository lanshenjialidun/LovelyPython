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
 * File Name: fcktools_ie.js
 * 	Utility functions. (IE version).
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-05-31 23:07:50
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

// Appends a CSS file to a document.
FCKTools.AppendStyleSheet = function( documentElement, cssFileUrl )
{
	documentElement.createStyleSheet( cssFileUrl ) ;
}

// Removes all attributes and values from the element.
FCKTools.ClearElementAttributes = function( element )
{
	element.clearAttributes() ;
}

FCKTools.GetAllChildrenIds = function( parentElement )
{
	var aIds = new Array() ;
	for ( var i = 0 ; i < parentElement.all.length ; i++ )
	{
		var sId = parentElement.all[i].id ;
		if ( sId && sId.length > 0 )
			aIds[ aIds.length ] = sId ;
	}
	return aIds ;
}