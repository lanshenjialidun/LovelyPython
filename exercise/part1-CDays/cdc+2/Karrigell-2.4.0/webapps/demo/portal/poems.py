# Calls menu for French poems

Labels=["Ronsard",
	"Corneille",
	"Musset",
	"Hugo",
	"Baudelaire",
	"Rimbaud",
	"Verlaine"]
Urls=["ronsard.htm",
	"corneille.htm",
	"musset.htm",
	"hugo.htm",
	"baudelaire.htm",
	"rimbaud.htm",
	"verlaine.htm"]

Include("k_menu.hip",
	labels=Labels,
	urls=Urls,
	targetUrl="index.pih")
