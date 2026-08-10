# Book Brain — System Architecture

**Project status:** Early development
**Version:** 0.1
**Last updated:** August 2026

---

# 1. Architecture Overview

Book Brain will initially be developed as a local Python application using SQLite.

The architecture will evolve incrementally as new functionality is introduced.

The initial system will focus on reliable book, library and reading data management. More advanced functionality such as external book discovery, recommendations, semantic search, AI, web access, mobile applications and wearable integration will be introduced only after the underlying functionality is stable.

The planned long-term architecture is:

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Web / Mobile UI    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
             ┌──────────────────────┼──────────────────────┐
             │                      │                      │
             ▼                      ▼                      ▼
      Library Services      Reading Services      Recommendation
                                                        Engine
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
              Analytics        Embeddings       Book Metadata
                   │                │           / External APIs
                   ▼                ▼                │
              Power BI       Semantic Search         │
                                    │                 │
                                    └────────┬────────┘
                                             ▼
                                      Recommendation
                                         Candidates
                                             │
                                             ▼
                                       AI Librarian
                                             │
                                             ▼
                                            LLM
```

This represents the planned long-term architecture rather than the initial implementation.

The architecture is deliberately designed so that the database, application logic and recommendation system remain functional without an LLM.

---

# 2. Architectural Principles

Book Brain will follow the following principles.

## 2.1 Incremental Development

The system will be developed in stages.

The initial implementation will contain only the functionality required for the MVP.

Future components will be introduced when they provide practical value.

The project should avoid introducing technologies simply because they are technically interesting.

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
* Reading history.
* Reading sessions.
* Notes.
* Formats.
* Series information.

External book databases may provide metadata, but they do not replace Book Brain's database.

The LLM must not invent or override factual library information.

---

## 2.3 Separation of Responsibilities

Different components should have clearly defined responsibilities.

```text
Database
    Stores application data

Python application
    Implements business logic

External book services
    Provide book metadata and external candidates

Recommendation engine
    Selects, filters and ranks books

LLM
    Understands natural language and communicates results

FastAPI
    Provides application functionality through an API

Frontend
    Provides user interface

Power BI
    Provides advanced analytics and visualisation

Embeddings / semantic search
    Identify semantic similarity between books
```

Each component should perform the work for which it is best suited.

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
Database / external sources
     ↓
Candidate books
     ↓
Filtering
     ↓
Ranking
     ↓
LLM explains results
```

The LLM therefore acts as an interface to Book Brain rather than as the authority on the user's library.

---

## 2.5 Keep AI Replaceable

Book Brain should not become permanently dependent on one LLM provider.

Where practical, AI functionality should be implemented behind an abstraction layer.

This should allow the application to switch between:

* Local models.
* External APIs.
* Different model providers.
* Different model versions.

The rest of the application should not need to be redesigned when the LLM changes.

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
│   ├── integrations/
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

* Book.
* Author.
* Genre.
* Series.
* Library Entry.
* Reading History.
* Reading Session.
* Rating.
* Note.

### Database layer

Responsible for:

* Creating database connections.
* Executing SQL.
* Managing schema.
* Persisting data.
* Managing transactions.

### Repository layer

Responsible for retrieving and modifying application data.

Examples:

```text
BookRepository
AuthorRepository
LibraryRepository
ReadingRepository
```

### Service layer

Contains business logic.

Examples:

```text
BookService
LibraryService
ReadingService
RecommendationService
AnalyticsService
```

The service layer should prevent business rules from becoming tightly coupled to database queries.

### Integration layer

Future external services should be isolated from the core application.

Examples:

```text
BookMetadataService
GoogleBooksClient
OpenLibraryClient
LLMProvider
```

External services should not directly manipulate the database.

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

Book Brain will eventually use external book databases and APIs for two distinct purposes:

1. **Book metadata lookup** when adding books to the user's library.
2. **External book discovery** when generating recommendations for books the user does not own.

These two functions should remain conceptually separate.

---

## 7.1 External Book Metadata

The primary purpose of external metadata lookup is to reduce manual data entry and prevent errors.

The user may enter:

* ISBN.
* Title.
* Author.

Book Brain can then search external book catalogues and return possible matches.

The intended flow is:

```text
User enters title / author / ISBN
              ↓
       Book Search Service
              ↓
       External Book API(s)
              ↓
       Candidate results
              ↓
        User selects result
              ↓
      Metadata mapped to model
              ↓
       User confirms / edits
              ↓
       Book Brain database
```

