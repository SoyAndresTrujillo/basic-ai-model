-- Academic Management System - Seed Data for PostgreSQL
-- This script populates the database with sample data

-- Clear existing data (optional - uncomment if needed)
-- TRUNCATE TABLE classes_attendances, payments, registration_fees, teachers_classes, students_classes, classes_headquarters, classes, teachers, students, headquarters, users CASCADE;

-- Insert Users (base table for students and teachers)
INSERT INTO users (id, name, last_name, type_document_id, document_id, email, phone, birthday) VALUES
-- Students
('550e8400-e29b-41d4-a716-446655440001', 'Ana', 'García', 'CC', '12345678', 'ana.garcia@email.com', '555-0101', '1995-03-15'),
('550e8400-e29b-41d4-a716-446655440002', 'Carlos', 'López', 'CC', '23456789', 'carlos.lopez@email.com', '555-0102', '1998-07-22'),
('550e8400-e29b-41d4-a716-446655440003', 'María', 'Rodríguez', 'CC', '34567890', 'maria.rodriguez@email.com', '555-0103', '1997-11-08'),
('550e8400-e29b-41d4-a716-446655440004', 'David', 'Martínez', 'TI', '45678901', 'david.martinez@email.com', '555-0104', '2000-01-30'),
('550e8400-e29b-41d4-a716-446655440005', 'Laura', 'González', 'CC', '56789012', 'laura.gonzalez@email.com', '555-0105', '1996-09-12'),
('550e8400-e29b-41d4-a716-446655440006', 'Pedro', 'Hernández', 'CC', '67890123', 'pedro.hernandez@email.com', '555-0106', '1999-04-18'),
('550e8400-e29b-41d4-a716-446655440007', 'Sofia', 'Jiménez', 'CC', '78901234', 'sofia.jimenez@email.com', '555-0107', '1994-12-03'),
('550e8400-e29b-41d4-a716-446655440008', 'Miguel', 'Torres', 'CC', '89012345', 'miguel.torres@email.com', '555-0108', '2001-06-25'),

-- Teachers
('550e8400-e29b-41d4-a716-446655440101', 'Dr. Roberto', 'Silva', 'CC', '11223344', 'roberto.silva@academy.com', '555-0201', '1975-08-14'),
('550e8400-e29b-41d4-a716-446655440102', 'Dra. Carmen', 'Vega', 'CC', '22334455', 'carmen.vega@academy.com', '555-0202', '1980-02-28'),
('550e8400-e29b-41d4-a716-446655440103', 'Prof. Luis', 'Morales', 'CC', '33445566', 'luis.morales@academy.com', '555-0203', '1978-10-17'),
('550e8400-e29b-41d4-a716-446655440104', 'Dra. Isabel', 'Ruiz', 'CC', '44556677', 'isabel.ruiz@academy.com', '555-0204', '1983-05-09');

-- Insert Headquarters
INSERT INTO headquarters (id, name, address, legal_name) VALUES
('660e8400-e29b-41d4-a716-446655440001', 'Campus Principal', 'Av. Libertador 1234, Bogotá', 'Academia Excellence S.A.S.'),
('660e8400-e29b-41d4-a716-446655440002', 'Sede Norte', 'Calle 127 #15-32, Bogotá', 'Academia Excellence S.A.S.'),
('660e8400-e29b-41d4-a716-446655440003', 'Sede Sur', 'Carrera 30 #40-25, Bogotá', 'Academia Excellence S.A.S.');

-- Insert Students (linking to users)
INSERT INTO students (id, id_headquarter, state) VALUES
('550e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', 'active'),
('550e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', 'active'),
('550e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', 'active'),
('550e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440002', 'active'),
('550e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440003', 'active'),
('550e8400-e29b-41d4-a716-446655440006', '660e8400-e29b-41d4-a716-446655440003', 'suspended'),
('550e8400-e29b-41d4-a716-446655440007', '660e8400-e29b-41d4-a716-446655440001', 'active'),
('550e8400-e29b-41d4-a716-446655440008', '660e8400-e29b-41d4-a716-446655440002', 'inactive');

-- Insert Teachers (linking to users)
INSERT INTO teachers (id, studies, professional_license) VALUES
('550e8400-e29b-41d4-a716-446655440101', 
 '{"degree": "PhD in Mathematics", "university": "Universidad Nacional", "year": 2005, "certifications": ["Advanced Calculus", "Linear Algebra"]}', 
 'MAT-2005-001'),
('550e8400-e29b-41d4-a716-446655440102', 
 '{"degree": "Master in Physics", "university": "Universidad de los Andes", "year": 2008, "certifications": ["Quantum Physics", "Thermodynamics"]}', 
 'PHY-2008-042'),
('550e8400-e29b-41d4-a716-446655440103', 
 '{"degree": "Bachelor in Computer Science", "university": "Universidad Javeriana", "year": 2003, "certifications": ["Java Programming", "Database Design"]}', 
 'CS-2003-156'),
