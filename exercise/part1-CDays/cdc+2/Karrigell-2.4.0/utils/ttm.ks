import datetime
from HTMLTags import *
import PyDbLite

import utils

db_users = PyDbLite.Base("users.pdl").open()
if not utils.is_logged(COOKIE,db_users):
    raise HTTP_REDIRECTION,"../index.html"

is_editor = COOKIE["role"].value in ["edit","admin"]

db = PyDbLite.Base("ttm.pdl").create("Nom","id_prog","statut",
    mode="open")
if not "description" in db.fields:
    db.add_field("description",default="")
if not "valid" in db.fields:
    db.add_field("valid",default=0)
db_prog = PyDbLite.Base("programmes.pdl").open()
db_pays = PyDbLite.Base("pays.pdl").open()
db_jalons_pays = PyDbLite.Base("jalons_pays.pdl").create("id_pays",
    "id_ttm","T_1","T0","T1","T2","T3",mode="open")
db_jalons_pays.create_index("id_ttm")
db_ttm_projet = PyDbLite.Base("ttm_projet.pdl").create("id_ttm",
    "id_projet",mode="open")
db_ttm_projet.create_index("id_ttm")
db_livrables = PyDbLite.Base("livrables.pdl").open()
db_prefs = PyDbLite.Base("prefs.pdl").create("login","prefs",mode="open")
if not "nom_liste" in db_prefs.fields:
    db_prefs.add_field("nom_liste",default="Liste 1")

fnames = dict([(k,k) for k in db.fields])
fnames.update({"id_prog":"Programme","T_1":"T-1"})

lstatuts = ["green","orange","red","n.d."]
lvalid = ["Offre","Produit potentiel"]

default_deb = "07/2007"
default_fin = "12/2008"

print "<html>"

def _next_month(d):
    # return first day of the month following date d
    y,m = d.year,d.month+1
    if m>12:
        y,m = d.year+1,1
    return datetime.date(y,m,1)

def _nbmonths(s_date,e_date):
    e_date = datetime.date(e_date.year,e_date.month,1)
    _date = s_date
    nb = 0
    while _date < e_date:
        nb += 1
        _date = _next_month(_date)
    return nb

def index():
    print utils.header("Projets TTM",src="roadmap.css")
    print H2("Projets TTM")

    persos = db_prefs(login=COOKIE["login"].value)

    lines = TR(TD(INPUT(Type="radio",name="pref_id",value=-1))+
               TD("Tous les programmes",colspan=2))
    for perso in persos: 
        lines += TR(TD(INPUT(Type="radio",name="pref_id",value=perso["__id__"]))
                   +TD(TEXT(perso["nom_liste"]+" ")+
                    SMALL(A("Modifier",href="edit_pref?pref_id=%s" %perso["__id__"]))))
    lines += TR(TD("&nbsp;")+TD(A(SMALL("[Créer une liste]"),href="edit_pref")))

    if "mois_ttm" in COOKIE:
        deb,fin = COOKIE["mois_ttm"].value.split(",")
    else:
        deb,fin = "07/2007","12/2008"

    m_deb,y_deb = [ int(x) for x in deb.split("/") ]
    m_fin,y_fin = [ int(x) for x in fin.split("/") ]

    lines += TR(TD("Mois début")+
               TD(SELECT(Sum([OPTION("%02d" %v,value=v,selected=v==m_deb) 
                    for v in range(1,13)]),name="mois_deb"))+
               TD(SELECT(Sum([OPTION("%02d" %v,value=v,selected=v==y_deb) 
                    for v in range(2007,2013)]),name="annee_deb"))
                )
    lines += TR(TD("Mois fin")+
               TD(SELECT(Sum([OPTION("%02d" %v,value=v,selected=v==m_fin) 
                    for v in range(1,13)]),name="mois_fin"))+
               TD(SELECT(Sum([OPTION("%02d" %v,value=v,selected=v==y_fin) 
                    for v in range(2007,2013)]),name="annee_fin"))
                )

    if COOKIE["role"].value=="admin":
        lines += TR(TD(INPUT(Type="checkbox",name="no_links"))+
                    TD("Version sans liens"))
    lines += TR(TD(INPUT(Type="submit",value="Voir la roadmap"),colspan=2))
    print FORM(TABLE(lines,
        style="border:1;border-style:solid;border-color:#B0B0B0"),
        action="show_roadmap",method="POST",target="_blank")

    if is_editor:
        print FORM(INPUT(Type="submit",value="Ajouter un projet"),
            action="edit")

