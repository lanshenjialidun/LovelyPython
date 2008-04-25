FCKToolbarPanelButton.prototype.HandleOnClick = function( panelButton, ev )
{
	// The X and Y position of the Panel must be calculated based on
	// the button position.
	var e = panelButton.DOMDiv ;

	// Get the DIV position.
	var oDivCoords = FCKTools.GetElementPosition( e ) ;

	// Get the actual window (IFRAME) position on screen.
	var iPanX = oDivCoords.X + window.screenLeft ;
	var iPanY = oDivCoords.Y + window.screenTop + e.offsetHeight + 1 ;		// The button height is added so the panel is aligned on its base line.

	panelButton.Command.Execute(iPanX,iPanY) ;
}