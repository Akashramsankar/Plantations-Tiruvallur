import uuid
from datetime import datetime
from src.common.database import Database
class Plantation(object):

    def __init__(self, typeOfPlantation, typeOfCrop, block, totalPits, workName, hectre, totalSanctionedPlants, plotNo, user_name, user_id,costOfCrops, plantationStatus= 'Open', plantationDate=None,plantation_id=None, pitsToBeTaken = None,panchayat = None, overseer = None, habitation = None,survivalRateOfCrops = None,pitsTaken = None ):
        if plantationDate:
            self.plantationDate = datetime.combine(datetime.strptime(plantationDate, '%Y-%m-%d').date(),

                                                 datetime.now().time())

        else:

            self.plantationDate = None

        self.typeOfPlantation = typeOfPlantation

        self.typeOfCrop = typeOfCrop

        self.block = block

        self.totalPits = totalPits

        self.workName = workName

        self.hectre = hectre

        self.totalSanctionedPlants = totalSanctionedPlants

        self.panchayat = panchayat

        self.habitation = habitation

        self.overseer = overseer

        self.pitsTaken = pitsTaken

        self.pitsToBeTaken = pitsToBeTaken

        self.plotNo = plotNo

        self.survivalRateOfCrops = survivalRateOfCrops

        self.costOfCrops = costOfCrops

        self.plantationStatus = plantationStatus

        self.user_id = user_id

        self.user_name = user_name

        self.plantation_id = uuid.uuid4().hex if plantation_id is None else plantation_id


    def save_to_mongo(self):

        Database.insert(collection='plantations', data=self.json())


    @classmethod

    def update_plantation(cls, plantation_id,panchayat, typeOfPlantation, workName, totalPits, hectre,overseer,habitation, totalSanctionedPlants,pitsTaken, pitsToBeTaken, typeOfCrop, plotNo, block, survivalRateOfCrops,user_name, user_id, costOfCrops, plantationDate, plantationStatus):

        Database.Update_Plantation(collection='plantations', query={'plantation_id': plantation_id}, typeOfCrop=typeOfCrop,

                                plotNo=plotNo, workName=workName, totalPits=totalPits, hectre=hectre, panchayat = panchayat, habitation = habitation, overseer = overseer, survivalRateOfCrops=survivalRateOfCrops, block = block, totalSanctionedPlants=totalSanctionedPlants, pitsTaken=pitsTaken, pitsToBeTaken=pitsToBeTaken,

                                costOfCrops=costOfCrops, typeOfPlantation=typeOfPlantation, plantationDate=plantationDate, plantationStatus=plantationStatus, user_id=user_id,

                                user_name=user_name)


    def json(self):

        return {

            'typeOfCrop': self.typeOfCrop,

            'typeOfPlantation': self.typeOfPlantation,

            'plotNo': self.plotNo,

            'survivalRateOfCrops': self.survivalRateOfCrops,

            'totalPits': self.totalPits,

            'hectre': self.hectre,

            'workName':self.workName,

            'totalSanctionedPlants': self.totalSanctionedPlants,

            'pitsTaken': self.pitsTaken,

            'pitsToBeTaken': self.pitsToBeTaken,

            'costOfCrops': self.costOfCrops,

            'block': self.block,

            'panchayat': self.panchayat,

            'habitation': self.habitation,

            'overseer': self.overseer,

            'plantationDate': self.plantationDate,

            'plantationStatus': self.plantationStatus,

            'user_id': self.user_id,

            'user_name': self.user_name,

            'plantation_id': self.plantation_id,

        }


    @classmethod

    def from_mongo(cls, plantation_id):

        Intent = Database.find_one(collection='plantations', query={'plantation_id': plantation_id})

        return cls(**Intent)

    @classmethod
    def deletefrom_mongo(cls, plantation_id):

        Database.delete_from_mongo(collection='plantations', query={'plantation_id': plantation_id})

    @classmethod

    def find_by_district(cls, blocks):

        intent = Database.find(collection='plantations', query={'blocks': blocks})

        return [cls(**inten) for inten in intent]