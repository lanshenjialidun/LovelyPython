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
 * File Name: fckcolorpanel.js
 * 	FCKColorPanel Class: represents a Color Selection panel.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-08-20 22:35:45
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKColorPanel = function( setColorFunction )
{
	// SetColorFunction is the function to be called when the user selects the
	// desired color (from the panel itself or from the "More Colors..." popup.
	this.SetColorFunction = setColorFunction ;
}

// Inherit from FCKPanel.
FCKColorPanel.prototype = new FCKPanel ;

FCKColorPanel.prototype.CreatePanelBody = function( targetDocument, targetDiv )
{
	function CreateSelectionDiv()
	{
		var oDiv = targetDocument.createElement( "DIV" ) ;
		oDiv.className = 'ColorDeselected' ;
		oDiv.onmouseover	= function() { this.className='ColorSelected' ; } ;
		oDiv.onmouseout		= function() { this.className='ColorDeselected' ; } ;
		
		return oDiv ;
	}

	// Create the Table that will hold all colors.
	var oTable = targetDocument.createElement( "TABLE" ) ;
	oTable.cellPadding = 0 ;
	oTable.cellSpacing = 0 ;
	oTable.border = 0 ;

	// Create the Button for the "Automatic" color selection.
	var oDiv = CreateSelectionDiv() ;
	oDiv.innerHTML = 
		'<table cellspacing="0" cellpadding="0" width="100%" border="0">\
			<tr>\
				<td><div class="ColorBoxBorder"><div class="ColorBox" style="background-color: #000000"></div></div></td>\
				<td nowrap width="100%" align="center" unselectable="on">Automatic</td>\
			</tr>\
		</table>' ;

	oDiv.Panel = this ;
	oDiv.onclick = function()
	{
		this.className = 'ColorDeselected' ;
		this.Panel.SetColorFunction( '' ) ;
		this.Panel.Hide() ;
	}

	var oCell = oTable.insertRow(-1).insertCell(-1) ;
	oCell.colSpan = 8 ;
	oCell.appendChild( oDiv ) ;

	// Create an array of colors based on the configuration file.
	var aColors = FCKConfig.FontColors.split(',') ;

	// Create the colors table based on the array.
	var iCounter = 0 ;
	while ( iCounter < aColors.length )
	{
		var oRow = oTable.insertRow(-1) ;
		
		for ( var i = 0 ; i < 8 && iCounter < aColors.length ; i++, iCounter++ )
		{
			var oDiv = CreateSelectionDiv() ;
			oDiv.Color = aColors[iCounter] ;
			oDiv.innerHTML = '<div class="ColorBoxBorder"><div class="ColorBox" style="background-color: #' + aColors[iCounter] + '"></div></div>' ;

			oDiv.Panel = this ;
			oDiv.onclick = function()
			{
				this.className = 'ColorDeselected' ;
				this.Panel.SetColorFunction( '#' + this.Color ) ;
				this.Panel.Hide() ;
			}
		
			oCell = oRow.insertCell(-1) ;
			oCell.appendChild( oDiv ) ;
		}
	}

	// Create the Row and the Cell for the "More Colors..." button.
	var oDiv = CreateSelectionDiv() ;
	oDiv.innerHTML = '<table width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td nowrap align="center">More Colors...</td></tr></table>' ;

	oDiv.Panel = this ;
	oDiv.onclick = function()
	{
		this.className = 'ColorDeselected' ;
		this.Panel.Hide() ;
		FCKDialog.OpenDialog( 'FCKDialog_Color', 'Select a Color', 'dialog/fck_colorselector.html', 400, 330, this.Panel.SetColorFunction ) ;
	}

	var oCell = oTable.insertRow(-1).insertCell(-1) ;
	oCell.colSpan = 8 ;
	oCell.appendChild( oDiv ) ;

	// Append the resulting table to the target DIV.
	targetDiv.appendChild( oTable ) ;
}