def edit_pref(pref_id=-1):
    print utils.header("Sélection des programmes 3P",src="budget.css")
    print SCRIPT(src="../sel_progs.js")
    print H3("Sélection des programmes 3P")
    print '<form action="save_prefs" method="post">'

    if pref_id == -1: # nouvelle liste
        nblists = db_prefs(login=COOKIE["login"].value)
        nom = "Liste %s" %(len(nblists)+1)
        prog_ids = []
    else:
        pref = db_prefs[int(pref_id)]
        nom = pref["nom_liste"]
        prog_ids = pref["prefs"]

    nom_liste = TEXT("Liste") + INPUT(name="nom_liste",value=nom) +\
        INPUT(Type="hidden",name="pref_id",value=pref_id)
    progs = db_prog()
    progs.sort(lambda x,y:cmp(x["Nom"].lower(),y["Nom"].lower()))
    options = Sum([OPTION(p["Nom"],value=p["__id__"]) for p in progs
        if not p["__id__"] in prog_ids])
    s1 = SELECT(options,name="prog_list[]",id="origine",
        onClick="enable_button_add()",
        multiple=True,size="20")

    choice = Sum([OPTION(db_prog[prog_id]["Nom"],value=prog_id) 
        for prog_id in prog_ids])
    s2 = SELECT(choice,name="progs[]",id="destination",size=20,
        onClick="enable_buttons()")
    
    add = INPUT(Type="button",Id="add_button",value="==>",
        onClick="add()",disabled=True)
    rem = INPUT(Type="button",Id="remove_button",value="<==",
        onClick="remove()",disabled=True)

    monte = INPUT(Type="button",name="subm",value="Monter",Id="monte",
        onClick="monte_option()",disabled= True)
    descend = INPUT(Type="button",name="subm",value="Descendre",Id="descend",
        onClick="descend_option()",disabled= True)
    
    print TABLE(TR(TD(nom_liste)+TD(s1)+TD(add+BR()+rem)+
        TD(s2)+TD(monte+BR()+descend)))
    print INPUT(Type="hidden",name="new_prefs",id="new_prefs",value="-1")
    print INPUT(Type="submit",name="subm",value="Enregistrer et voir la roadmap",
        onClick="target_blank()")
    if not pref_id == -1:
        print INPUT(Type="submit",name="subm",value="Supprimer",
            onClick="target_blank()")
    else:
        print INPUT(Type="submit",name="subm",value="Annuler")
    print '</form>'
    print '</body>'

def save_prefs(**kw):

    pref_id = int(kw["pref_id"])
    if kw["subm"] == "Supprimer":
        del db_prefs[pref_id]
        db_prefs.commit()
        raise HTTP_REDIRECTION,"index"
    elif kw["subm"] == "Annuler":
        raise HTTP_REDIRECTION,"index"
    else:
        if kw["new_prefs"]=="-1":
            del kw["new_prefs"]
        else:
            new_prefs = [int(x) for x in kw["new_prefs"].rstrip(",").split(",")]
            kw["prefs"] = new_prefs
        if pref_id == -1: # nouvelle liste
            pref_id = db_prefs.insert(login=COOKIE["login"].value,**kw)
        else:
            db_prefs.update(db_prefs[int(pref_id)],**kw)
    db_prefs.commit()
    raise HTTP_REDIRECTION,"show_roadmap?pref_id=%s" %pref_id

