### Projet Big Data DIC 2 GIT 2022/2023
Ce repository contient le code source de notre pipeline de récupération et de traitement des données météorologiques de la région de Thiès. Cette pipeline se présente comme nous pouvons le voir dans la figure ci-dessous

![img](./screenshots/Screenshot%202023-07-22%20at%2013.58.15.png)

La structure du repository est la suivante:
- Dans le dossier **Dataset**, vous trouverez le jeu de données weather.csv ainsi que le notebook utilisé pour créer ce dataset, le prétraiter et entrainer le modèle
- Dans le dossier **API** vous trouverez le code de l'API REST développée avec FastAPI et qui utilise le modèle de prédiction précédement créé
- Dans le dossier **SparkStreaming**, vous pouvez trouver le code pour le traitement des données arrivant sur Spark, le système de journalisation avec envoi de mail via SMTP et l'interaction avec l'API pour effectuer des préductions et S3 pour la sauvegarde des données
- Dans le dossier **weatherDashboard**, vous trouverez le code source de l'application Django pour la création du dashboard.

### Exécution
Pour exécuter le projet, nous avons un fichier docker-compose à la racine du projet qui vous permet de conteneuriser et exécuter l'API et le streaming.
Ensuite il vous suffit de démarrer le dashboard en utilisant la commande pour visualiser `python manage.py runserver`

#### Containers

![img](./screenshots/Screenshot%202023-07-22%20at%2014.00.25.png)

#### Dashboard

**Acceuil**

![img](./screenshots/Screenshot%202023-07-22%20at%2014.01.59.png)

**Predictions**

![img](./screenshots/Screenshot%202023-07-22%20at%2014.02.09.png)

**Moyenne par heure et par jour**

![img](./screenshots/Screenshot%202023-07-22%20at%2014.02.23.png)