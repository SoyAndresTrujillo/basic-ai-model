# MongoDB Data Export - Business Intelligence

## Overview

This directory contains scripts to export data from MongoDB in denormalized format suitable for Business Intelligence analysis.

## Files

- **export_student_data.py**: Exports student payment data in wide format (one row per student)

## Export Script: export_student_data.py

### Purpose

Exports denormalized student data with registration fees and payments. The data is transformed from MongoDB's document structure into a wide format CSV file with one row per student, making it ideal for BI tools and analysis.

### Data Structure

The export creates a wide-format CSV with the following structure:

#### Student Base Columns (8 columns)
- `name` - Student first name
- `last_name` - Student last name
- `type_document_id` - Document type (CC, TI, CE, RC)
- `document_id` - Document number (unique identifier)
- `email` - Student email
- `phone` - Student phone number
- `student_state` - Student status (active, inactive, suspended)
- `headquarter_name` - Name of the headquarter/location

#### Registration Columns (dynamic)
- `state_1`, `state_2`, `state_3`, ... - Registration status for each registration period

#### Payment Columns (dynamic, up to 10 per registration)
For each registration (1, 2, 3...) and payment (1-10):
- `amount_X_Y` - Payment amount (X=registration number, Y=payment number)
- `payment_method_X_Y` - Payment method (Efectivo, Tarjeta, Transferencia, etc.)
- `receipt_number_X_Y` - Receipt number
- `concept_X_Y` - Payment concept/description

### Usage

```bash
# Activate virtual environment
source logistic_project_env/bin/activate

# Run export script
python data/scripts/mongodb/export/export_student_data.py
```

### Output

The script generates a CSV file with the naming pattern:
```
student_payment_bi_export_mongodb_YYYYMMDD_HHMMSS.csv
```

Example output:
```
✓ Retrieved 80 student records
✓ Total columns: 131
Total students: 80
Active students: 70
Total revenue: $278,414,362.83
Payment columns: 30
Registration columns: 3
✅ Data successfully exported to: student_payment_bi_export_mongodb_20251009_224138.csv
```

### Configuration

The script uses environment variables from the `.env` file:
- `DB_URI_MONGO` - MongoDB connection string (default: `mongodb://localhost:27017/`)

Database name is hardcoded to: `football_school_db`

### Features

1. **Denormalized Structure**: Converts MongoDB's normalized collections into a single wide table
2. **One Row Per Student**: Each student appears once with all their data
3. **Limited Payments**: Exports up to 10 payments per registration (as per specification)
4. **Sorted Output**: Data sorted by document_id for consistency
5. **Memory Efficient**: Uses iterative approach instead of large aggregations
6. **Decimal Handling**: Properly converts MongoDB Decimal128 to float values

### Data Flow

```
MongoDB Collections:
├── students
├── users
├── headquarters
├── registration_fees
└── payments

        ↓ (Join & Transform)

Wide Format CSV:
One row per student with all registrations and payments
```

### Comparison with PostgreSQL Export

This script replicates the exact same logic and output structure as the PostgreSQL export script:
- Same column naming convention
- Same data ordering (by document_id)
- Same limit of 10 payments per registration
- Same wide-format transformation

**Key Differences:**
- Uses MongoDB queries instead of SQL
- Handles MongoDB-specific types (ObjectId, Decimal128)
- Iterative approach to avoid aggregation memory limits

### Example Data Structure

```csv
name,last_name,document_id,email,state_1,amount_1_1,payment_method_1_1,amount_1_2,...
Juan,Pérez,12345678,juan@example.com,active,150000.00,Tarjeta,150000.00,...
María,García,87654321,maria@example.com,active,200000.00,Efectivo,200000.00,...
```

### Performance Considerations

- **Students**: Iterates through all students (80 in test data)
- **Registrations**: Fetches per student (1-3 per student typically)
- **Payments**: Limited to 10 per registration
- **Memory**: Efficient for datasets up to 10,000 students
- **Export Time**: ~2-5 seconds for 80 students with 50,000 payments

### Troubleshooting

#### Connection Issues
```bash
# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"

# Check .env file
cat .env | grep DB_URI_MONGO
```

#### No Data Exported
- Verify database name is correct (`football_school_db`)
- Check if data exists: `python data/scripts/mongodb/verify_data.py`
- Ensure students collection has records

#### Memory Issues
The script uses an iterative approach to avoid memory issues. If you still encounter problems with very large datasets:
- Process students in batches
- Reduce payment limit from 10 to fewer
- Export specific student segments

### Integration with BI Tools

The exported CSV can be directly imported into:
- **Power BI**: Use "Get Data" → "Text/CSV"
- **Tableau**: Connect to CSV file
- **Excel**: Open CSV or import as table
- **Python/Pandas**: `pd.read_csv('filename.csv')`
- **R**: `read.csv('filename.csv')`

### Data Quality

The export includes:
- ✅ All student records from MongoDB
- ✅ Null values preserved (empty cells in CSV)
- ✅ Decimal precision maintained
- ✅ Special characters properly encoded (UTF-8)
- ✅ Consistent column ordering

### Future Enhancements

Potential improvements:
1. Add command-line arguments for date ranges
2. Export other entities (teachers, classes, attendances)
3. Support multiple output formats (Excel, Parquet, JSON)
4. Add data validation and quality checks
5. Implement incremental exports
6. Add filtering options (by headquarter, state, etc.)

## Related Scripts

- **PostgreSQL Export**: `/data/scripts/postgres/export/export_student_data.py`
- **MongoDB Data Generation**: `/data/scripts/mongodb/generate_football_data_mongodb.py`
- **Data Verification**: `/data/scripts/mongodb/verify_data.py`
