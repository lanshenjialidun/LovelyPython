function draw_slider(elt_id,nb)
{
 ch = '<span class="slider">\n'
 ch += '<span style="position:absolute;left:'+(10*nb+5)+'"><input id="slider_'+elt_id+'"></span>'
 for (i=0;i<nb;i++)

 { ch += '<span class="slider" style="top:5;height:20;width:3;left:'+10*i+'" '
 ch += 'onMouseOver="sel_slider(this,'+"'"+'slider_'+elt_id+"',"+i+')"'

 ch += '>&nbsp;</span>' }
 ch += '</span>\n'
 ch += '<span class="slider" style="background-color:#888;top:25;height:5;width='+10*nb+'">&nbsp;</span>'
 return ch
}

function sel_slider(sl,elt_id,v)
{ 
 if (current != null)
 { current.style.backgroundColor = "white"; }
 sl.style.backgroundColor = "blue"
document.getElementById(elt_id).value = v
current = sl
}

function desel_slider(sl)
{ sl.style.backgroundColor = "#888"
}

current = null