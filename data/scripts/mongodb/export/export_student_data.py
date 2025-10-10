#!/usr/bin/env python3
"""
Business Intelligence Export Script - Student Payment Data (MongoDB)
Exports denormalized student data with registration fees and payments in wide format.
One row per student with all their registration fees and associated payments.
"""

import os
import pandas as pd
import sys
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import Decimal128

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv('DB_URI_MONGO', 'mongodb://localhost:27017/')
DB_NAME = 'football_school_db'


def get_student_payment_data(db):
    """
    Extract student data with registration fees and payments in denormalized format.
    One row per student, with columns expanding based on number of registrations and payments.
    
    This function replicates the PostgreSQL query logic using MongoDB queries.
    Uses a simpler approach to avoid memory issues with large aggregations.
    """
    
    # Fetch all students with their user and headquarter data
    students = []
    for student in db.students.find():
        user = db.users.find_one({'_id': student['user_id']})
        headquarter = db.headquarters.find_one({'_id': student['headquarter_id']})
        
        if user and headquarter:
            students.append({
                'student_id': student['_id'],
                'name': user.get('name'),
                'last_name': user.get('last_name'),
                'type_document_id': user.get('type_document_id'),
                'document_id': user.get('document_id'),
                'email': user.get('email'),
                'phone': user.get('phone'),
                'student_state': student.get('state'),
                'headquarter_name': headquarter.get('name')
            })
    
    if not students:
        print("⚠️  No students found in database")
        return pd.DataFrame()
    
    # Build complete dataset with registrations and payments
    all_rows = []
    
    for student in students:
        student_id = student['student_id']
        
        # Get registrations for this student
        registrations = list(db.registration_fees.find(
            {'student_id': student_id}
        ).sort('created_at', 1))
        
        if not registrations:
            # Student with no registrations
            all_rows.append(student.copy())
            continue
        
        for reg_idx, registration in enumerate(registrations, 1):
            # Get payments for this registration (limit to 10 as per spec)
            payments = list(db.payments.find(
                {'registration_fee_id': registration['_id']}
            ).sort('created_at', 1).limit(10))
            
            if not payments:
                # Registration with no payments
                row = student.copy()
                row['reg_number'] = reg_idx
                row['registration_id'] = registration['_id']
                row['registration_state'] = registration.get('state')
                row['registration_created_at'] = registration.get('created_at')
                all_rows.append(row)
                continue
            
            for pay_idx, payment in enumerate(payments, 1):
                row = student.copy()
                row['reg_number'] = reg_idx
                row['registration_id'] = registration['_id']
                row['registration_state'] = registration.get('state')
                row['registration_created_at'] = registration.get('created_at')
                row['payment_number'] = pay_idx
                row['payment_id'] = payment['_id']
                row['amount'] = payment.get('amount')
                row['payment_method'] = payment.get('payment_method')
                row['receipt_number'] = payment.get('receipt_number')
                row['concept'] = payment.get('concept')
                row['payment_created_at'] = payment.get('created_at')
                all_rows.append(row)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_rows)
    
    if df.empty:
        print("⚠️  No data found")
        return pd.DataFrame()
    
    # Sort by document_id
    df = df.sort_values(['document_id', 'reg_number', 'payment_number'], 
                        na_position='first').reset_index(drop=True)
    
    # Transform to wide format
    wide_df = denormalize_student_data(df)
    
    return wide_df


def denormalize_student_data(df):
    """
    Convert long format data to wide format with one row per student.
    Creates columns like: state_1, amount_1_1, payment_method_1_1, etc.
    
    This matches the exact structure from the PostgreSQL export.
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
                    # Convert Decimal128 to float for amount
                    amount_value = payment['amount']
                    if isinstance(amount_value, Decimal128):
                        amount_value = float(amount_value.to_decimal())
                    
                    row_data[f'amount_{reg_num}_{payment_num}'] = amount_value
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
        filename = f'student_payment_bi_export_mongodb_{timestamp}.csv'
    
    df.to_csv(filename, index=False, encoding='utf-8')
    return filename


def main():
    """
    Main function to connect to MongoDB, extract data, and export to CSV.
    """
    try:
        print("🔌 Connecting to MongoDB...")
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Verify connection
        client.admin.command('ping')
        print(f"✓ Connected to database: {DB_NAME}")
        
        print("📊 Extracting and transforming student payment data...")
        df = get_student_payment_data(db)
        
        if df.empty:
            print("❌ No data to export")
            sys.exit(1)
        
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
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
