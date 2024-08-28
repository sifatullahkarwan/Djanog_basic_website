from django.db import models
from django.contrib.auth.models import User 
from django.db.models.deletion import CASCADE



# Create your models here.
# it create a class that we call the class name as table name
# inside the class we have some field that represent column in the table



class Topic(models.Model):
        name = models.CharField(max_length=200)
        def __str__(self):
            return self.name



# A foreign key is applied to a column of one table which references the primary key of a column in another table.

class Room(models.Model):# Room is our table name
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    topic = models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)# Foreignkey provide many_to on relationship
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)# blank mean if we submit the db it can be empyty
    patricipants = models.ManyToManyField(User,related_name='patricipants',blank=True)
    updated = models.DateTimeField(auto_now=True)# auto-now = it take the snapshot on every time we save of this itme
    created = models.DateTimeField(auto_now_add=True)# auto_now_add=takes a time stamp when we first save

# 
    class Meta:
         ordering = ['-updated','-created']# it respect the order according updated and bring it first

    def __str__(self):
        return self.name
    
# create super user
#python manage.py createsuperuser


    

class Message(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]# first 50 charecters
    class Meta:
         ordering = ['-updated','-created']