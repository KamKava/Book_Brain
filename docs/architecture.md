# Book Brain — System Architecture

**Project status:** Early development
**Version:** 0.1
**Last updated:** August 2026

---

# 1. Architecture Overview

Book Brain will initially be developed as a local Python application using SQLite.

The architecture will evolve incrementally as new functionality is introduced.

The initial system will focus on reliable book and reading data management. More advanced functionality such as recommendations, semantic search, AI, web access, mobile applications and wearable integration will be introduced only after the underlying functionality is stable.

The planned high-level architecture is:

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                         Future Web / Mobile UI
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      Library Management     Reading Management    Recommendation
             │                      │                      │
             └──────────────────────┼──────────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Database       │
                         │      SQLite         │
                         │  → PostgreSQL later │
                         └──────────┬──────────┘
                                    │
                   ┌────────────────┼────────────────┐
                   │                │                │
                   ▼                ▼                ▼
              Analytics       Embeddings       External APIs
                   │                │                │
                   ▼                ▼                ▼
              Power BI       Semantic Search    Book Metadata
                                    │
                                    ▼
                             ┌─────────────┐
                             │     LLM     │
                             └──────┬──────┘
                                    │
                             RAG / Tool Calling
                                    │
                                    ▼
                             AI Librarian
```

This represents the planned long-term architecture rather than the initial implementation.

---

# 2. Architectural Principles

Book Brain will follow the following principles:

## 2.1 Incremental Development

The system will be developed in stages.

The initial implementation will contain only the functionality required for the MVP.

Future components will be introduced when they provide practical value.

---

## 2.2 Database as the Source of Truth

The application database will be the authoritative source for the user's personal library data.

This includes:

* Books.
* Ownership.
* TBR status.
* Reading status.
* Ratings.
* Reading dates.
* Reading sessions.
* Notes.
* Formats.

The AI system must not invent or modify factual library information without going through controlled application functionality.

---

## 2.3 Separation of Responsibilities

Different components should have clearly defined responsibilities.

For example:

```text
Database
    Stores data

Python application
    Implements business logic

Recommendation engine
    Selects and ranks books

LLM
    Understands natural language and communicates results

FastAPI
    Provides application functionality through an API

Frontend
    Provides user interface

Power BI
    Provides advanced analytics and visualisation
```

---

## 2.4 AI Should Enhance Rather Than Replace Application Logic

The AI system should not be responsible for basic database operations or deterministic filtering.

For example, if the user asks:

> "Give me something short that I already own for the beach."

The LLM should interpret the request, but the application should determine which books actually satisfy the requirements.

The intended flow is:

```text
User request
     ↓
LLM interprets request
     ↓
Structured constraints
     ↓
Recommendation engine
     ↓
Database query
     ↓
Candidate books
     ↓
Ranking
     ↓
LLM explains recommendation
```

---

# 3. Initial Technology Stack

The initial MVP is expected to use:

| Component            | Technology               |
| -------------------- | ------------------------ |
| Programming language | Python                   |
| Database             | SQLite                   |
| Query language       | SQL                      |
| Version control      | Git                      |
| Repository           | GitHub                   |
| Testing              | Python testing framework |
| Documentation        | Markdown                 |

The initial application will not require a frontend, web server, cloud hosting or AI model.

---

# 4. Initial Python Architecture

The initial application will use a modular Python structure.

A possible structure is:

```text
book-brain/
│
├── docs/
│
├── src/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── analytics/
│   └── main.py
│
├── tests/
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

The exact structure may change during implementation.

The important principle is separation of responsibilities.

### Models

Represent application entities such as:

* Book
* Author
* Genre
* Library Entry
* Reading Session

### Database layer

Responsible for:

* Creating database connections.
* Executing SQL.
* Managing schema.
* Persisting data.

### Repository layer

Responsible for retrieving and modifying application data.

Examples:

```text
BookRepository
AuthorRepository
ReadingRepository
```

### Service layer

Contains business logic.

Examples:

```text
BookService
ReadingService
RecommendationService
AnalyticsService
```

The service layer should prevent business rules from becoming tightly coupled to database queries.

