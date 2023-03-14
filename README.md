TODO :

 - ajouter RPN pour xlim et ylim
 - gestion fichier (avec analyse format)
 - ajout constantes dans l'expression (venants de fichier)
 - les constantes peuvent être elles mêmes des expressions
 - fonction depuis fichiers

Paramètres CLI :
 - une ou plusieurs expressions entre guillemets OK
 - -x pour changer les bornes x (suivi de deux int/float) OK
 - -y pour forcer les bornes y (suivi de deux int/float) OK
 - -v pour changer la variable du graphique (def x) OK
 - -n pour changer le nombre de point (def 100000?) OK
 - -i pour forcer les entrées à être des entiers (linspace -> floor -> unique) OK
 - -xlog/-ylog pour mettre l'axe en échelle logs OK
 - -z pour forcer 0 à être dans l'échelle verticale (override les commandes -y) OK

 - -xl/-yl pour ajouter un titre aux axes OK
 - -t pour ajouter un titre au graphique OK
 - -rl pour retirer la légende OK
 - --no-plot pour ne pas plot la fonction

 - --zeros pour calculer les zéros

 - -s pour enregistrer la figure au lieu de la show (avec nom fichier)
 - -c pour charger des constantes (soit un nom de fichier, soit de la forme "a=123;b=3214;c=324")
 - -f pour charger un fichier contenant des points (possible de le faire plusieurs fois)
 - -d pour enregistrer les valeurs des points des fonctions dans un fichier csv
 - -r pour lire les équations depuis un ou plusieurs fichiers (une par ligne)
 - -p pour charger des fonctions customs (dans un fichier python avec un décorateur spécifique)
