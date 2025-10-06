#!/usr/bin/env python3
"""
Script para generar datos de prueba para el sistema de gestión académica
de una escuela deportiva de fútbol.

Características implementadas:
- 10% de records con valores null
- 5% de records duplicados
- Pocos records con poca varianza
- Campos no categorizados con datos diversos
- 50,000+ registros en tablas operacionales (payments, classes_attendances)
- Máximo 100 registros en tablas maestras
"""

import psycopg
import random
import uuid
from datetime import datetime, date, timedelta
from faker import Faker
import json
import sys

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'logictics_local',
    'user': 'root',
    'password': 'root123'
}

fake = Faker('es_ES')  # Configurar para español
Faker.seed(42)  # Para resultados reproducibles
random.seed(42)

class FootballSchoolDataGenerator:
    def __init__(self):
        self.conn = None
        self.cursor = None
        
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
        """Conectar a la base de datos PostgreSQL"""
        try:
            self.conn = psycopg.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("✓ Conexión exitosa a la base de datos")
        except psycopg.Error as e:
            print(f"✗ Error conectando a la base de datos: {e}")
            sys.exit(1)

    def close_db(self):
        """Cerrar conexión a la base de datos"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

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
        
        for i in range(count):
            if i < len(headquarters_data):
                name, address, legal_name = headquarters_data[i]
            else:
                name = f"Sede {fake.city()}"
                address = fake.address()
                legal_name = f"Academia de Fútbol {fake.city()} SAS"
            
            hq_id = str(uuid.uuid4())
            self.headquarter_ids.append(hq_id)
            
            query = """
                INSERT INTO headquarters (id, name, address, legal_name)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (hq_id, name, address, legal_name))

    def generate_users(self, count=100):
        """Generar usuarios base"""
        print(f"Generando {count} usuarios...")
        
        # Generar algunos duplicados (5%)
        duplicates_count = int(count * 0.05)
        unique_count = count - duplicates_count
        
        duplicate_users = []
        
        for i in range(unique_count):
            user_id = str(uuid.uuid4())
            self.user_ids.append(user_id)
            
            name = fake.first_name() if not self.generate_null_value() else None
            last_name = fake.last_name() if not self.generate_null_value() else None
            
            # Tipos de documento colombianos
            doc_types = ['CC', 'TI', 'CE', 'RC']
            type_document_id = random.choice(doc_types)
            document_id = str(random.randint(10000000, 99999999))
            
            email = fake.email() if not self.generate_null_value() else None
            phone = self.generate_phone_inconsistent()
            birthday = fake.date_of_birth(minimum_age=8, maximum_age=45) if not self.generate_null_value() else None
            
            user_data = (user_id, name, last_name, type_document_id, document_id, email, phone, birthday)
            
            query = """
                INSERT INTO users (id, name, last_name, type_document_id, document_id, email, phone, birthday)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, user_data)
            
            # Guardar algunos para duplicar
            if i < duplicates_count:
                duplicate_users.append(user_data)
        
        # Insertar duplicados con pequeñas variaciones
        for user_data in duplicate_users:
            duplicate_id = str(uuid.uuid4())
            self.user_ids.append(duplicate_id)
            
            # Cambiar solo el ID y documento para crear "duplicado"
            modified_data = list(user_data)
            modified_data[0] = duplicate_id
            modified_data[4] = str(int(modified_data[4]) + 1)  # Documento ligeramente diferente
            
            self.cursor.execute(query, tuple(modified_data))

    def generate_students(self, count=80):
        """Generar estudiantes (jugadores)"""
        print(f"Generando {count} estudiantes...")
        
        available_users = self.user_ids[:count]
        states = ['active', 'inactive', 'suspended']
        
        for user_id in available_users:
            self.student_ids.append(user_id)
            
            headquarter_id = random.choice(self.headquarter_ids)
            state = random.choices(states, weights=[85, 10, 5], k=1)[0]  # Mayoría activos
            
            query = """
                INSERT INTO students (id, id_headquarter, state)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (user_id, headquarter_id, state))

    def generate_teachers(self, count=15):
        """Generar entrenadores"""
        print(f"Generando {count} entrenadores...")
        
        available_users = self.user_ids[80:80+count]  # Usuarios no usados como estudiantes
        
        for user_id in available_users:
            self.teacher_ids.append(user_id)
            
            # Generar estudios variados en JSON
            num_studies = random.randint(1, 3)
            studies = random.sample(self.teacher_studies, num_studies)
            studies_json = json.dumps(studies)
            
            professional_license = f"ENT-{random.randint(1000, 9999)}" if not self.generate_null_value() else None
            
            query = """
                INSERT INTO teachers (id, studies, professional_license)
                VALUES (%s, %s, %s)
            """
            self.cursor.execute(query, (user_id, studies_json, professional_license))

    def generate_classes(self, count=25):
        """Generar clases de entrenamiento"""
        print(f"Generando {count} clases...")
        
        schedules = [
            'Lunes 16:00-18:00', 'Martes 17:00-19:00', 'Miércoles 15:00-17:00',
            'Jueves 16:00-18:00', 'Viernes 17:00-19:00', 'Sábado 09:00-11:00',
            'Sábado 14:00-16:00', 'Domingo 09:00-11:00'
        ]
        
        for i in range(count):
            class_id = str(uuid.uuid4())
            self.class_ids.append(class_id)
            
            class_type = random.choice(self.class_types)
            name = f"{class_type} - Grupo {chr(65 + i % 26)}"
            capacity = random.randint(15, 25)
            schedule = random.choice(schedules)
            
            query = """
                INSERT INTO classes (id, name, capacity, schedule, class_type)
                VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (class_id, name, capacity, schedule, class_type))

    def generate_classes_headquarters(self):
        """Generar relación clases-sedes"""
        print("Generando relaciones clases-sedes...")
        
        for class_id in self.class_ids:
            # Cada clase puede estar en 1-3 sedes
            num_headquarters = random.randint(1, 3)
            selected_hqs = random.sample(self.headquarter_ids, num_headquarters)
            
            for hq_id in selected_hqs:
                start_date = fake.date_between(start_date='-6M', end_date='today')
                end_date = start_date + timedelta(days=random.randint(90, 365))
                
                query = """
                    INSERT INTO classes_headquarters (id_class, id_headquarter, start_date, end_date)
                    VALUES (%s, %s, %s, %s)
                """
                self.cursor.execute(query, (class_id, hq_id, start_date, end_date))

    def generate_students_classes(self):
        """Generar inscripciones de estudiantes en clases"""
        print("Generando inscripciones estudiante-clase...")
        
        states = ['enrolled', 'active', 'withdrawn', 'completed']
        
        for student_id in self.student_ids:
            # Cada estudiante puede estar en 1-4 clases
            num_classes = random.randint(1, 4)
            selected_classes = random.sample(self.class_ids, min(num_classes, len(self.class_ids)))
            
            for class_id in selected_classes:
                state = random.choices(states, weights=[20, 60, 15, 5], k=1)[0]
                
                query = """
                    INSERT INTO students_classes (id_student, id_class, state)
                    VALUES (%s, %s, %s)
                """
                self.cursor.execute(query, (student_id, class_id, state))

    def generate_teachers_classes(self):
        """Generar asignación de profesores a clases"""
        print("Generando asignaciones profesor-clase...")
        
        roles = ['lead', 'assistant', 'substitute']
        
        for class_id in self.class_ids:
            # Cada clase tiene 1-2 profesores
            num_teachers = random.randint(1, 2)
            selected_teachers = random.sample(self.teacher_ids, min(num_teachers, len(self.teacher_ids)))
            
            for i, teacher_id in enumerate(selected_teachers):
                role = 'lead' if i == 0 else random.choice(['assistant', 'substitute'])
                start_date = fake.date_between(start_date='-6M', end_date='today')
                end_date = start_date + timedelta(days=random.randint(90, 365)) if random.random() > 0.7 else None
                
                query = """
                    INSERT INTO teachers_classes (id_teacher, id_class, teacher_role, start_date, end_date)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, (teacher_id, class_id, role, start_date, end_date))

    def generate_registration_fees(self):
        """Generar matrículas/registros"""
        print("Generando registros de matrícula...")
        
        states = ['active', 'expired', 'cancelled']
        
        for student_id in self.student_ids:
            # Cada estudiante puede tener 1-3 registros (históricos)
            num_registrations = random.randint(1, 3)
            
            for _ in range(num_registrations):
                reg_id = str(uuid.uuid4())
                self.registration_fee_ids.append(reg_id)
                
                start_date = fake.date_between(start_date='-1y', end_date='today')
                end_date = start_date + timedelta(days=random.randint(30, 365))
                state = random.choices(states, weights=[70, 20, 10], k=1)[0]
                
                query = """
                    INSERT INTO registration_fees (id, id_student, start_date, end_date, state)
                    VALUES (%s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, (reg_id, student_id, start_date, end_date, state))

    def generate_payments(self, target_count=50000):
        """Generar pagos (tabla operacional)"""
        print(f"Generando {target_count} pagos...")
        
        payment_methods = ['Efectivo', 'Tarjeta', 'Transferencia', 'PSE', 'Daviplata', 'Nequi']
        concepts = [
            'Mensualidad', 'Matrícula', 'Material deportivo', 'Torneo interno',
            'Campamento', 'Uniforme', 'Cuota adicional', 'Descuento hermanos',
            'Pago anticipado', 'Recargo por mora'
        ]
        
        payments_per_registration = target_count // len(self.registration_fee_ids)
        extra_payments = target_count % len(self.registration_fee_ids)
        
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
                
                query = """
                    INSERT INTO payments (id_registration_fee, amount, payment_date, payment_method, receipt_number, concept)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                self.cursor.execute(query, (reg_id, amount, payment_date, payment_method, receipt_number, concept))

    def generate_classes_attendances(self, target_count=50000):
        """Generar asistencias a clases (tabla operacional)"""
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
                
                try:
                    query = """
                        INSERT INTO classes_attendances (id_student, id_class, id_headquarter, id_teacher, date, attended, observations)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id_student, id_class, date) DO NOTHING
                    """
                    self.cursor.execute(query, (student_id, class_id, headquarter_id, teacher_id, attendance_date, attended, observations))
                except psycopg.IntegrityError:
                    # Ignorar duplicados por la restricción UNIQUE
                    continue

    def generate_all_data(self):
        """Generar todos los datos"""
        try:
            print("🚀 Iniciando generación de datos para escuela de fútbol...")
            
            # Generar datos maestros
            self.generate_headquarters(10)
            self.generate_users(100)
            self.generate_students(80)
            self.generate_teachers(15)
            self.generate_classes(25)
            
            # Commit datos maestros
            self.conn.commit()
            print("✓ Datos maestros generados")
            
            # Generar relaciones
            self.generate_classes_headquarters()
            self.generate_students_classes()
            self.generate_teachers_classes()
            self.generate_registration_fees()
            
            # Commit relaciones
            self.conn.commit()
            print("✓ Relaciones generadas")
            
            # Generar datos operacionales (grandes volúmenes)
            self.generate_payments(50000)
            self.conn.commit()
            print("✓ Pagos generados")
            
            self.generate_classes_attendances(50000)
            self.conn.commit()
            print("✓ Asistencias generadas")
            
            print("🎉 ¡Generación de datos completada exitosamente!")
            
        except Exception as e:
            print(f"✗ Error durante la generación: {e}")
            self.conn.rollback()
            raise

def main():
    generator = FootballSchoolDataGenerator()
    
    try:
        generator.connect_db()
        generator.generate_all_data()
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE DATOS GENERADOS:")
        print("=" * 50)
        
        tables_to_count = [
            'users', 'headquarters', 'students', 'teachers', 'classes',
            'students_classes', 'teachers_classes', 'registration_fees',
            'payments', 'classes_attendances'
        ]
        
        for table in tables_to_count:
            generator.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = generator.cursor.fetchone()[0]
            print(f"{table:20}: {count:>8,} registros")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        generator.close_db()

if __name__ == "__main__":
    main()
