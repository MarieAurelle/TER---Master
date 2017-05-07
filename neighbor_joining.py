import numpy as np

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

####  Fonction main   ####
if __name__ == '__main__':
	
				############################
				###    INITIALISATION    ###
				############################
				
	branches = []; #Liste contenant tous les arcs de notre arbre
	iteration = True; #Pour continuer a joindre les sommets entre eux
	sommet_oublie = []; #Liste contenant les sommets dont il ne faut plus tenir compte
	nom_sommets = []; #Liste contenant le nom des sommets
	
	### Initialisation matrice de distances ### 
	fichier = input("Entrez le nom du fichier contenant la matrice de distance : ");
	matrice = np.genfromtxt(fichier, delimiter = " ");
	print(matrice);
	nom_sommets = rempli_nom_sommets(len(matrice), nom_sommets);
	
				############################
				###    Algorithme N-J    ###
				############################
	
	while(iteration):
		### Initialisation de la matrice temporaire pour echanger la matrice de distances avec la nouvelle et de la matrice Q###
		matriceTMP = np.zeros((len(matrice), len(matrice)), dtype=np.int);
		matriceQ = np.zeros((len(matrice), len(matrice)), dtype=np.int);
		
		### Calcul de la matrice Q ###
		matriceQ = calcul_matriceQ(matriceQ, matrice, sommet_oublie);
		print(matriceQ);
	
		### Recherche du minimum de la matrice Q ###
		minimum = trouve_min(matriceQ);
		print(minimum["sommet1"]);
		print(minimum["sommet2"]);
		print(minimum["valeur"]);
		
		chaine1 = str(nom_sommets[minimum["sommet1"]]);
		chaine2 = str(nom_sommets[minimum["sommet2"]]);
	
		### On entre les deux arcs dans un dictionnaire qu'on ajoutera dans la liste branches ###
		arc = {};
		arc["source"] = nom_sommets[minimum["sommet1"]];
		arc["cible"] = chaine1+"-"+chaine2;
		poids = 0.5*matrice[minimum["sommet1"],minimum["sommet2"]]+((np.sum(matrice[minimum["sommet1"]])-np.sum(matrice[minimum["sommet2"]]))/(2*(len(matrice)-2)));
		arc["poids"] = poids;
		print(arc["poids"]);
		branches.append(arc);
	
		arc = {};
		arc["source"] = nom_sommets[minimum["sommet2"]];
		arc["cible"] = chaine1+"-"+chaine2;
		arc["poids"] = matrice[minimum["sommet1"],minimum["sommet2"]]-poids;
		print(arc["poids"]);
		branches.append(arc);
		sommet_oublie.append(minimum["sommet2"]);
		nom_sommets[minimum["sommet1"]] = chaine1+"-"+chaine2;
		print(branches);
		print(sommet_oublie);
		
		### Modification de la matrice avec les nouvelles valeurs ###
		matriceTMP = calcul_matriceTMP(matriceTMP, matrice, minimum, sommet_oublie);
		print(matriceTMP);
		if(len(sommet_oublie) != len(matrice)-1):
			### On remplace la matrice de base par la nouvelle matrice ###
			matrice = remplace_matrice(matriceTMP, matrice);
			print(matrice);
		else:
			iteration = False;
			print(matrice);
