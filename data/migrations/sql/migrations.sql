-- Academic Management System Database Schema for PostgreSQL
-- Generated from Mermaid ER Diagram

-- Enable UUID extension (required for UUID generation)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Main Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    type_document_id VARCHAR(20) NOT NULL,
    document_id VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    birthday DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger function for auto-updating updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for users table
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Headquarters table
CREATE TABLE headquarters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    legal_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger for headquarters table
CREATE TRIGGER update_headquarters_updated_at 
    BEFORE UPDATE ON headquarters 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Students table (inherits from users)
CREATE TABLE students (
    id UUID PRIMARY KEY,
    id_headquarter UUID NOT NULL,
    state VARCHAR(20) CHECK (state IN ('active', 'inactive', 'suspended')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (id_headquarter) REFERENCES headquarters(id) ON DELETE RESTRICT
);

-- Create trigger for students table
CREATE TRIGGER update_students_updated_at 
    BEFORE UPDATE ON students 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Teachers table (inherits from users)
CREATE TABLE teachers (
    id UUID PRIMARY KEY,
    studies JSONB,
    professional_license VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create trigger for teachers table
CREATE TRIGGER update_teachers_updated_at 
    BEFORE UPDATE ON teachers 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Classes table
CREATE TABLE classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    schedule VARCHAR(100) NOT NULL,
    class_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create trigger for classes table
CREATE TRIGGER update_classes_updated_at 
    BEFORE UPDATE ON classes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Classes_headquarters junction table
CREATE TABLE classes_headquarters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_class UUID NOT NULL,
    id_headquarter UUID NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (id_class) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_headquarter) REFERENCES headquarters(id) ON DELETE CASCADE,
    UNIQUE (id_class, id_headquarter, start_date)
);

-- Students_classes junction table
CREATE TABLE students_classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_student UUID NOT NULL,
    id_class UUID NOT NULL,
    state VARCHAR(20) CHECK (state IN ('enrolled', 'active', 'withdrawn', 'completed')) DEFAULT 'enrolled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_student) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (id_class) REFERENCES classes(id) ON DELETE CASCADE,
    UNIQUE (id_student, id_class)
);

-- Create trigger for students_classes table
CREATE TRIGGER update_students_classes_updated_at 
    BEFORE UPDATE ON students_classes 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Teachers_classes junction table
CREATE TABLE teachers_classes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_teacher UUID NOT NULL,
    id_class UUID NOT NULL,
    teacher_role VARCHAR(20) CHECK (teacher_role IN ('lead', 'assistant', 'substitute')) DEFAULT 'lead',
    start_date DATE NOT NULL,
    end_date DATE,
    FOREIGN KEY (id_teacher) REFERENCES teachers(id) ON DELETE CASCADE,
    FOREIGN KEY (id_class) REFERENCES classes(id) ON DELETE CASCADE
);

-- Registration fees table
CREATE TABLE registration_fees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_student UUID NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    state VARCHAR(20) CHECK (state IN ('active', 'expired', 'cancelled')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_student) REFERENCES students(id) ON DELETE CASCADE
);

-- Create trigger for registrations_fees table
CREATE TRIGGER update_registration_fees_updated_at 
    BEFORE UPDATE ON registration_fees 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Payment table
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_registration_fee UUID NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    receipt_number VARCHAR(100),
    concept VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_registration_fee) REFERENCES registration_fees(id) ON DELETE CASCADE
);

-- Create trigger for payment table
CREATE TRIGGER update_payments_updated_at 
    BEFORE UPDATE ON payments
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Classes attendances table
CREATE TABLE classes_attendances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    id_student UUID NOT NULL,
    id_class UUID NOT NULL,
    id_headquarter UUID NOT NULL,
    id_teacher UUID NOT NULL,
    date DATE NOT NULL,
    attended BOOLEAN DEFAULT FALSE,
    observations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_student) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (id_class) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_headquarter) REFERENCES headquarters(id) ON DELETE CASCADE,
    FOREIGN KEY (id_teacher) REFERENCES teachers(id) ON DELETE CASCADE,
    UNIQUE (id_student, id_class, date)
);

-- Create trigger for classes_attendances table
CREATE TRIGGER update_classes_attendances_updated_at 
    BEFORE UPDATE ON classes_attendances 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
