import configparser
import pymongo
import os

def getCollection(collection):
    config = configparser.RawConfigParser()
    config.read('./data/mongo.properties')
    #client = pymongo.MongoClient("mongodb+srv://"+config.get('Auth_Info', 'user')+":"+config.get('Auth_Info', 'pass')+"@cluster0.csbwv.mongodb.net/Cluster0?retryWrites=true&w=majority")
    client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
    return client[config.get('Auth_Info', 'auth_database')][str(collection)]
