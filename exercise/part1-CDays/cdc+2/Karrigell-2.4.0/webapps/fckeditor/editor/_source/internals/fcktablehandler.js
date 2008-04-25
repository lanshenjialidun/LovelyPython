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
 * File Name: fcktablehandler.js
 * 	Manage table operations.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-07 00:42:30
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKTableHandler = new Object() ;

FCKTableHandler.InsertRow = function()
{
	// Get the row where the selection is placed in.	
	var oRow = FCKSelection.MoveToAncestorNode("TR") ;
	if ( !oRow ) return ;

	// Create a clone of the row.
	var oNewRow = oRow.cloneNode( true ) ;

	// Insert the new row (copy) before of it.
	oRow.parentNode.insertBefore( oNewRow, oRow ) ;

	// Clean the row (it seems that the new row has been added after it).
	FCKTableHandler.ClearRow( oRow ) ;
}

FCKTableHandler.DeleteRows = function( row )
{
	// If no row has been passed as a parameer,
	// then get the row where the selection is placed in.	
	if ( !row )
		row = FCKSelection.MoveToAncestorNode("TR") ;
	if ( !row ) return ;

	// Get the row's table.	
	var oTable = FCKTools.GetElementAscensor( row, 'TABLE' ) ;

	// If just one row is available then delete the entire table.
	if ( oTable.rows.length == 1 ) 
	{
		FCKTableHandler.DeleteTable( oTable ) ;
		return ;
	}

	// Delete the row.
	row.parentNode.removeChild( row ) ;
}

FCKTableHandler.DeleteTable = function( table )
{
	// If no table has been passed as a parameer,
	// then get the table where the selection is placed in.	
	if ( !table )
		table = FCKSelection.MoveToAncestorNode("TABLE") ;
	if ( !table ) return ;

	// Delete the table.
	table.parentNode.removeChild( table ) ;
}

FCKTableHandler.InsertColumn = function()
{
	// Get the cell where the selection is placed in.
	var oCell = FCKSelection.MoveToAncestorNode("TD") ;
	if ( !oCell ) return ;
	
	// Get the cell's table.
	var oTable = FCKTools.GetElementAscensor( oCell, 'TABLE' ) ;

	// Get the index of the column to be created (based on the cell).
	var iIndex = oCell.cellIndex + 1 ;

	// Loop throw all rows available in the table.
	for ( var i = 0 ; i < oTable.rows.length ; i++ )
	{
		// Get the row.
		var oRow = oTable.rows[i] ;
	
		// If the row doens't have enought cells, ignore it.
		if ( oRow.cells.length < iIndex )
			continue ;
		
		// Create the new cell element to be added.
		oCell = FCK.EditorDocument.createElement('TD') ;
		oCell.innerHTML = '&nbsp;' ;
		
		// Get the cell that is placed in the new cell place.
		var oBaseCell = oRow.cells[iIndex] ;

		// If the cell is available (we are not in the last cell of the row).
		if ( oBaseCell )
		{
			// Insert the new cell just before of it.
			oRow.insertBefore( oCell, oBaseCell ) ;
		}
		else
		{
			// Append the cell at the end of the row.
			oRow.appendChild( oCell ) ;
		}
	}
}

FCKTableHandler.DeleteColumns = function()
{
	// Get the cell where the selection is placed in.
	var oCell = FCKSelection.MoveToAncestorNode("TD") ;
	if ( !oCell ) return ;
	
	// Get the cell's table.	
	var oTable = FCKTools.GetElementAscensor( oCell, 'TABLE' ) ;

	// Get the cell index.
	var iIndex = oCell.cellIndex ;

	// Loop throw all rows (from down to up, because it's possible that some
	// rows will be deleted).
	for ( var i = oTable.rows.length - 1 ; i >= 0 ; i-- )
	{
		// Get the row.
		var oRow = oTable.rows[i] ;
		
		// If the cell to be removed is the first one and the row has just one cell.
		if ( iIndex == 0 && oRow.cells.length == 1 )
		{
			// Remove the entire row.
			FCKTableHandler.DeleteRows( oRow ) ;
			continue ;
		}
		
		// If the cell to be removed exists the delete it.
		if ( oRow.cells[iIndex] )
			oRow.removeChild( oRow.cells[iIndex] ) ;
	}
}

FCKTableHandler.InsertCell = function()
{
	// Get the cell where the selection is placed in.
	var oCell = FCKSelection.MoveToAncestorNode("TD") ;
	if ( !oCell ) return ;

	// Create the new cell element to be added.
	var oNewCell = FCK.EditorDocument.createElement("TD");
	oNewCell.innerHTML = "&nbsp;" ;

	// If it is the last cell in the row.
	if ( oCell.cellIndex == oCell.parentNode.cells.lenght - 1 )
	{
		// Add the new cell at the end of the row.
		oCell.parentNode.appendChild( oNewCell ) ;
	}
	else
	{
		// Add the new cell before the next cell (after the active one).
		oCell.parentNode.insertBefore( oNewCell, oCell.nextSibling ) ;
	}
}

FCKTableHandler.DeleteCell = function( cell )
{
	// If this is the last cell in the row.
	if ( cell.parentNode.cells.length == 1 )
	{
		// Delete the entire row.
		FCKTableHandler.DeleteRows( FCKTools.GetElementAscensor( cell, 'TR' ) ) ;
		return ;
	}

	// Delete the cell from the row.
	cell.parentNode.removeChild( cell ) ;
}

FCKTableHandler.DeleteCells = function()
{
	var aCells = FCKTableHandler.GetSelectedCells() ;
	
	for ( var i = aCells.length - 1 ; i >= 0  ; i-- )
	{
		FCKTableHandler.DeleteCell( aCells[i] ) ;
	}
}

FCKTableHandler.MergeCells = function()
{
	alert( 'Command not implemented.' ) ;
}

FCKTableHandler.SplitCell = function()
{
	alert( 'Command not implemented.' ) ;
}

FCKTableHandler.ClearRow = function( tr )
{
	// Get the array of row's cells.
	var aCells = tr.cells ;

	// Replace the contents of each cell with "nbsp;".
	for ( var i = 0 ; i < aCells.length ; i++ ) 
	{
		aCells[i].innerHTML = '&nbsp;' ;
	}
}