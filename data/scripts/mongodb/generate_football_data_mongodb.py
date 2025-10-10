#!/usr/bin/env python3
"""
Script para generar datos de prueba para el sistema de gestión académica
de una escuela deportiva de fútbol en MongoDB.

Características implementadas:
- 10% de records con valores null
- 5% de records duplicados
- Pocos records con poca varianza
- Campos no categorizados con datos diversos
- 50,000+ registros en colecciones operacionales (payments, classes_attendances)
- Máximo 100 registros en colecciones maestras
"""

import os
import random
from datetime import datetime, date, timedelta
from faker import Faker
import sys
from bson import ObjectId, Decimal128
from pymongo import MongoClient, ASCENDING, IndexModel
from pymongo.errors import DuplicateKeyError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos MongoDB
MONGO_URI = os.getenv('DB_URI_MONGO', 'mongodb://localhost:27017/')
DB_NAME = 'football_school_db'

fake = Faker('es_ES')  # Configurar para español
Faker.seed(42)  # Para resultados reproducibles
random.seed(42)


class FootballSchoolMongoDBGenerator:
    def __init__(self):
        self.client = None
        self.db = None
        
        # Listas para almacenar IDs generados
        self.user_ids = []
        self.student_ids = []
        self.teacher_ids = []
        self.headquarter_ids = []
        self.class_ids = []
        self.registration_fee_ids = []
        
        # Datos específicos de fútbol
        self.football_positions = [
            'Portero', 'Defensa Central', 'Lateral Derecho', 'Lateral Izquierdo',
            'Mediocentro Defensivo', 'Mediocentro', 'Mediocentro Ofensivo',
            'Extremo Derecho', 'Extremo Izquierdo', 'Delantero Centro'
        ]
        
        self.football_skills = [
            'Técnica individual', 'Pases', 'Regate', 'Finalización',
            'Táctica defensiva', 'Táctica ofensiva', 'Condición física',
            'Velocidad', 'Resistencia', 'Fuerza'
        ]
        
        self.class_types = [
            'Técnica Individual', 'Táctica', 'Condición Física', 
            'Partido Amistoso', 'Entrenamiento Integral', 'Porteros'
        ]
        
        self.teacher_studies = [
            {'titulo': 'Licenciatura en Educación Física', 'universidad': 'Universidad Nacional', 'año': '2018'},
            {'titulo': 'Entrenador de Fútbol Nivel I', 'institucion': 'CONMEBOL', 'año': '2020'},
            {'titulo': 'Especialización en Alto Rendimiento', 'universidad': 'Universidad del Deporte', 'año': '2019'},
            {'titulo': 'Curso FIFA para Entrenadores', 'institucion': 'FIFA Academy', 'año': '2021'},
            {'titulo': 'Maestría en Ciencias del Deporte', 'universidad': 'Universidad Deportiva', 'año': '2022'}
        ]

    def connect_db(self):
        """Conectar a la base de datos MongoDB"""
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DB_NAME]
            # Verificar conexión
            self.client.admin.command('ping')
            print(f"✓ Conexión exitosa a MongoDB: {DB_NAME}")
        except Exception as e:
            print(f"✗ Error conectando a MongoDB: {e}")
            sys.exit(1)

    def close_db(self):
        """Cerrar conexión a la base de datos"""
        if self.client:
            self.client.close()

    def create_indexes(self):
        """Crear índices para optimizar consultas"""
        print("Creando índices...")
        
        # Users indexes
        self.db.users.create_index([("document_id", ASCENDING)], unique=True)
        self.db.users.create_index([("email", ASCENDING)])
        self.db.users.create_index([("user_type", ASCENDING)])
        
        # Headquarters indexes
        self.db.headquarters.create_index([("name", ASCENDING)])
        
        # Students indexes
        self.db.students.create_index([("user_id", ASCENDING)], unique=True)
        self.db.students.create_index([("headquarter_id", ASCENDING)])
        self.db.students.create_index([("state", ASCENDING)])
        
        # Teachers indexes
        self.db.teachers.create_index([("user_id", ASCENDING)], unique=True)
        
        # Classes indexes
        self.db.classes.create_index([("class_type", ASCENDING)])
        self.db.classes.create_index([("name", ASCENDING)])
        
        # Classes_headquarters indexes
        self.db.classes_headquarters.create_index([
            ("class_id", ASCENDING),
            ("headquarter_id", ASCENDING),
            ("start_date", ASCENDING)
        ], unique=True)
        self.db.classes_headquarters.create_index([("class_id", ASCENDING)])
        self.db.classes_headquarters.create_index([("headquarter_id", ASCENDING)])
        
        # Students_classes indexes
        self.db.students_classes.create_index([
            ("student_id", ASCENDING),
            ("class_id", ASCENDING)
        ], unique=True)
        self.db.students_classes.create_index([("student_id", ASCENDING)])
        self.db.students_classes.create_index([("class_id", ASCENDING)])
        self.db.students_classes.create_index([("state", ASCENDING)])
        
        # Teachers_classes indexes
        self.db.teachers_classes.create_index([("teacher_id", ASCENDING), ("class_id", ASCENDING)])
        self.db.teachers_classes.create_index([("class_id", ASCENDING)])
        self.db.teachers_classes.create_index([("teacher_role", ASCENDING)])
        
        # Registration_fees indexes
        self.db.registration_fees.create_index([("student_id", ASCENDING)])
        self.db.registration_fees.create_index([("state", ASCENDING)])
        self.db.registration_fees.create_index([("start_date", ASCENDING), ("end_date", ASCENDING)])
        
        # Payments indexes
        self.db.payments.create_index([("registration_fee_id", ASCENDING)])
        self.db.payments.create_index([("payment_date", ASCENDING)])
        self.db.payments.create_index([("payment_method", ASCENDING)])
        
        # Classes_attendances indexes
        self.db.classes_attendances.create_index([
            ("student_id", ASCENDING),
            ("class_id", ASCENDING),
            ("date", ASCENDING)
        ], unique=True)
        self.db.classes_attendances.create_index([("student_id", ASCENDING)])
        self.db.classes_attendances.create_index([("class_id", ASCENDING)])
        self.db.classes_attendances.create_index([("date", ASCENDING)])
        self.db.classes_attendances.create_index([("attended", ASCENDING)])
        
        print("✓ Índices creados")

    def drop_collections(self):
        """Eliminar todas las colecciones existentes"""
        print("Eliminando colecciones existentes...")
        collections = [
            'users', 'headquarters', 'students', 'teachers', 'classes',
            'classes_headquarters', 'students_classes', 'teachers_classes',
            'registration_fees', 'payments', 'classes_attendances'
        ]
        for collection in collections:
            self.db[collection].drop()
        print("✓ Colecciones eliminadas")

    def generate_null_value(self, probability=0.1):
        """Generar valor NULL con probabilidad dada"""
        return None if random.random() < probability else False

    def generate_phone_inconsistent(self):
        """Generar números de teléfono con formatos inconsistentes"""
        formats = [
            f"+57 {random.randint(300, 350)} {random.randint(100, 999)} {random.randint(1000, 9999)}",
            f"0{random.randint(300, 350)}{random.randint(1000000, 9999999)}",
            f"{random.randint(300, 350)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            f"({random.randint(300, 350)}) {random.randint(1000000, 9999999)}",
            str(random.randint(3000000000, 3509999999))
        ]
        return random.choice(formats) if not self.generate_null_value() else None

    def generate_headquarters(self, count=10):
        """Generar sedes de la escuela de fútbol"""
        print(f"Generando {count} sedes...")
        
        headquarters_data = [
            ('Sede Norte', 'Calle 100 #15-20, Bogotá', 'Academia de Fútbol Norte SAS'),
            ('Sede Sur', 'Carrera 30 #40-50, Bogotá', 'Academia de Fútbol Sur SAS'),
            ('Sede Centro', 'Avenida 19 #25-30, Bogotá', 'Academia de Fútbol Centro SAS'),
            ('Sede Suba', 'Calle 145 #90-15, Bogotá', 'Academia de Fútbol Suba SAS'),
            ('Sede Chapinero', 'Carrera 15 #63-25, Bogotá', 'Academia de Fútbol Chapinero SAS'),
        ]
        
        documents = []
        for i in range(count):
            if i < len(headquarters_data):
                name, address, legal_name = headquarters_data[i]
            else:
                name = f"Sede {fake.city()}"
                address = fake.address()
                legal_name = f"Academia de Fútbol {fake.city()} SAS"
            
            hq_id = ObjectId()
            self.headquarter_ids.append(hq_id)
            
            document = {
                '_id': hq_id,
                'name': name,
                'address': address,
                'legal_name': legal_name,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            documents.append(document)
        
        self.db.headquarters.insert_many(documents)

    def generate_users(self, count=100):
        """Generar usuarios base"""
        print(f"Generando {count} usuarios...")
        
        # Generar algunos duplicados (5%)
        duplicates_count = int(count * 0.05)
        unique_count = count - duplicates_count
        
        duplicate_users = []
        documents = []
        
        for i in range(unique_count):
            user_id = ObjectId()
            self.user_ids.append(user_id)
            
            name = fake.first_name() if not self.generate_null_value() else None
            last_name = fake.last_name() if not self.generate_null_value() else None
            
            # Tipos de documento colombianos
            doc_types = ['CC', 'TI', 'CE', 'RC']
            type_document_id = random.choice(doc_types)
            document_id = str(random.randint(10000000, 99999999))
            
            email = fake.email() if not self.generate_null_value() else None
            phone = self.generate_phone_inconsistent()
            birthday_date = fake.date_of_birth(minimum_age=8, maximum_age=45) if not self.generate_null_value() else None
            # Convert date to datetime for MongoDB
            birthday = datetime.combine(birthday_date, datetime.min.time()) if birthday_date else None
            
            user_data = {
                '_id': user_id,
                'name': name,
                'last_name': last_name,
                'type_document_id': type_document_id,
                'document_id': document_id,
                'email': email,
                'phone': phone,
                'birthday': birthday,
                'user_type': 'pending',  # Will be updated when creating students/teachers
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            documents.append(user_data)
            
            # Guardar algunos para duplicar
            if i < duplicates_count:
                duplicate_users.append(user_data.copy())
        
        # Insertar duplicados con pequeñas variaciones
        for user_data in duplicate_users:
            duplicate_id = ObjectId()
            self.user_ids.append(duplicate_id)
            
            # Cambiar solo el ID y documento para crear "duplicado"
            user_data['_id'] = duplicate_id
            user_data['document_id'] = str(int(user_data['document_id']) + 1)
            documents.append(user_data)
        
        self.db.users.insert_many(documents)

    def generate_students(self, count=80):
        """Generar estudiantes (jugadores)"""
        print(f"Generando {count} estudiantes...")
        
        available_users = self.user_ids[:count]
        states = ['active', 'inactive', 'suspended']
        
        documents = []
        for user_id in available_users:
            student_id = user_id  # Use same ID as user for easy reference
            self.student_ids.append(student_id)
            
            headquarter_id = random.choice(self.headquarter_ids)
            state = random.choices(states, weights=[85, 10, 5], k=1)[0]  # Mayoría activos
            
            document = {
                '_id': student_id,
                'user_id': user_id,
                'headquarter_id': headquarter_id,
                'state': state,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            documents.append(document)
            
            # Update user type
            self.db.users.update_one(
                {'_id': user_id},
                {'$set': {'user_type': 'student', 'updated_at': datetime.now()}}
            )
        
        self.db.students.insert_many(documents)

    def generate_teachers(self, count=15):
        """Generar entrenadores"""
        print(f"Generando {count} entrenadores...")
        
        available_users = self.user_ids[80:80+count]  # Usuarios no usados como estudiantes
        
        documents = []
        for user_id in available_users:
            teacher_id = user_id  # Use same ID as user for easy reference
            self.teacher_ids.append(teacher_id)
            
            # Generar estudios variados
            num_studies = random.randint(1, 3)
            studies = random.sample(self.teacher_studies, num_studies)
            
            professional_license = f"ENT-{random.randint(1000, 9999)}" if not self.generate_null_value() else None
            
            document = {
                '_id': teacher_id,
                'user_id': user_id,
                'studies': studies,
                'professional_license': professional_license,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            documents.append(document)
            
            # Update user type
            self.db.users.update_one(
                {'_id': user_id},
                {'$set': {'user_type': 'teacher', 'updated_at': datetime.now()}}
            )
        
        self.db.teachers.insert_many(documents)

    def generate_classes(self, count=25):
        """Generar clases de entrenamiento"""
        print(f"Generando {count} clases...")
        
        schedules = [
            'Lunes 16:00-18:00', 'Martes 17:00-19:00', 'Miércoles 15:00-17:00',
            'Jueves 16:00-18:00', 'Viernes 17:00-19:00', 'Sábado 09:00-11:00',
            'Sábado 14:00-16:00', 'Domingo 09:00-11:00'
        ]
        
        documents = []
        for i in range(count):
            class_id = ObjectId()
            self.class_ids.append(class_id)
            
            class_type = random.choice(self.class_types)
            name = f"{class_type} - Grupo {chr(65 + i % 26)}"
            capacity = random.randint(15, 25)
            schedule = random.choice(schedules)
            
            document = {
                '_id': class_id,
                'name': name,
                'capacity': capacity,
                'schedule': schedule,
                'class_type': class_type,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            documents.append(document)
        
        self.db.classes.insert_many(documents)

    def generate_classes_headquarters(self):
        """Generar relación clases-sedes"""
        print("Generando relaciones clases-sedes...")
        
        documents = []
        for class_id in self.class_ids:
            # Cada clase puede estar en 1-3 sedes
            num_headquarters = random.randint(1, 3)
            selected_hqs = random.sample(self.headquarter_ids, num_headquarters)
            
            for hq_id in selected_hqs:
                start_date = fake.date_between(start_date='-6M', end_date='today')
                end_date = start_date + timedelta(days=random.randint(90, 365))
                
                document = {
                    'class_id': class_id,
                    'headquarter_id': hq_id,
                    'start_date': datetime.combine(start_date, datetime.min.time()),
                    'end_date': datetime.combine(end_date, datetime.min.time()),
                    'created_at': datetime.now()
                }
                documents.append(document)
        
        self.db.classes_headquarters.insert_many(documents)

    def generate_students_classes(self):
        """Generar inscripciones de estudiantes en clases"""
        print("Generando inscripciones estudiante-clase...")
        
        states = ['enrolled', 'active', 'withdrawn', 'completed']
        
        documents = []
        for student_id in self.student_ids:
            # Cada estudiante puede estar en 1-4 clases
            num_classes = random.randint(1, 4)
            selected_classes = random.sample(self.class_ids, min(num_classes, len(self.class_ids)))
            
            for class_id in selected_classes:
                state = random.choices(states, weights=[20, 60, 15, 5], k=1)[0]
                
                document = {
                    'student_id': student_id,
                    'class_id': class_id,
                    'state': state,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                documents.append(document)
        
        self.db.students_classes.insert_many(documents)

    def generate_teachers_classes(self):
        """Generar asignación de profesores a clases"""
        print("Generando asignaciones profesor-clase...")
        
        roles = ['lead', 'assistant', 'substitute']
        
        documents = []
        for class_id in self.class_ids:
            # Cada clase tiene 1-2 profesores
            num_teachers = random.randint(1, 2)
            selected_teachers = random.sample(self.teacher_ids, min(num_teachers, len(self.teacher_ids)))
            
            for i, teacher_id in enumerate(selected_teachers):
                role = 'lead' if i == 0 else random.choice(['assistant', 'substitute'])
                start_date = fake.date_between(start_date='-6M', end_date='today')
                end_date_val = start_date + timedelta(days=random.randint(90, 365)) if random.random() > 0.7 else None
                
                document = {
                    'teacher_id': teacher_id,
                    'class_id': class_id,
                    'teacher_role': role,
                    'start_date': datetime.combine(start_date, datetime.min.time()),
                    'end_date': datetime.combine(end_date_val, datetime.min.time()) if end_date_val else None,
                    'created_at': datetime.now()
                }
                documents.append(document)
        
        self.db.teachers_classes.insert_many(documents)

    def generate_registration_fees(self):
        """Generar matrículas/registros"""
        print("Generando registros de matrícula...")
        
        states = ['active', 'expired', 'cancelled']
        
        documents = []
        for student_id in self.student_ids:
            # Cada estudiante puede tener 1-3 registros (históricos)
            num_registrations = random.randint(1, 3)
            
            for _ in range(num_registrations):
                reg_id = ObjectId()
                self.registration_fee_ids.append(reg_id)
                
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(30, 365))
                state = random.choices(states, weights=[70, 20, 10], k=1)[0]
                
                document = {
                    '_id': reg_id,
                    'student_id': student_id,
                    'start_date': datetime.combine(start_date, datetime.min.time()),
                    'end_date': datetime.combine(end_date, datetime.min.time()),
                    'state': state,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                documents.append(document)
        
        self.db.registration_fees.insert_many(documents)

    def generate_payments(self, target_count=50000):
        """Generar pagos (colección operacional)"""
        print(f"Generando {target_count} pagos...")
        
        payment_methods = ['Efectivo', 'Tarjeta', 'Transferencia', 'PSE', 'Daviplata', 'Nequi']
        concepts = [
            'Mensualidad', 'Matrícula', 'Material deportivo', 'Torneo interno',
            'Campamento', 'Uniforme', 'Cuota adicional', 'Descuento hermanos',
            'Pago anticipado', 'Recargo por mora'
        ]
        
        payments_per_registration = target_count // len(self.registration_fee_ids)
        extra_payments = target_count % len(self.registration_fee_ids)
        
        batch_size = 1000
        documents = []
        
        for i, reg_id in enumerate(self.registration_fee_ids):
            # Calcular cuántos pagos para este registro
            num_payments = payments_per_registration
            if i < extra_payments:
                num_payments += 1
            
            for _ in range(num_payments):
                amount = round(random.uniform(50000, 300000), 2)  # Pesos colombianos
                payment_date = fake.date_between(start_date='-1y', end_date='today')
                payment_method = random.choice(payment_methods)
                receipt_number = f"REC-{random.randint(100000, 999999)}" if not self.generate_null_value() else None
                concept = random.choice(concepts) if not self.generate_null_value() else None
                
                document = {
                    'registration_fee_id': reg_id,
                    'amount': Decimal128(str(amount)),
                    'payment_date': datetime.combine(payment_date, datetime.min.time()),
                    'payment_method': payment_method,
                    'receipt_number': receipt_number,
                    'concept': concept,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                documents.append(document)
                
                # Insert in batches
                if len(documents) >= batch_size:
                    self.db.payments.insert_many(documents)
                    documents = []
        
        # Insert remaining documents
        if documents:
            self.db.payments.insert_many(documents)

    def generate_classes_attendances(self, target_count=50000):
        """Generar asistencias a clases (colección operacional)"""
        print(f"Generando {target_count} registros de asistencia...")
        
        observations_pool = [
            'Excelente desempeño en el entrenamiento',
            'Llegó 10 minutos tarde',
            'Mostró gran mejora en técnica de pase',
            'Necesita trabajar más la condición física',
            'Participó activamente en ejercicios tácticos',
            'Leve molestia en tobillo izquierdo',
            'Destacó en ejercicios de finalización',
            'Faltó concentración durante la sesión',
            'Muy buen trabajo en equipo',
            'Requiere refuerzo en técnica defensiva'
        ]
        
        # Calcular asistencias por estudiante
        attendances_per_student = target_count // len(self.student_ids)
        extra_attendances = target_count % len(self.student_ids)
        
        batch_size = 1000
        documents = []
        
        for i, student_id in enumerate(self.student_ids):
            num_attendances = attendances_per_student
            if i < extra_attendances:
                num_attendances += 1
            
            for _ in range(num_attendances):
                class_id = random.choice(self.class_ids)
                headquarter_id = random.choice(self.headquarter_ids)
                teacher_id = random.choice(self.teacher_ids)
                
                attendance_date = fake.date_between(start_date='-6M', end_date='today')
                attended = random.choices([True, False], weights=[85, 15], k=1)[0]  # 85% asistencia
                observations = random.choice(observations_pool) if not self.generate_null_value(0.3) else None
                
                document = {
                    'student_id': student_id,
                    'class_id': class_id,
                    'headquarter_id': headquarter_id,
                    'teacher_id': teacher_id,
                    'date': datetime.combine(attendance_date, datetime.min.time()),
                    'attended': attended,
                    'observations': observations,
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                }
                documents.append(document)
                
                # Insert in batches
                if len(documents) >= batch_size:
                    try:
                        self.db.classes_attendances.insert_many(documents, ordered=False)
                    except DuplicateKeyError:
                        # Ignorar duplicados por la restricción UNIQUE
                        pass
                    documents = []
        
        # Insert remaining documents
        if documents:
            try:
                self.db.classes_attendances.insert_many(documents, ordered=False)
            except DuplicateKeyError:
                # Ignorar duplicados por la restricción UNIQUE
                pass

    def generate_all_data(self):
        """Generar todos los datos"""
        try:
            print("🚀 Iniciando generación de datos para escuela de fútbol en MongoDB...")
            
            # Limpiar colecciones existentes
            self.drop_collections()
            
            # Crear índices únicos ANTES de insertar datos para evitar duplicados
            print("Creando índices únicos...")
            self.db.users.create_index([("document_id", ASCENDING)], unique=True)
            self.db.students.create_index([("user_id", ASCENDING)], unique=True)
            self.db.teachers.create_index([("user_id", ASCENDING)], unique=True)
            self.db.classes_headquarters.create_index([
                ("class_id", ASCENDING),
                ("headquarter_id", ASCENDING),
                ("start_date", ASCENDING)
            ], unique=True)
            self.db.students_classes.create_index([
                ("student_id", ASCENDING),
                ("class_id", ASCENDING)
            ], unique=True)
            self.db.classes_attendances.create_index([
                ("student_id", ASCENDING),
                ("class_id", ASCENDING),
                ("date", ASCENDING)
            ], unique=True)
            print("✓ Índices únicos creados")
            
            # Generar datos maestros
            self.generate_headquarters(10)
            self.generate_users(100)
            self.generate_students(80)
            self.generate_teachers(15)
            self.generate_classes(25)
            print("✓ Datos maestros generados")
            
            # Generar relaciones
            self.generate_classes_headquarters()
            self.generate_students_classes()
            self.generate_teachers_classes()
            self.generate_registration_fees()
            print("✓ Relaciones generadas")
            
            # Generar datos operacionales (grandes volúmenes)
            self.generate_payments(50000)
            print("✓ Pagos generados")
            
            self.generate_classes_attendances(50000)
            print("✓ Asistencias generadas")
            
            # Crear índices adicionales (no únicos)
            print("Creando índices adicionales...")
            self.db.users.create_index([("email", ASCENDING)])
            self.db.users.create_index([("user_type", ASCENDING)])
            self.db.headquarters.create_index([("name", ASCENDING)])
            self.db.students.create_index([("headquarter_id", ASCENDING)])
            self.db.students.create_index([("state", ASCENDING)])
            self.db.classes.create_index([("class_type", ASCENDING)])
            self.db.classes.create_index([("name", ASCENDING)])
            self.db.classes_headquarters.create_index([("class_id", ASCENDING)])
            self.db.classes_headquarters.create_index([("headquarter_id", ASCENDING)])
            self.db.students_classes.create_index([("student_id", ASCENDING)])
            self.db.students_classes.create_index([("class_id", ASCENDING)])
            self.db.students_classes.create_index([("state", ASCENDING)])
            self.db.teachers_classes.create_index([("teacher_id", ASCENDING), ("class_id", ASCENDING)])
            self.db.teachers_classes.create_index([("class_id", ASCENDING)])
            self.db.teachers_classes.create_index([("teacher_role", ASCENDING)])
            self.db.registration_fees.create_index([("student_id", ASCENDING)])
            self.db.registration_fees.create_index([("state", ASCENDING)])
            self.db.registration_fees.create_index([("start_date", ASCENDING), ("end_date", ASCENDING)])
            self.db.payments.create_index([("registration_fee_id", ASCENDING)])
            self.db.payments.create_index([("payment_date", ASCENDING)])
            self.db.payments.create_index([("payment_method", ASCENDING)])
            self.db.classes_attendances.create_index([("student_id", ASCENDING)])
            self.db.classes_attendances.create_index([("class_id", ASCENDING)])
            self.db.classes_attendances.create_index([("date", ASCENDING)])
            self.db.classes_attendances.create_index([("attended", ASCENDING)])
            print("✓ Índices adicionales creados")
            
            print("🎉 ¡Generación de datos completada exitosamente!")
            
        except Exception as e:
            print(f"✗ Error durante la generación: {e}")
            raise


def main():
    generator = FootballSchoolMongoDBGenerator()
    
    try:
        generator.connect_db()
        generator.generate_all_data()
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE DATOS GENERADOS:")
        print("=" * 50)
        
        collections_to_count = [
            'users', 'headquarters', 'students', 'teachers', 'classes',
            'classes_headquarters', 'students_classes', 'teachers_classes',
            'registration_fees', 'payments', 'classes_attendances'
        ]
        
        for collection in collections_to_count:
            count = generator.db[collection].count_documents({})
            print(f"{collection:25}: {count:>8,} registros")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        generator.close_db()


if __name__ == "__main__":
    main()