---

# 5. SQLite Database

SQLite will be used for the initial MVP.

SQLite is appropriate because:

* It is free.
* It requires no separate database server.
* It is lightweight.
* It works well with Python.
* It is easy to develop and test locally.
* It is sufficient for a single-user application during early development.

The database will contain structured information representing the user's library and reading history.

The database design will be documented separately in:

`docs/database-design.md`

The database will initially be treated as the system's source of truth.

---

# 6. Future Database Architecture

If Book Brain eventually becomes a multi-user or remotely accessible application, SQLite may be replaced or supplemented by a server-based database.

The planned migration target is:

**PostgreSQL**

Potential future architecture:

```text
Web / Mobile
      ↓
FastAPI
      ↓
PostgreSQL
```

PostgreSQL may also eventually support vector storage through technologies such as `pgvector` if semantic search requires it.

A migration will only be performed when justified by requirements such as:

* Multiple users.
* Remote access.
* Increased concurrency.
* Cloud deployment.
* Vector search requirements.

---

# 7. External Book Data

Book Brain will eventually use external book databases/APIs to reduce manual data entry and allow discovery of books outside the user's library.

Potential sources include:

* Google Books.
* Open Library.
* Other suitable book metadata APIs.

External APIs will not replace the Book Brain database.

The relationship will be:

```text
External Book API
       ↓
Book metadata
       ↓
Book Brain
       ↓
User reviews/edits
       ↓
Book Brain database
```

External API failures must not compromise existing user data.

---

# 8. Reading and Session Architecture

Book Brain will distinguish between information about a book and information about the user's interaction with that book.

For example:

```text
Book
 └── "Dracula"

Library Entry
 └── User owns Dracula

Reading Record
 └── User read Dracula

Reading Sessions
 ├── 20 minutes
 ├── 35 minutes
 └── 45 minutes
```

This allows the application to calculate:

* Total reading time.
* Average session duration.
* Reading frequency.
* Reading time by book.
* Reading time by genre.
* Reading time over time.

Reading sessions may eventually be associated with a currently selected book.

Unassigned sessions may also be supported.

---

# 9. Analytics Architecture

Analytics will use structured application data rather than manually created datasets.

The architecture will support several levels of analytics:

```text
Book Brain Database
        │
        ├───────────────┐
        │               │
        ▼               ▼
Application        Analytical queries
statistics              │
                        ▼
                    Python/Pandas
                        │
                        ▼
                     Power BI
```

The core application should be capable of producing basic statistics without Power BI.

Power BI will provide an additional analytical and portfolio layer.

Potential Power BI analysis includes:

* Books read over time.
* Pages read.
* Reading time.
* Genre distribution.
* Rating distribution.
* Book-length distribution.
* Author analysis.
* Reading trends.

Power BI will not be required for the core application to function.

---

# 10. Recommendation Architecture

The recommendation engine will initially be implemented independently of an LLM.

This is intentional.

The recommendation system should be able to:

1. Identify eligible books.
2. Apply user constraints.
3. Score candidates.
4. Rank candidates.
5. Explain the factors used.

For example:

```text
User request
     ↓
Constraints
     ↓
Candidate selection
     ↓
Filtering
     ↓
Scoring
     ↓
Ranking
     ↓
Recommendation
```

Potential recommendation inputs include:

* Ownership.
* TBR status.
* Reading history.
* Ratings.
* Genres.
* Authors.
* Page count.
* Reading context.
* Similar books.
* User preferences.

---

# 11. Context-Aware Recommendations

Book Brain will treat the user's situation as part of the recommendation request.

For example:

### Beach reading

```text
Context: Beach
Availability: Owned
Status: Unread/TBR
Preferred length: Short
```

The system should prioritise books already physically owned.

It should not recommend a book that the user would need to purchase before going to the beach.

### Bookshop visit

```text
Context: Bookshop
Availability: Not owned
Preferences: Based on reading history
```

The system may search external book catalogues and recommend books that match the user's interests but are not already owned.

This distinction will be implemented in the recommendation layer rather than relying entirely on the LLM.