def show_roadmap(**kw):
    
    if "pref_id" in kw:
        SET_COOKIE["prefs"] = kw["pref_id"]
        SET_COOKIE["prefs"]["path"] = '/'+THIS.baseurl.rstrip('/')
        pref_id = int(kw["pref_id"])
    elif "prefs" in COOKIE.keys():
        pref_id = int(COOKIE["prefs"].value)
    else:
        pref_id = -1

    no_links = kw.get("no_links",None)

    if not "mois_deb" in kw:
        if "mois_ttm" in COOKIE:
            deb,fin = COOKIE["mois_ttm"].value.split(",")
            kw["mois_deb"],kw["annee_deb"] = deb.split("/")
            kw["mois_fin"],kw["annee_fin"] = fin.split("/")
        else:
            kw["mois_deb"],kw["annee_deb"] = default_deb.split("/")
            kw["mois_fin"],kw["annee_fin"] = default_fin.split("/")
    else:
        SET_COOKIE["mois_ttm"] = "%s/%s,%s/%s" %(kw["mois_deb"],kw["annee_deb"],
            kw["mois_fin"],kw["annee_fin"])
        SET_COOKIE["mois_ttm"]["path"] = '/'+THIS.baseurl.rstrip('/')

    prog_width = 120
    ttm_width = 300
    statut_width = 30
    flag_width = 22
    _top = 150
    _left = 10
    height = 28
    padding = 15

    start_date = datetime.date(int(kw["annee_deb"]),int(kw["mois_deb"]),1)
    end_date = datetime.date(int(kw["annee_fin"]),int(kw["mois_fin"]),30)
    nb_months = utils.nbmonths(start_date,end_date)
    month_width = 20
    
    print utils.header_ttm("Projets TTM")
    print H2("Projets TTM")
    print DIV(IMG(src="../images/legende.png"),
        style="top:0;left:250;width:571;height:109")

    # initialisations sur les mois
    _date = start_date
    month_types = []
    while _date < end_date:
        if _date.month == 12:
            month_types.append("year_end")
        elif not _date.month%3:
            month_types.append("term_end")
        else:
            month_types.append("month")
        _date = _next_month(_date)

    progs = db_prog()
    if not pref_id == -1:
        progs = [ db_prog[prog_id] for prog_id in db_prefs[pref_id]["prefs"] ]
    for prog in progs:
        ttm_prog = [ r for r in db if r["id_prog"] == prog["__id__"] ]
        if ttm_prog:

            # affichage du nom du programme
            print DIV(prog["Nom"],Class="prog",
                style="top:%s;left:%s;width:%s;height:%s"
                %(_top,_left,ttm_width,height))

            # affichage du calendrier
            _date = start_date
            month_num = 0
            left = _left + ttm_width + statut_width
            start_year = left
            start_month = _date.month
            while _date < end_date:
                m = _date.strftime("%b")[:3]
                print DIV(m,Class="month",
                    style="top:%s;left:%s;width:%s;height:%s"
                    %(_top+height/2,left+month_num*month_width,month_width,height/2))
                # fin d'annee
                if _date.month == 12:
                    print DIV(_date.year,Class="year",
                        style="top:%s;left:%s;width:%s;height:%s"
                        %(_top,start_year,month_width*(12-start_month+1),height/2))
                    start_year += month_width*(12-start_month+1)
                    start_month = 1
                _date = _next_month(_date)
                month_num += 1
            _top += height

            # affichage des projets TTM du programme
            prog_top = _top

            # bordure de la liste des projets
            # afficher en premier sinon pas de lien par projet sous Firefox...
            print DIV("&nbsp;",style="top:%s;left:%s;height:%s;width:%s; \
                border-width:2;border-style:solid;border-color:#B0B0B0;" 
                %(prog_top-height,_left-2,height*(len(ttm_prog)+1)+2,
                    ttm_width+5))

            for num_ttm,r in enumerate(ttm_prog):
                left = _left
                r["id_prog"] = db_prog[r["id_prog"]]["Nom"]
                val = r["Nom"] or "(Sans nom)"
                if len(val)>50:
                    val = val[:50]+"..." # tronque pour affichage
                if len(db_ttm_projet._id_ttm[r["__id__"]]):
                    val = B(val)
                if is_editor and no_links is None:
                    val = A(val,
                        href="edit?recid=%s&prefs=%s" %(r["__id__"],pref_id),
                        Class="ttm")
                print DIV(val,Class="projet",
                    style="top:%s;left:%s;width:%s;height:%s" 
                        %(_top,left,ttm_width,height))
                left += ttm_width
                if r["statut"] in ["green","orange","red"]:
                    st = IMG(src="../images/%s.png" %r["statut"])
                else:
                    st = ""
                left += statut_width
                jalons = [ r_jalon for r_jalon in db_jalons_pays 
                    if r_jalon["id_ttm"] == r["__id__"] ]
                d_jalons = dict([(m,[]) for m in range(nb_months+1)])
                for jalon in jalons:
                    for k in [ k for k in jalon if k.startswith("T")]:
                        if jalon[k]:
                            month_num = utils.nbmonths(start_date,jalon[k])
                            if month_num in d_jalons:
                                d_jalons[month_num].append((jalon["id_pays"],k))
                for month_num in range(nb_months+1):
                    style="top:%s;left:%s;width:%s;height:%s" \
                        %(_top,left+month_num*month_width,month_width,height)
                    if not d_jalons[month_num]:
                        print DIV("&nbsp;",Class="T3",style=style)
                    else:
                        for (id_pays,k) in d_jalons[month_num]:
                            src = "../images/%s.png" %k
                            print DIV(IMG(src=src),Class="T3",style=style)
                for month_num in range(nb_months+1):
                    pos = 0
                    for (id_pays,k) in d_jalons[month_num]:
                        if not k=="T3":
                            continue
                        nom_pays = db_pays[id_pays]["Nom"].lower()
                        style="top:%s;left:%s;width:%s;height:%s" \
                            %(_top+height/2,
                              left+month_num*month_width+pos*flag_width,
                              flag_width,height/2)
                        print DIV(IMG(src="../images/%s.png" %nom_pays,
                            alt=nom_pays),
                            Class="T3",style=style)
                        pos += 1
                _top += height
            _top += padding

            # bordure du calendrier entier
            print DIV("&nbsp;",style="top:%s;left:%s;height:%s;width:%s; \
                border-width:2;border-style:solid;border-color:#B0B0B0;" 
                %(prog_top-height,left,height*(len(ttm_prog)+1),
                    month_width*(nb_months+1)))

            # bordure pour les mois
            print DIV("",style="top:%s;left:%s;height:%s;width:%s; \
                border-width:1 0 0 0;border-style:solid;border-color:#B0B0B0;" 
                %(prog_top-height/2,left,1,month_width*(nb_months+1)))
            print DIV("",style="top:%s;left:%s;height:%s;width:%s; \
                border-width:1 0 0 0;border-style:solid;border-color:#B0B0B0;" 
                %(prog_top-2,left,1,month_width*(nb_months+1)))

            # barres verticales de fin de trimestre
            style="top:%s;left:%s;height:%s;width:%s; \
                border-width:0 0 0 %s;border-style:%s;border-color:#B0B0B0;" 
            for i,month_type in enumerate(month_types[:-1]):
                if month_type == "term_end":
                    print DIV("",style= style %(prog_top-(height/2),left+(i+1)*month_width-1,
                            (height*len(ttm_prog))+height/2,1,1,"solid"))
                elif month_type == "year_end":
                    print DIV("",style= style %(prog_top-height,left+(i+1)*month_width-1,
                            height*(1+len(ttm_prog)),1,2,"solid"))
                else:
                    print DIV("",style= style %(prog_top-(height/2),left+(i+1)*month_width-1,
                            (height*len(ttm_prog))+height/2,1,1,"dotted"))

            # barres horizontales entre projets
            for i in range(len(ttm_prog)-1):
                # dans la liste des projets
                print DIV("",style="top:%s;left:%s;height:1;width:%s; \
                    border-width:1 0 0 0;border-style:dotted;border-color:#B0B0B0;" 
                    %(prog_top+(i+1)*height-2,_left,ttm_width))
                # dans le calendrier
                print DIV("",style="top:%s;left:%s;height:1;width:%s; \
                    border-width:1 0 0 0;border-style:dotted;border-color:#B0B0B0;" 
                    %(prog_top+(i+1)*height-2,left,month_width*(nb_months+1)))

    if COOKIE["role"].value in ["admin","edit"] and no_links is None:
        print A("Nouveau",href="edit")

