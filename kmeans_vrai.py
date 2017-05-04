#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import random
import time

## Fonction permettant de vider la liste de clusters C ##
def vider_C(nbClusters) :
	i = 0;
	while i < nbClusters :
		del(C[i][:]);
		i = i+1;

# Calcul du carre de la distance entre un element et un centre de clusters passes en parametres
#element = numero de lelement duquel on veut trouver la distance par rapport au centre
#centre = vecteur du centre
def calcul_distance_vecteurs(matriceD, element, centre) :
	distance = 0;
	i = 0;
	while i < len(matriceD[0]) :# taille dune ligne
		distance += (matriceD[element][i] - centre[i])*(matriceD[element][i] - centre[i]);
		i = i+1;
	return distance;

##Calcul du carre de la distance entre les centres actuels et les centres anciens
## les centres sont definis par des listes de vecteurs 
## la distance est calculee comme la somme des distances de tous les centres deux a deux
def calcul_distance_centres(centre_anc, centre_nouv) :
	distance = 0;
	i = 0;
	while i < len(centre_anc) :# taille dune ligne
		j = 0;
		while j < len(centre_anc[i]):
			distance += (centre_anc[i][j] - centre_nouv[i][j])*(centre_anc[i][j] - centre_nouv[i][j]);
			j = j+1
		i = i+1;
	return distance;

## Determine le centre des clusters  le plus proche pour un element ##
## centres = liste de vecteurs centres
## element = numero de lelement dans la matriceD 
def calcul_plus_proche(matriceD, element, centres) :
	i = 1;
	minimum = calcul_distance_vecteurs(matriceD, element, centres[0]);
	posmin = 0;
	while i < len(centres) :
		distance = calcul_distance_vecteurs(matriceD, element, centres[i]);
		if(distance < minimum) :
			minimum = distance;
			posmin = i;
		i = i+1;
	return posmin;
		
## Determine aleatoirement parmi tous les elements un nbClusters d elements qui seront les premiers centres ## 
def choix_k_alea(matriceD, nbClusters, numeros_centres, C) :
	i = 0;
	centres = [[]];
	while i<nbClusters :
		if(i != 0) : # initialise le bon nombre de clusters dans la liste C
			listevide1 = [];
			listevide2 = [];
			C.append(listevide1);
			centres.append(listevide2);
		alea = random.randint(0,len(matriceD)-1);
		while alea in numeros_centres : alea = random.randint(0,len(matriceD)-1); ## pour prendre une nouvelle valeur
		numeros_centres.append(alea);
		j = 0;
		while j < len(matriceD[0]) :
			centres[i].append(matriceD[alea][j]);
			j = j+1;
		i = i+1;
	return centres;
	
##Ajoute les premiers centres definis par lutilisateur dans la liste de vecteurs centres
## numeros_centres = une liste contenant les numeros des centres choisis par lutilisateur	
def choix_k_nonAlea(matriceD, nbClusters, numeros_centres, C) :
	i = 0;
	centres = [[]];
	while i<nbClusters :
		if(i != 0) : # initialise le bon nombre de clusters dans la liste C
			listevide1 = [];
			listevide2 = [];
			C.append(listevide1);
			centres.append(listevide2);
	 	
		j = 0;
		while j < len(matriceD[0]) :
			centres[i].append(matriceD[numeros_centres[i]][j]);
			j = j+1;
		i = i+1;
	return centres;

##Calcul du vecteur moyenne de chaque cluster pour la mise a jour
def calcul_centres_clusters(matrice, centres, C) :
	i = 0;
	while i < len(C) :
		nouveau_centre = [0]*len(matrice[0]);
		for element in C[i] :
			j = 0;
			while j < len(matrice[0]) : 
				nouveau_centre[j] += matrice[element][j];
				j = j+1;
		j = 0;
		while j < len(matrice[0]) :
			nouveau_centre[j] = nouveau_centre[j]/(1.0*len(C[i]));
			j = j+1
		centres[i] = list(nouveau_centre);
		i = i+1
	return centres;	

