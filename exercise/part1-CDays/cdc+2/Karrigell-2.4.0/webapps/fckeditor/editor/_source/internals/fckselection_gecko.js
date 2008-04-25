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
 * File Name: fckselection_gecko.js
 * 	Active selection functions. (Gecko specific implementation)
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-02 01:13:50
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

// Retrieves the selected element (if any), just in the case that a single 
// element is selected.
FCKSelection.GetSelectedElement = function()
{
	var oSel = FCK.EditorWindow.getSelection() ;
	if ( oSel.rangeCount == 1 )
	{
		var oRange = oSel.getRangeAt(0) ;
		if ( oRange.startContainer == oRange.endContainer && (oRange.endOffset - oRange.startOffset) == 1 )
			return oSel.anchorNode.childNodes[ oSel.anchorOffset ] ;
	}
}

FCKSelection.MoveToNode = function( node )
{
	var oSel = FCK.EditorWindow.getSelection() ;

	for ( i = oSel.rangeCount - 1 ; i >= 0 ; i-- )
	{
		if ( i == 0 )
			oSel.getRangeAt(i).selectNodeContents( node ) ;
		else
			oSel.removeRange( oSel.getRangeAt(i) ) ;
	}
}

// The "nodeTagName" parameter must be Upper Case.
FCKSelection.HasAncestorNode = function( nodeTagName )
{
	var oContainer = this.GetSelectedElement() ;
	if ( ! oContainer && FCK.EditorWindow )
	{
		try		{ oContainer = FCK.EditorWindow.getSelection().getRangeAt(0).startContainer ; }
		catch(e){}
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
	
	var oContainer = this.GetSelectedElement() ;
	if ( ! oContainer )
		oContainer = FCK.EditorWindow.getSelection().getRangeAt(0).startContainer ;

	while ( oContainer )
	{
		if ( oContainer.tagName == nodeTagName ) return oContainer ;
		oContainer = oContainer.parentNode ;
	}
}

FCKSelection.Delete = function()
{
	// Gets the actual selection.
	var oSel = FCK.EditorWindow.getSelection() ;

	// Deletes the actual selection contents.
	for ( var i = 0 ; i < oSel.rangeCount ; i++ )
	{
		oSel.getRangeAt(i).deleteContents() ;
	}
	
	return oSel ;
}