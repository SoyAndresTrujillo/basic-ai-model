#!/usr/bin/env python3
"""
Script to verify MongoDB data generation
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('DB_URI_MONGO', 'mongodb://localhost:27017/')
DB_NAME = 'football_school_db'

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

print("\n📊 RESUMEN DE DATOS EN MONGODB:")
print("=" * 50)

collections = [
    'users', 'headquarters', 'students', 'teachers', 'classes',
    'classes_headquarters', 'students_classes', 'teachers_classes',
    'registration_fees', 'payments', 'classes_attendances'
]

for collection in collections:
    count = db[collection].count_documents({})
    print(f"{collection:25}: {count:>8,} registros")

client.close()
