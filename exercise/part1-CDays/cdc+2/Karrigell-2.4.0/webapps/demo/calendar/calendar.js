function new_entry(elt)
{
hour = elt.id.substr(4)
ch = '<form action="addEntry.py" method="post" target="_parent">'
ch += '<input name="content" id="content" size="30" style="font-family:sans-serif; font-size: 8pt">'
ch += '<input name="begin_time" type="hidden" value="'+hour+'">'
ch += '<input type="submit" name="subm" value="Ok">'
ch += '<input type="submit" name="subm" value="Cancel">'
ch += '</form>'
elt.innerHTML = ch
document.getElementById("content").focus()
elt.onclick=null
return false
}

function edit_entry(rec_id,bh,bm,eh,em,elt)
{
txt = elt.innerText
if (txt == undefined)
{ txt = elt.textContent }
while (txt.charAt(txt.length-1)==' ')
{ txt = txt.substr(0,txt.length-1) }

b_hour = parseInt(bh)
b_minute = parseInt(bm)
e_hour = parseInt(eh)
e_minute = parseInt(em)

ch = '<form action="editEntry.py" method="post" target="_parent">'
ch += '<input type="hidden" name="rec_id" value="'+rec_id+'">'
ch += 'Start <select name="begin_hour" size="1">'
for (h=0;h<24;h++)
{ if (h==b_hour)
  { ch += '<option value="'+h+'" selected>'+h }
  else
  { ch += '<option value="'+h+'">' + h }
}
ch += '</select>'
ch += '<select name="begin_minute" size="1">'
for (m=0;m<60;m+=5)
{ if (m==b_minute)
  { ch += '<option value="'+m+'" selected>'+m }
  else
  { ch += '<option value="'+m+'">' + m }
}
ch += '</select>'
ch += '<br>End <select name="end_hour" size="1">'
for (h=0;h<24;h++)
{ if (h==e_hour)
  { ch += '<option value="'+h+'" selected>'+h }
  else
  { ch += '<option value="'+h+'">' + h }
}
ch += '</select>'
ch += '<select name="end_minute" size="1">'
for (m=0;m<60;m+=5)
{ if (m==e_minute)
  { ch += '<option value="'+m+'" selected>'+m }
  else
  { ch += '<option value="'+m+'">' + m }
}
ch += '</select>'
ch += '<br><input name="content" id="content" size="30" value="'+txt
ch += '" style="font-family:sans-serif; font-size: 8pt">'
if (rec_id==-1)
{
ch +='<input type="submit" name="subm" value="Add">'
}
else
{
ch +='<input type="submit" name="subm" value="Update">'
ch +='<input type="submit" name="subm" value="Delete">'
}

ch +='<input type="submit" name="subm" value="Cancel">'
ch += '</form>'
with (document.getElementById("d_entry"))
{ style.top = elt.style.top
  style.left = elt.style.left
  style.width = 200
  style.height = 100
  innerHTML = ch
}
document.getElementById("content").focus()
elt.onclick=null
return false
}

function scroll8()
{
window.scrollTo(0,280)
}
function today()
{
location.href=index.pih
}