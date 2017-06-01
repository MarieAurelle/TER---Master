import numpy as np
import time

def trouve_min(matrice):
	reponse = {};
	reponse["valeur"] = 0;
	i=0
	
	while(i<len(matrice)):
		j=i+1;
		while(j<len(matrice)):
			if(matrice[i,j] < reponse["valeur"]):
				reponse["valeur"] = matrice[i,j];
				reponse["sommet1"] = i;
				reponse["sommet2"] = j;
			j = j+1
		i = i+1
	
	return reponse;
	
def calcul_matriceQ(matriceQ, matrice_distance, sommet_oublie):
	i=0;
	while(i<len(matrice)):
		j=0;
		while(j<len(matrice)):
			if(i!=j and (i not in sommet_oublie) and (j not in sommet_oublie)):
				matriceQ[i,j] = (len(matrice)-len(sommet_oublie)-2)*matrice[i,j]-np.sum(matrice[i])-np.sum(matrice[j]);
			j = j+1
		i = i+1;
	return matriceQ;

def calcul_matriceTMP(matriceTMP, matrice, donnees, sommet_oublie):
	i=0;
	while(i<len(matrice)):
		j=0;
		while(j<len(matrice)):
			if(i!=j and (i not in sommet_oublie) and (j not in sommet_oublie)):
				if(i == donnees["sommet1"]):
					matriceTMP[i,j] = (matrice[donnees["sommet1"],j]+matrice[donnees["sommet2"],j]-matrice[donnees["sommet1"],donnees["sommet2"]])/2;
				else:
					if(j == donnees["sommet1"]):
						matriceTMP[i,j] = (matrice[i,donnees["sommet1"]]+matrice[i,donnees["sommet2"]]-matrice[donnees["sommet1"],donnees["sommet2"]])/2;
					else:
						if(i != donnees["sommet2"] and j != donnees["sommet2"]):
							matriceTMP[i,j] = matrice[i,j];
			j = j+1;
		i = i+1;
	return matriceTMP;

def remplace_matrice(matrice_source, matrice_cible):
	i=0;
	while(i<len(matrice_source)):
		j=0;
		while(j<len(matrice_source)):
			matrice_cible[i,j] = matrice_source[i,j];
			j = j+1;
		i = i+1;
	return matrice_cible;

def rempli_nom_sommets(taille, nom_sommets):
	i=0;
	while(i<taille):
		nom_sommets.append(i);
		i = i+1;
	return nom_sommets;

def verif_appartenance(liste, liste_dico):
	for elt in liste:
		for d in liste_dico:
			if(elt in d["souches"]):
				return d["groupe"];
	return -1;

def ajout_souches(liste, liste_dico, numero_groupe):
	compteur = -1;
	for d in liste_dico:
		if(d["groupe"] != numero_groupe):
			compteur = compteur +1;
	for elt in liste:
		if(elt not in liste_dico[compteur]["souches"]):
			liste_dico[compteur]["souches"] = liste_dico[compteur]["souches"]+"-"+str(elt);
	return liste_dico;

def ajout_groupe(liste, liste_dico, numero_groupe):
	dico = {};
	dico["groupe"] = numero_groupe;
	dico["souches"] = "";
	for elt in liste:
		if(len(dico["souches"]) > 0):
			dico["souches"] = dico["souches"]+"-"+str(elt);
		else:
			dico["souches"] = str(elt);
	liste_dico.append(dico);
	return liste_dico;

