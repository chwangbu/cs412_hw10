from django.db import models

# Create your models here.
class Voter(models.Model):
    lastName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    streetNumber = models.CharField(max_length=10)
    steetName = models.CharField(max_length=100)
    apartmentNumber = models.CharField(max_length=10, blank=True, null=True)
    zipCode = models.CharField(max_length=10)
    dateOfBirth = models.DateField()
    dateOfRegistration = models.DateField()
    partyAffiliation = models.CharField(max_length=50)
    precinctNumber = models.IntegerField()
    v20State = models.BooleanField(default=False)
    v21Town = models.BooleanField(default=False)
    v21Primary = models.BooleanField(default=False)
    v22General = models.BooleanField(default=False)
    v23Town = models.BooleanField(default=False)
    voterScore = models.IntegerField()

    def __str__(self):
        return f"{self.firstName} {self.lastName} - Precinct {self.precinctNumber}"

