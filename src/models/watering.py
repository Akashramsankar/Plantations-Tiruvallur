import uuid

from datetime import datetime

from src.common.database import Database


class Watering(object):

    def __init__(self, typeOfCrop,plotNo,block,overseer, totalSanctionedPlants, costOfCrops, panchayat,originalCountOfCrops, currentCountOfCrops,user_name, user_id,asDate=None,numberOfReplacedCrops=None,estimateCostOfWatering=None,numberOfManDays=None,numberOfPeople=None,plantation_id=None,_id=None):
        if asDate:
            self.asDate = datetime.combine(datetime.strptime(asDate, '%Y-%m-%d').date(),
                                                   datetime.now().time())
        else:

            self.asDate = None
        self.typeOfCrop = typeOfCrop

        self.plotNo = plotNo

        self.block = block

        self.overseer = overseer

        self.panchayat = panchayat

        self.totalSanctionedPlants = totalSanctionedPlants

        self.costOfCrops = costOfCrops

        self.originalCountOfCrops = originalCountOfCrops

        self.currentCountOfCrops = currentCountOfCrops

        self.numberOfReplacedCrops = numberOfReplacedCrops

        self.user_id = user_id

        self.user_name = user_name

        self.estimateCostOfWatering = estimateCostOfWatering

        self.numberOfManDays = numberOfManDays

        self.numberOfPeople = numberOfPeople

        self.plantation_id = plantation_id

        self._id = uuid.uuid4().hex if _id is None else _id


    def save_to_mongo(self):

        Database.insert(collection='waterings', data=self.json())


    @classmethod

    def update_watering(cls, _id,originalCountOfCrops, currentCountOfCrops, totalSanctionedPlants, costOfCrops, numberOfReplacedCrops, estimateCostOfWatering, numberOfManDays, numberOfPeople,  user_name, user_id,
                        asDate,typeOfCrop,plotNo,plantation_id, block, overseer, panchayat):

        Database.update_watering(collection='waterings', query={'_id': _id}, panchayat = panchayat, typeOfCrop=typeOfCrop, block=block, overseer = overseer,
                                plotNo=plotNo,originalCountOfCrops= originalCountOfCrops, currentCountOfCrops= currentCountOfCrops, numberOfReplacedCrops=numberOfReplacedCrops,plantation_id=plantation_id,
                                estimateCostOfWatering=estimateCostOfWatering,numberOfManDays=numberOfManDays, asDate=asDate,numberOfPeople=numberOfPeople, user_id=user_id,
                                 user_name=user_name, totalSanctionedPlants=totalSanctionedPlants,costOfCrops=costOfCrops)
    def json(self):
        return {
            'typeOfCrop': self.typeOfCrop,
            'plotNo': self.plotNo,
            'asDate': self.asDate,
            'block': self.block,
            'panchayat':self.panchayat,
            'overseer': self.overseer,
            'totalSanctionedPlants': self.totalSanctionedPlants,
            'costOfCrops':self.costOfCrops,
            'originalCountOfCrops': self.originalCountOfCrops,
            'currentCountOfCrops': self.currentCountOfCrops,
            'numberOfReplacedCrops': self.numberOfReplacedCrops,
            'estimateCostOfWatering': self.estimateCostOfWatering,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'numberOfManDays': self.numberOfManDays,
            'numberOfPeople': self.numberOfPeople,
            'plantation_id': self.plantation_id,
            '_id': self._id,
        }
    @classmethod
    def from_mongo(cls, _id):
        Intent = Database.find_one(collection='waterings', query={'_id': _id})
        return cls(**Intent)
    @classmethod
    def deletefrom_mongo(cls, _id):
        Database.delete_from_mongo(collection='waterings', query={'_id': _id})
    @classmethod
    def find_by_district(cls, blocks):
        intent = Database.find(collection='waterings', query={'blocks': blocks})
        return [cls(**inten) for inten in intent]