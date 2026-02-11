# System Architecture

## Overview

Strategic Intelligence AI uses a microservices architecture with event-driven communication between components.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                 │
│  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐  │
│  │ INGESTION    │─────────▶│  PROCESSING   │─────────▶│  VECTOR STORE │  │
│  │              │         │              │         │              │  │
│  │  Documents    │         │  NLP          │         │  Qdrant       │  │
│  │  Web          │         │  Entities      │         │  Milvius       │  │
│  │  Social       │         │  Patterns      │         │  (backup)     │  │
│  │               │         │              │         │              │  │
│  └───────┬───────┘         └───────┬─────┘         └───────┬─────┘  │
│         │                            │              │         │              │  │
│         ▼                            ▼              ▼         │              ▼  │
│  ┌─────────────────────────────────────────────────────────────┐   │  │
│  │            MESSAGE BUS / EVENT QUEUE                │   │  │
│  │  ┌─────────────────────────────────────────────────────┐   │  │
│  │  │           Apache Kafka / Redis Pub/Sub            │   │  │
│  │  └─────────────────────────────────────────────────────┘   │  │
│  └───────────────────────────────┬─────────────────────────┘   │  │
│                              │                             │         │  │
│  ──────────────────────────────┴──────────────────────────────►│         │  │
│                              │                             │         │  │
│                              ▼                             │         ▼  │
│  ┌─────────────────────────────────────────────────────┐           │  │
│  │            ORCHESTRATOR LAYER                 │           │  │
│  │  ┌────────────────────────────────────────────────┐           │  │
│  │  │  PLANNER          EXECUTOR        EVALUATOR   │           │  │
│  │  │  (LangChain)      │                │  │           │  │
│  │  │    ├──────────────►│                │  │           │  │
│  │  │    │                │                │  │           │  │
│  │  │  AGENT COORDINATOR  AGENT MEMORY      │           │  │
│  │  │    (AutoGen/CrewAI)   │                │  │           │  │
│  │  └────────────────────────────────────────┘           │  │
│  └───────────────────────┬─────────────────────────┘           │  │
│                              │                             │         │  │
│  ──────────────────────────┴──────────────────────────────►│         │  │
│                              │                             │         │  │
│                              ▼                             ▼         ▼  │
│  ┌─────────────────────────────────────────────────────┐           │  │
│  │              LLM LAYER                         │           │  │
│  │  ┌────────────────────────────────────────────────┐           │  │
│  │  │  EMBEDDINGS      RETRIEVER        GENERATOR    │           │  │
│  │  │  (sentence-      │  (Vector Search)│  (Gemini/    │           │  │
│  │  │   transformers)  │                  │  Llama)      │           │  │
│  │  │                │                  │              │           │  │
│  │  └────────────────┴────────────────┘           │           │  │
│  └─────────────────────────────────────────────┘           │  │
│                                                     │         │  │
└─────────────────────────────────────────────────────────────┘           │  │
                                                      │         │  │
                                                      │         ▼  │
┌─────────────────────────────────────────────────────────────────────────┐
│                     INTERFACES                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐  │
│  │  WEB UI     │───│  REST API     │───│  WebSocket    │  │
│  │  (Gradio/    │   │  (FastAPI)    │   │  (Real-time)  │  │
│  │   Streamlit) │   │              │   │              │  │
│  │              │   │              │   │              │  │
│  └─────────────┘   └─────────────┘   └─────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Ingestion Service

**Responsibilities:**
- Accept document uploads (API, drag-drop, watched folder)
- Extract text from PDF, DOCX, images (OCR)
- Detect language and encoding
- Split into semantic chunks
- Generate embeddings
- Store in vector database

**API Endpoints:**
```
POST   /api/v1/ingest/document
POST   /api/v1/ingest/batch
POST   /api/v1/ingest/url
GET    /api/v1/ingest/status/{job_id}
```

### Processing Service

**Responsibilities:**
- Named Entity Recognition (NER)
- Key phrase and pattern extraction
- Sentiment analysis
- Relationship extraction
- Temporal analysis

**Extractors:**
- Dates, times, monetary values
- People, organizations, locations
- Email addresses, phone numbers
- Technical terms, product names

### OSINT Service

**Responsibilities:**
- Web scraping automation
- Social media monitoring
- Domain intelligence
- Dark web scanning
- Geolocation correlation

**Sources:**
```
Public Web:
- Search engines (Google, Bing, DuckDuckGo)
- Social networks (LinkedIn, Twitter/X, Facebook)
- Company registries
- News archives
- Academic publications

Dark Web:
- Tor hidden services (.onion)
- I2P services
- Leak markets and forums
- Carding forums
- Credential dumps

Infrastructure:
- DNS records (A, AAA, MX, NS, TXT)
- SSL certificates
- IP geolocation
- ASN lookup
- Shodan/Censys search results
```

### Orchestrator

**Agent Types:**

1. **Planner Agent** - Decomposes complex queries into subtasks
2. **Research Agent** - Web search and information gathering
3. **Analyst Agent** - Data synthesis and correlation
4. **Writer Agent** - Report generation
5. **Reviewer Agent** - Quality assessment
6. **Orchestrator** - Coordinates all agents

**Tools:**
- LangChain - Agent framework
- AutoGen - Multi-agent orchestration
- CrewAI - Role-playing agent system

### LLM Gateway

**Models:**
- Gemini 2.5 Flash (fast, cost-effective)
- Gemini 2.5 Pro (complex reasoning)
- Llama 3 70B (local, privacy)
- Mistral 7B (edge deployment)

**Features:**
- Streaming responses
- Function calling
- Context window management
- Token optimization
- Fallback routing

---

## Data Flow

```
1. DOCUMENT INGESTION
   User uploads PDF
   ↓
   OCR/Text extraction
   ↓
   Language detection
   ↓
   Chunking (500-2000 chars)
   ↓
   Embedding generation (384-dim)
   ↓
   Vector storage

2. QUERY PROCESSING
   User query: "Analyze recent competitor activities"
   ↓
   Query embedding
   ↓
   Vector search (Top-10, cosine similarity)
   ↓
   Context retrieval
   ↓
   LLM generation with sources

3. OSINT PIPELINE
   Target company/entity
   ↓
   Web scraping (parallel)
   ↓
   Social media API queries
   ↓
   Domain intelligence lookup
   ↓
   Data normalization
   ↓
   Vector storage + metadata
   ↓
   Analysis and alerting

4. DECISION SUPPORT
   Intelligence request
   ↓
   Multi-agent analysis
   ↓
   Information synthesis
   ↓
   Recommendation generation
   ↓
   Confidence scoring
   ↓
   Brief/report output
```

---

## Deployment

**Development:**
```bash
docker-compose -f docker-compose.yml up --build
```

**Production:**
```bash
kubectl apply -f k8s/
helm upgrade intelligence-system ./helm/
```

---

## Monitoring

**Metrics:**
- Ingestion rate (docs/sec)
- Query latency (P50, P95, P99)
- Vector search time
- LLM tokens/sec
- Agent execution time
- OSINT success rate

**Dashboards:**
- Grafana for system metrics
- Custom Streamlit for operational view
- Sentry for error tracking
