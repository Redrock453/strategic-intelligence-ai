# API Reference

## Authentication

All API endpoints require authentication except `/health` and `/docs`.

```bash
POST /api/v1/auth/login
{
  "username": "user@domain.com",
  "password": "password",
  "mfa_code": "123456"  # Optional
}

Response:
{
  "access_token": "jwt_token_here",
  "refresh_token": "refresh_token_here",
  "expires_in": 3600
}
```

## Document Ingestion

### Upload Document

```bash
POST /api/v1/ingest/document
Content-Type: multipart/form-data

{
  "file": "<binary>",
  "metadata": {
    "title": "Competitor Analysis Q4 2024",
    "source": "internal",
    "classification": "confidential",
    "tags": ["competitor", "quarterly", "2024"]
  }
}

Response:
{
  "job_id": "ingest_job_uuid",
  "status": "processing",
  "estimated_time": 45  # seconds
}
```

### Ingest from URL

```bash
POST /api/v1/ingest/url
Content-Type: application/json

{
  "url": "https://example.com/document.pdf",
  "depth": 1,  # for recursive crawling
  "follow_redirects": true
  "metadata": {
    "schedule": "daily",
    "source": "web"
  }
}
```

### Check Job Status

```bash
GET /api/v1/ingest/status/{job_id}

Response:
{
  "job_id": "ingest_job_uuid",
  "status": "completed",
  "progress": 100,
  "chunks_created": 47,
  "embeddings_generated": 47,
  "error": null
}
```

## Vector Search

### Semantic Search

```bash
POST /api/v1/search/semantic
Content-Type: application/json
Authorization: Bearer {token}

{
  "query": "competitor expansion strategy",
  "filters": {
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    },
    "sources": ["internal", "osint"],
    "min_confidence": 0.7
  },
  "limit": 10,
  "retrieval_config": {
    "search_type": "hybrid",  # vector + keyword
    "top_k": 10,
    "score_threshold": 0.6
  }
}

Response:
{
  "results": [
    {
      "chunk_id": "vec_123456",
      "content": "...",
      "metadata": {...},
      "score": 0.92,
      "source": "internal/competitor_analysis.pdf",
      "timestamp": "2024-02-11T10:30:00Z"
    }
  ],
  "total_results": 10,
  "search_time_ms": 245
}
```

### Hybrid Search

```bash
POST /api/v1/search/hybrid
Content-Type: application/json

{
  "query": "market entry barriers",
  "vector_weight": 0.7,
  "keyword_weight": 0.3,
  "rerank": true,
  "limit": 20
}
```

## OSINT Operations

### Start OSINT Collection

```bash
POST /api/v1/osint/collect
Authorization: Bearer {token}

{
  "target": {
    "type": "company",  # or person, domain, ip
    "identifier": "Acme Corp",
    "attributes": ["financials", "technology", "executives"]
  },
  "sources": {
    "web": true,
    "social_media": true,
    "domains": true,
    "dark_web": false,
    "leak_sites": false
  },
  "depth": 2,  # levels of recursive search
  "max_results": 100,
  "duration": 3600  # max runtime in seconds
}

Response:
{
  "job_id": "osint_job_uuid",
  "status": "running",
  "estimated_completion": "2024-02-11T12:00:00Z"
}
```

### Get OSINT Results

```bash
GET /api/v1/osint/results/{job_id}

Response:
{
  "job_id": "osint_job_uuid",
  "status": "completed",
  "findings": {
    "domains": 15,
    "subdomains": 47,
    "emails": 23,
    "social_profiles": 8,
    "leaked_credentials": 0,
    "dark_web_mentions": 2
  },
  "risk_score": 0.35,
  "summary": "Low-risk digital footprint detected"
}
```

## Orchestration

### Execute Agent Task

```bash
POST /api/v1/orchestrator/execute
Authorization: Bearer {token}

{
  "task": "Analyze competitor Q4 earnings and provide strategic recommendations",
  "agents": ["planner", "researcher", "analyst", "writer"],
  "context": {
    "previous_findings": ["job_id_1", "job_id_2"],
    "constraints": ["budget_limit", "timeline_q2_2024"],
    "output_format": "executive_brief"
  },
  "priority": "high",
  "timeout": 600
}

Response:
{
  "execution_id": "exec_uuid",
  "status": "running",
  "agent_messages": [
    {
      "agent": "planner",
      "message": "Decomposed task into 5 subtasks"
    }
  ]
}
```

### Stream Agent Messages

```bash
GET /api/v1/orchestrator/stream/{execution_id}

Response: Server-Sent Events (text/event-stream)
```

## LLM Operations

### Generate Text

```bash
POST /api/v1/llm/generate
Authorization: Bearer {token}

{
  "prompt": "Summarize the following OSINT findings...",
  "context": [...],  # retrieved chunks
  "model": "gemini-2.5-flash",
  "parameters": {
    "temperature": 0.3,
    "max_tokens": 4096,
    "top_p": 0.9,
    "stream": true
  }
}

Response (stream):
data: {"token": {"content": "Based on the OSINT..."}}
done: true
```

### Get Embeddings

```bash
POST /api/v1/llm/embed
Content-Type: application/json

{
  "texts": [
    "The company is expanding into European markets.",
    "New product launch scheduled for Q2 2025."
  ],
  "model": "sentence-transformers/all-MiniLM-L6-v2"
}

Response:
{
  "embeddings": [
    [0.123, -0.456, ..., 0.789]  # 384-dimensional
  "model": "all-MiniLM-L6-v2",
  "dimension": 384
}
```

## WebSocket Events

### Connect to Real-time Updates

```javascript
const ws = new WebSocket('wss://api.example.com/v1/ws');

ws.on('open', () => {
  console.log('Connected to intelligence stream');
  ws.send(JSON.stringify({
    event: 'authenticate',
    token: getAuthToken()
  }));
});

ws.on('message', (data) => {
  const event = JSON.parse(data);

  switch(event.type) {
    case 'job.progress':
      updateProgressBar(event.data.progress);
      break;
    case 'osint.finding':
      displayNewFinding(event.data.finding);
      break;
    case 'agent.message':
      displayAgentOutput(event.data.agent, event.data.message);
      break;
    case 'llm.token':
      updateTokenUsage(event.data.usage);
      break;
  }
});
```

## Error Codes

| Code | Meaning | Action |
|-------|----------|--------|
| 200 | Success | - |
| 201 | Created | - |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Refresh token |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Check endpoint |
| 429 | Rate Limited | Back off and retry |
| 500 | Server Error | Retry with exponential backoff |

## Rate Limits

| Tier | Requests/Minute | Requests/Hour | Features |
|-------|----------------|---------------|----------|
| Free | 10 | 100 | Basic search, public docs |
| Pro | 100 | 2000 | Full OSINT, agents, API |
| Enterprise | 1000 | 50000 | Priority support, custom models |

---

Last Updated: 2025-02-11
