#!/usr/bin/env python
# -*- coding: utf-8 -*

import numpy as np
import random
import time
from math import sqrt
from sklearn.cluster import KMeans


## Fonction permettant de vider la liste de clusters C ##
def vider_C(C, nbClusters) :
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
def kmeans(matriceD, nbClusters, K, centres, C, numeros_centres) :	
	entree1 = True;
	centres_nouv = list(centres);
	compteur = 0;
	
	## ajout des premiers centres comme premier element de chaque cluster ##
	i = 0;
	while i<nbClusters :
		C[i].append(numeros_centres[i]);
		i = i+1;	
	print(C);
	
	while entree1 or (calcul_distance_centres(centres, centres_nouv) > 1e-4 and compteur < K):## condition darret plus de modification des vecteurs moyennes ou compteur depasse
		print(compteur);
		
		if (C and entree1 == False) : vider_C(C, nbClusters);

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
	print(C);
	return centres_nouv;

##Calcul la somme des carres des distances de chaque element dun cluster a son centre
## pour chaque cluster	
def calcul_somme_carres(matrice, C, centres) :
	i = 0
	liste_somme_carres = []
	while i < len(C) :
		j = 0
		somme = 0.0
		while j < len(C[i]) :
			somme += calcul_distance_vecteurs(matrice, C[i][j], centres[i]);
			j = j+1
		liste_somme_carres.append(somme);
		i = i+1
	i = 0
	somme_Tot = 0.0
	while i < len(C) :
		somme_Tot += liste_somme_carres[i];
		i = i+1
	return somme_Tot;
		

## Fonctions de sortie ##
## 1 individu par ligne avec le numero du cluster
## les individus sont ranges par ordre croissant de numero
def sortie_ligne_espece(C, matrice, nom_fichier) :
	fichier = open(nom_fichier, 'w');
	i = 0;
	while i < len(matrice) :
		j = 0; 
		while i not in C[j] : 
			j = j+1;
		fichier.write("%d %d\n"%(i+1, j+1));
		i = i+1;
	fichier.close();

## tous les numeros de clusters des individus sur la meme ligne
##les individus sont ranges par ordre croissant de numero
def sortie_ligne_cluster(C, matrice, nom_fichier) :
	fichier = open(nom_fichier, 'w');
	i = 0;
	while i < len(matrice) :
		for j in range(0, len(C)) :
			if i in C[j] : fichier.write("%d "%(C[j]));
		i = i+1;

##Calcule le diametre des cluster
## et les stocke dans une liste
def calcul_diametre(C, matrice) :
	liste_diam = [];
	i = 0
	while i < len(C) : #chaque cluster
		j = 0
		maximum = 0.0
		while j < len(C[i]) :
			k = j+1
			temp = 0.0
			while k < len(C[i]) :
				l = 0
				print(k);
				while l < len(matrice[0]) :
					temp += (matrice[C[i][j]][l] - matrice[C[i][k]][l])*(matrice[C[i][j]][l] - matrice[C[i][k]][l]);
					l = l+1
				temp = sqrt(temp)
				if temp > maximum :
					maximum = temp;
					print(maximum);
				k = k+1
			j = j+1
		liste_diam.append(maximum);
		i = i+1;
	return liste_diam;

##Calcule la distance moyenne intra cluster de tous les clusters
## et les stocke dans une liste
def calcul_dist_moyenne(C, matrice) :
	liste_moy = [];
	i = 0
	while i < len(C) : #chaque cluster
		j = 0
		somme = 0.0
		while j < len(C[i]) :
			k = j+1
			temp = 0.0
			while k < len(C[i]) :
				l = 0
				print(k);
				while l < len(matrice[0]) :
					temp += (matrice[C[i][j]][l] - matrice[C[i][k]][l])*(matrice[C[i][j]][l] - matrice[C[i][k]][l]);
					l = l+1
				temp = sqrt(temp)
				somme += temp;
				print(somme)
				k = k+1
			j = j+1
		if len(C[i]) > 1 :
			liste_moy.append(somme/((len(C[i])*(len(C[i])-1))/2));
		i = i+1;
	return liste_moy;

