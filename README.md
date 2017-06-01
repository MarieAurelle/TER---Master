# TER---Master

DBSCAN : 
effectue l'algo DBSCAN avec des paramètres choisis par l'utilisateur (MinPts, epsilon, point de depart)
et ecrit le resultat dans un fichier sous la forme 1 espece par ligne avec le numero de son groupe

cree un fichier "epsDBSCAN.txt" qui donne le resultat de DBSCAN pour MinPts fixé à 5 et le point de depart à la 1ere espece
mais pour tous les epsilons entre 1 et 100. Format du fichier par ligne : epsilon nombre de clusters nombre d'especes dans le Bruit nombre d'especes dans chaque cluster
 

KMEANS : 
effectue l'algo kmeans avec en entrée : 
- une matrice indiquant pour chaque espece quel est l allele de chacun des genes (1 pour le bon allele, 0 pour les autres)
- un nombre de clusters
- un nombre d iterations maximal

ecrit le resultat dans un fichier sous la forme 1 espece par ligne avec le numero de son groupe. Il faut changer le code du main pour choisir un mode aleatoire du choix des premiers centres. 


Neighbor-Joining : 
effectue l'algo de Neighbor-Joining sur une matrice de distances donnée en entrée.

L'algorithme va calculer à chaque itération une nouvelle matrice de distance, choisir lesdeux points se situant à la distance minimale, les relier en un nouveau point (on réutilise dans l'algorithme le premier point choisit dans la paire et on le renomme dans un tableau pour lui donner comme nom la concaténation des deux points reliés) et on recalcule la matrice de distance de base avec ce nouveau et ainsi de suite jusqu'à ce qu'il n'y ai plus qu'un point à relier. On stocke tous les arcs créés dans une liste de dictionnaire et ne reste plus qu'a afficher cette liste sous la forme d'un arbre.




distance_edition.py : contient les fonctions permettant d'obtenir les matrices à 
partir de deux fichiers en entrée (SNPlist.txt et STlist.txt)


distance_clustering.py : contient les fonctions permettant de comparer deux clustering à l'aide de fichiers 
contenant deux colonnes, l'une pour le numéro de l'individu l'autre pour le numéro du cluster



Les STlist et SNPlist de M.abscessus sont disponibles dans le répertoire

Les matrices le sont également, donc il est possible de lancer les algorithmes 
sans avoir au préalable lancé les calculs de distances d'édition