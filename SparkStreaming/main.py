import io
import findspark
findspark.init()

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from datetime import datetime, timedelta
import requests
import pandas as pd
import socket
import boto3
import configparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialisation des Credentials
config = configparser.ConfigParser()
config.read("config.ini")
api_key = config.get('Credentials', 'api_key')
aws_s3_bucket = config.get('Credentials','AWS_S3_BUCKET')
aws_access_key_id = config.get('Credentials','AWS_ACCESS_KEY_ID')
aws_secret_access_key = config.get('Credentials','AWS_SECRET_ACCESS_KEY')
smtp_password = config.get('Credentials', 'SMTP_PASSWORD')

# Création de la session Spark
spark = SparkSession\
    .builder\
    .appName("apiToS3")\
    .master("local[*]")\
    .getOrCreate()

# Initialisation des variables pour récupérer les données de Weatherbit
ip_address = socket.gethostbyname(socket.gethostname())
city = "Thies"
country = "SN"
url = f"https://api.weatherbit.io/v2.0/current?city={city}&country={country}&key={api_key}"

# Initialisation du client pour la connexion avec s3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    )

logSchema = StructType([
    StructField("timestamp", TimestampType(), True),
    StructField("message", StringType(), True)
])
logs = spark.createDataFrame([], logSchema)

# Initialisation des variables pour le serveur smtp
smtp_server = 'mail.galgit.com'
smtp_port = 587
sender_email = 'dic2-2023@galgit.com'
receiver_email = 'tunknowed@gmail.com'

# Méthode pour l'envoi du mail
def sendEmail(subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(sender_email, smtp_password)
            server.send_message(msg)
    except smtplib.SMTPException as e:
        print('Error sending email:', str(e))

#Methodes pour la journalisation
def checkDelay():
    if logs.rdd.isEmpty():
        return False
    sorted_logs = logs.orderBy(desc("timestamp"))
    last_timestamp = sorted_logs.limit(1).collect()[0]["timestamp"]
    return (datetime.now()-last_timestamp).total_seconds()/60>16
    
def checkLogs():
    sorted_logs = logs.orderBy(desc("timestamp"))
    msg = sorted_logs.limit(1).collect()[0]["message"]
    if msg.startswith("E"):
        print(f"{msg}, un email vous sera envoyé")
        sendEmail("Réception des données", "Les données de prédiction n'ont pas été récupérées")
    elif msg.startswith("W"):
        print(f"{msg}, un email vous sera envoyé")
        sendEmail("Réception des données", "Il y a eu un délai lors de la récupération des données de prédiction")
    else:
        print(f"{msg}")
    
predictionSchema = StructType([
    StructField('t1',FloatType(),True),
    StructField('t2',FloatType(),True),
    StructField('t3',FloatType(),True),
    StructField('t4',FloatType(),True),
    StructField('t5',FloatType(),True),
    StructField('t6',FloatType(),True),
    StructField('t7',FloatType(),True),
    StructField('t8',FloatType(),True),
    StructField('t9',FloatType(),True),
    StructField('t10',FloatType(),True),
    StructField('t11',FloatType(),True),
    StructField('t12',FloatType(),True)
])

weatherSchema = StructType([
    StructField('app_temp', FloatType(), True),
    StructField('hum', FloatType(), True),
    StructField('wsp', FloatType(), True),
    StructField('wdir', FloatType(), True),
    StructField('nua', FloatType(), True),
    StructField('prec', FloatType(), True),
    StructField('vis', FloatType(), True),
    StructField('temp', FloatType(), True)
])

#predictions_df = spark.createDataFrame([],predictionSchema)
#weather_df = spark.createDataFrame([],weatherSchema)

response = s3_client.get_object(Bucket=aws_s3_bucket, Key="predictions.csv")
file_content = response['Body'].read().decode('utf-8')
pandas_df = pd.read_csv(io.StringIO(file_content))
predictions_df = spark.createDataFrame(pandas_df)
response = s3_client.get_object(Bucket=aws_s3_bucket, Key="weather.csv")
file_content = response['Body'].read().decode('utf-8')
pandas_df = pd.read_csv(io.StringIO(file_content))
weather_df = spark.createDataFrame(pandas_df)

weather_df.show()
predictions_df.show()

def process_batch(batch_df, batch_id):
    """
        Cette fonction permet de récupèrer les données arrivant de nos requêtes et les enregistre au niveau de S3
    """
    global predictions_df, weather_df,logs
    now = datetime.now()
    start_timestamp = int((now - timedelta(minutes=15)).timestamp())
    end_timestamp = int(now.timestamp())
    try:
        response = requests.get(f'{url}&start={start_timestamp}&end={end_timestamp}')
        data = response.json()
        body = {}
        for entry in data['data']:
            temp =entry["temp"]
            body['app_temp'] = entry['app_temp']
            body['hum'] = entry["rh"]
            body['wsp'] = entry["wind_spd"]
            body['wdir'] = entry["wind_dir"]
            body['nua'] = entry['clouds'],
            body['prec'] = entry['precip']
            body['vis'] = entry["vis"]
        body['nua'] = body['nua'][0]
    except Exception as e:
        data = data = {
            "timestamp": datetime.now(),
            "message": "Erreur: Une erreur s'est produite lors de la récupération des données"
        }
        df = pd.DataFrame(data,index=[0])
        new_df = spark.createDataFrame(df)
        logs = logs.union(new_df)
    else:
        try:
            reponse = requests.post(f'http://spark-api:4555/weather', json=body, headers={"Accept": "application/json"})
            data = reponse.json()['temps']
            body["temp"] = temp
        except Exception as e:
            data = data = {
                "timestamp": datetime.now(),
                "message": "ERROR: Une erreur s'est produite lors de la récupération des données"
            }
            df = pd.DataFrame(data,index=[0])
            new_df = spark.createDataFrame(df)
            logs = logs.union(new_df)
        else:
            print("Here")
            pandas_df = pd.DataFrame(data,index=[0])
            spark_df = spark.createDataFrame(pandas_df)
            predictions_df = predictions_df.union(spark_df)
            pandas_weather = pd.DataFrame(body,index=[0])
            spark_weather = spark.createDataFrame(pandas_weather)
            weather_df = weather_df.union(spark_weather)
            s3_client.put_object(Body=predictions_df.toPandas().to_csv(index=False),Bucket=aws_s3_bucket,Key="predictions.csv")
            s3_client.put_object(Body=weather_df.toPandas().to_csv(index=False),Bucket=aws_s3_bucket,Key="weather.csv")
            if checkDelay():
                data = data = {
                    "timestamp": datetime.now(),
                    "message": "WARNING: Une délai est survenu lors de la récupération des données"
                }
                df = pd.DataFrame(data,index=[0])
                new_df = spark.createDataFrame(df)
                logs = logs.union(new_df)
            else:
                data = data = {
                    "timestamp": datetime.now(),
                    "message": "INFOS: Les données ont été enregistrées"
                }
                df = pd.DataFrame(data,index=[0])
                new_df = spark.createDataFrame(df)
                logs = logs.union(new_df)
            print("Data Written to S3")
    finally:
        checkLogs()
        
print("L'application a démarré")
streaming_df = spark.readStream.format("rate").load()
query = streaming_df\
    .writeStream\
    .foreachBatch(process_batch)\
    .trigger(processingTime="15 minutes")\
    .start()\
    .awaitTermination()