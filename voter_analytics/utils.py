import csv
from datetime import datetime
from .models import Voter

def load_data(file_path = '/Users/chwang/Downloads/newton_voters.csv'):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Voter.objects.create(
                lastName = row['Last Name'],
                firstName = row['First Name'],
                streetNumber = row["Residential Address - Street Number"],
                streetName = row['Residential Address - Street Name'],
                apartmentNumber = row.get('Residential Address - Apartment Number', None),
                zipCode = row['Residential Address - Zip Code'],
                dateOfBirth=datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date(),
                dateOfRegistration=datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date(),
                partyAffiliation=row['Party Affiliation'],
                precinctNumber=row['Precinct Number'],
                v20State=row['v20state'] == 'TRUE',
                v21Town=row['v21town'] == 'TRUE',
                v21Primary=row['v21primary'] == 'TRUE',
                v22General=row['v22general'] == 'TRUE',
                v23Town=row['v23town'] == 'TRUE',
                voterScore=int(row['voter_score']),
            )