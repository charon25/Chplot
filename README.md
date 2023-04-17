TODO :

 - voir pour que des trucs genre 3x ou 4sin(x) fonctionnent
 - fonction depuis fichiers
 - revoir le nom et l'emplacement des loggers

Paramètres CLI :
 - une ou plusieurs expressions entre guillemets OK
 - -x pour changer les bornes x (suivi de deux expressions mathématiques (inclue int ou float) ; ATTENTION à ne pas commencer l'expression par un tiret (mettre 0-EXP plutôt que -EXP)) OK
 - -y pour forcer les bornes y (suivi de deux int/float) OK
 - -v pour changer la variable du graphique (def x) OK
 - -n pour changer le nombre de point (def 100000?) OK
 - -i pour forcer les entrées à être des entiers (linspace -> floor -> unique) OK
 - -xlog/-ylog pour mettre l'axe en échelle logs OK
 - -z pour forcer 0 à être dans l'échelle verticale (override les commandes -y) OK

 - -xl/-yl pour ajouter un titre aux axes OK
 - -t pour ajouter un titre au graphique OK
 - -rl pour retirer la légende OK
 - --no-plot pour ne pas plot la fonction OK
 - --dis pour enlever les interpolations linéaires OK

 - --zeros pour calculer les zéros OK
 - --integral pour calculer l'intégrale sur l'interval considéré OK
 - --deriv pour afficher des dérivées (suivies par une liste d'ordre de dérivation) OK

 - -s pour enregistrer la figure (avec nom fichier)
 - -c pour charger des constantes (au moins 1 paramètres, soit de la forme "\<nom\>=\<expression\>" soit un fichier contenant ce format, un par ligne) OK
 - -f pour charger un fichier contenant des points (possible d'en mettre plusieurs)
 - -d pour enregistrer les valeurs des points des fonctions dans un fichier csv
 - -e pour lire les équations depuis un ou plusieurs fichiers (une par ligne)
 - -p pour charger des fonctions customs (dans un fichier python avec un décorateur spécifique)
