AppSecGate README.md — Copy/Paste Version
Copy everything below this line into README.md. The Markdown syntax is preserved as plain text.
────────────────────────────────────────────────────────────────────────
<div align="center">
 
# 🛡️ AppSecGate
 
### Intelligent DevSecOps Security Assessment & Release Decision Platform
 
**From fragmented scanner output to contextual risk intelligence, security controls, evidence, and explainable release decisions.**
 
`SAST` · `SCA` · `DAST` · `Secrets` · `IaC` · `Container Security`
 
<br>
 
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=nextdotjs)
![React](https://img.shields.io/badge/React-19-20232A?style=flat-square&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript)
![Semgrep](https://img.shields.io/badge/SAST-Semgrep-6C5CE7?style=flat-square)
![Trivy](https://img.shields.io/badge/SCA%20%7C%20Container-Trivy-1904DA?style=flat-square)
![OWASP ZAP](https://img.shields.io/badge/DAST-OWASP%20ZAP-00549E?style=flat-square)
![Checkov](https://img.shields.io/badge/IaC-Checkov-6B5BFF?style=flat-square)
![Gitleaks](https://img.shields.io/badge/Secrets-Gitleaks-E74C3C?style=flat-square)
 
</div>
 
---
 
## Overview
 
**AppSecGate** is a full-stack application security platform that orchestrates multiple security testing disciplines through a unified assessment workflow.
 
Rather than treating scanner output as isolated alerts, AppSecGate:
 
- normalizes findings into a unified security model,
- correlates scanner and asset context,
- calculates contextual risk,
- maps findings to security controls,
- preserves scanner evidence and provenance,
- evaluates assessment integrity,
- and produces an explainable security gate decision.
 
The platform is built around one practical DevSecOps question:
 
> **Can this application move forward based on its current security posture?**
 
---
 
## Security Pipeline
 
```text
Security Inputs
      │
      ▼
Security Scanners
      │
      ├── Semgrep ────── SAST
      ├── Gitleaks ───── Secrets
      ├── Trivy FS ───── SCA
      ├── Checkov ────── IaC
      ├── Trivy Image ── Container
      └── OWASP ZAP ──── DAST
      │
      ▼
Normalize Findings
      │
      ▼
Correlate & Enrich
      │
      ▼
Contextual Risk Engine
      │
      ▼
Control Mapping
      │
      ▼
Evidence Generation
      │
      ▼
Policy Engine
      │
      ▼
Security Gate
      │
      ▼
PASS / WARN / BLOCK
```
 
---
 
## Core Capabilities
 
### Multi-Scanner Assessment
 
| Security Domain | Engine |
|---|---|
| SAST | Semgrep |
| Secrets Detection | Gitleaks |
| Software Composition Analysis | Trivy FS |
| Infrastructure-as-Code | Checkov |
| Container Security | Trivy Image |
| Dynamic Application Security Testing | OWASP ZAP |
 
Each scanner is integrated through a dedicated adapter and participates in the same downstream intelligence pipeline.
 
### Asset & Security Input Management
 
Assessment targets can include:
 
- Source-code ZIP archives
- Public HTTPS Git repositories
- Infrastructure-as-Code
- Container images and archives
- Web application DAST targets
- OpenAPI specifications
- Environment and business criticality context
 
### Scanner Applicability
 
AppSecGate determines which scanners are relevant to each asset and distinguishes between:
 
`Executed` · `Failed` · `Not Configured` · `Not Applicable`
 
This prevents incomplete scanner coverage from appearing as a clean assessment.
 
### Unified Finding Intelligence
 
Scanner-specific output is normalized into a common finding model containing:
 
`Severity` · `Risk` · `Scanner Provenance` · `Location` · `Component` · `Package` · `CVE` · `Evidence` · `Asset Context`
 
### Contextual Risk Engine
 
Risk prioritization considers more than raw scanner severity.
 
AppSecGate evaluates factors including:
 
- technical severity,
- asset criticality,
- environment,
- exposure,
- exploitability context,
- and production relevance.
 
### Security Control Intelligence
 
Technical findings are mapped to reusable security control definitions.
 
Controls aggregate:
 
- linked findings,
- open exposure,
- affected assets,
- control severity,
- ownership,
- required evidence,
- and control guidance.
 
### Evidence Vault
 
AppSecGate maintains traceability across the security decision chain:
 
```text
Assessment
   ↓
Finding
   ↓
Scanner Evidence
   ↓
Security Control
   ↓
Risk / Policy Decision
```
 
### Finding Lifecycle
 
Finding state follows scanner truth:
 
```text
Detected → OPEN
 
Absent from a successful responsible scanner run → CLOSED
 
Detected again → REOPENED
```
 
A failed or incomplete scanner run does not silently close an existing finding.
 
### Assessment Integrity
 
Security risk and scanner completeness are evaluated separately.
 
A release decision is therefore based not only on discovered vulnerabilities, but also on whether the required security assessment actually completed successfully.
 
---
 
## Security Gate
 
The policy engine evaluates normalized findings, contextual risk, controls, evidence, and scanner coverage.
 
Final assessment decisions are expressed as:
 
```text
PASS
WARN
BLOCK
```
 
The result is designed to be **explainable and evidence-backed**, rather than a simple severity threshold.
 
---
 
## Platform Workspaces
 
| Workspace | Purpose |
|---|---|
| **Overview** | Executive risk posture and final release decision |
| **Assets & Inputs** | Assessment targets and security artifact acquisition |
| **Assessment Runs** | Scanner execution and persisted assessment history |
| **Finding Intelligence** | Contextual finding analysis and prioritization |
| **Security Controls** | Control-centric security intelligence |
| **Evidence Vault** | Scanner evidence and security traceability |
| **Assessment Report** | Technical and management reporting |
 
Reports can be exported as **PDF** and **Excel**.
 
---
 
## Architecture
 
```text
┌───────────────────────────────────────────────────────────┐
│                     AppSecGate UI                         │
│  Overview · Assets · Findings · Controls · Evidence       │
├───────────────────────────────────────────────────────────┤
│                       API Layer                           │
│  Assets · Assessments · Findings · Controls · Inputs      │
├───────────────────────────────────────────────────────────┤
│                   Assessment Engine                       │
├───────────────────────────────────────────────────────────┤
│          Applicability & Scan Profile Validation          │
├───────────────────────────────────────────────────────────┤
│                    Scanner Adapters                       │
│ Semgrep · Gitleaks · Trivy · Checkov · ZAP                │
├───────────────────────────────────────────────────────────┤
│                Intelligence Pipeline                      │
│ Normalize → Risk → Controls → Evidence → Policy           │
├───────────────────────────────────────────────────────────┤
│                 Persistent Server Store                   │
└───────────────────────────────────────────────────────────┘
```
 
---
 
## Technology Stack
 
| Layer | Technology |
|---|---|
| Framework | Next.js 16 |
| Frontend | React 19 |
| Language | TypeScript |
| SAST | Semgrep |
| Secrets | Gitleaks |
| SCA | Trivy |
| IaC Security | Checkov |
| Container Security | Trivy |
| DAST | OWASP ZAP |
| PDF Reports | jsPDF |
| Excel Reports | ExcelJS |
| Archive Processing | yauzl |
 
---
 
## API Surface
 
```text
/api/assets
/api/assessments
/api/assessments/[id]
/api/findings
/api/controls
 
/api/imports/repository
 
/api/uploads/source
/api/uploads/iac
/api/uploads/container
/api/uploads/openapi
 
/api/inputs/container/validate
/api/inputs/dast/validate
```
 
---
 
## Project Structure
 
```text
src/
├── app/
│   ├── api/
│   ├── globals.css
│   └── page.tsx
│
├── components/
│   ├── AssessmentRuns.tsx
│   ├── AssetsInputs.tsx
│   ├── EvidenceVault.tsx
│   ├── FindingIntelligence.tsx
│   ├── Reports.tsx
│   └── SecurityControls.tsx
│
└── lib/server/
    ├── assessment-engine.ts
    ├── scan-profile-validator.ts
    ├── store.ts
    │
    ├── pipeline/
    │   ├── normalizer.ts
    │   ├── risk-engine.ts
    │   ├── control-mapper.ts
    │   ├── evidence-builder.ts
    │   └── policy-engine.ts
    │
    └── scanners/
        ├── semgrep-adapter.ts
        ├── gitleaks-adapter.ts
        ├── trivy-fs-adapter.ts
        ├── checkov-adapter.ts
        ├── trivy-image-adapter.ts
        └── zap-adapter.ts
```
 
---
 
## Run Locally
 
```bash
git clone https://github.com/AmrAbd-Elaziz/appsecgate-platform.git
cd appsecgate-platform
 
npm install
npm run dev
```
 
Then open:
 
```text
http://localhost:3000
```
 
For production validation:
 
```bash
npx tsc --noEmit
npm run build
npm start
```
 
The complete assessment pipeline additionally requires the configured security scanners to be available in the execution environment.
 
---
 
## Environment Configuration
 
Optional scanner/target configuration used by the platform:
 
```env
APPSECGATE_SCAN_TARGET=
APPSECGATE_DAST_TARGET=
APPSECGATE_SCANNER_NETWORK=
```
 
---
 
## Engineering Principles
 
> **Scanner output is evidence — not the final security decision.**
 
> **Risk should include application and environment context.**
 
> **A security gate must account for assessment completeness.**
 
> **Security decisions should remain traceable to their evidence.**
 
> **Release decisions should be explainable.**
 
---
 
## Project Status
 
### AppSecGate V2 — Complete
 
```text
Asset
  → Security Inputs
  → Scanner Execution
  → Normalization
  → Contextual Risk
  → Finding Intelligence
  → Security Controls
  → Evidence
  → Policy Gate
  → Release Decision
  → Assessment Report
```
 
---
 
## Author
 
**Amr Abdelaziz**
 
Cybersecurity Engineer  
Security Engineering · Application Security · DevSecOps · Vulnerability Management
 
[GitHub Profile](https://github.com/AmrAbd-Elaziz)
 
---
 
<div align="center">
 
### AppSecGate
 
**From security findings to explainable security decisions.**
 
</div>
