#!/usr/bin/env python
# -*- coding: utf-8 -*
import numpy as np
import time
import random
from sklearn.cluster import DBSCAN

####################################
##### Algorithme DBSCAN ############
###################################
	
Bruit = []; # liste contenant les especes ne pouvant etre classees dans un cluster et donc associee a du bruit


## initialisation de la liste visite indiquant si l espece a deja ete traitee ###
def init_visite(nbElements) :
	visite = [];
	i = 0;
	while i < nbElements:
		visite.append("NON");
		i = i+1;
	return visite;

## fonction permettant de faire l union de deux listes en conservant l ordre : liste1 puis elements de liste2 n appartenant pas a liste1 ##
def union(liste1, liste2) :
	i = 0;
	while i < len(liste2) :
		if(liste2[i] not in liste1): liste1.append(liste2[i]);
		i = i+1;
	return liste1;
	
## determine si l espece P est deja classee dans un cluster ##
def membreCluster(P, C) : 
	i = 0;
	while i < len(C) :
		if P in C[i] : return True;
		i = i+1;
	return False;
	
## renvoie les especes dont la distance  par rapport a l espece P est inferieure a eps ##	
def epsilonVoisinage(matriceD, P, eps) :
	i = 0;
	PtsVoisins = [];
	
	while i < len(matriceD[0]) : 
		if (P-1 != i) and (matriceD[P-1,i] <= eps) :
			PtsVoisins.append(i+1);
		i = i+1;
		
	return PtsVoisins;


## ajoute au cluster de P les especes voisines de P et les voisines de ces voisines sauf si elles appartiennent deja a un autre cluster ##
def etendreCluster(matriceD, P, PtsVoisins, eps, MinPts, compteurClusters, visite, C) :
	listeVide = [];
	if(compteurClusters > 0) : C.append(listeVide);
	
	C[compteurClusters].append(P);
	i = 0;
	PtsVoisinsBis = [];
	
	while i < len(PtsVoisins) :
		if visite[PtsVoisins[i]-1] == "NON" :
			visite[PtsVoisins[i]-1] = "OUI";
			PtsVoisinsBis = epsilonVoisinage(matriceD, PtsVoisins[i], eps);
			if len(PtsVoisinsBis) >= MinPts :
				PtsVoisins = union(PtsVoisins, PtsVoisinsBis);
		if membreCluster(PtsVoisins[i], C) == False : 
			C[compteurClusters].append(PtsVoisins[i]);
			if(PtsVoisins[i] in Bruit) : Bruit.remove(PtsVoisins[i]);
				
		i = i+1;

## algorithme DBSCAN ##
def dbscan(matriceD, eps, MinPts, ordre) :
	 ##initialisation##
	visite = init_visite(len(matriceD));
	i = 0;
	PtsVoisins = [];
	compteurCluster = 0; 
	C = [[]]; # liste de listes contenant chacune un cluster
	 
	 ##boucle principale## 
	while i < len(ordre) :
		if visite[ordre[i]-1] == "NON" :
			visite[ordre[i]-1] = "OUI";
			PtsVoisins = epsilonVoisinage(matriceD, ordre[i], eps);
			if len(PtsVoisins) < MinPts :
				Bruit.append(ordre[i]);
			else : 
				etendreCluster(matriceD, ordre[i], PtsVoisins, eps, MinPts, compteurCluster, visite, C);
				compteurCluster = compteurCluster + 1;
		i = i+1;
	return C; 
				
		
## Fonction permettant de vider la liste de clusters C ##
def vider_C() :
	i = 0;
	while i < len(C) :
		del(C[i][:]);
		i = i+1;

##Fonctions de sortie##
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

## Fonction permettant de choisir aleatoirement l ordre de traitements
# des individus
def choix_depart_alea(nbEspeces) :
	liste = [];
	i = 0;
	while i < nbEspeces :
		alea = random.randint(1,nbEspeces);
		while alea in liste :
			alea = random.randint(1,nbEspeces);
		liste.append(alea);
		i = i+1;
		print(i);
		print(alea);
	return liste;

