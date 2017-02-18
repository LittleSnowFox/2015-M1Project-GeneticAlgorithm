.Manuel de l’utilisateur.

Ce manuel a été conçu par des bioinformaticiens dans le but de mettre à disposition de biologistes ou de chercheurs, un descriptif complet d’utilisation de ce logiciel.
Il contient un algorithme génétique permettant de comparer des données d’expression et d’epigénétiques de distances euclidiennes (en 3D) afin de regrouper des données –omics en clusters par profil de similarité.

L’outil prend en entrée deux (2) fichiers au format « .txt » :
L’un relatif aux données epigénétiques organisé en colonnes comprenant le numéro d'accession du gène, le numéro du chromosome sur lequel il se situe, et ses coordonées (x,y,z) dans l’espace ;
L’autre relatif aux données d’expression organisé en colonnes comprenant le numéro d'accession du gène et un vecteur d’expression 

L’utilisateur a la possibilité de pré-Visualiser ses données, i.e d’observer leur conformation spatiale (3D) et temporelle (données expression a un temps « t »).

Les paramètres de l’algorithme génétique sont multiples ; ce qui permet à l’utilisateur de les modifier à sa guise. Il s’agit du :
Taux de mutation : initialisé à 5% par défaut. Il permet de diversifier la population et varie entre 0 et 100%. Il est recommandé de ne jamais dépasser les 5% afin de ne pas dépasser l’équilibre minimal.
Le nombre d’individu : initialisé à 20 par défaut. Ce qui est largement suffisant. Cependant il est préférable de l’adapter au jeu de données dont on dispose sans toute fois dépasser de 200 individus .Passé ce seuil, le temps de calcule du programme dépassera probablement trois (3) heures.
Nombre de clusters. Il générer par défaut dans l’implémentation de l’outil mais l’utilisateur a la possibilité de générer le nombre de cluster qu’il souhaite en fonction du type de données et de l’objectif visé. 
Nombre de run de l’algorithme : il varie entre 50 et 100 000. Il s’agit du nombre de fois que l’utilisateur fera appel à l’algorithme génétique sur lequel se base l’outil afin de générer des populations.


Il est possible de visualiser le temps de calcul du programme qui s’affiche automatiquement dès que le programme cesse de tourner. Ce temps est visible avec l’option « Timer ». Dès lors, il est possible de sauvegarder le résultat avec l’option « save as ». On peut aussi observer les données sous forme de clusters avec l’option « visualize your result » et ainsi les interpréter.
Enfin, pour quitter la fenêtre, il suffit de quitter sur le bouton « QUIT ».

