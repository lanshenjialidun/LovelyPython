from HTMLTags import *

labels = [("Current config","current.ks"),("Config file","config.ks"),
    ("Folders","rights.ks"),("Root directory","seldir.ks"),("Misc","misc.ks")]

def menu(selected):
    print HEAD(TITLE("Select root directory")+
        LINK(rel="stylesheet",href="../admin.css"))

    print A("Admin",href="/admin")+BR()

    cells = []
    for (label,target) in labels:
        if target==selected:
            cells.append(LI(A(label,href="../%s" %target,id="current"),id="active"))
        else:
            cells.append(LI(A(label,href="../%s" %target)))

    print DIV(UL(Sum(cells),id="navlist"),id="navcontainer")        