##Calcule le diametre des cluster
## et les stocke dans une liste
def calcul_diametre(C, matrice) :
	liste_diam = [];
	i = 0
	while i < len(C) : #chaque cluster
		j = 0
		k = 0
		maximum = matrice[C[i][j]-1][C[i][k]-1];
		while j < len(C[i]) : # interieur d un cluster
			k = j;
			while k < len(C[i]) :
				temp = matrice[C[i][j]-1][C[i][k]-1];
				if temp > maximum :
					maximum = temp;
				k = k+1;
			j = j+1;
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
		somme = 0.0;
		while j < len(C[i]) : # interieur d un cluster
			k = j;
			while k < len(C[i]) :
				somme += matrice[C[i][j]-1][C[i][k]-1];
				k = k+1;
			j = j+1;
		if(len(C[i]) > 1 ) : liste_moy.append(somme/((len(C[i])*(len(C[i])-1))/2.0));
		else : liste_moy.append(somme);
		i = i+1;
	return liste_moy;


##Calcule la distance moyenne inter cluster entre tous les clusters
## et les stocke dans une liste
def calcul_dist_intercluster(C, matrice) :
	liste_moy = [];
	i = 0
	while i < len(C) :
		j = i+1
		while j < len(C) :
			somme = 0.0;
			k = 0
			while k < len(C[i]) :
				m = 0 
				while m < len(C[j]) :
					somme += matrice[C[i][k]-1][C[j][m]-1];
					m = m+1;
				k = k+1;
			liste_moy.append(somme/(len(C[i])*len(C[j])));
			j = j+1;
		i = i+1;
	return liste_moy;
	print(liste_moy);


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
	print(liste_dist);

##Permet d'obtenir une liste de clusters a partir de la sortie de l algorithme du package
def convertisseur(dbscan) :
	nb_clusters = len(set(dbscan.labels_)) - (1 if -1 in dbscan.labels_ else 0)
	C = [];
	for i in range(nb_clusters) :
		liste = []
		C.append(liste) 
	print(C);
	for j in range(215) :
		if(dbscan.labels_[j] == -1) : Bruit.append(j);
		else : C[dbscan.labels_[j]].append(j);
	return C
	
####  Fonction main   ####
if __name__ == '__main__':
	
	### Algo DBSCAN  ### 
	matrice = np.genfromtxt("matrice.txt", delimiter = " ");
	print(matrice);

	tps1 = time.clock();
	depart = range(1,216)
	C = [];
	print("Saisie de MinPts\n");
	MinPts = input();
	print("Saisie d epsilon\n");
	eps = input();
	C = dbscan(matrice, eps, MinPts, depart);
	tps2 = time.clock();
	print(tps2-tps1);	
	
	sortie_ligne_espece("result_DBSCAN"+str(eps)+"-"+str(MinPts) + ".txt", matrice, C);
	
	liste_diam = calcul_diametre(C, matrice);
	liste_moy_intra = calcul_dist_moyenne(C, matrice);
	liste_moy_inter = calcul_dist_intercluster(C, matrice);
	liste_min = calcul_distance_inter_minimale(C, matrice);
	
	print(liste_diam)
	print(liste_moy_intra)
	print(liste_moy_inter);
	print(liste_min);
	
	#### Algo DBSCAN avec le package ########
	print("Saisie de MinPts\n");
	MinPts = input();
	print("Saisie d epsilon\n");
	eps = input();
	dbscan = DBSCAN(eps = eps, min_samples = MinPts, metric = 'precomputed', algorithm = 'auto')
	dbscan.fit(matrice);
	print(dbscan)
	print(dbscan.labels_)
	C = convertisseur(dbscan);
	
	liste_diam = calcul_diametre(C, matrice);
	liste_moy_intra = calcul_dist_moyenne(C, matrice);
	liste_moy_inter = calcul_dist_intercluster(C, matrice);
	liste_dist_min = calcul_distance_inter_minimale(C, matrice);
		
	print(liste_diam);
	print(liste_moy_intra);
	print(liste_moy_inter);
	print(liste_dist_min);
	
	
	
	
	

	
	
	