---

# 12. Semantic Search and Embeddings

A later version may introduce embeddings to improve book similarity.

Book metadata such as descriptions, genres and other relevant information may be converted into embeddings.

Conceptually:

```text
Book metadata
     ↓
Embedding model
     ↓
Vector representation
     ↓
Similarity search
     ↓
Similar books
```

Potential uses include:

* Finding books similar to highly-rated books.
* Improving recommendations.
* Finding semantically similar genres/themes.
* Supporting AI librarian retrieval.

Potential technologies include:

* Local embedding models.
* PostgreSQL + pgvector.
* Chroma.
* Qdrant.

A separate vector database will only be introduced if it provides a meaningful benefit.

---

# 13. LLM Architecture

The LLM will be introduced after the core recommendation system has been implemented.

The LLM's primary responsibilities will be:

* Understanding natural-language requests.
* Extracting constraints.
* Communicating recommendations.
* Explaining recommendation results.
* Answering questions using retrieved Book Brain data.

The LLM should not be treated as the authoritative source of the user's library information.

Potential LLM approaches include:

* Local open-source models.
* External AI APIs.
* Hybrid approaches.

A provider abstraction should be considered so that the application is not permanently dependent on a single model provider.

---

# 14. AI Librarian Architecture

The AI librarian will eventually combine:

* LLM.
* Database queries.
* Recommendation engine.
* Analytics.
* Semantic search.
* Application tools.

The intended architecture is:

```text
                       User
                        │
                        ▼
                       LLM
                        │
                 Understand request
                        │
                        ▼
                 Select appropriate
                     capability
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       Library       Analytics   Recommendations
       Search        Queries        Engine
          │             │             │
          └─────────────┼─────────────┘
                        │
                        ▼
                     Results
                        │
                        ▼
                       LLM
                        │
                        ▼
                  User response
```

---

# 15. Retrieval-Augmented Generation

RAG may be introduced when the AI librarian requires access to larger amounts of Book Brain data.

The basic flow will be:

```text
User question
      ↓
LLM
      ↓
Retrieve relevant data
      ↓
Database / semantic search
      ↓
Relevant information
      ↓
LLM
      ↓
Answer
```

RAG will be used where retrieval provides a benefit.

Simple structured questions may instead use direct SQL queries.

For example:

> "How many books did I read this year?"

may be better handled by a direct database query than semantic search.

---

# 16. AI Tool Architecture

The AI librarian may eventually have controlled access to application tools.

Potential tools include:

```text
search_library()
get_book()
get_tbr()
get_current_book()
get_reading_statistics()
find_books_by_genre()
find_books_under_pages()
get_recommendations()
start_reading_session()
stop_reading_session()
search_external_books()
```

The AI should only be able to perform actions explicitly exposed through these tools.

Tool arguments should be validated by the application.

Destructive operations should require additional safeguards.

---

# 17. Web Application Architecture

The web application will be introduced after the core functionality and recommendation system are stable.

The planned architecture is:

```text
                 Browser
                    │
                    ▼
             Frontend application
                    │
                    ▼
                FastAPI
                    │
          ┌─────────┼─────────┐
          ▼         ▼         ▼
       Services  Analytics  AI
          │
          ▼
       Database
```

Potential frontend technologies include:

* HTML.
* CSS.
* JavaScript.
* React.
* TypeScript.

The final frontend technology will be selected when implementation begins.

---

# 18. FastAPI Backend

FastAPI will eventually provide a backend API between the user interfaces and the application logic.

Potential API areas include:

```text
/books
/authors
/genres
/reading
/sessions
/statistics
/recommendations
/ai
```

The API will provide controlled access to application functionality.

The business logic should remain in application services rather than being embedded directly into API endpoints.

---

# 19. Mobile Architecture

The mobile application will communicate with the same backend used by the web application.

Planned architecture:

```text
                    ┌─────────────┐
                    │   FastAPI   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │                         │
              ▼                         ▼
        Web application          Mobile application
              │                         │
              └────────────┬────────────┘
                           │
                           ▼
                       Database
```

Potential technology:

**React Native**

