from django.db import models


class UserRegistration(models.Model):
    firstName = models.CharField(max_length=15)
    lastName = models.CharField(max_length=15)
    username = models.CharField(max_length=20)
    address = models.TextField()
    gender = models.CharField(max_length=15)
    dob = models.DateField()
    email = models.EmailField()
    mobileNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.username