def edit(prefs=None,recid=-1):

    if not is_editor:
        raise HTTP_REDIRECTION,"index"
    if prefs is not None:
        SET_COOKIE["prefs"] = prefs
        SET_COOKIE["prefs"]["path"] = '/'+THIS.baseurl.rstrip('/')
    elif "prefs" in COOKIE.keys():
        prefs = COOKIE["prefs"].value
    else:
        prefs = "tous"

    db_projets = PyDbLite.Base("projets.pdl").open()
    recid = int(recid)
    if recid>=0:
        r_ttm = db[int(recid)]
        print utils.header_ttm("Edition")
    else:
        r_ttm = {}
        print utils.header_ttm("Nouveau")
    print "<table>"
    print '<form action="insert" method="post">'
    print INPUT(name="recid",Type="hidden",value=recid)
    
    sel_prog = Sum([INPUT(Type="radio",name="id_prog",
        value=rp["__id__"]) + TEXT(rp["Nom"]) for rp in db_prog])

    print '<tr><td valign="top"><table>'

    print TR(TH("Nom")+TD(INPUT(name="Nom",value=r_ttm.get("Nom",""),size=40)))
    print TR(TH(fnames["statut"])+
        TD(Sum([INPUT(Type="radio",name="statut",value=t,
            checked=t==r_ttm.get("statut","")) + TEXT(t) +BR()
               for t in lstatuts])))

    descr = r_ttm["description"]
    print TR(TH(TEXT("Description")+BR(SMALL("(1000 caractères max.)")))+
        TD(TEXTAREA(descr,name="description",cols=40,rows=10)))

    print TR(TH("Maturité")+
        TD(Sum([INPUT(Type="radio",name="valid",value=i,
            checked=i==r_ttm.get("valid",0)) + TEXT(t) +BR()
               for i,t in enumerate(lvalid)])))

    progs = [ r for r in db_prog ]
    progs.sort(lambda x,y:cmp(x["Nom"].lower(),y["Nom"].lower()))
    print TR(TH("Programme")+
             TD(SELECT(Sum([OPTION(rp["Nom"],value=rp["__id__"],
                    selected=rp["__id__"]==r_ttm.get("id_prog",-1)) for rp in progs]),
                    name="id_prog")))

    projets = db_ttm_projet._id_ttm[recid]
    if projets:
        db_proj = PyDbLite.Base("projets.pdl").open()
        print TR(TH("Projet R&D associé")+
            TD(Sum([ TEXT(db_proj[projet["id_projet"]]["Nom"])+BR() for projet in projets])+
               A("Modifier",href="edit_projet?ttm_id=%s" 
                %(recid))))
    elif recid != -1:
        print TR(TH("Projet R&D associé")+
                TD(A("Associer",href="edit_projet?ttm_id=%s" %recid)))

    print "</table></td>"

    print "<td><table>"
    jalons = ("T_1","T-1"),("T0","T0"),("T1","T1"),("T2","T2"),("T3","T3")
    print TR(TD("&nbsp;")+Sum([TH(jalon[1]) for jalon in jalons]))

    dates_jalons = db_jalons_pays._id_ttm[recid]

    for r_pays in db_pays:
        jalons_pays = [ r_date for r_date in dates_jalons
                    if r_date["id_pays"] == r_pays["__id__"] ]
        if jalons_pays:
            jalons_pays = jalons_pays[0]
        else:
            jalons_pays = {}
        print "<tr>"
        print TD(r_pays["Nom"])
        for jalon in jalons:
            if jalon[0] in jalons_pays and jalons_pays[jalon[0]]:
                s_date = jalons_pays[jalon[0]].strftime("%d/%m/%Y")
            else:
                s_date = ""
            print TD(INPUT(name="jalonp%sp%s" %(jalon[0],r_pays["__id__"]),
                    value = s_date,size=8)) 
        print "</tr>"
    print "</table></td>"
    print '</tr></table>'
    print TR(TD(INPUT(Type="submit",value="Mise a jour"),colspan="2",Class="noborder"))
    print '</form></table>'
    
    if COOKIE["role"].value in ["admin","edit"] and recid>=0:
        print P()+FORM(INPUT(Type="hidden",name="recid",value=recid)+
                    INPUT(Type="submit",value="Supprimer"),action="delete")