('550e8400-e29b-41d4-a716-446655440104', 
 '{"degree": "PhD in Chemistry", "university": "Universidad Nacional", "year": 2010, "certifications": ["Organic Chemistry", "Lab Safety"]}', 
 'CHE-2010-089');

-- Insert Classes
INSERT INTO classes (id, name, capacity, schedule, class_type) VALUES
('770e8400-e29b-41d4-a716-446655440001', 'Cálculo I', 30, 'Lunes y Miércoles 8:00-10:00', 'Matemáticas'),
('770e8400-e29b-41d4-a716-446655440002', 'Física General', 25, 'Martes y Jueves 10:00-12:00', 'Ciencias'),
('770e8400-e29b-41d4-a716-446655440003', 'Programación Java', 20, 'Miércoles y Viernes 14:00-16:00', 'Informática'),
('770e8400-e29b-41d4-a716-446655440004', 'Química Orgánica', 15, 'Lunes y Viernes 16:00-18:00', 'Química'),
('770e8400-e29b-41d4-a716-446655440005', 'Álgebra Linear', 25, 'Martes y Jueves 8:00-10:00', 'Matemáticas');

-- Insert Classes_headquarters (which classes are taught where)
INSERT INTO classes_headquarters (id, id_class, id_headquarter, start_date, end_date) VALUES
('880e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '2024-02-01', '2024-06-30'),
('880e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', '2024-02-01', '2024-06-30'),
('880e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', '2024-02-01', '2024-06-30'),
('880e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440003', '2024-02-01', '2024-06-30'),
('880e8400-e29b-41d4-a716-446655440005', '770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440002', '2024-02-01', '2024-06-30');

-- Insert Students_classes (student enrollments)
INSERT INTO students_classes (id, id_student, id_class, state) VALUES
('990e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', 'active'),
('990e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440002', 'active'),
('990e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440001', 'active'),
('990e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440003', 'active'),
('990e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440002', 'enrolled'),
('990e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440005', '770e8400-e29b-41d4-a716-446655440004', 'active'),
('990e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440007', '770e8400-e29b-41d4-a716-446655440005', 'active'),
('990e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440003', 'completed');

-- Insert Teachers_classes (teacher assignments)
INSERT INTO teachers_classes (id, id_teacher, id_class, teacher_role, start_date, end_date) VALUES
('aa0e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440101', '770e8400-e29b-41d4-a716-446655440001', 'lead', '2024-02-01', '2024-06-30'),
('aa0e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440101', '770e8400-e29b-41d4-a716-446655440005', 'lead', '2024-02-01', '2024-06-30'),
('aa0e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440102', '770e8400-e29b-41d4-a716-446655440002', 'lead', '2024-02-01', '2024-06-30'),
('aa0e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440103', '770e8400-e29b-41d4-a716-446655440003', 'lead', '2024-02-01', '2024-06-30'),
('aa0e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440104', '770e8400-e29b-41d4-a716-446655440004', 'lead', '2024-02-01', '2024-06-30'),
('aa0e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440102', '770e8400-e29b-41d4-a716-446655440001', 'assistant', '2024-02-01', '2024-06-30');

-- Insert Registration_fees
INSERT INTO registration_fees (id, id_student, start_date, end_date, state) VALUES
('bb0e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', '2024-02-01', '2024-06-30', 'active'),
('bb0e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002', '2024-02-01', '2024-06-30', 'active'),
('bb0e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440003', '2024-02-01', '2024-06-30', 'active'),
('bb0e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440004', '2024-02-01', '2024-06-30', 'active'),
('bb0e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440005', '2024-02-01', '2024-06-30', 'active'),
('bb0e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440006', '2024-02-01', '2024-06-30', 'cancelled'),
('bb0e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440007', '2024-02-01', '2024-06-30', 'active'),
('bb0e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440008', '2024-02-01', '2024-06-30', 'expired');

-- Insert Payments
INSERT INTO payments (id, id_registration_fee, amount, payment_date, payment_method, receipt_number, concept) VALUES
('cc0e8400-e29b-41d4-a716-446655440001', 'bb0e8400-e29b-41d4-a716-446655440001', 450000.00, '2024-01-15', 'Transferencia bancaria', 'REC-2024-001', 'Matrícula semestre 2024-1'),
('cc0e8400-e29b-41d4-a716-446655440002', 'bb0e8400-e29b-41d4-a716-446655440001', 300000.00, '2024-03-15', 'Tarjeta de crédito', 'REC-2024-015', 'Mensualidad marzo 2024'),
('cc0e8400-e29b-41d4-a716-446655440003', 'bb0e8400-e29b-41d4-a716-446655440002', 450000.00, '2024-01-20', 'Efectivo', 'REC-2024-002', 'Matrícula semestre 2024-1'),
('cc0e8400-e29b-41d4-a716-446655440004', 'bb0e8400-e29b-41d4-a716-446655440003', 450000.00, '2024-01-25', 'PSE', 'REC-2024-003', 'Matrícula semestre 2024-1'),
('cc0e8400-e29b-41d4-a716-446655440005', 'bb0e8400-e29b-41d4-a716-446655440004', 450000.00, '2024-02-01', 'Transferencia bancaria', 'REC-2024-004', 'Matrícula semestre 2024-1'),
('cc0e8400-e29b-41d4-a716-446655440006', 'bb0e8400-e29b-41d4-a716-446655440005', 450000.00, '2024-02-05', 'Tarjeta de débito', 'REC-2024-005', 'Matrícula semestre 2024-1'),
('cc0e8400-e29b-41d4-a716-446655440007', 'bb0e8400-e29b-41d4-a716-446655440007', 450000.00, '2024-01-30', 'PSE', 'REC-2024-006', 'Matrícula semestre 2024-1'),
('cc0e8400-e29b-41d4-a716-446655440008', 'bb0e8400-e29b-41d4-a716-446655440002', 300000.00, '2024-04-15', 'Efectivo', 'REC-2024-032', 'Mensualidad abril 2024'),
('cc0e8400-e29b-41d4-a716-446655440009', 'bb0e8400-e29b-41d4-a716-446655440003', 300000.00, '2024-03-20', 'Transferencia bancaria', 'REC-2024-018', 'Mensualidad marzo 2024'),
('cc0e8400-e29b-41d4-a716-446655440010', 'bb0e8400-e29b-41d4-a716-446655440005', 300000.00, '2024-04-10', 'Tarjeta de crédito', 'REC-2024-028', 'Mensualidad abril 2024');

-- Insert Classes_attendances
INSERT INTO classes_attendances (id, id_student, id_class, id_headquarter, id_teacher, date, attended, observations) VALUES
-- Ana García attendance
('dd0e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440101', '2024-02-05', true, 'Excelente participación'),
('dd0e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440101', '2024-02-07', true, 'Buen desempeño'),
('dd0e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440001', '770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440102', '2024-02-06', true, 'Muy atenta en clase'),

-- Carlos López attendance  
('dd0e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440101', '2024-02-05', false, 'Justificó inasistencia por enfermedad'),
('dd0e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440001', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440101', '2024-02-07', true, 'Se puso al día con los temas'),
('dd0e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440002', '770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440103', '2024-02-07', true, 'Demostró interés en programación'),

-- María Rodríguez attendance
('dd0e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440103', '2024-02-07', true, 'Realizó ejercicios prácticos exitosamente'),
('dd0e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440003', '770e8400-e29b-41d4-a716-446655440003', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440103', '2024-02-09', true, 'Presentó proyecto parcial'),

-- David Martínez attendance
('dd0e8400-e29b-41d4-a716-446655440009', '550e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440102', '2024-02-06', true, 'Participó activamente en laboratorio'),
('dd0e8400-e29b-41d4-a716-446655440010', '550e8400-e29b-41d4-a716-446655440004', '770e8400-e29b-41d4-a716-446655440002', '660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440102', '2024-02-08', true, 'Excelente comprensión de conceptos'),

-- Laura González attendance  
('dd0e8400-e29b-41d4-a716-446655440011', '550e8400-e29b-41d4-a716-446655440005', '770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440104', '2024-02-05', true, 'Demostró conocimientos previos sólidos'),
('dd0e8400-e29b-41d4-a716-446655440012', '550e8400-e29b-41d4-a716-446655440005', '770e8400-e29b-41d4-a716-446655440004', '660e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440104', '2024-02-09', true, 'Participó en discusión grupal'),

-- Sofia Jiménez attendance
('dd0e8400-e29b-41d4-a716-446655440013', '550e8400-e29b-41d4-a716-446655440007', '770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440101', '2024-02-06', true, 'Resolvió ejercicios correctamente'),
('dd0e8400-e29b-41d4-a716-446655440014', '550e8400-e29b-41d4-a716-446655440007', '770e8400-e29b-41d4-a716-446655440005', '660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440101', '2024-02-08', false, 'Llegó tarde por transporte público');

-- Verification queries (uncomment to test data)
/*
-- Total students per headquarters
SELECT h.name as headquarters, COUNT(s.id) as student_count
FROM headquarters h
LEFT JOIN students s ON h.id = s.id_headquarter
GROUP BY h.id, h.name;

-- Classes with teacher assignments
SELECT c.name as class_name, u.name || ' ' || u.last_name as teacher_name, tc.teacher_role
FROM classes c
JOIN teachers_classes tc ON c.id = tc.id_class
JOIN teachers t ON tc.id_teacher = t.id
JOIN users u ON t.id = u.id;

-- Student enrollment summary
SELECT u.name || ' ' || u.last_name as student_name, COUNT(sc.id_class) as enrolled_classes
FROM users u
JOIN students s ON u.id = s.id
LEFT JOIN students_classes sc ON s.id = sc.id_student
GROUP BY u.id, u.name, u.last_name;
*/