Potential metadata includes:

* Title.
* Author.
* ISBN.
* Page count.
* Publication date.
* Publisher.
* Edition information.
* Genres/categories.
* Cover image.
* Book description.

The external source should not directly write into the database.

The user should remain in control of the final library record.

Potential sources include:

* Google Books.
* Open Library.
* Other suitable book metadata APIs.

The selected sources will be documented in the relevant technical decision record.

---

## 7.2 External Recommendation Discovery

External book discovery is a separate capability used when Book Brain needs to find books that are **not already in the user's library**.

For example:

> "I'm going to the bookshop. What should I buy?"

The intended flow is:

```text
User request
      ↓
Recommendation context
      ↓
External book catalogues
      ↓
Potential candidates
      ↓
Remove books already owned
      ↓
Apply preferences and exclusions
      ↓
Recommendation engine
      ↓
Rank candidates
      ↓
Return recommendations
```

External discovery may search using:

* Genres.
* Authors.
* Keywords.
* Themes.
* Book descriptions.
* Similarity.
* Publication information.

External recommendation candidates are not automatically added to the user's library.

They remain recommendation candidates until the user chooses to acquire or add a book.

---

## 7.3 External API Reliability

External APIs must not compromise existing Book Brain data.

The application should:

* Handle API failures.
* Handle timeouts.
* Handle rate limits.
* Handle incomplete metadata.
* Handle unavailable cover images.
* Handle duplicate results.
* Validate returned data.
* Allow manual correction.
* Never overwrite existing user data automatically.

---

# 8. Reading and Session Architecture

Book Brain will distinguish between information about a book and information about the user's interaction with that book.

For example:

```text
Book
 └── "Dracula"

Library Entry
 └── User owns Dracula

Reading History
 └── User read Dracula

Reading Sessions
 ├── 20 minutes
 ├── 35 minutes
 └── 45 minutes
```

Reading sessions are intended to support **both manual and future automated tracking**.

A user should eventually be able to start a reading session directly within Book Brain:

```text
User selects:
Dracula

       ↓

[ Start Reading ]

       ↓

Reading session begins

       ↓

[ Stop Reading ]

       ↓

Session saved
```

The application should therefore not design reading sessions as Fitbit-specific functionality.

Potential session sources may include:

```text
Manual
Mobile
Web
Wearable
Imported
```

The resulting reading session should use the same underlying data model regardless of its source.

Reading sessions may be associated with a currently selected book.

Unassigned sessions may also be supported.

This allows the application to calculate:

* Total reading time.
* Average session duration.
* Reading frequency.
* Reading time by book.
* Reading time by genre.
* Reading time over time.

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
* Reading-session analysis.

Power BI will not be required for the core application to function.

---

# 10. Recommendation Architecture

The recommendation engine will initially be implemented independently of an LLM.

This is intentional.

The recommendation system should be able to operate using deterministic application logic and structured data.

It should be capable of:

1. Identifying eligible candidates.
2. Applying user constraints.
3. Applying exclusion rules.
4. Scoring candidates.
5. Ranking candidates.
6. Recording recommendation factors.
7. Providing structured explanations.

The recommendation engine may receive candidates from multiple sources.

```text
                       Recommendation request
                                ↓
                       Context / constraints
                                ↓
                 ┌──────────────┴──────────────┐
                 │                             │
                 ▼                             ▼
          Library candidates            External candidates
                 │                             │
                 │                       External APIs
                 │                             │
                 └──────────────┬──────────────┘
                                ↓
                       Candidate filtering
                                ↓
                       Recommendation rules
                                ↓
                             Scoring
                                ↓
                             Ranking
                                ↓
                         Recommendations
```

The recommendation engine should not need to know whether a candidate originally came from the user's library or an external source in order to score it.

However, candidate origin and availability should remain explicit so that context-specific rules can be applied.

---

# 11. Context-Aware Recommendations

Book Brain will treat the user's situation as part of the recommendation request.

For example:

## Beach reading

```text
Context: Beach
Availability: Owned
Status: Unread / TBR
Preferred length: Short
```

The system should prioritise books already physically owned.

It should not recommend a book that the user would need to purchase before going to the beach.

---

## Bookshop visit

```text
Context: Bookshop
Availability: Not owned
Preferences: Based on reading history
```