def edit_projet(ttm_id):
    """Sélection du lien entre un TTM et un projet R&D"""
    print utils.header("Lien entre projet TTM et projet R&D",
        src="ttm_projets.css")
    ttm_id = int(ttm_id)
    projets = db_ttm_projet._id_ttm[ttm_id]
    proj_ids = [ p["id_projet"] for p in projets ]

    nom_ttm = db[ttm_id]["Nom"]
    print H2("Projet R&D associé au TTM %s" %nom_ttm)

    db_proj = PyDbLite.Base("projets.pdl").open()
    f = INPUT(Type="hidden",name="ttm_id",value=ttm_id)

    projets = db_proj()
    projets.sort(lambda x,y:cmp(x["Nom"].lower(),y["Nom"].lower()))
    options = []
    for r in projets:
        options.append(OPTION(r["Nom"],value=r["__id__"],
            selected=r["__id__"] in proj_ids))

    f += TD(SELECT(Sum(options),name="proj_ids[]",multiple=True,size=40),
        valign="top",Class="noborder")
    f += INPUT(Type="submit",name="subm",
        value="Associer au projet sélectionné")
    f += INPUT(Type="submit",name="subm",
        value="Pas de projet R&D associé")
    print FORM(TABLE(f),action="update_ttm_proj",method="post")

