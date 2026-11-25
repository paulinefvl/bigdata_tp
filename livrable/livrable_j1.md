# Big Data – Jour 1 : BigData Commerce Analytics

Pauline Fauvel & Antoine Ledentu

## Atelier 1 : Explorer les sources de BigData Commerce Analytics

Source : DummyJSON (https://dummyjson.com), données fictives de démonstration
Date de collecte : 25/11/2026

### 1. Inventaire des sources

| Source | Endpoint | Producteur | Format | Volume | Fréquence | Qualité attendue |
|--------|----------|------------|--------|--------|-----------|------------------|
| Produits | /products | DummyJSON | JSON | 194 | À la demande | Bonne (fictive) |
| Paniers | /carts | DummyJSON | JSON imbriqué | 208 | À la demande | Moyenne (date inventée) |
| Utilisateurs | /users | DummyJSON | JSON imbriqué | 208 | À la demande | Moyenne (données sensibles) |
| Commentaires | /comments | DummyJSON | JSON | 340 | À la demande | Faible (hors produits) |

### 2. Évaluation des 5V

| V | Niveau | Justification chiffrée |
|---|--------|------------------------|
| Volume | Faible | 194 produits, 208 paniers, 800 lignes de panier, ~1,7 Mo au total |
| Vitesse | Faible | Données statiques récupérées à la demande, aucun flux continu |
| Variété | Moyen | 8 ressources, JSON imbriqué + CSV aplati, texte libre |
| Véracité | Faible | Données fictives, date inventée, 1 panier par utilisateur (208/208) |
| Valeur | Moyen | Bon pour l'entraînement, aucune décision réelle possible |

### 3. Usages et limites

- **Usage 1 : Analyse des catégories et des prix.** Croiser les paniers et le catalogue
  produits pour identifier les catégories qui pèsent le plus dans les paniers et la
  répartition des prix.
- **Usage 2 : Analyse de panier.** Repérer les produits qui apparaissent souvent ensemble
  dans un même panier, une première étape vers un système de recommandation.

- **Limite 1 : Qualité des données.** Les données sont fictives et la date `order_date`
  est générée par le script : impossible d'analyser les ventes dans le temps. Des
  problèmes techniques (types mal reconnus, doublons, valeurs manquantes) sont aussi
  possibles et devront être vérifiés avant analyse.
- **Limite 2 : Protection de la vie privée.** La ressource `users` contient des champs
  sensibles (mot de passe, numéro de carte, IBAN), fictifs mais à traiter comme des
  données réelles. Selon le RGPD (Règlement Général sur la Protection des Données), il
  faut minimiser les champs conservés et anonymiser les clients : le script de collecte
  retire déjà ces champs.

**Source complémentaire possible :** le jeu de données Kaggle « Brazilian E-Commerce
Public Dataset by Olist », qui contient de vraies commandes datées et des avis clients
liés aux produits. Il comblerait les principales limites de DummyJSON.

## Atelier 2 : Profiler les commandes avec Python

Fichier analysé : `data/processed/commandes_ecommerce.csv`
(une ligne = un produit dans un panier)

### Résultats du profilage

| Contrôle | Résultat |
|----------|----------|
| shape | 800 lignes, 16 colonnes |
| dtypes | `order_date` lue en `str`, à convertir en `datetime` ; les autres colonnes sont bien typées |
| isna | `brand` : 377 valeurs manquantes sur 800 (~47 %) |
| duplicated | 0 doublon |
| describe | Pas de valeur négative ; quantités entre 1 et 5 ; remises entre 0,04 % et 19,61 % ; prix unitaire entre 0,79 et 36 999,99 (médiane 34,99) |

### 3 problèmes de véracité à traiter

1. **Dates mal typées et inventées par le script** : `order_date` est stockée en texte et a
   été générée par le script de collecte. Il faut la convertir en date, et ne pas
   l'utiliser pour analyser les ventes dans le temps.
2. **Marque manquante** : près de la moitié des lignes n'ont pas de `brand`. On ne
   peut pas analyser les ventes par marque sans compléter ou exclure ces lignes.
3. **Prix extrêmes** : un prix unitaire maximum de 36 999,99 pour une médiane de
   34,99. Ces valeurs doivent être vérifiées (produit réellement cher ou erreur)
   avant de calculer des moyennes.

**À noter :** `cart_total` est répété sur chaque ligne d'un même panier, il ne faut donc
pas l'additionner ligne par ligne.

## Atelier 3 : Cartographier les 5V de BigData Commerce Analytics

| V | Questions | Réponse |
|---|-----------|---------|
| Volume | Combien de commandes et d'événements par jour ? Quelle croissance ? | 208 paniers et 800 lignes sur 2025, soit environ 2,2 lignes par jour ; aucun événement (logs) disponible ; croissance non mesurable car les dates sont inventées par le script |
| Vitesse | Quelles données en temps réel, lesquelles par lots ? | Aucune donnée en temps réel : l'API est interrogée à la demande et le script capture un instantané, donc tout est traité par lots |
| Variété | Quelles sources et formats à intégrer ? | 8 ressources JSON issues de l'API (dont products, carts et users pour l'e-commerce), aplaties en 4 fichiers CSV ; pas de logs ni de paiements |
| Véracité | Quels problèmes relevés dans l'atelier 2 ? | Dates inventées par le script et lues comme du texte, marques manquantes sur près de la moitié des lignes, et prix extrêmes (jusqu'à 36 999,99) qui faussent les moyennes |
| Valeur | Quelles décisions améliorer ? | Recommandation possible à partir des paniers, gestion des stocks limitée aux quantités par produit, fraude non couverte faute de données de paiement |

### Conclusion

Les données DummyJSON présentent un volume et une vitesse faibles : elles ne relèvent
pas du Big Data à proprement parler, mais permettent de mettre en place la chaîne
complète sur un cas réduit. Leur principale difficulté est la variété (JSON imbriqué)
et la véracité (dates inventées, marques manquantes, prix extrêmes). Pour le jour 2,
MongoDB est adapté car il stocke directement des documents JSON, sans devoir les
aplatir. Avant ce chargement, il faudra convertir les dates, traiter les marques
manquantes et éviter d'additionner `cart_total`. Spark servira ensuite à appliquer
des traitements qui resteraient valables sur un volume réel bien plus important.