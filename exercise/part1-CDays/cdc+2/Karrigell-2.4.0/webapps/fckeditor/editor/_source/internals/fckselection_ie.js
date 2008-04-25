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
 * File Name: fckselection_ie.js
 * 	Active selection functions. (IE specific implementation)
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-02 01:13:51
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

// Retrieves the selected element (if any), just in the case that a single 
// element is selected.
FCKSelection.GetSelectedElement = function()
{
	var oRange = FCK.EditorDocument.selection.createRange() ;
	if ( FCK.EditorDocument.selection.type != 'Text' && oRange.length == 1)
	{
		return oRange.item(0) ;
	}
}

FCKSelection.MoveToNode = function( node )
{
	FCK.EditorDocument.selection.empty() ;
	var oRange = FCK.EditorDocument.selection.createRange() ;
	oRange.moveToElementText( node ) ;
	oRange.select() ;
}

// The "nodeTagName" parameter must be Upper Case.
FCKSelection.HasAncestorNode = function( nodeTagName )
{
	var oContainer ;
	
	if ( FCK.EditorDocument.selection.type == "Control" )
	{
		oContainer = this.GetSelectedElement() ;
	}
	else
	{
		var oRange  = FCK.EditorDocument.selection.createRange() ;
		oContainer = oRange.parentElement() ;
	}

	while ( oContainer )
	{
		if ( oContainer.tagName == nodeTagName ) return true ;
		oContainer = oContainer.parentNode ;
	}

	return false ;
}

// The "nodeTagName" parameter must be Upper Case.
FCKSelection.MoveToAncestorNode = function( nodeTagName )
{
	var oNode ;
	
	if ( FCK.EditorDocument.selection.type == "Control" )
	{
		var oRange = FCK.EditorDocument.selection.createRange() ;
		for ( i = 0 ; i < oRange.length ; i++ )
		{
			if (oRange(i).parentNode)
			{
				oNode = oRange(i).parentNode ;
				break ;
			}
		}
	}
	else
	{
		var oRange  = FCK.EditorDocument.selection.createRange() ;
		oNode = oRange.parentElement() ;
	}

	while ( oNode && oNode.nodeName != nodeTagName )
		oNode = oNode.parentNode ;
	
	return oNode ;
}

FCKSelection.Delete = function()
{
	// Gets the actual selection.
	var oSel = FCK.EditorDocument.selection ;
	
	// Deletes the actual selection contents.
	if ( oSel.type.toLowerCase() != "none" )
	{
		oSel.clear() ;
	}
	
	return oSel ;
}