def update_ttm_proj(subm,ttm_id,proj_ids):
    proj_ids = [ int(x) for x in proj_ids ]
    ttm_id = int(ttm_id)
    ttm_proj = db_ttm_projet._id_ttm[ttm_id]
    db_ttm_projet.delete(ttm_proj)
    if not subm.startswith("Pas"):
        for proj_id in proj_ids:
            db_ttm_projet.insert(ttm_id,proj_id)
    db_ttm_projet.commit()
    raise HTTP_REDIRECTION,"show_roadmap"

def delete(recid):
    print utils.header_ttm("Suppression")
    print "Suppression de %s ?" %db[int(recid)]["Nom"]
    print A("Oui",href="confirm_delete?recid=%s" %recid)
    print A("Non",href="index")

def confirm_delete(recid):
    del db[int(recid)]
    db.commit()
    raise HTTP_REDIRECTION,"index"

def insert(**kw):

    if not kw["Nom"]:
        print "Erreur - Il faut donner un nom de projet"
        print BR()+A("Retour",href="javascript:history.back()")
        raise SCRIPT_END
    if not kw["id_prog"]:
        print "Erreur - il faut associer le projet à un programme. "
        print 'Eventuellement utiliser le programme "3P à définir"'
        raise SCRIPT_END

    if len(kw.get("description",""))>1000:
        print "Erreur - la description ne doit pas dépasser"
        print " 1000 caractères"
        raise SCRIPT_END

    id_ttm = int(kw["recid"])
    del kw["recid"]

    # valeurs pour le projet TTM dans la base db
    kw_ttm = dict([(k,v) for (k,v) in kw.iteritems() if k in db.fields ])
    kw_ttm["id_prog"] = int(kw["id_prog"])
    kw_ttm["valid"] = int(kw.get("valid",0))
    kw_ttm["statut"] = kw.get("statut",None)
    if id_ttm >= 0:
        r = db[id_ttm]
        db.update(r,**kw_ttm)
    else:
        id_ttm = db.insert(**kw_ttm)

    jalons = [ r_jalon for r_jalon in db_jalons_pays 
        if r_jalon["id_ttm"] == id_ttm ]

    d_jalons = dict([(jalon["id_pays"],jalon) for jalon in jalons])

    n_jalons = {}
    for k in kw:
        if k.startswith("jalon"):
            a,jalon,id_pays = k.split("p")
            id_pays = int(id_pays)
            if not id_pays in n_jalons:
                n_jalons[id_pays] = {}

            if not kw[k]:
                n_jalons[id_pays][jalon] = None
            else:
                _date = utils.make_date(kw[k])
                if not _date:
                    print utils.header_ttm("Erreur")
                    print "Mauvais format de date (JJ/MM/AAAA) : %s" %kw[k]
                    print A("Retour",href="javascript:window.history.back()")
                    raise SCRIPT_END

                n_jalons[id_pays][jalon] = _date

    for id_pays in n_jalons:
        if not id_pays in d_jalons:
            db_jalons_pays.insert(id_ttm=id_ttm,id_pays=id_pays,
                **n_jalons[id_pays])
        else:
            db_jalons_pays.update(d_jalons[id_pays],**n_jalons[id_pays])

    db_jalons_pays.commit()
    db.commit()
    raise HTTP_REDIRECTION,"show_roadmap"

