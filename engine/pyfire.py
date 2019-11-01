import mysql.connector as mdb
import pandas as pd
import os
import pyrebase

import firebase_admin
from firebase_admin import credentials



class FireBaseCollections(object):
    def __init__(self):
        config = {
            
        }
        cred = credentials.Certificate("coolbagsafe-rentlocker-firebase-adminsdk-lbgfi-a22e73d4e9.json")
        firebase_admin.initialize_app(cred)