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
 * File Name: fckdialog_ie.js
 * 	Dialog windows operations. (IE specific implementations)
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-05-31 23:07:50
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

FCKDialog.Show = function( dialogInfo, dialogName, pageUrl, dialogWidth, dialogHeight )
{
	window.showModalDialog( pageUrl, dialogInfo, "dialogWidth:" + dialogWidth + "px;dialogHeight:" + dialogHeight + "px;help:no;scroll:no;status:no") ;
}

