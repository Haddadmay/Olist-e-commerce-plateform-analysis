# Olist-e-commerce-plateform-analysis
Ce projet réalise une base de données relationnelle en utilisant SQL sur la plateforme Postgre. Elle est composée de neuf tables correspondant à différents jeux de données transactionnels publiques de la plus grande plateforme d’e-commerce du Brésil, à savoir Olist. Il s’agit de données d’environ 100 000 commandes effectuées de 2016 à 2018.

Partant de 0, on collecte, stocke et prépare de manière minutieuse l’ensemble des données dans l’objectif de construire ces tables SQL. L’ensemble de ces étapes vous sont soigneusement expliqués par la suite offrant une explication détaillée du fruit de notre travail.

Les données issus de la base Olist sont d’une importance capitale et stratégique. Son positionnement sur le marché (plus grande plateforme d’e commerce au  Brésil) font que ces données représentent une valeur capital de l'écosystème  du commerce en ligne dans ces pays en plein essor. De plus, cette base de données est un modèle important, du fait que ces donnés soient répartis sur un panel large (de 2016 à 2018) avec un nombre très élevé de commandes( environ 100 000). Ces éléments nous permettent d’analyser et d’évaluer des données pour en déceler des informations sur les tendances à long terme, sur les tendances de marchés, les préférences et besoins clients dans une logique d’amélioration de la performance et l'efficacité d’une entreprise. La base de données d'Olist, avec ses neuf tables distinctes couvrant une multitude d'informations cruciales, est ainsi un élément stratégique et un atout majeur pour être une marketplace e commerce qui peut améliorer l'expérience client, augmenter la rentabilité et maintenir la compétitivité dans un environnement de commerce électronique en constante évolution. 

[Olist dataset sur kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

## Description des données :
**Table : **
Il s’agit de la structure de la base de données. En effet, elle représente l’ensemble des données organisées. On parle alors d’un élément permettant de stocker des informations structurées de manière tabulaire.

**Classe : **
Il s’agit de la conceptualisation d’un objet réel. Elle permet de définir la structure et les caractéristiques d’un objet.

**Attribut : **
Il s’agit d’un champ dans une table qui permet de définir le type de donnée qu’elle peut contenir. Ainsi, les attributs définissent la structure de la table.

**Clé primair : e**
Il s’agit d’un attribut ou d’un ensemble d’attributs présent dans la table de base de données permettant d’identifier de manière unique chaque attributs de la table.

**Clé étrangère : **
Il s’agit d’un attribut dans la table de base de données qui établit une relation entre deux tables et ce grâce au référencement de la clé primaire d’une autre table.On parle alors de relations entre les données.

### 1 - La base de données d'Olist est structurée en neuf tables distinctes, chacune ayant un rôle spécifique dans l'organisation et la gestion des données :
**olist_customers :** 
Cette table contient des informations sur les clients, avec une clé primaire pour identifier de manière unique chaque client.

**olist_geolocation :** 
Cette table concerne la géolocalisation, mais elle ne dispose pas de clé primaire.

**product_category_name_translation :** 
Cette table est liée à la traduction des noms de catégories de produits. Elle ne possède pas de clé primaire.

**olist_orders :**
Cette table recueille des données sur les commandes et possède une clé primaire pour identifier chaque commande de manière unique.

**olist_products :** 
Elle contient des informations sur les produits, avec une clé primaire pour chaque produit.

**olist_sellers :** 
Cette table comprend des données sur les vendeurs, avec une clé primaire pour les identifier de manière unique.

**olist_order_reviews :** 
Elle stocke les avis sur les commandes et dispose d'une clé secondaire liée aux commandes.

**olist_order_payments :** 
Cette table enregistre des informations sur les paiements, avec une clé secondaire liée aux commandes.

**olist_order_items :** 
Cette table concerne les articles des commandes, avec une clé secondaire liée aux commandes.
