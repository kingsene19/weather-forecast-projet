### Projet Big Data DIC 2 GIT 2022/2023
Ce repository contient le code source de notre pipeline de récupération et de traitement des données météorologiques de la région de Thiès. Cette pipeline se présente comme nous pouvons le voir dans la figure ci-dessous

![img](https://ibb.co/rHG48cZ)

La structure du repository est la suivante:
- Dans le dossier **Dataset**, vous trouverez le jeu de données weather.csv ainsi que le notebook utilisé pour créer ce dataset, le prétraiter et entrainer le modèle
- Dans le dossier **API** vous trouverez le code de l'API REST développée avec FastAPI et qui utilise le modèle de prédiction précédement créé
- Dans le dossier **SparkStreaming**, vous pouvez trouver le code pour le traitement des données arrivant sur Spark, le système de journalisation avec envoi de mail via SMTP et l'interaction avec l'API pour effectuer des préductions et S3 pour la sauvegarde des données
- Dans le dossier **weatherDashboard**, vous trouverez le code source de l'application Django pour la création du dashboard.

### Exécution
Pour exécuter le projet, nous avons un fichier docker-compose à la racine du projet qui vous permet de conteneuriser et exécuter l'API et le streaming.
Ensuite il vous suffit de démarrer le dashboard en utilisant la commande pour visualiser `python manage.py runserver` 
#### Containers
![img](https://ibb.co/TTycRz4)
#### Dashboard

**Acceuil**
![img](https://ibb.co/QQcp382)

**Predictions**
![img](https://ibb.co/bL5XWLX)

**Moyenne par heure et par jour**
![img](https://ibb.co/3CpbXZH)