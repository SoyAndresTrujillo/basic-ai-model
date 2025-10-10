# MongoDB Schema - Academic Management System

## Overview
This document describes the MongoDB schema design for the Academic Management System. The schema is designed to leverage MongoDB's document-oriented nature while maintaining data integrity and query performance.

## Collections

### 1. users
Stores all user information (students and teachers).

```javascript
{
  _id: ObjectId,
  name: String,
  last_name: String,
  type_document_id: String,  // 'CC', 'TI', 'CE', 'RC'
  document_id: String,       // Unique
  email: String,
  phone: String,
  birthday: Date,
  user_type: String,         // 'student', 'teacher'
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ document_id: 1 }` - unique
- `{ email: 1 }`
- `{ user_type: 1 }`

---

### 2. headquarters
Stores information about school locations/headquarters.

```javascript
{
  _id: ObjectId,
  name: String,
  address: String,
  legal_name: String,
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ name: 1 }`

---

### 3. students
Stores student-specific information with embedded user reference.

```javascript
{
  _id: ObjectId,              // Same as user_id for easy reference
  user_id: ObjectId,          // Reference to users collection
  headquarter_id: ObjectId,   // Reference to headquarters collection
  state: String,              // 'active', 'inactive', 'suspended'
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ user_id: 1 }` - unique
- `{ headquarter_id: 1 }`
- `{ state: 1 }`

---

### 4. teachers
Stores teacher-specific information with embedded studies.

```javascript
{
  _id: ObjectId,              // Same as user_id for easy reference
  user_id: ObjectId,          // Reference to users collection
  studies: [                  // Array of study records
    {
      titulo: String,
      universidad: String,
      institucion: String,
      año: String
    }
  ],
  professional_license: String,
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ user_id: 1 }` - unique

---

### 5. classes
Stores class/course information.

```javascript
{
  _id: ObjectId,
  name: String,
  capacity: Number,
  schedule: String,
  class_type: String,
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ class_type: 1 }`
- `{ name: 1 }`

---

### 6. classes_headquarters
Junction collection for many-to-many relationship between classes and headquarters.

```javascript
{
  _id: ObjectId,
  class_id: ObjectId,         // Reference to classes collection
  headquarter_id: ObjectId,   // Reference to headquarters collection
  start_date: Date,
  end_date: Date,
  created_at: Date
}
```

**Indexes:**
- `{ class_id: 1, headquarter_id: 1, start_date: 1 }` - unique
- `{ class_id: 1 }`
- `{ headquarter_id: 1 }`

---

### 7. students_classes
Junction collection for student enrollments in classes.

```javascript
{
  _id: ObjectId,
  student_id: ObjectId,       // Reference to students collection
  class_id: ObjectId,         // Reference to classes collection
  state: String,              // 'enrolled', 'active', 'withdrawn', 'completed'
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ student_id: 1, class_id: 1 }` - unique
- `{ student_id: 1 }`
- `{ class_id: 1 }`
- `{ state: 1 }`

---

### 8. teachers_classes
Junction collection for teacher assignments to classes.

```javascript
{
  _id: ObjectId,
  teacher_id: ObjectId,       // Reference to teachers collection
  class_id: ObjectId,         // Reference to classes collection
  teacher_role: String,       // 'lead', 'assistant', 'substitute'
  start_date: Date,
  end_date: Date,
  created_at: Date
}
```

**Indexes:**
- `{ teacher_id: 1, class_id: 1 }`
- `{ class_id: 1 }`
- `{ teacher_role: 1 }`

---

### 9. registration_fees
Stores student registration/enrollment periods.

```javascript
{
  _id: ObjectId,
  student_id: ObjectId,       // Reference to students collection
  start_date: Date,
  end_date: Date,
  state: String,              // 'active', 'expired', 'cancelled'
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ student_id: 1 }`
- `{ state: 1 }`
- `{ start_date: 1, end_date: 1 }`

---

### 10. payments
Stores payment transactions (high-volume operational data).

```javascript
{
  _id: ObjectId,
  registration_fee_id: ObjectId,  // Reference to registration_fees collection
  amount: Decimal128,
  payment_date: Date,
  payment_method: String,
  receipt_number: String,
  concept: String,
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ registration_fee_id: 1 }`
- `{ payment_date: 1 }`
- `{ payment_method: 1 }`

---

### 11. classes_attendances
Stores attendance records (high-volume operational data).

```javascript
{
  _id: ObjectId,
  student_id: ObjectId,       // Reference to students collection
  class_id: ObjectId,         // Reference to classes collection
  headquarter_id: ObjectId,   // Reference to headquarters collection
  teacher_id: ObjectId,       // Reference to teachers collection
  date: Date,
  attended: Boolean,
  observations: String,
  created_at: Date,
  updated_at: Date
}
```

**Indexes:**
- `{ student_id: 1, class_id: 1, date: 1 }` - unique
- `{ student_id: 1 }`
- `{ class_id: 1 }`
- `{ date: 1 }`
- `{ attended: 1 }`

---

## Design Decisions

### 1. **Normalized Structure**
While MongoDB supports embedded documents, this schema maintains a normalized structure similar to the PostgreSQL schema to:
- Avoid data duplication
- Maintain referential integrity
- Support complex queries across collections
- Facilitate data updates

### 2. **ObjectId References**
Using ObjectId for references instead of UUIDs to leverage MongoDB's native ID generation and indexing capabilities.

### 3. **Embedded Arrays**
The `teachers.studies` field uses an embedded array since:
- Studies are tightly coupled to teachers
- Limited number of studies per teacher
- Frequently accessed together

### 4. **Separate Junction Collections**
Many-to-many relationships use separate junction collections to:
- Store additional relationship metadata (dates, states, roles)
- Maintain query flexibility
- Support efficient updates

### 5. **Indexes**
Strategic indexes are defined to optimize:
- Unique constraints
- Foreign key lookups
- Common query patterns
- Date range queries

---

## Migration Notes

### From PostgreSQL to MongoDB:
1. **UUIDs → ObjectIds**: PostgreSQL UUIDs are replaced with MongoDB ObjectIds
2. **JSONB → Embedded Documents**: PostgreSQL JSONB fields become embedded documents/arrays
3. **Triggers → Application Logic**: Auto-update timestamps handled in application code
4. **Foreign Keys → References**: Foreign key constraints become ObjectId references with application-level validation
5. **CHECK Constraints → Validation**: Database constraints become schema validation rules

---

## Performance Considerations

1. **High-Volume Collections**: `payments` and `classes_attendances` are designed for high write throughput
2. **Compound Indexes**: Used for unique constraints and common query patterns
3. **Date Indexes**: Support efficient time-range queries
4. **Sharding Candidates**: `payments` and `classes_attendances` can be sharded by date for horizontal scaling
