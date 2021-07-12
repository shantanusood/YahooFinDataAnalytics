import configparser
import pymongo

def getCollection(collection):
    config = configparser.RawConfigParser()
    config.read('./data/mongo.properties')
    config.get('Auth_Info', 'user')
    client = pymongo.MongoClient("mongodb+srv://"+config.get('Auth_Info', 'user')+":"+config.get('Auth_Info', 'pass')+"@cluster0.csbwv.mongodb.net/Cluster0?retryWrites=true&w=majority")
    return client[config.get('Auth_Info', 'database')][str(collection)]
