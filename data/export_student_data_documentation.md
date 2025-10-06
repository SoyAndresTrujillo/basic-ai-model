# Student Payment Data Export Script - Documentation

## Overview

**Script Name:** `export_student_data.py`

**Purpose:** Business Intelligence (BI) focused data export tool that extracts student payment data from a PostgreSQL database and transforms it into a denormalized wide-format CSV file suitable for BI analysis and reporting.

**Version:** 1.0

**Author:** Generated for Football Academy Management System

---

## Table of Contents

1. [Introduction](#introduction)
2. [Data Model](#data-model)
3. [Export Structure](#export-structure)
4. [Technical Implementation](#technical-implementation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Output Format](#output-format)
8. [Examples](#examples)
9. [Dependencies](#dependencies)
10. [Troubleshooting](#troubleshooting)

---

## Introduction

This script performs ETL (Extract, Transform, Load) operations to create a denormalized dataset from a normalized relational database. The output is optimized for:

- **Business Intelligence Tools** (Power BI, Tableau, Looker)
- **Excel-based Analysis**
- **Statistical Analysis**
- **Data Warehousing**

### Key Features

✅ **One row per student** - Simplified analytical structure  
✅ **Dynamic column generation** - Columns expand based on actual data  
✅ **Payment-centric focus** - Optimized for revenue and payment analysis  
✅ **No dates or UUIDs** - Clean, human-readable output  
✅ **Handles variable records** - Students with different numbers of registrations/payments  

---

## Data Model

### Source Database Schema

The script extracts data from the following PostgreSQL tables:

```
students
├── users (1:1 relationship)
├── headquarters (N:1 relationship)
└── registration_fees (1:N relationship)
    └── payments (1:N relationship)
```

### Entity Relationships

```
STUDENT → REGISTRATION_FEES → PAYMENTS
   ↓
USERS & HEADQUARTERS
```

**Table Hierarchy:**

1. **`users`** - Base personal information
2. **`students`** - Student-specific data and status
3. **`headquarters`** - Campus/location information
4. **`registration_fees`** - Enrollment periods and fees
5. **`payments`** - Individual payment transactions

---

## Export Structure

### Denormalization Strategy

The script converts a **normalized relational structure** into a **wide-format table**:

**Before (Normalized):**
```
Student A → Registration 1 → Payment 1
                          → Payment 2
         → Registration 2 → Payment 1
                          → Payment 2
                          → Payment 3
```

**After (Denormalized):**
```
Student A | state_1 | amount_1_1 | amount_1_2 | state_2 | amount_2_1 | amount_2_2 | amount_2_3
```

### Column Naming Convention

The script uses a **hierarchical numbering system**:

- **`state_{N}`** - Registration fee state (N = registration number)
- **`amount_{N}_{M}`** - Payment amount (N = registration number, M = payment number)
- **`payment_method_{N}_{M}`** - Payment method
- **`receipt_number_{N}_{M}`** - Receipt number
- **`concept_{N}_{M}`** - Payment concept/description

**Example:**
- `amount_1_1` = First payment of first registration
- `amount_1_2` = Second payment of first registration
- `amount_2_1` = First payment of second registration

---

## Technical Implementation

### Data Flow

```
┌─────────────────┐
│  PostgreSQL DB  │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   SQL Query     │ ← Extract with CTEs & Window Functions
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Pandas DataFrame│ ← Long format data
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│ Denormalization │ ← Transform to wide format
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   CSV Export    │ ← Final output
└─────────────────┘
```

### SQL Query Components

#### 1. Student Base CTE
Extracts core student and user information:
```sql
WITH student_base AS (
    SELECT s.id, u.name, u.last_name, u.document_id, 
           s.state, h.name as headquarter_name
    FROM students s
    INNER JOIN users u ON s.id = u.id
    INNER JOIN headquarters h ON s.id_headquarter = h.id
)
```

#### 2. Registrations CTE
Numbers registration fees per student:
```sql
registrations AS (
    SELECT rf.id, rf.id_student, rf.state,
           ROW_NUMBER() OVER (PARTITION BY id_student 
                              ORDER BY created_at) as reg_number
    FROM registration_fees rf
)
```

#### 3. Payments CTE
Numbers payments per registration (limited to 10):
```sql
payments_data AS (
    SELECT p.id_registration_fee, p.amount, p.payment_method,
           ROW_NUMBER() OVER (PARTITION BY id_registration_fee 
                              ORDER BY created_at) as payment_number
    FROM payments p
)
```

### Transformation Algorithm

**`denormalize_student_data()` function:**

1. **Extract unique students** from long-format dataframe
2. **Iterate over each student:**
   - Initialize row with base student data
   - Find all registrations for the student
   - For each registration:
     - Add `state_{N}` column
     - Find all payments (max 10)
     - For each payment:
       - Add `amount_{N}_{M}` column
       - Add `payment_method_{N}_{M}` column
       - Add `receipt_number_{N}_{M}` column
       - Add `concept_{N}_{M}` column
3. **Build final dataframe** with all columns
4. **Sort columns** (student info first, then dynamic columns)

---

## Usage

### Basic Usage

```bash
python export_student_data.py
```

### Expected Output

```
🔌 Connecting to database...
📊 Extracting and transforming student payment data...
✓ Retrieved 80 student records
✓ Total columns: 131

📋 Columns included:
   1. name
   2. last_name
   3. type_document_id
   ...

📈 Data Summary:
  Total students: 80
  Active students: 71
  Total revenue: $275,696,084.67
  Payment columns: 30
  Registration columns: 3

💾 Exporting to CSV...
✅ Data successfully exported to: student_payment_bi_export_20251005_215433.csv
```

### Output File

The script generates a timestamped CSV file:

**Format:** `student_payment_bi_export_YYYYMMDD_HHMMSS.csv`

**Example:** `student_payment_bi_export_20251005_215433.csv`

---

## Configuration

### Database Connection

Edit the `DB_CONFIG` dictionary in the script:

```python
DB_CONFIG = {
    'host': 'localhost',      # Database server
    'port': 5432,             # PostgreSQL port
    'dbname': 'logictics_local',  # Database name
    'user': 'root',           # Username
    'password': 'root123'     # Password
}
```

### Payment Limit

By default, the script exports **up to 10 payments per registration**. To modify:

```python
# In SQL query (line 63):
AND pd.payment_number <= 10  # Change this number

# In denormalization function (line 122):
if payment_num <= 10:  # Change this number
```

---

## Output Format

### Column Structure

#### Fixed Columns (Student Base Data)

| Column | Type | Description |
|--------|------|-------------|
| `name` | String | Student first name |
| `last_name` | String | Student last name |
| `type_document_id` | String | ID type (CC, TI, CE, RC) |
| `document_id` | String | Unique document number |
| `email` | String | Student email |
| `phone` | String | Contact phone |
| `student_state` | String | active/inactive/suspended |
| `headquarter_name` | String | Campus/location name |

#### Dynamic Columns (Registration Data)

| Column Pattern | Type | Description | Example |
|----------------|------|-------------|---------|
| `state_{N}` | String | Registration status | `state_1` = "active" |

#### Dynamic Columns (Payment Data)

| Column Pattern | Type | Description | Example |
|----------------|------|-------------|---------|
| `amount_{N}_{M}` | Decimal | Payment amount | `amount_1_1` = 150000.00 |
| `payment_method_{N}_{M}` | String | Payment method | `payment_method_1_1` = "Tarjeta" |
| `receipt_number_{N}_{M}` | String | Receipt number | `receipt_number_1_1` = "REC-123456" |
| `concept_{N}_{M}` | String | Payment concept | `concept_1_1` = "Mensualidad" |

### Data Types

- **String fields:** May contain NULL values
- **Decimal fields:** Stored with 2 decimal places
- **Missing data:** Represented as empty cells in CSV

---

## Examples

### Example 1: Student with Single Registration and 3 Payments

| document_id | name | student_state | state_1 | amount_1_1 | payment_method_1_1 | amount_1_2 | payment_method_1_2 | amount_1_3 | payment_method_1_3 |
|-------------|------|---------------|---------|------------|--------------------|-----------|--------------------|-----------|-------------------|
| 12345678 | Juan | active | active | 150000.00 | Tarjeta | 150000.00 | Efectivo | 50000.00 | Transferencia |

### Example 2: Student with 2 Registrations

| document_id | name | state_1 | amount_1_1 | amount_1_2 | state_2 | amount_2_1 | amount_2_2 |
|-------------|------|---------|------------|------------|---------|------------|------------|
| 87654321 | Maria | expired | 100000.00 | 100000.00 | active | 175000.00 | 175000.00 |

### Example 3: Typical Export Statistics

```
Total students: 80
Total columns: 131
Registration columns: 3 (state_1, state_2, state_3)
Payment columns: 120 (30 per metric × 4 metrics)
Total revenue: $275,696,084.67
```

This indicates:
- 80 students in the database
- Maximum of 3 registrations per student
- Maximum of 10 payments per registration
- 4 payment metrics tracked (amount, method, receipt, concept)

---

## Dependencies

### Required Python Packages

Install using pip:

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
psycopg[binary]
pandas
faker==19.6.2
```

### Package Versions

- **psycopg** (v3.x) - PostgreSQL database adapter
- **pandas** (latest) - Data manipulation and analysis
- **Python** 3.8+ recommended

### Database Requirements

- **PostgreSQL** 12+ 
- **Database:** Must have the football academy schema installed
- **Tables required:**
  - `users`
  - `students`
  - `headquarters`
  - `registration_fees`
  - `payments`

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Error

**Error:**
```
❌ Database error: connection to server at "localhost" failed
```

**Solution:**
- Verify PostgreSQL is running: `pg_isready`
- Check `DB_CONFIG` credentials
- Verify database name exists
- Check firewall/network settings

#### 2. No Data Retrieved

**Error:**
```
✓ Retrieved 0 student records
```

**Solution:**
- Verify data exists in tables: `SELECT COUNT(*) FROM students;`
- Check foreign key relationships
- Run `generate_football_data.py` to populate database

#### 3. Column Count Mismatch

**Issue:** Different runs produce different column counts

**Explanation:** This is **normal behavior**. Column count varies based on:
- Number of registrations per student
- Number of payments per registration
- The script dynamically creates columns as needed

#### 4. Memory Issues with Large Datasets

**Error:**
```
MemoryError: Unable to allocate array
```

**Solution:**
- Process students in batches
- Reduce payment limit from 10 to 5
- Use chunked export for very large datasets

#### 5. Pandas Warning

**Warning:**
```
UserWarning: pandas only supports SQLAlchemy connectable
```

**Explanation:** This is a **harmless warning**. The script works correctly with psycopg connections. To suppress:

```python
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
```

Or upgrade to use SQLAlchemy:
```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://user:pass@localhost/dbname')
df = pd.read_sql_query(query, engine)
```

---

## Performance Considerations

### Execution Time

- **Small dataset** (<100 students): ~1-2 seconds
- **Medium dataset** (100-1,000 students): ~5-10 seconds  
- **Large dataset** (1,000-10,000 students): ~30-60 seconds

### Optimization Tips

1. **Database Indexes:** Ensure indexes on:
   - `students.id`
   - `registration_fees.id_student`
   - `payments.id_registration_fee`

2. **Limit Payment History:** Reduce from 10 to 5 most recent payments

3. **Filter Data:** Add WHERE clauses to focus on active students only

4. **Use Views:** Create a database view for the base query

---

## Advanced Usage

### Custom Filename

```python
filename = export_to_csv(df, filename='my_custom_export.csv')
```

### Filter Active Students Only

Add to SQL query:
```sql
WHERE s.state = 'active'
```

### Export Specific Date Range

Add to payments CTE:
```sql
WHERE p.payment_date BETWEEN '2024-01-01' AND '2024-12-31'
```

### Change Column Order

Modify in `denormalize_student_data()`:
```python
# Custom column sorting
ordered_cols = ['document_id', 'name', 'last_name', ...] + reg_payment_cols
result_df = result_df[ordered_cols]
```

---

## Business Intelligence Use Cases

### 1. Revenue Analysis
**Columns to use:**
- All `amount_{N}_{M}` columns
- `payment_method_{N}_{M}` for method analysis
- `headquarter_name` for location comparison

### 2. Payment Method Distribution
**Columns to use:**
- All `payment_method_{N}_{M}` columns
- Pivot/aggregate by method type

### 3. Student Lifecycle Analysis
**Columns to use:**
- `student_state` (current status)
- `state_{N}` (registration history)
- Count non-null registration columns

### 4. Headquarter Performance
**Columns to use:**
- `headquarter_name`
- Aggregate all `amount_*` columns
- Count students per location

---

## File Information

**Created:** 2025-10-05  
**Script Location:** `/path/to/export_student_data.py`  
**Output Location:** Same directory as script  
**Encoding:** UTF-8  
**CSV Separator:** Comma (,)  

---

## Support

For issues or questions:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify database schema matches expected structure
3. Review SQL query logic in the script
4. Test with sample data first

---

## License

This script is part of the Football Academy Management System project.

---

**End of Documentation**
