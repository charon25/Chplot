TODO :

 - gestion fichier (avec analyse format)
 - ajout constantes dans l'expression (venants de fichier)
 - fonction depuis fichiers

Paramètres CLI :
 - une ou plusieurs expressions entre guillemets
 - -v pour changer la variable du graphique (def x)
 - -c pour charger des constantes (soit un nom de fichier, soit de la forme "a=123;b=3214;c=324")
 - -f pour charger un fichier contenant des points (possible de le faire plusieurs fois)
 - -p pour charger des fonctions customs (dans un fichier python avec un décorateur spécifique)
 - -s pour enregistrer la figure au lieu de la show (avec nom fichier)
 - -x pour changer les bornes x (suivi de deux int/float)
 - -ex/-ey pour changer l'échelle du graphique (suivi par lin ou log, def lin)
 - -d pour enregistrer les valeurs des points des fonctions dans un fichier csv
 - -n pour changer le nombre de point (def 100000?)
 - -i pour forcer les entrées à être des entiers (linspace -> floor -> unique)
 - -r pour lire les équations depuis un ou plusieurs fichiers (une par ligne)
