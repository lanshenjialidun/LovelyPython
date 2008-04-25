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
 * File Name: fcklanguagemanager.js
 * 	Defines the FCKLanguageManager object that is used for language 
 * 	operations.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-09-10 01:48:58
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKLanguageManager = new Object() ;

FCKLanguageManager.AvailableLanguages = 
{
	'ar'	: 'Arabic',
	'en'	: 'English',
	'it'	: 'Italian'
}

FCKLanguageManager.GetActiveLanguage = function()
{
	if ( FCKConfig.AutoDetectLanguage )
	{
		// IE accepts "navigator.userLanguage" while Gecko "navigator.language".
		var sUserLang = navigator.language ? navigator.language.toLowerCase() : navigator.userLanguage.toLowerCase() ;

		FCKDebug.Output( 'Navigator Language = ' + sUserLang ) ;
		
		// Some language codes are set in 5 characters, 
		// like "pt-br" for Brasilian Portuguese.
		if ( sUserLang.length >= 5 )
		{
			sUserLang = sUserLang.substr(0,5) ;
			if ( this.AvailableLanguages[sUserLang] ) return sUserLang ;
		}
		
		// If the user's browser is set to, for example, "pt-br" but only the 
		// "pt" language file is available then get that file.
		if ( sUserLang.length >= 2 )
		{
			sUserLang = sUserLang.substr(0,2) ;
			if ( this.AvailableLanguages[sUserLang] ) return sUserLang ;
		}
	}
	
	return FCKConfig.DefaultLanguage ;
}

FCKLanguageManager.TranslateElements = function( targetDocument, tag, propertyToSet )
{
	var aInputs = targetDocument.getElementsByTagName(tag) ;
	for ( var i = 0 ; i < aInputs.length ; i++ )
	{
		if ( aInputs[i].attributes['fckLang'] )
		{
			var s = FCKLang[ aInputs[i].attributes["fckLang"].value ] ;
			eval( 'aInputs[i].' + propertyToSet + ' = s' ) ;
		}
	}
}

FCKLanguageManager.TranslatePage = function( targetDocument )
{
	this.TranslateElements( targetDocument, 'INPUT', 'value' ) ;
	this.TranslateElements( targetDocument, 'SPAN', 'innerHTML' ) ;
	this.TranslateElements( targetDocument, 'OPTION', 'innerHTML' ) ;
}

FCKLanguageManager.ActiveLanguage = new Object() ;
FCKLanguageManager.ActiveLanguage.Code = FCKLanguageManager.GetActiveLanguage() ;
FCKLanguageManager.ActiveLanguage.Name = FCKLanguageManager.AvailableLanguages[ FCKLanguageManager.ActiveLanguage.Code ] ;

FCK.Language = FCKLanguageManager ;


// Load the language file and start the editor.
LoadLanguageFile() ;