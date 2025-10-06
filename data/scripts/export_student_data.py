#!/usr/bin/env python3
"""
Business Intelligence Export Script - Student Payment Data
Exports denormalized student data with registration fees and payments in wide format.
One row per student with all their registration fees and associated payments.
"""

import psycopg
import pandas as pd
import sys
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'logictics_local',
    'user': 'root',
    'password': 'root123'
}

def get_student_payment_data(conn):
    """
    Extract student data with registration fees and payments in denormalized format.
    One row per student, with columns expanding based on number of registrations and payments.
    """
    
    # Query to get all student data with registration fees and payments
    query = """
    WITH student_base AS (
        SELECT 
            s.id as student_id,
            u.name,
            u.last_name,
            u.type_document_id,
            u.document_id,
            u.email,
            u.phone,
            s.state as student_state,
            h.name as headquarter_name
        FROM students s
        INNER JOIN users u ON s.id = u.id
        INNER JOIN headquarters h ON s.id_headquarter = h.id
    ),
    registrations AS (
        SELECT 
            rf.id as registration_id,
            rf.id_student,
            rf.state as registration_state,
            ROW_NUMBER() OVER (PARTITION BY rf.id_student ORDER BY rf.created_at) as reg_number
        FROM registration_fees rf
    ),
    payments_data AS (
        SELECT 
            p.id_registration_fee,
            p.amount,
            p.payment_method,
            p.receipt_number,
            p.concept,
            ROW_NUMBER() OVER (PARTITION BY p.id_registration_fee ORDER BY p.created_at) as payment_number
        FROM payments p
    )
    SELECT 
        sb.student_id,
        sb.name,
        sb.last_name,
        sb.type_document_id,
        sb.document_id,
        sb.email,
        sb.phone,
        sb.student_state,
        sb.headquarter_name,
        r.reg_number,
        r.registration_state,
        pd.payment_number,
        pd.amount,
        pd.payment_method,
        pd.receipt_number,
        pd.concept
    FROM student_base sb
    LEFT JOIN registrations r ON sb.student_id = r.id_student
    LEFT JOIN payments_data pd ON r.registration_id = pd.id_registration_fee AND pd.payment_number <= 10
    ORDER BY sb.document_id, r.reg_number, pd.payment_number
    """
    
    # Execute query and get data
    df = pd.read_sql_query(query, conn)
    
    # Transform to wide format
    wide_df = denormalize_student_data(df)
    
    return wide_df

def denormalize_student_data(df):
    """
    Convert long format data to wide format with one row per student.
    Creates columns like: state_1, amount_1_1, payment_method_1_1, etc.
    """
    
    # Get student base columns
    student_columns = ['name', 'last_name', 'type_document_id', 'document_id', 
                      'email', 'phone', 'student_state', 'headquarter_name']
    
    # Group by student to create one row per student
    students = df[student_columns].drop_duplicates(subset=['document_id'])
    
    # Process each student
    result_rows = []
    
    for _, student in students.iterrows():
        row_data = student.to_dict()
        
        # Get all data for this student
        student_data = df[df['document_id'] == student['document_id']]
        
        # Get unique registrations for this student
        registrations = student_data[['reg_number', 'registration_state']].dropna().drop_duplicates()
        
        # Process each registration
        for _, reg in registrations.iterrows():
            reg_num = int(reg['reg_number'])
            
            # Add registration state column
            row_data[f'state_{reg_num}'] = reg['registration_state']
            
            # Get payments for this registration
            payments = student_data[
                (student_data['reg_number'] == reg['reg_number']) & 
                (student_data['payment_number'].notna())
            ].sort_values('payment_number')
            
            # Add payment columns (up to 10 payments per registration)
            for _, payment in payments.iterrows():
                payment_num = int(payment['payment_number'])
                if payment_num <= 10:  # Limit to 10 payments as specified
                    row_data[f'amount_{reg_num}_{payment_num}'] = payment['amount']
                    row_data[f'payment_method_{reg_num}_{payment_num}'] = payment['payment_method']
                    row_data[f'receipt_number_{reg_num}_{payment_num}'] = payment['receipt_number']
                    row_data[f'concept_{reg_num}_{payment_num}'] = payment['concept']
        
        result_rows.append(row_data)
    
    # Create final dataframe
    result_df = pd.DataFrame(result_rows)
    
    # Sort columns logically: student info first, then registration/payment data
    student_cols = [col for col in student_columns if col in result_df.columns]
    reg_payment_cols = sorted([col for col in result_df.columns if col not in student_cols])
    
    result_df = result_df[student_cols + reg_payment_cols]
    
    return result_df

def export_to_csv(df, filename=None):
    """
    Export dataframe to CSV file.
    """
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'student_payment_bi_export_{timestamp}.csv'
    
    df.to_csv(filename, index=False, encoding='utf-8')
    return filename

def main():
    """
    Main function to connect to database, extract data, and export to CSV.
    """
    try:
        print("🔌 Connecting to database...")
        conn = psycopg.connect(**DB_CONFIG)
        
        print("📊 Extracting and transforming student payment data...")
        df = get_student_payment_data(conn)
        
        print(f"✓ Retrieved {len(df)} student records")
        print(f"✓ Total columns: {len(df.columns)}")
        
        # Display column names
        print("\n📋 Columns included:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Display basic statistics
        print("\n📈 Data Summary:")
        print(f"  Total students: {len(df)}")
        print(f"  Active students: {len(df[df['student_state'] == 'active'])}")
        
        # Count total payments columns
        payment_amount_cols = [col for col in df.columns if col.startswith('amount_')]
        if payment_amount_cols:
            total_revenue = df[payment_amount_cols].sum().sum()
            print(f"  Total revenue: ${total_revenue:,.2f}")
            print(f"  Payment columns: {len(payment_amount_cols)}")
        
        # Count registration columns
        state_cols = [col for col in df.columns if col.startswith('state_')]
        print(f"  Registration columns: {len(state_cols)}")
        
        # Export to CSV
        print("\n💾 Exporting to CSV...")
        filename = export_to_csv(df)
        print(f"✅ Data successfully exported to: {filename}")
        
        # Display sample data
        print("\n🔍 Sample data (first 2 rows, first 10 columns):")
        pd.set_option('display.max_columns', 10)
        pd.set_option('display.width', None)
        print(df.head(2))
        
        conn.close()
        
    except psycopg.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
