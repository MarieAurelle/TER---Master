####################################
##### Algorithme DBSCAN ############
###################################
	
Bruit = []; # liste contenant les especes ne pouvant etre classees dans un cluster et donc associee a du bruit
C = [[]]; # liste de listes contenant chacune un cluster

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
def membreCluster(P) : 
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
def etendreCluster(matriceD, P, PtsVoisins, eps, MinPts, compteurClusters, visite) :
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
		if membreCluster(PtsVoisins[i]) == False : 
			C[compteurClusters].append(PtsVoisins[i]);
			if(PtsVoisins[i] in Bruit) : Bruit.remove(PtsVoisins[i]);
				
		i = i+1;

## algorithme DBSCAN ##
def dbscan(matriceD, eps, MinPts) :
	 ##initialisation##
	 visite = init_visite(len(matriceD));
	 i = 0;
	 PtsVoisins = [];
	 compteurCluster = 0; 
	 
	 ##boucle principale## 
	 while i < len(matriceD) :
		 if visite[i] == "NON" :
			 visite[i] = "OUI";
			 PtsVoisins = epsilonVoisinage(matriceD, i+1, eps);
			 if len(PtsVoisins) < MinPts :
				 Bruit.append(i+1);
			 else : 
				etendreCluster(matriceD, i+1, PtsVoisins, eps, MinPts, compteurCluster, visite);
				compteurCluster = compteurCluster + 1;
		 i = i+1;
	 return C; 
				
		


####  Fonction main   ####
if __name__ == '__main__':
	
	### Algo DBSCAN ### 
	matrice = np.genfromtxt("matrice.txt", delimiter = " ");
	print(matrice);
	print("Saisie d epsilon");
	eps = input();
	
	print("Saisie de MinPts");
	MinPts = input();
	
	f = open("result_DBSCAN.csv", 'a');
	dbscan(matrice, int(eps), int(MinPts));
	i = 0;
	while i < len(C) :
		np.savetxt(f, C[i], fmt = '%1.0f', newline = ',');
		f.write("\n");
		i = i+1;
	print(C);
	print(Bruit);
	f.close();
