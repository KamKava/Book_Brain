Book Brain — System Architecture

Project status: Early development
Version: 0.1
Last updated: August 2026

1. Purpose

This document describes how Book Brain is structured technically and how the architecture is expected to evolve.

It deliberately does not repeat:

Functional requirements → requirements.md
Database structure → database-design.md
Development history → development-log.md
Development sequence → roadmap.md

The architecture should describe system boundaries, responsibilities and dependencies rather than individual features.

2. Architectural Principles
2.1 Incremental development

Book Brain should remain as simple as possible at each development stage.

Future technologies should only be introduced when they solve an actual requirement.

2.2 Separation of responsibilities

Each layer should have a clear responsibility:

UI
 ↓
API
 ↓
Application Services
 ↓
Repositories
 ↓
Database

External services should be accessed through dedicated integration components.

2.3 Database independence

The database is the application's persistent data layer.

Application logic should not depend unnecessarily on SQLite-specific behaviour so that migration to PostgreSQL remains practical if required later.

2.4 AI independence

AI functionality must remain optional.

Core application functionality, database operations, analytics and recommendation logic should not require an LLM.

2.5 Controlled AI access

The LLM should interact with Book Brain through controlled application functions rather than unrestricted database or SQL access.

3. Current Architecture

The current MVP is intentionally small:

User
 │
 ▼
Python Application
 │
 ├── Application Logic
 │
 └── Database Access
        │
        ▼
      SQLite

Automated tests operate alongside the application.

        ┌──────────────┐
        │    Tests     │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   Python     │
        │ Application  │
        └──────┬───────┘
               │
               ▼
           SQLite DB

The MVP does not require:

FastAPI
React
External APIs
LLMs
Embeddings
Vector databases
Cloud infrastructure
Mobile applications
Wearable integration
4. Application Structure

As the application grows, responsibilities should be separated approximately as follows:

src/
├── database/
├── models/
├── repositories/
├── services/
├── integrations/
├── analytics/
└── main.py
Database layer

Responsible for:

Database connections.
Schema creation.
SQL execution.
Transactions.
Models

Represent application entities and structured data.

Repositories

Provide controlled access to persistent data.

Examples:

BookRepository
LibraryRepository
ReadingRepository

Repositories should contain data-access logic rather than broader business rules.

Services

Contain application and business logic.

Examples:

BookService
LibraryService
ReadingService
RecommendationService
AnalyticsService

Services should coordinate repositories and other application components.

Integrations

Isolate external dependencies from the core application.

Examples:

GoogleBooksClient
OpenLibraryClient
LLMProvider

External integrations should not directly modify the database without passing through application logic and validation.

5. Future Architecture

When web and mobile interfaces are introduced, the architecture is expected to become:

                    User
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
        Web                   Mobile
          │                     │
          └──────────┬──────────┘
                     ▼
                  FastAPI
                     │
                     ▼
              Application Services
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Database   Analytics   Integrations
          │
          ▼
      PostgreSQL

The frontend should not contain independent business logic.

Both web and mobile interfaces should use the same backend services.

6. External Services

External services should be isolated behind integration interfaces.

Book Brain
    │
    ├── Book Metadata APIs
    ├── AI / LLM Provider
    ├── External Search
    └── Future Device Integrations

This prevents external providers from becoming tightly coupled to the rest of the application.

Provider-specific implementation should remain replaceable where practical.

7. Recommendation Architecture

The recommendation engine is an application service rather than an AI component.

Request
   │
   ▼
Structured constraints
   │
   ▼
Candidate generation
   │
   ▼
Filtering
   │
   ▼
Scoring
   │
   ▼
Ranking
   │
   ▼
Results

Candidates may originate from internal data or external sources.

The recommendation engine should produce structured results that can be consumed by other parts of the application.

An LLM may later provide the natural-language interface and explanation layer, but should not replace the recommendation engine.

8. AI Architecture

The AI librarian is planned as a layer above existing application functionality.

User
 │
 ▼
LLM
 │
 ▼
Structured request
 │
 ▼
Application tools/services
 │
 ├── Library
 ├── Reading
 ├── Analytics
 └── Recommendations
 │
 ▼
Structured results
 │
 ▼
