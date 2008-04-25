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
 * File Name: fckxhtml.js
 * 	Defines the FCKXHtml object, responsible for the XHTML operations.
 * 
 * Version:  2.0 Beta 2
 * Modified: 2004-06-18 01:08:15
 * 
 * File Authors:
 * 		Frederico Caldeira Knabben (fredck@fckeditor.net)
 */

var FCKXHtml = new Object() ;

FCKXHtml.GetXHTML = function( node )
{
	// Create the XML DOMDocument objetc.
	if ( window.ActiveXObject )	// IE
		this.XML = new ActiveXObject( 'Msxml2.DOMDocument' ) ;
	else						// Gecko
		this.XML = document.implementation.createDocument( '', '', null ) ;
	
	// Add a root element that holds all child nodes.
	this.MainNode = this.XML.appendChild( this.XML.createElement( 'XHTML' ) ) ;
	
	// Start recursivelly calling the _AppendNode function.
	this._AppendChildNodes( this.MainNode, node ) ;

	// Get the resulting XHTML as a string.
	var sXHTML = document.all ? this.MainNode.xml : FCKXHtml._GetGeckoNodeXml( this.MainNode ) ;
	
	// Strip the "XHTML" root node.
	return sXHTML.substr( 7, sXHTML.length - 15 )  ;
}

FCKXHtml._GetGeckoNodeXml = function( node )
{
	// Create the XMLSerializer.
	var oSerializer = new XMLSerializer() ;

	// Return the serialized XML as a string.
	return oSerializer.serializeToString( node ) ;
}

FCKXHtml._AppendAttribute = function( xmlNode, attributeName, attributeValue )
{
	// There is a bug in Mozilla that returns the '_moz_dirty' as specified.
	if ( attributeName == '_moz_dirty' )
		return ;

	// Create the attribute.
	var oXmlAtt = this.XML.createAttribute( attributeName ) ;
	
	// XHTML doens't support attribute minimization like "CHECKED". It must be trasformed to cheched="checked".
	if ( typeof( attributeValue ) == 'boolean' && attributeValue == true )
		oXmlAtt.value = attributeName ;
	else
		oXmlAtt.value = attributeValue ;
	
	// Set the attribute in the node.
	xmlNode.attributes.setNamedItem( oXmlAtt ) ;
}

FCKXHtml._AppendChildNodes = function( xmlNode, htmlNode )
{
	// Get all children nodes.
	var oChildren = htmlNode.childNodes ;

	var i = 0 ;
	while ( i < oChildren.length )
	{
		i += this._AppendNode( xmlNode, oChildren[i] ) ;
	}
}

FCKXHtml._AppendNode = function( xmlNode, htmlNode )
{
	var iAddedNodes = 1 ;
	
	switch ( htmlNode.nodeType )
	{
		// Element Node.
		case 1 :
			// Create the Element.
			var sNodeName = htmlNode.nodeName.toLowerCase() ;
			var oNode = xmlNode.appendChild( this.XML.createElement( sNodeName ) ) ;

			// Add all attributes.
			var oAttributes = htmlNode.attributes ;
			for ( var n = 0 ; n < oAttributes.length ; n++ )
			{
				var oAttribute = oAttributes[n] ;
				if ( oAttribute.specified )
				{
					var sAttName	= oAttribute.nodeName.toLowerCase() ;
					var sAttValue	= oAttribute.nodeValue ;

					// The following must be done because of a bug on IE regarding the style
					// attribute. It returns "null" for the nodeValue.
					if ( sAttName == 'style' && document.all )
						sAttValue = htmlNode.style.cssText ;
					
					this._AppendAttribute( oNode, sAttName, sAttValue ) ;
				}
			}
			
			// Proccess the node.
			switch ( sNodeName )
			{
				// "SCRIPT" and "STYLE" must be a CDATA.
				case "script" :
				case "style" :
					oNode.appendChild( this.XML.createCDATASection( htmlNode.text ) ) ;
					break ;
				
				// There is a BUG in IE regarding the ABBR tag.
				case "abbr" :
					if ( document.all )
					{
						var oNextNode = htmlNode.nextSibling ;
						while ( true )
						{
							iAddedNodes++ ;
							if ( oNextNode && oNextNode.nodeName != '/ABBR' )
							{
								this._AppendNode( oNode, oNextNode ) ;
								oNextNode = oNextNode.nextSibling ;
							}
							else
								break ;
						}
						break ;
					}
					
				// IE ignores the "COORDS" attribute so we must add it manually.
				case "area" :
					if ( document.all && ! oNode.attributes.getNamedItem( 'coords' ) )
					{
						var sCoords = htmlNode.getAttribute( 'coords', 2 ) ;
						if ( sCoords && sCoords != '0,0,0' )
							this._AppendAttribute( oNode, 'coords', sCoords ) ;
					}
				
				case "img" :
					// The "ALT" attribute is required for XHTML support.
					if ( ! oNode.attributes.getNamedItem( 'alt' ) )
						this._AppendAttribute( oNode, 'alt', '' ) ;
				
				// Recursivelly call the function.
				default :
					this._AppendChildNodes( oNode, htmlNode ) ;
					break ;
			}
			break ;
		
		// Text Node.
		case 3 :
			xmlNode.appendChild( this.XML.createTextNode( htmlNode.nodeValue ) ) ;
			break ;
		
		// Unknown Node type.
		default :
			xmlNode.appendChild( this.XML.createComment( "Element not supported - Type: " + htmlNode.nodeType + " Name: " + htmlNode.nodeName ) ) ;
			break ;
	}
	
	return iAddedNodes ;
}