##Calcule la distance moyenne inter cluster entre tous les clusters
## et les stocke dans une liste
def calcul_dist_intercluster(C, matrice) :
	liste_moy = [];
	i = 0
	while i < len(C) : #chaque cluster
		m = i+1
		while m < len(C) :
			somme = 0.0
			j = 0
			while j < len(C[i]) :
				k = 0
				temp = 0.0
				while k < len(C[m]) :
					l = 0
					print(k)
					while l < len(matrice[0]) :
						temp += (matrice[C[i][j]][l] - matrice[C[m][k]][l])*(matrice[C[i][j]][l] - matrice[C[m][k]][l]);
						l = l+1
					print(k)
					print(j);
					temp = sqrt(temp)
					somme += temp;
					print(somme)
					k = k+1
				j = j+1
			print(len(C[i]));
			print(len(C[m]));
			liste_moy.append(somme/(len(C[i])*len(C[m])));
			m = m+1
		i = i+1;
	return liste_moy;

##Calcule la distance inter cluster minimale entre tous les clusters
## et les stocke dans une liste		
def calcul_distance_inter_minimale(C, matrice) :
	liste_dist = [];
	i = 0
	while i < len(C) :
		j = i+1
		while j < len(C) :
			minimum = 215;
			k = 0
			while k < len(C[i]) :
				m = 0 
				print(k)
				while m < len(C[j]) :
					dist = matrice[C[i][k]-1][C[j][m]-1];
					print((i,j));
					print(dist);
					if(dist < minimum) :
						minimum = dist;
					m = m+1;
				k = k+1;
			liste_dist.append(minimum);
			j = j+1;
		i = i+1;
	return liste_dist;
	
##Permet d'obtenir une liste de clusters a partir de la sortie de l algorithme du package	
def convertisseur(kmeans) :
	nb_clusters = len(set(kmeans.labels_));
	C = [];
	for i in range(nb_clusters) :
		liste = []
		C.append(liste) 
	print(C);
	for j in range(215) :
		C[kmeans.labels_[j]].append(j);
	print("C"); 
	print(C)
	return C

if __name__ == '__main__':

	##Algorithme kmeans##
	matrice = np.genfromtxt("matrice_alleles2.txt", delimiter = " ");
	print(matrice);
	
	Cmin = [];
	sommeMin = 10000;
	for j in range(1,10) :
		C = [[]];
		numeros_centres = [];
	
		centres = choix_k_alea(matrice, 3, numeros_centres, C);
		centres = kmeans(matrice, 3, 50, centres, C, numeros_centres); 
		
		somme = calcul_somme_carres(matrice, C, centres);
		print(somme);
		if sommeMin > somme :
			sommeMin = somme;
			Cmin = list(C);
		j = j+1;
		
	liste_diam = calcul_diametre(Cmin, matrice);
	liste_moy_intra = calcul_dist_moyenne(Cmin, matrice);
	liste_moy_inter = calcul_dist_intercluster(Cmin, matrice);	
	liste_min = calcul_distance_inter_minimale(Cmin, matrice);
	print(liste_diam);
	print(liste_moy_intra)
	print(liste_moy_inter)
	print(liste_min);
	
	##Algo Kmeans package##
	kmeans = KMeans(n_clusters = 2, n_init = 100, init = 'k-means++');
	kmeans.fit(matrice);
	C = convertisseur(kmeans);
	
	liste_diam = calcul_diametre(C, matrice);
	liste_moy_intra = calcul_dist_moyenne(C, matrice);
	liste_moy_inter = calcul_dist_intercluster(C, matrice);
	liste_dist_min = calcul_distance_inter_minimale(C, matrice);
		
	print(liste_diam);
	print(liste_moy_intra);
	print(liste_moy_inter);
	print(liste_dist_min);
	
	
	
	
	
			