def algorithme_NJ(MinPts, matrice):
	branches = []; #Liste contenant tous les arcs de notre arbre
	groupes = []; #Liste contenant les differents groupes avec les ST correspondants
	iteration = True; #Pour continuer a joindre les sommets entre eux
	sommet_oublie = []; #Liste contenant les sommets dont il ne faut plus tenir compte
	nom_sommets = []; #Liste contenant le nom des sommets
	nom_sommets = rempli_nom_sommets(len(matrice), nom_sommets);
	
	while(iteration):
		### Initialisation de la matrice temporaire pour echanger la matrice de distances avec la nouvelle et de la matrice Q###
		matriceTMP = np.zeros((len(matrice), len(matrice)), dtype=np.int);
		matriceQ = np.zeros((len(matrice), len(matrice)), dtype=np.int);
		
		### Calcul de la matrice Q ###
		matriceQ = calcul_matriceQ(matriceQ, matrice, sommet_oublie);
		#print(matriceQ);
	
		### Recherche du minimum de la matrice Q ###
		minimum = trouve_min(matriceQ);
		
		chaine1 = str(nom_sommets[minimum["sommet1"]]);
		chaine2 = str(nom_sommets[minimum["sommet2"]]);
	
		### On entre les deux arcs dans un dictionnaire qu'on ajoutera dans la liste branches ###
		arc = {};
		arc["source"] = nom_sommets[minimum["sommet1"]];
		arc["cible"] = chaine1+"-"+chaine2;
		poids = 0.5*matrice[minimum["sommet1"],minimum["sommet2"]]+((np.sum(matrice[minimum["sommet1"]])-np.sum(matrice[minimum["sommet2"]]))/(2*(len(matrice)-2)));
		arc["poids"] = poids;						
		branches.append(arc);
	
		arc = {};
		arc["source"] = nom_sommets[minimum["sommet2"]];
		arc["cible"] = chaine1+"-"+chaine2;
		arc["poids"] = matrice[minimum["sommet1"],minimum["sommet2"]]-poids;
		branches.append(arc);
		sommet_oublie.append(minimum["sommet2"]);
		nom_sommets[minimum["sommet1"]] = chaine1+"-"+chaine2;
		
		### Modification de la matrice avec les nouvelles valeurs ###
		matriceTMP = calcul_matriceTMP(matriceTMP, matrice, minimum, sommet_oublie);
		#print(matriceTMP);
		if(len(sommet_oublie) != len(matrice)-1):
			### On remplace la matrice de base par la nouvelle matrice ###
			matrice = remplace_matrice(matriceTMP, matrice);
			#print(matrice);
		else:
			iteration = False;
			#print(matrice);

	return branches;

def trouve_poids_max(liste_dico):
	poids_max = liste_dico[0]["poids"];
	sommet_poids_max = liste_dico[0];
	for s in liste_dico:
		if(s["poids"] > poids_max):
			poids_max = s["poids"];
			sommet_poids_max = s;
	return sommet_poids_max;

def suppression_sommet(liste_dico, sommet):
	for s in liste_dico:
		if(s["souches"] == sommet["souches"]):
			liste_dico.remove(s);
			return liste_dico;				
		
def filtrage_sommets(liste_dico, nb_sommets_choisis, numero_groupe, groupes):
	while(len(liste_dico) > nb_sommets_choisis):
		sommet_suppr = trouve_poids_max(liste_dico);
		groupes = ajout_groupe(str(sommet_suppr["souches"]).split("-"), groupes, numero_groupe,);
		suppression_sommet(liste_dico, sommet_suppr);
	return liste_dico;
		
	
