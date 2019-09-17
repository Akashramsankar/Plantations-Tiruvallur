import pymongo
import os

class Database(object):
    URI = os.environ['MONGODB_URI']
    DATABASE = None
    @staticmethod
    def initialize():
      client = pymongo.MongoClient(Database.URI)
      Database.DATABASE = client['heroku_vcrk1vkq']
    # URI = "mongodb://127.0.0.1:27017"
    # DATABASE = None
    # @staticmethod
    # def initialize():
    #       client = pymongo.MongoClient(Database.URI)
    #       Database.DATABASE = client['Tiruvallur']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)
    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
    @staticmethod
    def Update_Plantation(collection, query,  block, typeOfPlantation, workName, typeOfCrop, totalPits, panchayat, overseer, habitation,totalSanctionedPlants, pitsTaken, pitsToBeTaken,survivalRateOfCrops, user_name, user_id, costOfCrops, plantationDate, plantationStatus, hectre = None, plotNo = None, typeOfRoad = None, KM = None):

        return Database.DATABASE[collection].update_one(query, {'$set': {
                                                                         'typeOfCrop': typeOfCrop,
                                                                         'typeOfPlantation': typeOfPlantation,
                                                                         'totalSanctionedPlants': totalSanctionedPlants,
                                                                         'pitsTaken': pitsTaken,
                                                                         'totalPits': totalPits,
                                                                         'workName': workName,
                                                                         'hectre':hectre,
                                                                         'typeOfRoad':typeOfRoad,
                                                                         'KM':KM,
                                                                         'panchayat':panchayat,
                                                                         'habitation': habitation,
                                                                         'overseer': overseer,
                                                                         'pitsToBeTaken': pitsToBeTaken,
                                                                         'plotNo': plotNo,
                                                                         'block': block,
                                                                         'survivalRateOfCrops': survivalRateOfCrops,
                                                                         'costOfCrops': costOfCrops,
                                                                         'plantationDate': plantationDate,
                                                                         'plantationStatus': plantationStatus,
                                                                         'user_id' : user_id,
                                                                         'user_name' : user_name}}, True)

    @staticmethod
    def update_watering(collection, query, typeOfCrop,block,overseer, panchayat, totalSanctionePlants,costOfCrops,plotNo,originalCountOfCrops,currentCountOfCrops,numberOfReplacedCrops,estimateCostOfWatering,numberOfManDays,asDate,numberOfPeople,plantation_id,user_name, user_id):
        return Database.DATABASE[collection].update_one(query, {'$set': {'originalCountOfCrops': originalCountOfCrops,
                                                                         'currentCountOfCrops': currentCountOfCrops,
                                                                         'block': block,
                                                                         'panchayat':panchayat,
                                                                         'overseer': overseer,
                                                                         'totalSanctionedPlants':totalSanctionePlants,
                                                                         'costOfCrops':costOfCrops,
                                                                         'numberOfReplacedCrops': numberOfReplacedCrops,
                                                                         'estimateCostOfWatering': estimateCostOfWatering,
                                                                         'numberOfManDays': numberOfManDays,
                                                                         'asDate': asDate,
                                                                         'numberOfPeople': numberOfPeople,
                                                                         'plantation_id': plantation_id,
                                                                         'typeOfCrop': typeOfCrop,
                                                                         'plotNo': plotNo,
                                                                         'user_id': user_id,
                                                                         'user_name': user_name}}, True)

    @staticmethod
    def update_overseer(collection, query, block, overseer):
        return Database.DATABASE[collection].update_one(query, {'$set': {'block': block,
                                                                     'overseer': overseer}}, True)
    @staticmethod
    def delete_from_mongo(collection, query):
        Database.DATABASE[collection].remove(query)