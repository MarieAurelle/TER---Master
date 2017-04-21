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
def dbscan(matriceD, eps, MinPts, depart) :
	 ##initialisation##
	 visite = init_visite(len(matriceD));
	 i = 0;
	 compteurEspeces = depart -1;
	 PtsVoisins = [];
	 compteurCluster = 0; 
	 C = [[]]; # liste de listes contenant chacune un cluster
	 
	 ##boucle principale## 
	 while i < len(matriceD) :
		 if visite[compteurEspeces] == "NON" :
			 visite[compteurEspeces] = "OUI";
			 PtsVoisins = epsilonVoisinage(matriceD, compteurEspeces+1, eps);
			 if len(PtsVoisins) < MinPts :
				 Bruit.append(compteurEspeces+1);
			 else : 
				etendreCluster(matriceD, compteurEspeces+1, PtsVoisins, eps, MinPts, compteurCluster, visite, C);
				compteurCluster = compteurCluster + 1;
		 i = i+1;
		 compteurEspeces = (compteurEspeces + 1)%len(matriceD)
	 return C; 
				
		
## Fonction permettant de vider la liste de clusters C ##
def vider_C() :
	i = 0;
	while i < len(C) :
		del(C[i][:]);
		i = i+1;

####  Fonction main   ####
if __name__ == '__main__':

	### Algo DBSCAN ### 
	Ctemp = [[]];
	matrice = np.genfromtxt("matrice.txt", delimiter = " ");
	print(matrice);
	
	print("Saisie de MinPts\n");
	MinPts = input();
	print("Saisie d epsilon\n");
	eps = input();
	print("Saisie de depart\n");
	depart = input();

	Ctemp = dbscan(matrice, eps, MinPts, depart);
	## sortie fichier 1 ligne = 1 espece dans un groupe ##
	nomfichier = "result_DBSCAN_" + str(eps) + "-" + str(MinPts) + "-" + str(depart) + ".txt";
	fichier = open(nomfichier, 'a');
	i = 1;
	while i <= len(matrice) :
		if i in Bruit :
			fichier.write("%d 0\n"%(i));
		else :
			j = 0; 
			while i not in Ctemp[j] : 
				j = j+1;
			fichier.write("%d %d\n"%(i, j+1));
		i = i+1;
	
	k = 100;
	l = 0;
	tps1 = time.clock();
	f = open("epsDBSCAN.txt", 'w');
	
	#test nombre de groupes obtenus en fonction d epsilon
	while k > 0 :
		l = 0;
		del(Bruit[:]);
		Ctemp = dbscan(matrice, k, 5, 1);
		print("k :");
		print(k);
		print(Ctemp);
		f.write("%d %d %d"%(k, len(Ctemp), len(Bruit)));
		while l < len(Ctemp) :
			f.write(" %d "%(len(Ctemp[l])));
			l = l+1;
		f.write("\n");
		k = k-1;
	tps2 = time.clock();
	print("temps");
	print(tps2-tps1);	
	f.close();