def creation_arbre(liste_dico, groupes, MinPts, NbGp):
	if(NbGp >= 2):
		i = len(liste_dico)-1;
		
		if(NbGp == 2):
			while(len(str(liste_dico[i]["source"]).split("-")) < MinPts or len(str(liste_dico[i-1]["source"]).split("-")) < MinPts):
				i = i-2;
			groupes = ajout_groupe(str(liste_dico[i]["source"]).split("-"), groupes, 1);
			groupes = ajout_groupe(str(liste_dico[i-1]["source"]).split("-"), groupes, 2);
		
		else:
			numero_groupe = 1;
			sommets_choisis = []; #Liste contenant la liste des sommets choisis en fonction du poids des arcs
			nb_sommets_choisis = NbGp/2;
			while(nb_sommets_choisis > 0 and i>1):
				sommet = {}; #dictionnaire contenant le numero et le poids du sommet selectionne + indice
				if(len(str(liste_dico[i]["source"]).split("-")) >= MinPts*2 and len(str(liste_dico[i-1]["source"]).split("-")) >= MinPts*2):
					sommet["souches"] = liste_dico[i]["source"];
					sommet["poids"] = liste_dico[i]["poids"];
					sommet["indice"] = i;
					sommets_choisis.append(sommet);
						
					sommet = {};
					sommet["souches"] = liste_dico[i-1]["source"];
					sommet["poids"] = liste_dico[i-1]["poids"];
					sommet["indice"] = i+1;
					sommets_choisis.append(sommet);
					nb_sommets_choisis = nb_sommets_choisis -1;	
				i=i-2;
				sommets_choisis = filtrage_sommets(sommets_choisis, NbGp/2, numero_groupe, groupes);
			if(len(groupes) > 0):
				numero_groupe = numero_groupe+1;
			for s in sommets_choisis:
				iterateur = s["indice"]-1;
				while(iterateur>0):
					if(str(liste_dico[iterateur]["source"]) in str(s["souches"]) and len(str(liste_dico[iterateur]["source"]).split("-")) >= MinPts and len(str(liste_dico[iterateur-1]["source"]).split("-")) >= MinPts):
						groupes = ajout_groupe(str(liste_dico[iterateur]["source"]).split("-"), groupes, numero_groupe);
						numero_groupe = numero_groupe+1;
						groupes = ajout_groupe(str(liste_dico[iterateur-1]["source"]).split("-"), groupes, numero_groupe);
						numero_groupe = numero_groupe+1
						break;
					else:
						iterateur = iterateur-1;
				if(iterateur==0):
					print("Pas de sous groupe trouve pour : "+str(s["souches"]));
	return groupes;

def recherche_groupe(numero, groupes):
	for g in groupes:
		if(str(numero) in g["souches"].split("-")):
			return g["groupe"];

def visualisation(groupes, N, name):
	visu = open(name, "w");
	liste_sommets = [];
	for g in groupes:
		for elt in g["souches"].split("-"):
			liste_sommets.append(elt);
	print("Individus exclus : "+str(N-len(liste_sommets))+"\n");
	i=1;
	while(i<=N):
		if(str(i) in liste_sommets):
			g = recherche_groupe(i, groupes);
			visu.write(str(g));
		else:
			visu.write(str(0));
		visu.write(" ");
		i = i+1;
	visu.close();

def verif_visu(N, name):
	a = open(name, "r");
	b = a.readline();
	c = (b.split(" "))[:len(b.split(" "))-1];
	if(len(c) == N):
		print("Visualisation exacte.");

def calcul_distance(sommet, matrice, liste_sommets, liste_distances):
	distance = 0;
	for elt in liste_sommets:
		distance = distance+matrice[int(sommet), int(elt)];
		liste_distances.append(matrice[int(sommet), int(elt)]);
	if(sommet in liste_sommets):
		distance = distance/(len(liste_sommets)-1);
	else:
		distance = distance/(len(liste_sommets));
	return distance;

def recherche_max(liste):
	maximum = 0;
	for elt in liste:
		if(maximum < elt):
			maximum = elt;
	return maximum;

def recherche_min(liste):
	minimum = liste[0];
	for elt in liste:
		if(minimum > elt):
			minimum = elt;
	return minimum;

def calcul_intra_cluster(g, matrice, diam):
	liste_distances = [];
	distance_intra_cluster = 0;
	for s in g["souches"].split("-"):
		distance_intra_cluster = distance_intra_cluster + calcul_distance(s, matrice, g["souches"].split("-"), liste_distances);
	distance_intra_cluster = distance_intra_cluster/(len(g["souches"].split("-")));
	diam_max = recherche_max(liste_distances);
	diam.write("Groupe "+str(g["groupe"])+" : "+str(diam_max)+"\n");
	return distance_intra_cluster;
				
