#!/usr/bin/env python3
# -*- coding: utf-8 -*
import numpy as np
import time
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

def affichage_PCA_neighbor(nom_fichier) :
	matrice = np.genfromtxt("matrice.txt", delimiter = " ");
	print(matrice);
	reduced_data = PCA(n_components=2).fit_transform(matrice)
	print(reduced_data)
	print(reduced_data.shape)
	clustering = np.loadtxt(nom_fichier);
	print(clustering)
	print(clustering.shape)
	
	colors = ['y', 'r', 'b', 'g']
	plt.figure(figsize=(4,4))
	for i in range(4) :
		plt.plot(reduced_data[np.where(clustering == i), 0], reduced_data[np.where(clustering==i),1], c=colors[i], marker='o', markerfacecolor = colors[i], markeredgecolor = 'k');
	plt.xlabel("PC1");
	plt.ylabel("PC2");
	plt.title("Représentation d'un clustering \n obtenu par l'algorithme neighbor joining");
	plt.show();

def affichage_PCA_leur_kmeans() :
	matrice = np.genfromtxt("matrice_alleles2.txt", delimiter = " ");
	print(matrice);
	reduced_data = PCA(n_components=2).fit_transform(matrice)
	print(reduced_data)
	
	kmeans = KMeans(n_clusters = 3, n_init = 10);
	print(kmeans)
	kmeans.fit(matrice);
	print(kmeans.labels_)
	
	colors = ['g', 'b', 'r', 'y']
	plt.figure(figsize=(4,4))
	for i in range(4) :
		plt.plot(reduced_data[np.where(kmeans.labels_== i), 0], reduced_data[np.where(kmeans.labels_==i),1], c=colors[i], marker='o', markerfacecolor = colors[i], markeredgecolor = 'k');
	plt.xlabel("PC1");
	plt.ylabel("PC2");
	plt.title("Représentation d'un clustering \n obtenu par l'algorithme k-moyennes");
	plt.show();

def affichage_PCA_notre_kmeans(nom_fichier) :
	matrice = np.genfromtxt("matrice_alleles2.txt", delimiter = " ");
	print(matrice);
	reduced_data = PCA(n_components=2).fit_transform(matrice)
	print(reduced_data)
	print(reduced_data.shape)
	clustering = np.loadtxt(nom_fichier);
	print(clustering)
	print(clustering.shape)
	
	colors = ['y', 'r', 'b', 'g']
	plt.figure(figsize=(4,4))
	for i in range(4) :
		plt.plot(reduced_data[np.where(clustering == i), 0], reduced_data[np.where(clustering==i),1], c=colors[i], marker='o', markerfacecolor = colors[i], markeredgecolor = 'k');
	plt.xlabel("PC1");
	plt.ylabel("PC2");
	plt.title("Représentation d'un clustering \n obtenu par l'algorithme k-moyennes");
	plt.show();

def affichage_PCA_leur_DBSCAN() :
	matrice = np.genfromtxt("matrice.txt", delimiter = " ");
	print(matrice);
	reduced_data = PCA(n_components=2).fit_transform(matrice)
	print(reduced_data)
	
	dbscan = DBSCAN(eps = 40, min_samples = 23, metric = 'precomputed', algorithm = 'auto')
	print(dbscan)
	dbscan.fit(matrice);
	print(dbscan.labels_)
	print(dbscan.get_params(deep=True))
	
	colors = ['g', 'b', 'r', 'y']
	plt.figure(figsize=(4,4))
	for i in range(4) :
		plt.plot(reduced_data[np.where(dbscan.labels_== i), 0], reduced_data[np.where(dbscan.labels_==i),1], c=colors[i], marker='o', markerfacecolor = colors[i], markeredgecolor = 'k');
	plt.xlabel("PC1");
	plt.ylabel("PC2");
	plt.title("Représentation d'un clustering \n obtenu par l'algorithme DBSCAN");
	plt.text(-350, 350, r'$\epsilon=40,\ \ minPts=23$');
	plt.show();
	

def affichage_PCA_notre_DBSCAN(nom_fichier) :
	matrice = np.genfromtxt("matrice.txt", delimiter = " ");
	print(matrice);
	reduced_data = PCA(n_components=2).fit_transform(matrice)
	print(reduced_data)
	clustering = np.loadtxt(nom_fichier);
	print(clustering)
	colors = ['k', 'g', 'b', 'r', 'y']
	plt.figure(figsize=(5,5))
	for i in range(5) :
		if i == 0 :
			p1 = plt.plot(reduced_data[np.where(clustering == i), 0], reduced_data[np.where(clustering==i),1], c=colors[i], marker='o', markerfacecolor = colors[i], markeredgecolor = 'k');
		else :
			plt.plot(reduced_data[np.where(clustering == i), 0], reduced_data[np.where(clustering==i),1], c=colors[i], marker='o', markerfacecolor = colors[i], markeredgecolor = 'k');
	plt.xlabel("PC1");
	plt.ylabel("PC2");
	plt.title("Représentation d'un clustering \n obtenu par l'algorithme DBSCAN");
	plt.text(-350, 350, r'$\epsilon=40,\ \ minPts=22$');
	plt.legend((p1), ["Bruit"]);
	plt.show();
	
if __name__ == '__main__':
	
	print("Saisie nom fichier pour kmeans");
	nomfichier1 = raw_input();
	print("Saisie nom fichier pour dbscan ");
	nomfichier2 = raw_input();
	print("Saisie nom fichier pour neighbor ");
	nomfichier3 = raw_input();
	
	affichage_PCA_notre_kmeans(nomfichier1)
	affichage_PCA_leur_kmeans()
	affichage_PCA_notre_DBSCAN(nomfichier2)
	affichage_PCA_leur_DBSCAN()
	affichage_PCA_neighbor(nomfichier3)
