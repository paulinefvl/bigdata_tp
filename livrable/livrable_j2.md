## Synthèse

### 1. Différence entre une collection MongoDB et un DataFrame Spark
Une collection MongoDB **stocke** durablement des documents JSON sur disque : les données
restent disponibles après l'arrêt du programme, et chaque document peut avoir sa propre
structure (par exemple, `products` imbriqué dans un panier). Un DataFrame Spark est une
structure de **traitement** : un tableau distribué, avec des colonnes nommées et un schéma
commun, qui n'existe que pendant la session Spark. Dans notre projet, MongoDB conserve les
données brutes (`raw_commandes`, `raw_payments`) et Spark les lit pour les calculer.

### 2. Différence entre une transformation et une action
Une transformation (`select`, `filter`, `withColumn`, `groupBy`, `join`, `orderBy`)
décrit une opération et renvoie un nouveau DataFrame, sans rien calculer. Une action
(`show`, `count`, `collect`, `write`) déclenche réellement le calcul et renvoie un
résultat concret : un affichage, un nombre ou une liste.

### 3. Pourquoi parle-t-on de lazy evaluation ?
Parce que Spark est « paresseux » : il enregistre les transformations sous forme de plan
sans les exécuter, et n'exécute ce plan qu'au moment d'une action. Nous l'avons observé :
la cellule de transformations s'est exécutée en 0,0 s, sans créer de job dans Spark UI,
alors que le `show()` en a déclenché un. Ce fonctionnement permet à Spark d'optimiser le
plan complet avant de l'exécuter : `explain()` montre qu'il ne lit que les 2 colonnes
utiles sur 17.

### 4. Rôle des partitions, des Jobs, des Stages et des Tasks
- **Partition** : un morceau des données, et l'unité de parallélisme. Nos 800 lignes
  étaient dans 1 partition, puis dans 4 partitions de 200 lignes après `repartition(4)`.
- **Job** : déclenché par une action ; une action peut créer plusieurs jobs.
- **Stage** : une étape d'un job ; les stages sont séparés par les shuffles
  (redistributions de données, causées par `repartition` ou `groupBy`).
- **Task** : le travail sur une partition ; un stage exécute une task par partition.
  Nous avons observé un stage de 4 tasks (stage 21), puis un stage final d'une seule task
  qui rassemble les résultats (stage 24).

### 5. Pourquoi calculer le CA encaissé uniquement à partir des paiements PAID ?
Parce que seuls les paiements acceptés correspondent à de l'argent réellement reçu. Un
paiement refusé n'apporte rien, et un paiement en attente n'est pas encore confirmé. En
les comptant, on surestimerait le chiffre d'affaires : dans notre simulation, le montant
total des paniers est de 3 456 709,58, mais seuls 2 322 729,73 sont encaissés, soit
environ 1 134 000 d'écart.

## Analyse courte

**Répartition des paiements** : sur 208 paniers, la simulation donne 145 PAID (69,7 %),
42 REFUSED (20,2 %) et 21 PENDING (10,1 %), très proches des probabilités cibles de
70 / 20 / 10 %. Un seul paiement par panier a été généré (208 paiements pour 208
`cart_id` distincts). Le montant encaissé (PAID) est de 2 322 729,73, soit environ 67 %
du montant total des paniers.

**Lazy evaluation** : les transformations ne déclenchent aucun calcul. Spark construit un
plan, l'optimise (lecture des seules colonnes utiles, filtre transmis à MongoDB), puis
l'exécute au moment d'une action. Dans Spark UI, aucun job n'apparaît après la définition
des transformations, et un nouveau job apparaît après le `show()`.

