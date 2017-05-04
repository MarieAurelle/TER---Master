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