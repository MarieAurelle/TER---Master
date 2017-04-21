#!/usr/bin/env python
# -*- coding: utf-8 -*
import numpy as np
import time

##Distance entre clustering##

## Fonction permettant d obtenir une permutation d une suite de nombres
## passee en parametre
## Cette permutation fait tourner les nb derniers nombres de la suite 
## avec le dernier qui passe en premier, le premier en deuxieme etc
def trouve_permut(suite, nb) : 
	liste = [];
	j = 0;
	
	## les positions des premiers nombres de la suite ne sont pas modifiees ##
	for k in range(0, len(suite) - nb) : 
		liste.append(suite[k]);
		
	## les dernieres positions sont inversees ##
	temp = suite[len(suite) - 1];
	liste.append(temp);
	while j < nb - 1 :
		liste.append(suite[len(suite) - nb + j]);
		j = j+1;
	return liste;

## Fonction permettant de trouver toutes les permutations 
## d une suite de nombre passee en parametre
## en conservant la position des premiers nombres
## et ne modifiant que celle des nb derniers nombres
def permuts(nb, permutations) :
	i = 0;
	liste = [];
	
	while i < len(permutations) :
		liste = trouve_permut(permutations[i], nb);
		if(liste not in permutations) :
			permutations.append(liste);
		i = i+1;
		
	return permutations;

## Fonction retournant toutes les permutations possibles d une suite ordonnee
## de nombres de 0 à nbClusters
def toutes_permutations(nbClusters) : 
	i = 2;
	permutations = [[]];
	permutations[0] = range(0, nbClusters);

	while i < nbClusters + 1 :
		permutations = permuts(i, permutations);
		i = i+1;
	return permutations;
		
def calcul_distance(fichier1, fichier2, nouveauNoClusters) :
	cluster1 = -1;
	cluster2 = -1;
	nbDiff = 0;
	
	i = 0;
	for ligne in fichier1.readlines():
		cluster1 = ligne.split(" ")[1];
		cluster2 = fichier2.readline().split(" ")[1];
		cluster2 = nouveauNoClusters[int(cluster2)];
		if(int(cluster1) != int(cluster2)) : nbDiff = nbDiff + 1;
		i = i+1;
	return nbDiff;

def distance_clustering(nomfichier1, nomfichier2, nbClusters) :
	fichier1 = open(nomfichier1, 'r');
	fichier2 = open(nomfichier2, 'r');
	print(nomfichier1);
	print(nomfichier2);
	
	permutations = [[]];
	permutations = toutes_permutations(nbClusters);
	nbDiff = 0;
	i = 1;
	
	minimum = calcul_distance(fichier1, fichier2, permutations[0]);
	
	while i<len(permutations) :
		fichier1.seek(0);
		fichier2.seek(0);
		nbDiff = calcul_distance(fichier1, fichier2, permutations[i]);
		if(nbDiff < minimum) : 
			minimum = nbDiff;
		i = i+1;
		
	fichier1.close();
	fichier2.close();
	return minimum;	
		
	
	
	
if __name__ == '__main__':
	print("Saisie nom fichier 1");
	nomfichier1 = raw_input();
	print("Saisie nom fichier 2 ");
	nomfichier2 = raw_input();
	print("Saisie nombre clusters ");
	nbClusters = raw_input();

	dist = distance_clustering(nomfichier1, nomfichier2, int(nbClusters)); 
	print("distance");
	print(dist);
	