LLM
 │
 ▼
User

The LLM should:

Interpret natural-language requests.
Convert them into structured requests.
Call appropriate application functions.
Explain returned results.

The LLM should not:

Directly modify database tables.
Invent library information.
Replace deterministic application logic.
Become a required dependency for core functionality.
9. Retrieval Architecture

Different requests should use different retrieval methods.

User request
     │
     ▼
Request interpretation
     │
     ├───────────────┐
     ▼               ▼
Direct query    Semantic search
     │               │
     └───────┬───────┘
             ▼
          Results

Simple factual queries should use normal application/database queries where appropriate.

Semantic search and embeddings should only be introduced where they provide a meaningful advantage.

RAG is therefore an optional retrieval technique rather than a requirement for every AI interaction.

10. Analytics Architecture

Analytics should build on the application's underlying data rather than becoming a second source of truth.

Book Brain Database
        │
        ├── Application statistics
        │
        └── Analytical data
                 │
                 ▼
              Pandas
                 │
                 ▼
              Power BI

Power BI remains an optional analytics and portfolio layer.

The core application must remain functional without it.

11. Database Evolution

The initial database is SQLite.

If future requirements justify server-based infrastructure, the expected direction is:

Current


Python
  ↓
SQLite




Future


Web / Mobile
     ↓
FastAPI
     ↓
PostgreSQL

Migration should be driven by requirements such as:

Multiple users.
Remote access.
Increased concurrency.
Cloud deployment.
Advanced database requirements.

A vector extension such as pgvector may be considered later if semantic search requires it.

12. Mobile and Device Architecture

Mobile functionality should use the same backend and application services as the web application.

                 FastAPI
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
        Web                 Mobile
                              │
                         Device features
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                 Barcode             Wearable

Barcode scanning is an input mechanism for book identification.

Wearables are a potential future source of reading-session data rather than a separate reading-data architecture.

13. Security and Deployment

Security requirements will increase when Book Brain becomes remotely accessible.

Future deployed architecture should include appropriate:

Authentication.
Authorisation.
HTTPS.
Secret management.
API-key protection.
Input validation.
Secure external communication.
Logging and monitoring where appropriate.

The local MVP does not require production-scale infrastructure.

Secrets must never be committed to the repository.

14. Technology Evolution

The intended progression is:

Python + SQLite
        ↓
Repositories + Services + Testing
        ↓
External Book APIs
        ↓
Analytics + Power BI
        ↓
Recommendation Engine
        ↓
Embeddings / Semantic Search
        ↓
LLM
        ↓
AI Librarian + Tool Calling
        ↓
FastAPI + Web Application
        ↓
Mobile + Barcode
        ↓
Wearable Integration
        ↓
PostgreSQL + Deployment

The stages are not commitments to specific technologies. They represent the expected direction of development.

15. Architectural Boundaries

The following boundaries should be maintained as the project grows:

Database
    ↓
Stores data


Repositories
    ↓
Access data


Services
    ↓
Apply application logic


Integrations
    ↓
Communicate with external systems


Recommendation Engine
    ↓
Generate and rank candidates


LLM
    ↓
Interpret and communicate


API
    ↓
Expose application functionality


Frontend
    ↓
Present functionality to users

No layer should unnecessarily take responsibility for another layer's work.

16. Current vs Future
Component	Current MVP	Future
Python	Yes	Yes
SQLite	Yes	Potentially replaced
Repositories	Developing	Yes
Services	Developing	Yes
Automated tests	Yes	Yes
External APIs	No	Planned
Analytics	Basic	Pandas / Power BI
Recommendation engine	No	Planned
Embeddings	No	Possible
LLM	No	Planned
FastAPI	No	Planned
Web UI	No	Planned
Mobile	No	Planned
Barcode scanning	No	Planned
Wearables	No	Research / possible
PostgreSQL	No	Possible
Cloud deployment	No	Possible
17. Architecture Rule

Build the simplest architecture that supports the current development phase.

Future components should have a clear reason to exist before they are introduced.

The architecture should evolve from:

Simple
  ↓
Structured
  ↓
Extensible
  ↓
Intelligent
  ↓
Distributed

rather than attempting to build the final system from the beginning.