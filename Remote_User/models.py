from django.db import models

# Create your models here.
from django.db.models import CASCADE


class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    password = models.CharField(max_length=10)
    phoneno = models.CharField(max_length=10)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)


class traffic_prediction_type(models.Model):


    TRAFFIC_DATE= models.CharField(max_length=30000)
    TRAFFIC_TIME= models.CharField(max_length=30000)
    BOROUGH= models.CharField(max_length=30000)
    ZIP_CODE= models.CharField(max_length=30000)
    LATITUDE= models.CharField(max_length=30000)
    LONGITUDE= models.CharField(max_length=30000)
    LOCATION= models.CharField(max_length=30000)
    ON_STREET_NAME= models.CharField(max_length=30000)
    CROSS_STREET_NAME= models.CharField(max_length=30000)
    OFF_STREET_NAME= models.CharField(max_length=30000)
    CONTRIBUTING_FACTOR_VEHICLE= models.CharField(max_length=30000)
    REFERENCE_ID= models.CharField(max_length=30000)
    TRAFFIC_VEHICLE_TYPE_CODE1= models.CharField(max_length=30000)
    TRAFFIC_VEHICLE_TYPE_CODE2= models.CharField(max_length=30000)
    Junction= models.CharField(max_length=30000)
    Prediction= models.CharField(max_length=30000)


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)

class detection_ratio(models.Model):

    names = models.CharField(max_length=300)
    ratio = models.CharField(max_length=300)



