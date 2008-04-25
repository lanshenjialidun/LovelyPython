from HTMLTags import *

rows=[]
for client in clients:
    rows.append(
        TR( TD(client.surname+'&nbsp;'+client.firstname) +
            TD(A(client.email,href="mailto:"+client.email))
          ))

print HTML(HEAD(TITLE(title)) + BODY(TABLE(Sum(rows))))
   