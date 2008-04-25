FCKToolbarPanelButton.prototype.HandleOnClick = function( panelButton, ev )
{
	// The X and Y position of the Panel must be calculated based on
	// the button position.
	var e = panelButton.DOMDiv ;

	// Get the DIV and the editor frame positions.
	var oDivCoords = FCKTools.GetElementPosition( e ) ;
	var oFrmCoords = FCKTools.GetElementPosition( window.frameElement ) ;

	// Get the actual window (IFRAME) position on screen.
	var iPanelX = oDivCoords.X + oFrmCoords.X ;
	var iPanelY = oDivCoords.Y + oFrmCoords.Y + e.offsetHeight ;		// The button height is added so the panel is aligned on its base line.

	panelButton.Command.Execute(iPanelX,iPanelY) ;
}