from django.db import models
import csv
from datetime import datetime
from .models import Voter

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

def load_data(file_path = '/Users/chwang/Downloads/newton_voters.csv'):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                lastName = row['Last Name'],
                firstName = row['First Name'],
                streetNumber = row["Residential Address - Street Numner"],
                streetName = row['Residential Address -  Street Name'],
                apartmentNumebr = row.get('Residential Address - Apartment Number', None),
                zipCode = row['Residential Address - Zip Code'],
                dateOfBirth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                dateOfRegistration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                partyAffiliation=row['Party Affiliation'],
                precinctNumber=int(row['Precinct Number']),
                v20State=row['v20state'] == 'TRUE',
                v21Town=row['v21town'] == 'TRUE',
                v21Primary=row['v21primary'] == 'TRUE',
                v22General=row['v22general'] == 'TRUE',
                v23Town=row['v23town'] == 'TRUE',
                voterScore=int(row['voter_score']),
            )