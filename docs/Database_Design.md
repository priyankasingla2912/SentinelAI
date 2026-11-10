# SentinelAI Database Design

## 1. Overview

SentinelAI uses SQLAlchemy Core table definitions to manage transaction predictions, fraud cases, user accounts, audit events, and OTP verification records.

The database configuration supports:
- PostgreSQL for production-oriented deployments, subject to deployment security and readiness verification.
- SQLite as a local development fallback and for isolated automated tests.

The active database engine is selected through `app.config` and accessed through `get_active_engine()` in `app/database.py`.

## 2. Database Tables

The application defines five tables.

### 2.1 predictions

Stores transaction prediction results.

| Column | Type | Constraints / Description |
|---|---|---|
| id | Integer | Primary key, auto-increment |
| amount | Float | Required |
| fraud_probability | Float | Required |
| threshold | Float | Required |
| prediction | String | Required; classification result |
| risk_level | String | Required |
| recommended_action | Text | Required |
| shap_factors | Text | Nullable; SHAP factors serialized as JSON |
| created_at | DateTime | Defaults to database current time |
| source_database | String(20) | Nullable |
| source_record_id | Integer | Nullable |

Prediction records are created by `save_prediction()`. The function returns the generated prediction ID.

### 2.2 fraud_cases

Stores fraud cases associated with transaction predictions.

| Column | Type | Constraints / Description |
|---|---|---|
| case_id | Integer | Primary key, auto-increment |
| prediction_id | Integer | Required foreign key to predictions.id |
| status | String | Required; default NEW |
| analyst | String | Nullable |
| investigation_notes | Text | Nullable |
| created_at | DateTime | Defaults to database current time |
| updated_at | DateTime | Defaults to database current time |
| source_database | String(20) | Nullable |
| source_record_id | Integer | Nullable |

A fraud case references an existing prediction. The application provides functions to create, retrieve, list, and update cases.

Supported case statuses at the API level are NEW, IN_PROGRESS, and RESOLVED.

Case updates can modify status, analyst, and investigation notes. The update operation also refreshes `updated_at`.

### 2.3 users

Stores application user accounts and authorization information.

| Column | Type | Constraints / Description |
|---|---|---|
| id | Integer | Primary key, auto-increment |
| email | String(255) | Required, unique |
| full_name | String(150) | Required |
| password_hash | String(255) | Required; stores a password hash |
| role | String(30) | Required |
| is_active | Boolean | Required; default True |
| created_at | DateTime | Defaults to database current time |
| updated_at | DateTime | Defaults to database current time |

User records support authentication, account status checks, and role-based authorization.

### 2.4 audit_logs

Stores application audit events.

| Column | Type | Constraints / Description |
|---|---|---|
| id | Integer | Primary key, auto-increment |
| user_id | Integer | Nullable foreign key to users.id |
| action | String(100) | Required |
| resource_type | String(100) | Nullable |
| resource_id | String(100) | Nullable |
| ip_address | String(45) | Nullable |
| created_at | DateTime | Defaults to database current time |

The nullable user reference allows an audit event to exist without an associated user ID.

### 2.5 otp_verifications

Stores one-time password verification records for registration and password-reset workflows.

| Column | Type | Constraints / Description |
|---|---|---|
| id | Integer | Primary key, auto-increment |
| email | String(255) | Required |
| full_name | String(150) | Nullable |
| password_hash | String(255) | Nullable |
| purpose | String(30) | Required; identifies the verification purpose |
| otp_hash | String(255) | Required; stores the OTP hash |
| expires_at | DateTime | Required, timezone-aware |
| attempts | Integer | Required; default 0 |
| is_used | Boolean | Required; default False |
| created_at | DateTime | Defaults to database current time |

OTP records support registration and password-reset verification. The table does not declare a foreign key to the users table.

## 3. Entity Relationships

The declared foreign-key relationships are:

- One prediction can be referenced by multiple fraud cases.
- One user can be associated with multiple audit-log records.
- An audit-log record may have a null user reference.
- OTP verification records are associated with email addresses but do not have a declared foreign key to users.

```text
predictions
    |
    | 1-to-many
    |
    v
fraud_cases


users
    |
    | 1-to-many
    |
    v
audit_logs


otp_verifications
    |
    | Email-based verification
    |
    v
Registration / Password Reset
