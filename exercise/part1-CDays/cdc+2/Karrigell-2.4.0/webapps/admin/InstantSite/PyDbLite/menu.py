from HTMLTags import *

labels = [("Fields","index.ks/edit"),("Layout","index.ks/layout")]

def menu(db_name,selected):
    print HEAD(TITLE("Database management")+
        LINK(rel="stylesheet",href="../admin.css"))

    print H3("Managing database %s" %db_name)

    cells = []
    for (label,target) in labels:
        if target==selected:
            cells.append(LI(A(label,href="../%s?db=%s" %(target,db_name),
                id="current"),id="active"))
        else:
            cells.append(LI(A(label,href="../%s?db=%s" %(target,db_name))))

    print DIV(UL(Sum(cells),id="navlist"),id="navcontainer")        