The system may search external book catalogues and recommend books that match the user's interests but are not already owned.

---

## Short reading session

```text
Context: Short session
Availability: Owned
Preferred length: Short
```

The system may prioritise shorter books or books that are suitable for a limited reading period.

---

## General recommendation

```text
Context: General
Availability: Depends on request
Preferences: User history
```

The recommendation engine may consider both library and external candidates depending on the user's request.

The recommendation engine should explicitly model these differences rather than expecting the LLM to handle them implicitly.

---

# 12. Recommendation Candidate Sources

Recommendation candidates may come from several sources.

### Internal candidates

Books already known to Book Brain:

* Owned books.
* TBR books.
* Unread books.
* Previously read books where appropriate.

### External candidates

Books discovered through external sources:

* External book catalogues.
* Search results.
* Author searches.
* Genre searches.
* Keyword searches.
* Semantic similarity searches.

The recommendation engine should be responsible for applying rules such as:

* Excluding owned books when the user is shopping.
* Excluding already-read books where appropriate.
* Applying genre exclusions.
* Applying author exclusions.
* Applying page-count preferences.
* Applying contextual constraints.

---

# 13. Semantic Search and Embeddings

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
* Finding semantically similar themes.
* Finding books with similar descriptions.
* Supporting AI librarian retrieval.
* Improving external recommendation discovery.

Semantic similarity should complement rather than automatically replace the rule-based recommendation engine.

The recommendation system may combine:

```text
Rule-based score
        +
Semantic similarity
        ↓
Final recommendation score
```

Potential technologies include:

* Local embedding models.
* PostgreSQL + pgvector.
* Chroma.
* Qdrant.

A separate vector database will only be introduced if it provides a meaningful benefit.

---

# 14. LLM Architecture

The LLM will be introduced after the core recommendation system has been implemented.

The LLM's primary responsibilities will be:

* Understanding natural-language requests.
* Extracting constraints.
* Converting requests into structured requirements.
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

# 15. AI Librarian Architecture

The AI librarian will eventually combine:

* LLM.
* Database queries.
* Recommendation engine.
* Analytics.
* Semantic search.
* External book discovery.
* Controlled application tools.

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
                  Structured request
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ▼               ▼                ▼
       Library        Analytics      Recommendations
       queries          queries            │
          │               │          ┌─────┴─────┐
          │               │          ▼           ▼
          │               │      Internal     External
          │               │     candidates   candidates
          │               │          │           │
          └───────────────┼──────────┴───────────┘
                          │
                          ▼
                  Recommendation engine
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

The AI librarian should not independently decide which books satisfy database constraints.

Instead, it should delegate these tasks to Book Brain's application services.

---

# 16. Retrieval Architecture

Retrieval may be implemented using different mechanisms depending on the type of request.

Not every AI request requires RAG or semantic search.

For example:

> "How many books did I read this year?"

may be best handled through a direct SQL query.

Whereas:

> "Which books I own are most similar to the weird horror books I've rated highly?"

may benefit from semantic search and embeddings.

The architecture should therefore support:

```text
User request
      ↓
LLM interprets request
      ↓
Determine retrieval method
      │
      ├───────────────┐
      ▼               ▼
Direct query     Semantic retrieval
      │               │
      └───────┬───────┘
              ▼
           Results
              │
              ▼
             LLM
```

RAG should be introduced where retrieval provides a meaningful benefit rather than being used for every query.

---

# 17. AI Tool Architecture

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

Tools should be implemented as controlled application functionality.

The LLM should not receive unrestricted access to SQL or the database.

Tool arguments should be validated by the application.

Destructive operations should require additional safeguards.

Tool calls should be logged where appropriate for debugging and evaluation.

---

# 18. Web Application Architecture

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
          │         │         │
          └─────────┼─────────┘
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

The frontend should communicate with the application through the backend API rather than implementing separate business logic.

---

# 19. FastAPI Backend

FastAPI will eventually provide a backend API between the user interfaces and the application logic.

Potential API areas include:

```text
/books
/authors
/genres
/series
/library
/reading
/sessions
/statistics
/recommendations
/external-books
/ai
```

The API will provide controlled access to application functionality.

The business logic should remain in application services rather than being embedded directly into API endpoints.

API responses should use structured schemas and appropriate validation.

---

# 20. Mobile Architecture

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

# 21. Barcode Scanning

Barcode scanning will eventually allow users to scan an ISBN using a mobile device.