The mobile application should not create a separate copy of the application's core business logic.

---

# 20. Barcode Scanning

Barcode scanning will eventually allow users to scan an ISBN using a mobile device.

The planned flow is:

```text
Camera
  ↓
Barcode scanner
  ↓
ISBN
  ↓
Book metadata API
  ↓
Book information
  ↓
User confirmation
  ↓
Book Brain database
```

This functionality is expected to be primarily useful on mobile.

---

# 21. Wearable / Fitbit Integration

Wearable integration is a future research area rather than a confirmed feature.

The intended concept is a reading activity that allows the user to indicate:

**Start Reading**

and later:

**Stop Reading**

The resulting reading session could be synchronised with Book Brain.

Potential flow:

```text
Wearable
   ↓
Start Reading
   ↓
Reading session
   ↓
Stop Reading
   ↓
Synchronisation
   ↓
Book Brain
   ↓
Reading Session
```

The user may have a currently selected book:

```text
Currently Reading:
Dracula
```

In that case, the recorded session could automatically be associated with that book.

Alternatively, the session could remain unassigned:

```text
Reading session
Duration: 42 minutes
Book: Unknown
```

and be assigned later.

The technical feasibility of direct Fitbit integration must be investigated before this feature is committed to development.

---

# 22. Security Architecture

Security requirements will increase as Book Brain moves from a local application to a remotely accessible application.

The system should eventually include:

* Secure authentication.
* Secure password handling.
* Protected API credentials.
* Environment-based secrets.
* HTTPS.
* Input validation.
* Authorisation.
* Protection of personal library data.

API keys and secrets must never be committed to GitHub.

---

# 23. Deployment Architecture

The initial MVP will run locally.

A future deployed version is expected to use:

```text
Internet
   │
   ▼
Frontend hosting
   │
   ▼
FastAPI backend
   │
   ▼
PostgreSQL
```

Additional services may eventually include:

* AI model/API provider.
* External book APIs.
* Vector search.
* File/image storage.

Free or low-cost hosting should be preferred where practical.

---

# 24. Technology Evolution

The expected technology progression is:

```text
MVP

Python
SQLite
SQL
Git/GitHub
Testing


        ↓

External data

Book APIs
HTTP/API integration


        ↓

Analytics

Pandas
Power BI
Analytical SQL


        ↓

Recommendations

Python
Scoring
Content-based filtering


        ↓

Semantic intelligence

Embeddings
Vector search


        ↓

Generative AI

LLM
Prompting
Structured outputs


        ↓

AI Librarian

RAG
Tool calling
Controlled AI actions


        ↓

Web

FastAPI
React
TypeScript


        ↓

Mobile

React Native
Barcode scanning


        ↓

Device integration

Wearables
Reading-session synchronisation
```

This progression is intentional.

---

# 25. Current Architecture

At the current stage, only the following components are planned for immediate implementation:

```text
Python
   │
   ▼
Application logic
   │
   ▼
SQLite
   │
   ▼
Book / Library / Reading data
   │
   ▼
Automated tests
```

Everything beyond this is planned architecture rather than implemented functionality.

---

# 26. Architectural Decision: Avoid Premature Complexity

Book Brain will not initially implement:

* PostgreSQL.
* FastAPI.
* React.
* Mobile applications.
* Vector databases.
* LLMs.
* AI agents.
* Cloud infrastructure.
* Wearable integration.

These technologies will be introduced only when the relevant development phase begins.

This approach reduces unnecessary complexity while preserving a clear path toward the long-term vision.

---

# 27. Relationship to Other Documentation

This document describes **how the system is expected to be structured**.

Other project documentation provides complementary information:

| Document             | Purpose                                 |
| -------------------- | --------------------------------------- |
| `requirements.md`    | What Book Brain should do               |
| `roadmap.md`         | When functionality is planned           |
| `architecture.md`    | How the system will be structured       |
| `database-design.md` | How data will be stored                 |
| `development-log.md` | What has actually been done and learned |

These documents should be updated as architectural decisions change.

Major architectural changes should be recorded as technical decisions in the development documentation.
