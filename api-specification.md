# Justification Copilot API Specification

## 1. Patient Management

### GET /patients
Fetch a list of patients with optional filtering and pagination.

**Query Params**: `page`, `limit`, `search` (by name/ID), `status` (e.g., "pending").

**Response (200)**:
```json
{
  "patients": [
    {
      "id": "string",
      "name": "string",
      "progress": "string",  // e.g., "75%"
      "quantity": 10,  // e.g., number of queries
      "date": "2024-01-15",
      "queries": 5
    }
  ],
  "total": 100,
  "page": 1
}
```

### GET /patients/:id
Fetch detailed patient information.

**Response (200)**: Full patient object (matching frontend `mockPatientDetails` structure, including patient info, doctor, insurance, clinical summary, queries).

### POST /patients
Create a new patient (admin only).

**Request Body**: Patient object.

**Response (201)**: Created patient object.

### PUT /patients/:id
Update patient details.

**Request Body**: Partial patient object.

**Response (200)**: Updated patient object.

### DELETE /patients/:id
Delete a patient.

**Response (204)**: No content.

## 2. Insurance & Claims Management

### GET /patients/:id/insurance
Fetch insurance details for a patient.

**Response (200)**:
```json
{
  "provider": "string",
  "policyNumber": "string",
  "coverageType": "string",  // e.g., "Cashless"
  "claimRequested": 150000,
  "claimApproved": 150000,
  "status": "string"  // e.g., "Approved", "Pending"
}
```

### PUT /patients/:id/insurance
Update insurance/claim status.

**Request Body**:
```json
{
  "status": "Approved",
  "claimApproved": 150000
}
```

**Response (200)**: Updated insurance object.

### POST /patients/:id/claims
Submit a new claim.

**Request Body**:
```json
{
  "amount": 150000,
  "documents": ["url1", "url2"]
}
```

**Response (201)**: Created claim object.

## 3. Query Management

### GET /patients/:id/queries
Fetch queries for a patient.

**Response (200)**:
```json
[
  {
    "id": "string",
    "question": "string",
    "raisedOn": "2024-01-15",
    "answer": "string"
  }
]
```

### POST /patients/:id/queries
Create a new query (e.g., raised by insurer).

**Request Body**:
```json
{
  "question": "string"
}
```

**Response (201)**: Created query object.

### PUT /patients/:id/queries/:queryId
Submit/update answer to a query.

**Request Body**:
```json
{
  "answer": "string"
}
```

**Response (200)**: Updated query object.

### DELETE /patients/:id/queries/:queryId
Delete a query.

**Response (204)**: No content.

## 4. AI Response Generation

### POST /ai/generate-response
Generate an AI-assisted response for a query using patient context.

**Request Body**:
```json
{
  "query": "string",
  "patientId": "string",
  "context": "string"  // e.g., patient/insurance data
}
```

**Response (200)**:
```json
{
  "generatedResponse": "string"
}
```

**Notes**: Integrate with an AI service (e.g., OpenAI API). Ensure HIPAA compliance for healthcare data.

## 6. Dashboard & Analytics

### GET /dashboard/widgets
Fetch data for dashboard widgets (e.g., earnings, sales).

**Response (200)**:
```json
{
  "earnings": 340.5,
  "spend": 642.39,
  "sales": 574.34,
  "balance": 1000,
  "tasks": 145,
  "projects": 12
}
```

### GET /dashboard/charts
Fetch chart data (e.g., for line/bar charts).

**Response (200)**:
```json
{
  "barData": [...],  // Array of chart data points
  "lineData": [...],
  "options": {...}  // Chart options
}
```

### GET /dashboard/patients/summary
Fetch aggregated patient stats.

**Response (200)**:
```json
{
  "totalPatients": 100,
  "pendingClaims": 20,
  "approvedClaims": 80
}
```