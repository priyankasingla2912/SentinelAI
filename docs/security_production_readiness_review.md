# SentinelAI — Security & Production Readiness Review

**Review date:** November 7, 2026  
**Review scope:** Backend authentication, authorization, frontend token handling, CORS, input validation, database configuration, and Git secret protection.

## 1. Executive Summary

The review identified several positive security controls in SentinelAI, including Argon2id password hashing, JWT validation, database-backed user authorization, role-based permissions, HTTP-only authentication cookies, and environment-file exclusions in Git.

The review also identified areas requiring further hardening before production use in a financial institution, particularly login rate limiting, failed-login monitoring, CSRF protection, security headers, CORS restrictions, and token revocation.

This review is a code-level inspection. It is not a penetration test, compliance audit, or certification of production security.

## 2. Positive Security Controls

### 2.1 Password Security
- Password hashing uses Argon2id.
- Password verification uses the Argon2 password hashing library.
- Passwords are stored in a password_hash database column.
- Registration and password-reset models require passwords between 12 and 128 characters.

### 2.2 Authentication and JWT
- JWT signing uses a secret loaded from an environment variable.
- The application fails during initialization if the JWT secret is missing.
- The configured algorithm is restricted to HS256.
- Token expiration is configured, with a default of 30 minutes.
- Token decoding requires subject, issued-at, and expiration claims.
- User identity and current role are retrieved from the database during authentication.
- Inactive accounts are rejected.
- Invalid or expired tokens receive an authentication error.

### 2.3 Authorization
- Role-based permissions are centralized.
- Roles include ADMIN, SENIOR_FRAUD_ANALYST, FRAUD_ANALYST, and VIEWER.
- The investigation endpoint requires the appropriate permission.
- Fraud-case update permissions are restricted by role and assignment.

### 2.4 Frontend Authentication
- The frontend stores the JWT in an HTTP-only cookie.
- The cookie uses Secure in production.
- SameSite is configured as Lax.
- The cookie path is /.
- Cookie lifetime is 30 minutes, matching the default JWT expiration.
- Logout clears the cookie using maxAge 0.
- The frontend forwards the token to the backend through the Authorization header.
- No localStorage or sessionStorage token storage was found in the application search.

### 2.5 Database Configuration
- SQLAlchemy is used for database access.
- PostgreSQL is supported through DATABASE_URL.
- Connection health checking uses pool_pre_ping.
- Connection recycling is configured.
- SQLAlchemy SQL echo logging is disabled.
- Automated tests use isolated SQLite databases.
- User email has a unique constraint.
- Fraud cases reference predictions through a foreign key.
- Audit logs record actions, resource information, user IDs, IP addresses, and timestamps.

### 2.6 Git Secret Protection
- Root and frontend Git ignore rules exclude environment files.
- The checked files .env, backend/.env, and frontend/.env.local are ignored.
- git ls-files returned no entries for those exact paths, indicating they are not currently tracked under those paths.

## 3. Input Validation Review

Request models are defined in backend/app/main.py.

Observed validation includes:
- Transaction Time and Amount must be non-negative.
- Fraud-case prediction IDs must be positive.
- Analyst names have a maximum length of 100 characters.
- Investigation notes have a maximum length of 2,000 characters.
- Login email length is restricted to 5–255 characters.
- Registration email includes a format pattern.
- Registration passwords have a length of 12–128 characters.
- OTP values must contain exactly six digits.
- User roles use the Role enum.

Potential improvements:
- Add finite-number validation for transaction numeric fields.
- Apply consistent email validation across login, OTP, and password-reset models.
- Consider enum validation for fraud-case status in the request model.
- Review behavior for empty UserUpdate requests.
- Consider additional password-strength controls.

## 4. Findings Requiring Improvement

### 4.1 Login Rate Limiting
A search of backend/app for common rate-limiting and login-attempt implementation terms returned no matches.

Recommendation:
Implement rate limiting for login and other sensitive authentication endpoints. Consider account- and IP-based controls, progressive delays, and monitoring.

This search does not rule out rate limiting at an external hosting or proxy layer.

### 4.2 Failed Login Monitoring
Successful login auditing was observed. Failed-login tracking was not identified in the inspected login endpoint or application search.

Recommendation:
Record failed authentication events without logging passwords or other secrets. Monitor repeated failures and suspicious patterns.

### 4.3 CSRF Protection
The frontend uses HTTP-only cookies with SameSite=Lax. No explicit CSRF token or Origin/Referer validation was identified in the searched application files.

Recommendation:
Review all state-changing cookie-authenticated routes and implement an appropriate CSRF defense where required. SameSite=Lax is helpful but should not be treated as a complete CSRF solution.

### 4.4 Security Headers
No explicit Content-Security-Policy, X-Frame-Options, X-Content-Type-Options, or Strict-Transport-Security configuration was identified in the inspected Next.js configuration or searched application files.

Recommendation:
Configure appropriate security headers at the application or hosting/reverse-proxy layer. Verify the actual deployed response headers.

### 4.5 CORS Configuration
The backend currently allows:
- http://localhost:3000
- http://127.0.0.1:3000
- https://sentinel-ai-ten-zeta.vercel.app

Credentials are enabled, and allowed methods and headers are both set to wildcard values.

Recommendation:
Restrict methods and headers to those required by the application. Confirm the production origin and separate development configuration from production.

### 4.6 JWT Revocation
The inspected logout route clears the browser cookie but does not revoke the JWT at the backend.

Recommendation:
Assess whether token revocation, session tracking, or another invalidation strategy is needed for logout, account compromise, and administrative account changes.

### 4.7 Database Connection Security
The application supports PostgreSQL through DATABASE_URL and falls back to SQLite if the variable is absent.

Not verified during this review:
- Whether the deployed Neon connection enforces SSL/TLS.
- Whether the production database account follows least privilege.
- Whether database backups and recovery have been tested.
- Whether production deployment prevents accidental SQLite fallback.

Recommendation:
Verify these controls in deployment configuration and the database provider.

## 5. Review Limitations

The following were not established by this code inspection:
- Actual deployed HTTP response security headers.
- External reverse-proxy or hosting-layer rate limiting.
- Neon SSL/TLS enforcement.
- Backup and disaster-recovery readiness.
- Penetration-test results.
- Formal regulatory compliance.
- Complete production infrastructure security.

The absence of a matching code-search result is not proof that a control is absent from every infrastructure layer.

## 6. Recommended Priorities

| Priority | Improvement |
|---|---|
| High | Add login rate limiting and failed-login monitoring |
| High | Review and implement appropriate CSRF protection |
| High | Verify production HTTPS, database SSL/TLS, and deployment configuration |
| Medium | Configure and verify security headers |
| Medium | Restrict CORS methods and headers |
| Medium | Assess JWT revocation/session invalidation |
| Medium | Strengthen transaction input validation |
| Medium | Verify backups and recovery procedures |

## 7. Conclusion

SentinelAI has a useful foundation of authentication, authorization, password hashing, and database security controls.

However, additional hardening and deployment-level verification are required before describing the platform as production-ready for banking or financial-institution use.

This document records the findings from the November 7, 2026 code-level security review. It should be updated as remediation work is completed.