The planned flow is:

```text
Camera
  ↓
Barcode scanner
  ↓
ISBN
  ↓
Book metadata service
  ↓
Candidate book records
  ↓
User confirmation
  ↓
Book Brain database
```

Barcode scanning is therefore an input mechanism for the external book metadata system.

It should use the same book-search and metadata functionality as manually entering an ISBN.

---

# 22. Wearable / Fitbit Integration

Wearable integration is a future research area rather than a confirmed feature.

Reading sessions are designed to support manual tracking first, with wearable integration potentially becoming an additional session source later.

The intended concept is a reading activity that allows the user to indicate:

**Start Reading**

and later:

**Stop Reading**

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

# 23. Security Architecture

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
* Secure external API communication.

API keys and secrets must never be committed to GitHub.

The local MVP will have significantly fewer security requirements because it will not initially expose the application to the public internet.

---

# 24. Deployment Architecture

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
   ├──────────────┐
   │              │
   ▼              ▼
PostgreSQL    External APIs
   │
   ├──────────────┐
   ▼              ▼
Analytics      Vector storage
                  │
                  ▼
             AI services
```

Additional services may eventually include:

* AI model/API provider.
* External book APIs.
* Vector search.
* File/image storage.
* Monitoring and logging services.

Free or low-cost hosting should be preferred where practical.

---

# 25. Technology Evolution

The expected technology progression is:

```text
MVP

Python
SQLite
SQL
Git/GitHub
Testing


        ↓

Core library

Repositories
Services
Validation
Automated testing


        ↓

External data

Book APIs
HTTP/API integration
ISBN / title / author search


        ↓

Analytics

Pandas
Power BI
Analytical SQL


        ↓

Recommendations

Python
Rule-based scoring
Context-aware filtering
Content-based recommendations


        ↓

Semantic intelligence

Embeddings
Vector search
Semantic similarity


        ↓

Generative AI

LLM
Prompting
Structured outputs


        ↓

AI Librarian

Natural-language queries
Controlled retrieval
RAG where appropriate
Tool calling


        ↓

Web

FastAPI
React / JavaScript
TypeScript


        ↓

Mobile

React Native
Barcode scanning


        ↓

Device integration

Wearables
Reading-session synchronisation


        ↓

Deployment

Cloud hosting
PostgreSQL
Production infrastructure
```

This progression is intentional.

---

# 26. Current Architecture

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

The current implementation should not depend on:

* FastAPI.
* React.
* External APIs.
* Embeddings.
* LLMs.
* RAG.
* Vector databases.
* Cloud infrastructure.
* Mobile applications.
* Wearable devices.

---

# 27. Architectural Decision: Avoid Premature Complexity

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

# 28. Architectural Decision: External Data Does Not Own User Data

External book APIs are considered sources of information, not sources of truth.

The relationship is:

```text
External source
      ↓
Potential metadata
      ↓
Book Brain validation
      ↓
User confirmation
      ↓
Book Brain database
```

Once information has been accepted into Book Brain, the user's database record becomes authoritative.

External sources should not silently overwrite user edits.

For example, if an external API says a book has 320 pages but the user's physical edition has 347 pages, Book Brain should be able to preserve the user's edition-specific information.

---

# 29. Architectural Decision: Recommendation Engine Is Independent of the LLM

The recommendation engine must be capable of operating without an LLM.

This allows:

```text
Input
  ↓
Candidate selection
  ↓
Filtering
  ↓
Scoring
  ↓
Ranking
  ↓
Result
```

to be tested independently.

The LLM can later act as a natural-language interface:

```text
User
  ↓
LLM
  ↓
Structured constraints
  ↓
Recommendation engine
  ↓
Ranked results
  ↓
LLM explanation
  ↓
User
```

This separation makes recommendation behaviour more deterministic, explainable and testable.

---

# 30. Architectural Decision: Reading Sessions Are Source-Agnostic

Reading sessions should not be designed specifically around Fitbit or another wearable.

A reading session represents the user's reading activity regardless of how it was recorded.

Potential sources include:

```text
Manual
Web
Mobile
Wearable
Imported
```

All sources should ultimately produce the same logical reading-session record.

This allows Book Brain to introduce wearable integration later without redesigning the reading-session system.

---

# 31. Relationship to Other Documentation

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

The architecture document should describe both the current implementation and the intended evolution of the system, while avoiding the assumption that future components have already been built.
