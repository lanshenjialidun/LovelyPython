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
 * File Name: fckconfig.js
 * 	Creates and initializes the FCKConfig object.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-05-31 23:07:49
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKConfig = new Object() ;

// Editor Base Path
if ( document.location.protocol == 'file:' )
{
	FCKConfig.BasePath = document.location.pathname.substr(1) ;
	FCKConfig.BasePath = FCKConfig.BasePath.replace( /\\/gi, '/' ) ;
	FCKConfig.BasePath = 'file://' + FCKConfig.BasePath.substring(0,FCKConfig.BasePath.lastIndexOf('/')+1) ;
}
else
	FCKConfig.BasePath = document.location.pathname.substring(0,document.location.pathname.lastIndexOf('/')+1) ;

// Override the actual configuration values with the values passed throw the 
// hidden field "<InstanceName>___Config".
FCKConfig.LoadHiddenField = function()
{
	// Get the hidden field.
	var oConfigField = window.parent.document.getElementById( FCK.Name + '___Config' ) ;
	
	// Do nothing if the config field was not defined.
	if ( ! oConfigField ) return ;

	var aCouples = oConfigField.value.split('&') ;

	for ( var i = 0 ; i < aCouples.length ; i++ )
	{
		var aConfig = aCouples[i].split('=') ;
		var sConfigName  = aConfig[0] ;
		var sConfigValue = aConfig[1] ;

		if ( sConfigValue == "true" )			// If it is a boolean TRUE.
			FCKConfig[sConfigName] = true ;
		else if ( sConfigValue == "false" )		// If it is a boolean FALSE.
			FCKConfig[sConfigName] = false ;
		else if ( ! isNaN(sConfigValue) )		// If it is a number.
			FCKConfig[sConfigName] = parseInt( sConfigValue ) ;
		else									// In any other case it is a string.
			FCKConfig[sConfigName] = sConfigValue ;
	}
}