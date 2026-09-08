# Authenticated DAST Triage

## Scan Information

- Tool: OWASP ZAP API Scan
- Scan type: Authenticated API DAST
- Target specification: `openapi-remediated.yaml`
- Execution environment: GitHub Actions
- Authentication: Temporary JWT generated during CI
- Result: No actionable High, Medium, or Low vulnerabilities

## Summary

| Severity | Count |
|---|---:|
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Informational | 3 |

## Manual Validation

### 1. Client Error Responses

**Classification:** Expected behavior / Informational

ZAP generated invalid routes, malformed input, cloud metadata paths, and invalid login requests.

Observed responses included:

- `404` for undefined routes and metadata endpoints.
- `401` for invalid login credentials.
- `400` for rejected malformed search input.

These responses do not demonstrate a security vulnerability.

### 2. Authentication Request Identified

**Classification:** Expected behavior / Informational

ZAP correctly identified `/api/login` as an authentication endpoint.

CI authentication succeeded with HTTP `200`, and the resulting JWT was masked before being provided to ZAP.

Authenticated access was validated:

- `GET /api/users/1` returned `200`.
- `GET /api/search?q=alice` returned `200`.

### 3. Non-Storable Content

**Classification:** Positive security control

Sensitive API responses included:

`Cache-Control: no-store`

This prevents authentication and user data responses from being stored in shared or browser caches.

## Injection Validation

ZAP submitted SQL injection, command injection, SSRF, template injection, and malformed-input payloads to `/api/search`.

The payloads were treated as literal search values. No command execution, SQL manipulation, data extraction, or server error was observed.

This behavior is consistent with the parameterized SQL query implemented in the remediated application.

## Risk Decision

The three alerts are informational and do not represent exploitable vulnerabilities.

The DAST security gate passed while retaining complete JSON and HTML reports as audit evidence.

## Evidence

- GitHub Actions job status and retained pipeline artifacts.
- `zap-api-remediated.json`
- `zap-api-remediated.html`
- GitHub Actions application access logs