def new_livrable(id_ttm):
    id_ttm = int(id_ttm)
    _projet = [ r["id_projet"] for r in db_ttm_projet 
        if r["id_ttm"] == id_ttm ]
    print utils.header_ttm("Livrables R&D")
    print H2("Livrables R&D associés au projet TTM <br>"+db[int(id_ttm)]["Nom"])
    print H2("Projet R&D")
    db_livrables = PyDbLite.Base("livrables.pdl").open()
    db_proj = PyDbLite.Base("projets.pdl").open()
    print '<form action="update_livrable" method="post">'
    print INPUT(Type="hidden",name="id_ttm",value=id_ttm)
    print "<table>"
    for r in db_proj:
        livrables = db_livrables._id_projet[r["__id__"]]
        print TR(TH(r["Nom"],colspan=2))
        if livrables:
            for rl in livrables:
                print TR(TD(rl["Nom"])+
                         TD(INPUT(Type="checkbox",name="id_livrable[]",
                         value=rl["__id__"],
                         checked = rl["__id__"] in _livr)))
    print TR(TD(INPUT(Type="submit",value="Mise a jour"),colspan=2))
    print '</form>'
    print "</table>"

def update_livrable(**kw):
    id_ttm = int(kw["id_ttm"])
    new_p = [ int(v) for v in kw.get("id_projet",[]) ]
    old = [ r for r in db_ttm_projet if r["id_ttm"] == id_ttm ]
    old_p = [ r["id_projet"] for r in old ]
    new = [ _id for _id in new_p if not _id in old_p ]
    db_ttm_projet.delete([r for r in old if not r["id_projet"] in new_p])
    for _id in new:
        db_ttm_livrable.insert(id_ttm=id_ttm,id_projet=_id)
    db_ttm_projet.commit()
    raise HTTP_REDIRECTION,"edit?recid=%s&" %kw["id_ttm"]
    