# Système de transport de passagers
## Objectif
Ce programme modélise un système de transport de passagers entre plusieurs stations, en gérant les itinéraires, les segments de trajet (legs), les origines-destinations (OD) et les passagers.

## les principales classes  : 
- Service : Attribut => name ; departure_date ; legs ; ods.
- Leg : Attribut => origin, destination.
- OD : Attribut => origin, destination, passengers.
- Passenger : Attribut => origin, destination, sale_day_x, price.

## Fonctionnalités principales

- Gestion de l'itinéraire via la méthode  `itinerary`
- Détermination des segments(legs) parcourus par une OD( origine_destination) via la méthode `legs`
- Création automatique des segments et des OD via la méthode `load_itinerary`
- Associer les passagers aux OD correspondantes.
- Retourner la liste des passagers qui occupent un soège sur un segement via la méthode `passengers`
- Génèrer un rapport des ventes pour chaque OD via la méthode `history`
> Pour des contraintes de temps, la dernière fonctionalité,  qui concerne le chemin maximisant la somme des valeurs dans une matrice, n'a pas été developpé.

## Utilisation du code 
La définition des classes ainsi que les méthodes ajoutées sont disponibles dans le fichier `booking_reports.py`. Le code est hebergé sur un repository sur GitHub.
Pour l'utiliser il suffit de saisir la commande suivante dans un terminal : 
```bash
git clone https://github.com/ayyoubiyouness/booking_reports_test.git .
```

Et enfin pour tester le fonctionnement du code, il suffit de lancer la commande suivante dans la racine du projet : 
```bash
python booking_reports.py
```