## Algorithme k moyenne ##
def kmeans(matriceD, nbClusters, K, centres, C) :	
	entree1 = True;
	centres_nouv = list(centres);
	compteur = 0;

	## ajout des premiers centres comme premier element de chaque cluster ##
	i = 0;
	while i<nbClusters :
		C[i].append(numeros_centres[i]);
		i = i+1;	
	
	
	while entree1 or (calcul_distance_centres(centres, centres_nouv) > 0.0 and compteur < K):## condition darret plus de modification des vecteurs moyennes ou compteur depasse
		if (C and entree1 == False) : vider_C(nbClusters);

		centres = list(centres_nouv);
		entree1 = False;
		
		i = 0;
		while i < len(matriceD) :
				k = calcul_plus_proche(matriceD, i, centres);
				if(i not in C[k]) : C[k].append(i);
				i = i+1;
		centres_nouv = calcul_centres_clusters(matriceD, centres_nouv, C);
		
		compteur = compteur +1;
	print(compteur);


if __name__ == '__main__':
	
	matrice = np.genfromtxt("matrice_alleles2.txt", delimiter = " ");
	print(matrice);
	#f = open("Kmeans/result_kmeans_3-50-1-2-5.txt", 'a');
	C = [[]];
	print(C);
	#ecriture dans fichier 1 ligne = 1 cluster
	#i = 0;
	#while i < len(C) :
	#	np.savetxt(f, C[i], fmt = '%1.0f', newline = ',');
	#	f.write("\n");
	#	i = i+1;
	k = 0
	numeros_centres = [];
	#test nombre de groupes obtenus en fonction des centres de depart
	#while k < 50 :
	#	l = 0;
	#	del(numeros_centres[:]);
	#	C = [[]];
	#	centres = choix_k_alea(matrice, 3, numeros_centres, C); 
	#	kmeans(matrice, 3, 50, centres, C);
	#	print("k :");
	#	print(k);
	#	print(C);
	#	f.write("%d %d %d %d"%(numeros_centres[0], numeros_centres[1], numeros_centres[2], len(C)));
	#	while l < len(C) :
	#		f.write(" %d "%(len(C[l])));
	#		l = l+1;
	#	f.write("\n");
	#	k = k+1;
	#	vider_C(3);
	#tps2 = time.clock();
	#print("temps");
	#print(tps2-tps1);	
	
	#test nombre de groupes obtenus en fonction de depart non aleatoires
	#k = 2
	#while k < 215 : 
	#	l = 0;
	#	C = [[]];
	#	numeros_centres = [0,1,k];
	#	centres = choix_k_nonAlea(matrice, 3, numeros_centres, C);
	#	kmeans(matrice, 3, 50, centres, C);
	#	f.write("%d %d %d %d"%(numeros_centres[0] + 1, numeros_centres[1]+1, numeros_centres[2]+1, len(C)));
	#	while l < len(C) :
	#		f.write(" %d "%(len(C[l])));
	#		l = l+1;
	#	f.write("\n");
	#	k = k+1;
	#	vider_C(3);	
	#print(C);
	
	k = 5;
	#ecriture dans un fichier 1 espece dans un groupe = 1 ligne
	while k < 215 :  
		C = [[]];
		nomfichier = "Kmeans/result_kmeans_3-50-1-2-" + str(k) + ".txt";
		f = open(nomfichier, 'a');
		numeros_centres = [0,1,k];
		centres = choix_k_nonAlea(matrice, 3, numeros_centres, C);
		kmeans(matrice, 3, 50, centres, C);
		i = 0;
		while i < len(matrice) :
			j = 0; 
			while i not in C[j] : 
				j = j+1;
			f.write("%d %d\n"%(i+1, j+1));
			i = i+1
		k = k+1
		vider_C(3);
		f.close();
	
	
	
	
			
