function showMsg(msgid)
{
if (selectedMsg != null)
    {
    document.getElementById(selectedMsg).style.backgroundColor="#ffffff"
    }
document.getElementById("msg"+msgid).style.backgroundColor="#ffcc77"
selectedMsg = "msg"+msgid
}

function writeAnswer(msgid,title)
{
    selectedMsg = msgid
    elt = document.getElementById("msg"+msgid)
    save_html = elt.innerHTML
    enterMessage = '<form action="index.ks/save_message" method="POST" target="_top">'
    enterMessage += '<input type="hidden" name="parent" value="'+msgid+'">'
    enterMessage += 'Name <input name="author">'
    enterMessage += 'Title <input name="title" size="40" value="RE:'+title+'"><br>'
    enterMessage += '<textarea name="content" rows=10 cols=80></textarea><br>'
    enterMessage += '<input type="submit" value="Ok">'
    enterMessage += '<input type="button" value="<%_ "Cancel"%>"'
    enterMessage += 'onClick="removeForm('+msgid+')"><br>'
    enterMessage += '</form>'
    elt.innerHTML += enterMessage
}

function removeForm(msgid)
{
    elt = document.getElementById("msg"+msgid)
    elt.innerHTML = save_html
}
