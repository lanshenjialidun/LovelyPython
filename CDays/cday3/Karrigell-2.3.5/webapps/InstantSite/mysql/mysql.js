obl_length = new Array()
obl_length['CHAR']=new Array(1,255)
obl_length['VARCHAR']=new Array(1,255)
obl_length['DECIMAL']=new Array(1,64)
obl_length['NUMERIC']=obl_length['DECIMAL']

obl_decimals = new Array()
obl_decimals['DECIMAL'] = new Array(1,30)
obl_decimals['NUMERIC'] = obl_decimals['DECIMAL']

unsigned = new Array( 'BIGINT',
  'DECIMAL','DEC','FIXED',
  'DOUBLE','REAL',
  'FLOAT',
  'INT',
  'INTEGER',
  'MEDIUMINT',
  'NUMERIC',
  'REAL',
  'SMALLINT',
  'TINYINT','BIT','BOOL'
  )

is_unsigned = new Array()
for (i=0;i<unsigned.length;i++)
{ is_unsigned[unsigned[i]]=1 }

char_types = new Array()
char_types['CHAR'] = new Array('default','BINARY','ASCII','UNICODE')
char_types['VARCHAR'] = new Array('default','BINARY')

enum_vals = new Array('ENUM','SET')

keys = new Array('no','KEY','PRIMARY KEY')

key = ''
null_ = ''
char_type = ''

function k_field(elt)
{
	validate()
	return false
}

function t_entry()
{
	ch = 'Create new table'
    ch += '<form action="view"><input name="table"><br>'
    ch += '<input type="hidden" name="new_table" value="1">'
    ch += '<input type="submit" value="Ok">'
    ch += '<input type="button" onclick="leave()" value="Cancel"></form>'
    document.getElementById("new_table").innerHTML = ch
}

function drop_table(t)
{
	flag = confirm('Do you want to drop table '+t+'? This will definitely erase all data')
	if (flag)
	{ location.href="drop_table?table="+t }
}

function sel_field()
{
	nb = document.forms["fields"].elements["field[]"].length
	if (nb != undefined)
	{ nbsel = false
	  for (i=0;i<nb;i++)
	  { if (document.forms["fields"].elements["field[]"][i].checked)
	    { nbsel = true }
	  }
	} else {
	  nbsel = document.forms["fields"].elements["field[]"].checked
	}
	if (nbsel)
	{ document.getElementById("sub").disabled=false }
	else
	{ document.getElementById("sub").disabled=true }
}

function leave()
{
    ch='<a href="javascript:t_entry()">New table</a>'
    document.getElementById("new_table").innerHTML = ch
}

function ch_null(n_num)
{
	if (n_num == 1)
	{ null_ = 'NOT NULL'
	  document.getElementById("default").disabled=false 
	}
	else
	{ null_ = ''
	  document.getElementById("default").disabled=true 
	}
	validate()
}

function ch_key(k_num)
{
	key = keys[k_num]
	validate()
}

function ch_char_type(ch_num)
{
	elt = document.getElementById("Type")
	selType = elt.options[elt.selectedIndex].value
	char_type = char_types[selType][ch_num]
	validate()
}

function change_type()
{

	elt = document.getElementById("Type")
	selType = elt.options[elt.selectedIndex].value
	ch = '<table border="1">'
	if (obl_length[selType] != undefined)
	{
	  limits = obl_length[selType]
	  ch += '<tr><td>'
	  ch += 'Length ('+limits[0]+'-'+limits[1]+')</td>'
	  ch += '<td><input name="size"></td></tr>'
	}
	if (obl_decimals[selType] != undefined)
	{
	  limits = obl_decimals[selType]
	  ch += '<tr><td>'
	  ch += 'Decimals ('+limits[0]+'-'+limits[1]+')</td>'
	  ch += '<td><input name="decimals"></td></tr>'
	}
	if (is_unsigned[selType] != undefined)
	{
	  ch += '<tr><td>UNSIGNED</td>'
	  ch += '<td><input type="checkbox" name="unsigned" onChange="validate()"></td></tr>'
	  ch += '<tr><td>ZEROFILL</td>'
	  ch += '<td><input type="checkbox" name="zerofill" onChange="validate()"></td></tr>'
	}
	if (char_types[selType] != undefined)
	{
	  ch += '<tr><td>CHARTYPE</td><td>'
	  for (i=0;i<char_types[selType].length;i++)
	  { t = char_types[selType][i]
	    ch += t+'<input type="radio" name="spec_chartype" onClick="ch_char_type('+i+')"'
	    if (i==0) { ch += " checked" }
	    ch += '>'
	  }
	  ch += '</td></tr>'
	}
	if (selType == 'INT' || selType == 'INTEGER')
	{
	  ch += '<tr><td>AUTO_INCREMENT</td>'
	  ch += '<td><input type="checkbox" name="auto_increment" onClick="validate()"></td></tr>'
	}

	ch += '</table>'

    document.getElementById("f_opt").innerHTML = ch
    
    validate()
}

function validate()
{
 field = document.forms["add"].elements["field"].value
 document.forms["add"].elements["subm"].disabled = (field == '')
 if (field == '')
 {  document.forms["add"].elements["sql"].value = ''
    return
 }
 
 if (document.forms["add"].elements["new"].value == "0")
 { ch = "ALTER TABLE "+document.getElementById("table").value+" ADD " }
 else
 { ch = "CREATE TABLE "+document.getElementById("table").value+" (" }

 ch += document.forms["add"].elements["field"].value
 elt = document.getElementById("Type")
 selType = elt.options[elt.selectedIndex].value
 ch += ' '+ selType
 
 if (obl_length[selType] != undefined)
 { ch += "("+document.forms["add"].elements["size"].value
   if (obl_decimals[selType] != undefined)
   { ch += ","+document.forms["add"].elements["decimals"].value }
   ch += ")"
 }

 if (char_types[selType] != undefined && char_type != "default")
 {
   ch += ' '+char_type
 }
 ch += ' '+null_
 
 elt = document.forms["add"].elements["default"]
 if (!elt.disabled && elt.value != '')
 { if (is_unsigned[selType] == undefined)
   { ch += ' DEFAULT &quot;'+elt.value+'&quot; ' }
   else
   { ch += ' DEFAULT '+elt.value+' ' }
 }

 attrs = new Array("auto_increment","zerofill","unsigned")
 for (i=0;i<attrs.length;i++)
 {
  attr = attrs[i]
  if (document.forms["add"].elements[attr] != undefined)
   { if (document.forms["add"].elements[attr].checked)
     { ch += " "+attr+ " " }
   }
 } 
 if (key != "no")
  { ch += ' '+key }

 if (document.forms["add"].elements["new"].value == "1")
 { ch += ")" }

 elt = document.forms["add"].elements["position"]
 if ( elt != undefined)
 { position = elt.options[elt.selectedIndex].value
   ch += ' '+position
 }
 
 document.forms["add"].elements["sql"].value = ch
 
}