def calcul_inter_cluster(g1, g2, matrice, dist_min):
	liste_distances = [];
	distance_inter_cluster = 0;
	for elt1 in g1["souches"].split("-"):
		distance_inter_cluster = distance_inter_cluster + calcul_distance(elt1, matrice, g2["souches"].split("-"), liste_distances);
	distance_inter_cluster = distance_inter_cluster/(len(g1["souches"].split("-")));
	dist_min = recherche_min(liste_distances);
	print("Groupe "+str(g1["groupe"])+" - "+ str(g2["groupe"])+" distance minimale : "+str(dist_min)+"\n");
	return distance_inter_cluster;

####  Fonction main   ####
if __name__ == '__main__':
	
				############################
				###    INITIALISATION    ###
				############################

	fichier = input("Entrez le nom du fichier contenant la matrice de distance : ");
	nb_groupes = input("Entrez le nombre de groupes souhaite : ");
	MinPts = input("Entrez la taille minimun d'un cluster (en nombre de points) : ");
	tmp_debut = time.time();
	matrice = np.genfromtxt(fichier, delimiter = " ");
	#print(matrice);
	neighbor = []; #Liste qui va contenir le resultat de l'algorithme, c'est-a-dire la liste des arcs du graphe
	groupes = []; #Liste contenant les groupes avec les ST correspondants
	
				############################
				###    Algorithme N-J    ###
				############################
	
	neighbor = algorithme_NJ(MinPts, matrice);
	tmp_fin = time.time();
	print("Temps d'execution : "+str(tmp_fin-tmp_debut));
	#print(neighbor);
	groupes = creation_arbre(neighbor, groupes, MinPts, nb_groupes);
	print(str(len(groupes))+" groupes trouves :");
	for g in groupes:
		print("Groupe "+str(g["groupe"])+" :"+str(len(g["souches"].split("-")))+"\n"+str(g["souches"].split("-")));

				############################
				###    Sauvegarde.txt    ###
				############################
	
	i=1			
	nom_save = str(nb_groupes)+"_"+str(MinPts)+"_groupes_neighbor.txt";
	save = open(nom_save, "w");
	liste_sommets = [];
	for g in groupes:
		for elt in g["souches"].split("-"):
			liste_sommets.append(elt);
	while(i<=len(matrice)):
		save.write(str(i)+" ");
		if(str(i) in liste_sommets):
			g = recherche_groupe(i, groupes);
			save.write(str(g));
		else:
			save.write(str(0));
		save.write("\n");
		i = i+1;
	save.close();
	
	nom_save2 = "arcs_neighbor.txt";
	save2 = open(nom_save2, "w");
	for elt in neighbor:
		save2.write(str(elt["source"])+" "+str(elt["cible"])+" "+str(elt["poids"])+"\n");
	save2.close();
	
				############################
				###   Fichier visuali    ###
				############################
	
	name = str(nb_groupes)+"_"+str(MinPts)+"_visualisation.txt";
	visualisation(groupes, len(matrice), name);
	verif_visu(len(matrice), name);
	
	if(len(groupes) > 1):
					############################
					###   Inter - cluster    ###
					############################
		
		matrice = np.genfromtxt(fichier, delimiter = " ");
		inter = open(str(nb_groupes)+"_"+str(MinPts)+"_inter_cluster.txt", "w");
		i=0;
		while(i<len(groupes)):
			j=i+1;
			dist_min = 0;
			while(j<len(groupes)):
				dist_inter = calcul_inter_cluster(groupes[i], groupes[j], matrice, dist_min);
				inter.write("Groupe "+str(groupes[i]["groupe"])+" - "+ str(groupes[j]["groupe"])+" : "+str(dist_inter)+"\n");
				j = j+1;
			i=i+1;
		inter.close();

				############################
				###   Intra - cluster    ###
				############################
	
	intra = open(str(nb_groupes)+"_"+str(MinPts)+"_intra_cluster.txt", "w");
	diam = open(str(nb_groupes)+"_"+str(MinPts)+"_diametre_cluster.txt", "w");
	for g in groupes:
		dist_intra = calcul_intra_cluster(g, matrice, diam);
		intra.write("Groupe "+str(g["groupe"])+" : "+str(dist_intra)+"\n");
	intra.close();
	diam.close();
