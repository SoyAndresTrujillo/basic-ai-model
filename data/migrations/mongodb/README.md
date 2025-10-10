# MongoDB Implementation - Football School Management System

## Overview

This directory contains the MongoDB schema design and migration scripts for the Football School Management System. The implementation mirrors the PostgreSQL schema but leverages MongoDB's document-oriented features.

## Files

- **schema.md**: Complete MongoDB schema documentation with collection structures, indexes, and design decisions
- **../scripts/generate_football_data_mongodb.py**: Python script to generate test data in MongoDB

## Prerequisites

1. **MongoDB Server**: MongoDB 4.0 or higher installed and running
2. **Python Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**: Configure MongoDB connection in `.env` file
   ```env
   DB_URI_MONGO=mongodb://localhost:27017/
   ```

## Quick Start

### 1. Start MongoDB

Ensure MongoDB is running on your system:

```bash
# macOS (using Homebrew)
brew services start mongodb-community

# Or run manually
mongod --config /usr/local/etc/mongod.conf
```

### 2. Configure Connection

Create or update your `.env` file in the project root:

```env
DB_URI_MONGO=mongodb://localhost:27017/
```

For MongoDB Atlas or remote servers:
```env
DB_URI_MONGO=mongodb+srv://username:password@cluster.mongodb.net/
```

### 3. Generate Test Data

Run the data generation script:

```bash
python data/scripts/generate_football_data_mongodb.py
```

This will:
- Create database: `football_school_db`
- Generate 10 headquarters
- Generate 100 users
- Generate 80 students
- Generate 15 teachers
- Generate 25 classes
- Generate relationships between entities
- Generate 50,000 payments
- Generate 50,000 attendance records
- Create all necessary indexes

## Database Structure

### Collections

1. **users** - Base user information
2. **headquarters** - School locations
3. **students** - Student-specific data
4. **teachers** - Teacher-specific data with embedded studies
5. **classes** - Class/course information
6. **classes_headquarters** - Class-location relationships
7. **students_classes** - Student enrollments
8. **teachers_classes** - Teacher assignments
9. **registration_fees** - Student registration periods
10. **payments** - Payment transactions (high-volume)
11. **classes_attendances** - Attendance records (high-volume)

### Key Features

- **ObjectId References**: Native MongoDB IDs for relationships
- **Embedded Documents**: Teacher studies stored as embedded arrays
- **Indexes**: Optimized for common query patterns
- **Data Quality**: Includes realistic test data with:
  - 10% null values
  - 5% duplicate records
  - Varied data formats (phone numbers, etc.)
  - 50,000+ operational records

## Connecting to MongoDB

### Using MongoDB Shell

```bash
mongosh

use football_school_db

# View collections
show collections

# Count documents
db.users.countDocuments()
db.payments.countDocuments()

# Sample query
db.students.find({ state: "active" }).limit(5)
```

### Using Python

```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('DB_URI_MONGO'))
db = client['football_school_db']

# Query examples
active_students = db.students.find({ 'state': 'active' })
recent_payments = db.payments.find().sort('payment_date', -1).limit(10)
```

### Using MongoDB Compass

1. Download MongoDB Compass: https://www.mongodb.com/products/compass
2. Connect using your connection string
3. Browse collections and run queries visually

## Data Generation Details

The script generates realistic test data with the following characteristics:

- **Headquarters**: 10 locations in Bogotá
- **Users**: 100 users with Colombian document types (CC, TI, CE, RC)
- **Students**: 80 students distributed across headquarters
- **Teachers**: 15 teachers with varied educational backgrounds
- **Classes**: 25 classes with different types and schedules
- **Payments**: 50,000 payment records with various methods
- **Attendances**: 50,000 attendance records with observations

### Data Quality Features

- **Null Values**: ~10% of optional fields are null
- **Duplicates**: ~5% duplicate user records (different IDs)
- **Format Variations**: Phone numbers in multiple formats
- **Realistic Dates**: Date ranges from last year to present
- **Weighted Distributions**: Active students (85%), payment methods, etc.

## Indexes

All collections have optimized indexes for:
- Unique constraints (document_id, user_id references)
- Foreign key lookups
- Common query patterns
- Date range queries
- Compound indexes for complex queries

See `schema.md` for complete index documentation.

## Comparison with PostgreSQL

| Feature | PostgreSQL | MongoDB |
|---------|-----------|---------|
| IDs | UUID | ObjectId |
| JSON Fields | JSONB | Native Documents |
| Timestamps | Triggers | Application Logic |
| Foreign Keys | Database Constraints | Application Validation |
| Transactions | Full ACID | Multi-document Transactions |
| Indexes | B-tree, GiST, etc. | B-tree, Compound, Text |

## Performance Considerations

1. **Batch Inserts**: Large collections use batch inserts (1000 docs/batch)
2. **Index Creation**: Indexes created after data insertion for better performance
3. **Sharding Ready**: High-volume collections can be sharded by date
4. **Connection Pooling**: Use connection pooling in production

## Troubleshooting

### Connection Issues

```bash
# Check if MongoDB is running
brew services list | grep mongodb

# Check MongoDB logs
tail -f /usr/local/var/log/mongodb/mongo.log
```

### Permission Issues

```bash
# Fix data directory permissions
sudo chown -R $(whoami) /usr/local/var/mongodb
```

### Script Errors

- Ensure `.env` file exists with `DB_URI_MONGO`
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check MongoDB is accessible: `mongosh`

## Next Steps

1. **Query Optimization**: Add more indexes based on query patterns
2. **Aggregation Pipelines**: Create views for common reports
3. **Data Validation**: Implement schema validation rules
4. **Backup Strategy**: Set up automated backups
5. **Monitoring**: Configure MongoDB monitoring tools

## Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB University](https://university.mongodb.com/) - Free courses
- [MongoDB Compass](https://www.mongodb.com/products/compass) - GUI tool
