document.write('<span id="hour_entry" style="position:absolute"></span>\n')
document.write('<style type="text/css">\n')
document.write('span.hour { height: 5; background-color: red; }\n')
document.write('a.minute { font-size:10; text-decoration:none }\n')
document.write('a.minute:hover { background-color: #BBB }\n')
document.write('</style>\n')

function hourShow(elt)
{
  f_top = 0
  f_left = 0
  x = elt
  while (x.offsetParent != undefined)
  {
   f_top += x.offsetTop
   f_left += x.offsetLeft
   x = x.offsetParent
  }
  with (document.getElementById("hour_entry").style)
  { 
  	top = f_top + 20
    left = f_left
    backgroundColor = "#DDD"
   }
   v = elt.value.split(":")
   if (v.length == 1) { v.push("00");v.push("00") }
   else if (v.length == 2) { v.push("00") }
   else if (v.length > 3) { v = new Array(v[0],v[1],v[2]) }
   
   ch = '<form name="hour_entry" action="javascript:update_hour('+"'"+elt.name+"'"+')">'
   ch += '<table>'
   ch += '<tr><td><table width="100%"><tr><td>'
   for (i=0;i<25;i++)
   { ch += '<a class="minute" href="javascript:sel('+"'hour',"+i+')">'+i+'</a> '
     if (i==11) { ch +='</td></tr><tr><td>' }
   }
   ch += '</td></tr></table>'
   ch += '</td><td><input id="hour" size="2" value="'+v[0]+'"></td></tr>'
   ch += '<tr><td>'
   for (i=0;i<60;i=i+5)
   { ch += '<a class="minute" href="javascript:sel('+"'minute',"+i+')">'+i+'</a> ' }
   ch += '</td><td><input id="minute" size="2" value="'+v[1]+'"></td></tr>'
   ch += '<tr><td>'
   for (i=0;i<60;i=i+5)
   { ch += '<a class="minute" href="javascript:sel('+"'second',"+i+')">'+i+'</a> ' }
   ch += '</td><td><input id="second" size="2" value="'+v[2]+'"></td></tr>'
   ch += '<td><input type="submit" value="Ok">'
   ch += '</tr></table>'
   ch += '</form>'

   document.getElementById("hour_entry").innerHTML=ch
}

function sel(elt_id,h)
{ document.getElementById(elt_id).value = h
}

function update_hour(elt_id)
{
 x = document.forms["hour_entry"].elements
 ch = ''

 for (i=0;i<x.length-1;i++)
 { if (i != 0) { ch += ":" }
   ch += x[i].value
 }
 document.getElementById(elt_id).value = ch
 document.getElementById("hour_entry").innerHTML = ""
}

function hourHide(elt)
{
 //document.getElementById("hour_entry").innerHTML = ""
}