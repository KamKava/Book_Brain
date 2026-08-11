# Book Brain — Software Requirements Specification

**Project status:** Initial development
**Version:** 0.2
**Last updated:** August 2026

---

# 1. Project Overview

Book Brain is a personal book management, reading-tracking, analytics, recommendation, and AI librarian application.

The application is designed to help a user:

* Catalogue books they own.
* Manage their TBR collection.
* Track books they are currently reading.
* Record completed books and ratings.
* Track reading dates and reading sessions.
* Record reading notes.
* Analyse reading habits.
* Discover books already available in their collection.
* Identify books they may wish to acquire.
* Eventually interact with an AI librarian through natural language.
* Potentially track reading sessions through wearable devices.

Book Brain will begin as a local Python and SQLite application. It will progressively evolve through additional development phases rather than implementing the complete long-term vision at once.

Potential future functionality includes:

* External book metadata APIs.
* Barcode/ISBN scanning.
* Advanced analytics.
* Personalised recommendations.
* Semantic search.
* Conversational AI.
* A web application.
* A mobile application.
* Wearable integration.
* Remote access and multi-user support.

The project is intended to be both a genuinely useful personal application and a portfolio project demonstrating skills in:

* Software engineering.
* Database design.
* SQL.
* Data modelling.
* Data analysis.
* API integration.
* Recommendation systems.
* Artificial intelligence.
* Web development.
* Mobile development.
* Testing.
* Deployment.
* Technical documentation.

---

# 2. Project Goals

The primary goals of Book Brain are to:

1. Provide a reliable digital catalogue of the user's books.
2. Separate information about books and editions from the user's ownership of those books.
3. Minimise manual data entry through ISBN lookup and, eventually, barcode scanning.
4. Allow the user to manage their TBR collection and reading history.
5. Track reading status, ratings, dates, notes, formats, and reading sessions.
6. Track the amount of time spent reading.
7. Provide meaningful statistics about reading habits.
8. Allow reading habits to be analysed by genre, author, length, rating, time period, and reading time.
9. Provide recommendations based on the user's actual library and reading behaviour.
10. Distinguish between books that are already available to the user and books that require acquisition.
11. Support context-aware recommendations.
12. Develop a recommendation engine independently from the conversational AI.
13. Eventually provide a conversational AI librarian.
14. Investigate wearable integration for reading-session tracking.
15. Provide web and mobile access in future versions.
16. Allow the user to retain control of and export their personal library data.
17. Provide a modular architecture that can evolve without unnecessarily rewriting the core application.

---

# 3. Development Philosophy

## 3.1 Incremental Development

Book Brain shall be developed incrementally.

The project shall begin with a small, functional core and introduce additional functionality only when the underlying components are sufficiently stable and tested.

Future functionality shall not be implemented solely because it is part of the long-term vision.

Each development phase should introduce functionality that provides a meaningful benefit to the application.

---

## 3.2 Database as the Source of Truth

The application database shall be the authoritative source for the user's personal library information.

This includes:

* Books.
* Editions.
* Ownership.
* Library status.
* Reading history.
* Ratings.
* Reading dates.
* Reading sessions.
* Notes.
* User preferences where applicable.

External APIs may provide metadata, but they shall not become the authoritative source for the user's personal data.

AI-generated information shall not override authoritative application data.

---

## 3.3 Separation of Responsibilities

The system shall separate responsibilities between application components.

The intended responsibilities are:

```text
Database
    Stores persistent application data

Repositories
    Retrieve and persist data

Services
    Implement business rules

Recommendation Engine
    Filters, scores and ranks candidates

API
    Exposes application functionality

Frontend
    Provides user interaction

Analytics
    Calculates and presents reading statistics

LLM
    Interprets natural language and communicates results

External APIs
    Provide optional external data

Wearable integrations
    Provide optional activity/session data
```

Core application functionality should not depend unnecessarily on optional components.

---

## 3.4 AI Should Enhance Rather Than Replace Application Logic

The AI system shall not be responsible for deterministic business rules.

For example, if the user asks:

> "Give me something short that I already own for the beach."

The AI may interpret:

```text
context = beach
availability = owned
status = unread
preferred_length = short
```

The application shall then determine which books actually satisfy those requirements.

The intended flow is:

```text
User request
     ↓
LLM interprets request
     ↓
Structured request / constraints
     ↓
Application logic
     ↓
Database query
     ↓
Candidate books
     ↓
Recommendation engine
     ↓
Ranked results
     ↓
LLM explains results
```

The recommendation engine shall remain usable without an LLM.

---

## 3.5 External Services Are Optional Dependencies

External services such as book metadata APIs, AI providers, wearable platforms, and future cloud services shall not be required for core library functionality.

Failure of an external service should not result in loss of existing application data.

---

# 4. Scope

## 4.1 Initial MVP

The Minimum Viable Product shall provide:

* SQLite database.
* Book and edition data management.
* Library ownership records.
* Basic CRUD functionality.
* Basic book search.
* Reading status.
* Ratings.
* Reading dates.
* Reading notes.
* Reading sessions.
* Basic reading statistics.
* Automated tests.
* Basic data export.

The MVP shall operate locally.

---

## 4.2 Explicitly Out of Scope for MVP

The initial MVP shall not require:

* Graphical frontend.
* FastAPI.
* Web application.
* Mobile application.
* AI.
* LLM integration.
* Recommendation engine.
* Semantic search.
* Vector database.
* Barcode scanning.
* External book APIs.
* Wearable integration.
* Cloud deployment.
* User accounts.
* Multi-user functionality.
* Power BI integration.

These features may be introduced during later development phases.

---

# 5. Functional Requirements

# 5.1 Book and Edition Management

Book Brain shall distinguish between a **work/title** and a specific **edition** where necessary.

For example:

```text
Work
 └── Dracula

Editions
 ├── 1897 edition
 ├── Penguin paperback
 └── E-book edition
```

This allows different editions of the same work to exist without treating them as unrelated books.

The exact implementation will be defined in the database design.

---

## FR-001 — Create Book Record

The system shall allow the user to create a record representing a book/work.

A book record may contain information such as:

* Title.
* Description.
* Language.
* Publication information where appropriate.
* Genre/category associations.

---

## FR-002 — Create Edition Record

The system shall allow a specific edition of a book/work to be recorded.

An edition may contain:

* ISBN-10.
* ISBN-13.
* Publisher.
* Publication date.
* Page count.
* Format.
* Cover image.
* Edition-specific metadata.

Books without an ISBN shall be supported.

---

## FR-003 — Unique Internal Identification

The system shall assign a unique internal identifier to each major entity.

Internal identifiers shall not depend exclusively on ISBN values.

---

## FR-004 — ISBN Uniqueness

Where an ISBN is available, the system should prevent duplicate ISBN records within the relevant edition data.

Different editions may have different ISBNs.

---

## FR-005 — Author Management

The system shall allow books to be associated with one or more authors.

An author may be associated with multiple books.

The database shall support many-to-many relationships between books and authors where required.

---

## FR-006 — Genre Management

The system shall allow books to be associated with one or more genres or categories.

A genre may be associated with multiple books.

The database shall support many-to-many relationships between books and genres.

---

## FR-007 — View Book

The system shall allow the user to retrieve detailed information about a book and its relevant editions.

---

## FR-008 — Update Book

The system shall allow the user to modify book information.

---

## FR-009 — Update Edition

The system shall allow the user to modify edition-specific information.

---

## FR-010 — Delete Book or Edition

The system shall allow the user to remove book or edition information where appropriate.

The application should request confirmation before permanent deletion.

Deletion shall respect relationships with library and reading records.

The system should prevent accidental deletion of historical data where doing so would compromise data integrity.

---

# 6. Library Management

The user's relationship with a book shall be stored separately from general book metadata.

For example:

```text
Book
 └── Dracula

Library Entry
 ├── User owns Dracula
 ├── Status: TBR
 └── Format: Paperback
```

This separation allows the same book to exist independently of whether the user owns it.

---

## FR-011 — Add Book to Library

The system shall allow the user to add an edition/book to their personal library.

---

## FR-012 — Ownership

The system shall record whether a book/edition is currently owned by the user.

---

## FR-013 — Library Status

The system shall allow the user to assign a library/reading status.

Initial statuses shall include:

* TBR.
* Currently Reading.
* Read.

The status model may evolve as requirements become clearer.

---

## FR-014 — Multiple Formats

The system shall support ownership of different editions or formats of the same work where appropriate.

For example, a user may own:

* Paperback.
* E-book.
* Audiobook.

These shall not unnecessarily be treated as the same physical item.

---

## FR-015 — View Personal Library

The system shall allow the user to retrieve their personal library.

---

## FR-016 — Remove From Library

The system shall allow the user to remove a book/edition from their personal library.

Historical reading information should not be unintentionally destroyed when an ownership record is removed.

---

# 7. Reading Management

Reading information shall be represented separately from general book metadata and ownership.

This allows the application to distinguish between:

```text
Book
    Dracula

Library Entry
    User owns Dracula

Reading Record
    User read Dracula

Reading Sessions
    20 minutes
    35 minutes
    45 minutes
```

---

## FR-017 — Reading Status

The system shall allow the user to indicate whether a book is:

* TBR.
* Currently Reading.
* Read.

The system may support additional states in future versions.

---

## FR-018 — Rating

The system shall allow the user to rate a completed book using a five-point rating system.

Ratings shall be optional.

Ratings shall be validated against the permitted range.

---

## FR-019 — Reading Start Date

The system shall allow the user to record when they started reading a book.

---

## FR-020 — Reading Finish Date

The system shall allow the user to record when they finished a book.

---

## FR-021 — Reading Date Validation

Where both dates are provided, the system shall ensure that the finish date is not earlier than the start date.

---

## FR-022 — Reading Notes

The system shall allow the user to store personal notes associated with their reading of a book.

---

## FR-023 — Reading History

The system shall maintain historical reading information where applicable.

The data model should allow the application to distinguish between a book currently being read and a book previously completed.

The possibility of rereading a book should not be prevented by the data model.

---

# 8. Reading Session Tracking

Reading sessions shall represent individual periods of reading activity.

A session may exist independently of a specific book.

This allows:

```text
Reading Session
    45 minutes
    Book: Unknown
```

to be recorded and associated with a book later.

---

## FR-024 — Start Reading Session

The system shall allow the user to start a reading session.

A session shall record:

* Start date and time.

A session may optionally be associated with a book.

---

## FR-025 — End Reading Session

The system shall allow the user to end an active reading session.

The system shall record:

* End date and time.
* Session duration.

Duration should be calculated from timestamps rather than manually entered where possible.

---

## FR-026 — Associate Session With Book

The user shall be able to associate a reading session with a book.

The user shall be able to:

* Select a book before starting.
* Select a book after starting.
* Change the associated book.
* Leave the session unassigned.

---

## FR-027 — Reading Session History

The system shall allow the user to view historical reading sessions.

Session information may include:

* Book.
* Start time.
* End time.
* Duration.
* Date.
* Format where available.

---

## FR-028 — Current Reading Book

The system should allow the user to identify their current book.

This information may later be used to automatically associate wearable-generated reading sessions.

---

## FR-029 — Reading Time Statistics

The system shall calculate reading-time statistics where sufficient session data exists.

Possible statistics include:

* Total reading time.
* Reading time per book.
* Average session duration.
* Longest session.
* Reading time per day.
* Reading time per week.
* Reading time per month.
* Reading time per year.
* Reading time by genre.
* Reading time by format.

---

# 9. Search and Filtering

## FR-030 — Basic Search

The system shall allow the user to search their library by:

* Title.
* Author.
* ISBN.

---

## FR-031 — Filtering

The system shall support filtering by relevant attributes.

Potential filters include:

* Reading status.
* Genre.
* Author.
* Rating.
* Page count.
* Publication year.
* Reading year.
* Format.
* Ownership.
* Reading time.

---

## FR-032 — Combined Filters

The application should allow multiple filters to be applied simultaneously.

For example:

```text
Owned
+
Unread
+
Horror
+
Under 200 pages
```

This functionality will become particularly important to the recommendation engine.

---

# 10. External Book Metadata

External metadata services are a future feature.

---

## FR-033 — ISBN Lookup

A future version shall allow an ISBN to be submitted to an external book metadata service.

---

## FR-034 — Metadata Import

Where available, the system should retrieve:

* Title.
* Authors.
* Publisher.
* Publication date.
* Page count.
* Description.
* Cover.
* Categories.
* Language.
* ISBN information.

Imported data shall be reviewed before becoming part of the user's authoritative library information where appropriate.

---

## FR-035 — Metadata Provenance

The application should record where imported metadata originated.

Potential sources include:

* User.
* Google Books.
* Open Library.
* Other APIs.

The system should distinguish imported data from manually entered data where practical.

---

## FR-036 — External API Failure

The system shall handle:

* Invalid ISBNs.
* ISBN not found.
* Network failures.
* API downtime.
* Rate limits.
* Incomplete metadata.
* Unexpected API responses.

External API failure shall not prevent manual book management.

---

# 11. Barcode Scanning

Barcode scanning is a future feature primarily intended for mobile use.

---

## FR-037 — ISBN Barcode Scanning

A future mobile application shall allow the user to scan a supported ISBN barcode.

The scanned ISBN shall be passed to the metadata lookup process.

---

## FR-038 — Scan-to-Library Workflow

The intended workflow is:

```text
Scan barcode
     ↓
Extract ISBN
     ↓
Retrieve metadata
     ↓
Display proposed book information
     ↓
User confirms/edits
     ↓
Create book/edition
     ↓
Add to library
```

The user shall be able to correct imported information before saving.

---

# 12. Reading Statistics and Analytics

Analytics shall use structured application data.

The application should be capable of producing basic statistics without requiring Power BI.

---

## FR-039 — Basic Statistics

The application shall provide statistics including, where sufficient data exists:

* Total books owned.
* Total books read.
* Total TBR books.
* Total currently reading.
* Books completed during a selected period.
* Average rating.
* Total pages read.
* Average book length.
* Shortest book read.
* Longest book read.
* Total reading time.
* Average session duration.

---

## FR-040 — Time-Based Analysis

The system shall support analysis by:

* Day.
* Week.
* Month.
* Quarter.
* Year.
* Custom date range.

Possible metrics include:

* Books completed.
* Pages read.
* Reading time.
* Average rating.
* Average book length.

---

## FR-041 — Genre Analysis

The system shall support analysis by genre/category.

Possible metrics include:

* Books read per genre.
* Books owned per genre.
* Average rating by genre.
* Pages read by genre.
* Reading time by genre.
* Percentage of reading by genre.
* Genre trends over time.

Books may belong to multiple genres.

---

## FR-042 — Book Length Analysis

The system shall support analysis by page count.

Possible metrics include:

* Average page count.
* Median page count.
* Book-length distribution.
* Books below a selected threshold.
* Books above a selected threshold.
* Average rating by length.
* Reading time by length.

Potential categories include:

* Under 100 pages.
* 100–199 pages.
* 200–299 pages.
* 300–399 pages.
* 400–499 pages.
* 500+ pages.

These categories may become configurable in future versions.

---

## FR-043 — Author Analysis

The system should provide:

* Most-read authors.
* Books read per author.
* Average rating by author.
* Pages read by author.
* Reading time by author.
* Highest-rated authors.

---

## FR-044 — Rating Analysis

The system shall support:

* Average rating.
* Rating distribution.
* Books per rating.
* Average rating by genre.
* Average rating by author.
* Rating trends over time.

---

## FR-045 — Reading Pace

Where sufficient data exists, the system should calculate:

* Days spent reading a book.
* Average days per book.
* Books completed per month.
* Average session duration.
* Reading time per book.
* Estimated reading pace.

Measured values and estimates shall be clearly distinguished.

---

## FR-046 — Reading Trends

The system should identify changes in reading behaviour over time, including:

* Number of books read.
* Average book length.
* Preferred genres.
* Average rating.
* Reading frequency.
* Reading-session duration.
* Total reading time.

---

# 13. Analytics Dashboard

A future user interface may provide visual analytics.

Potential visualisations include:

* Books read over time.
* Pages read over time.
* Reading time over time.
* Genre distribution.
* Rating distribution.
* Book-length distribution.
* Top authors.
* Reading status.
* Session duration.
* Reading time by genre.

The dashboard should support relevant time-period filtering.

---

# 14. Power BI Integration

Power BI is an additional analytics and portfolio component rather than a dependency of the application.

---

## FR-047 — Analytics Data Export

The application shall provide structured data that can be consumed by Power BI.

Potential methods include:

* CSV export.
* SQLite access.
* PostgreSQL connection in later versions.
* Dedicated analytical datasets in future versions.

---

## FR-048 — Power BI Dashboard

A separate Power BI dashboard may demonstrate:

* Reading trends.
* Genre analysis.
* Book-length analysis.
* Rating analysis.
* Author analysis.
* Reading-time analysis.
* Yearly reading summaries.

The dashboard should use data generated from Book Brain rather than manually created sample data.

---

# 15. Recommendation System

The recommendation engine is a major long-term feature.

It shall be implemented independently of the conversational AI.

The recommendation system shall distinguish between **candidate generation**, **filtering**, **scoring**, and **ranking**.

---

## FR-049 — Personalised Recommendations

The recommendation engine shall eventually use relevant information such as:

* Reading history.
* Ratings.
* Genres.
* Authors.
* Book descriptions.
* Page count.
* Reading time.
* TBR status.
* Ownership.
* Current reading status.
* Stated preferences.

---

## FR-050 — Recommendation Context

The system shall support contextual recommendation requests.

Potential contexts include:

* Immediate reading.
* Beach reading.
* Holiday reading.
* Short reading session.
* Long reading session.
* Bedtime reading.
* Mood-based reading.
* Bookshop visit.
* General discovery.
* Surprise me.

The context model may evolve.

---

## FR-051 — Ownership-Aware Recommendations

The recommendation system shall distinguish between:

* Owned books.
* TBR books.
* Currently reading books.
* Completed books.
* Unowned books.

Ownership requirements expressed or implied by the user shall be treated as recommendation constraints.

---

## FR-052 — Immediate Reading Recommendations

When the user asks for something they can read immediately, the system shall prioritise books already available to them.

The system should:

1. Exclude books requiring acquisition.
2. Prefer suitable unread/TBR books.
3. Avoid completed books unless rereading is requested.
4. Consider currently reading books appropriately.
5. Consider historical preferences.
6. Consider context.
7. Consider relevant constraints such as length.

---

## FR-053 — Short-Book Recommendations

For requests such as:

> "Suggest something short for the beach."

the system should give greater weight to:

* Owned books.
* Unread/TBR books.
* Appropriate genres.
* Historical preferences.
* Shorter books.

A preference of approximately **100–150 pages** may be used as a recommendation weighting.

This shall not be an absolute requirement.

If suitable books are unavailable within that range, longer books may be considered.

---

## FR-054 — Bookshop Recommendations

When the user requests recommendations for purchasing, the system shall allow books outside the user's existing library.

The system should:

1. Analyse reading history.
2. Analyse highly rated books.
3. Identify preferred genres and authors.
4. Consider relevant TBR information.
5. Exclude books already owned.
6. Retrieve candidate books from external sources where available.
7. Rank candidates.
8. Explain recommendations.

---

## FR-055 — Candidate Filtering

Before ranking candidates, the system shall apply relevant constraints.

Potential constraints include:

* Ownership.
* TBR status.
* Reading status.
* Genre.
* Author.
* Page count.
* Rating history.
* User preferences.
* Context.
* Previous completion.
* Availability.

---

## FR-056 — Candidate Ranking

The recommendation engine shall assign relevance scores to eligible candidates.

Different contexts may use different weighting factors.

For example:

### Beach-read request

```text
Owned                 Very high
TBR                   High
Genre compatibility   High
Preference match      High
Book length           High
Previous ratings      Medium/High
```

### Bookshop request

```text
Not owned             Very high
Genre compatibility   High
Preference match      High
Similarity             High
Author preference     Medium/High
Book length           Context-dependent
```

The exact algorithm shall be developed and evaluated during the recommendation phase.

---

## FR-057 — Recommendation Availability

Recommendations shall distinguish between:

**Available now**

and:

**Requires acquisition**

An unavailable book shall not be presented as an immediately available reading option unless acquisition is acceptable in the request.

---

## FR-058 — Recommendation Explanation

The system should provide reasons for recommendations.

For example:

> "I'd pick this one because you already own it, it's on your TBR, and at 137 pages it's one of your shorter unread books. You've also rated several books in this genre highly."

---

## FR-059 — Recommendation Transparency

The recommendation engine shall expose sufficient scoring information for:

* Testing.
* Debugging.
* Evaluation.
* Algorithm improvement.

The technical scoring data may be simplified when presented to the user.

---

## FR-060 — Recommendation Exclusions

The system shall support explicit exclusions such as:

* Do not recommend books already read.
* No books over 300 pages.
* No romance.
* Exclude a specific author.
* Only recommend TBR books.
* Only recommend books physically owned.

Explicit exclusions shall take precedence over general preferences.

---

# 16. Recommendation Architecture

## FR-061 — Structured Recommendation Requests

The recommendation engine shall accept structured requests independent of natural-language input.

Example:

```text
context = beach_read
availability = owned
status = unread
preferred_pages = 100–150
genre_preference = high
```

---

## FR-062 — Independent Recommendation Engine

The recommendation engine shall be independently executable and testable without an LLM.

For example:

```text
Structured request
       ↓
Candidate query
       ↓
Filtering
       ↓
Scoring
       ↓
Ranking
       ↓
Ranked books
```

---

## FR-063 — Database Source of Truth

Recommendation decisions shall use authoritative application data for:

* Ownership.
* Reading status.
* TBR.
* Ratings.
* Reading history.
* Reading sessions.
* User notes.

---

# 17. Semantic Search and Embeddings

Semantic search is a future capability.

---

## FR-064 — Book Embeddings

A future version may generate embeddings from relevant book information such as:

* Descriptions.
* Genres.
* Themes.
* Other suitable metadata.

---

## FR-065 — Similarity Search

The system may use embeddings to identify semantically similar books.

Potential uses include:

* Finding books similar to highly rated books.
* Improving recommendations.
* Finding thematic similarities.
* Supporting AI librarian retrieval.

Potential technologies include:

* Local embedding models.
* PostgreSQL with `pgvector`.
* Chroma.
* Qdrant.

A separate vector database shall only be introduced where the requirements justify its complexity.

---

# 18. AI Librarian

The AI librarian is a future feature that will provide natural-language access to Book Brain functionality.

---

## FR-066 — Conversational Queries

The AI librarian shall eventually support requests such as:

* "What should I read next?"
* "What horror books do I own?"
* "Show me books under 300 pages."
* "Which books have I rated five stars?"
* "I want something dark and romantic."
* "I have a week off. What should I read?"
* "How much have I read this week?"
* "I'm going to the beach. Pick something short."
* "I'm going to the bookshop. What should I buy?"

---

## FR-067 — Natural-Language Intent

The AI shall interpret natural-language requests into structured application operations.

For example:

```text
"I'm going to the beach today."

→ context = beach
→ availability = owned
→ likely_status = unread
```

---

## FR-068 — Library-Aware AI

The AI librarian shall distinguish between:

* Owned books.
* TBR books.
* Currently reading books.
* Completed books.
* Unowned books.

The AI shall not claim that a book belongs to the user without authoritative application data.

---

## FR-069 — Statistics-Aware AI

The AI librarian should eventually use application statistics to answer questions such as:

* "What genre do I read most?"
* "Have I been reading longer books this year?"
* "Which authors do I rate highest?"
* "How much time did I spend reading last month?"

---

## FR-070 — Context-Aware AI

The AI shall use contextual information when interpreting recommendation requests.

For example:

```text
Beach today
→ immediate availability

Bookshop today
→ acquisition permitted
```

---

## FR-071 — Clarification

Where ambiguity materially affects the requested operation, the AI should ask a clarification question.

It should avoid unnecessary clarification when a reasonable interpretation exists.

---

## FR-072 — AI Provider Independence

The AI architecture should avoid permanent dependency on one model provider.

Potential approaches include:

* Local open-weight models.
* External APIs.
* Multiple interchangeable providers.

The final implementation shall consider:

* Capability.
* Cost.
* Privacy.
* Hardware requirements.
* Licensing.
* Maintainability.

---

# 19. AI Tool Architecture

The AI librarian may eventually access controlled application tools.

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

The AI shall only have access to functionality explicitly exposed as tools.

Tool arguments shall be validated by the application.

Destructive operations shall require appropriate safeguards.

---

# 20. Retrieval-Augmented Generation

RAG may be introduced where retrieval provides a meaningful benefit.

The intended pattern is:

```text
User question
      ↓
LLM
      ↓
Determine required information
      ↓
Application retrieval
      ↓
Database / semantic search
      ↓
Relevant information
      ↓
LLM
      ↓
Response
```

Structured questions should use direct application queries where appropriate.

For example:

> "How many books did I read this year?"

should preferably use a deterministic database/analytics query rather than semantic search.

---

# 21. Wearable Integration

Wearable integration is a future development area.

It shall not be required for the MVP.

---

## FR-073 — Wearable Reading Sessions

The application should investigate integration with wearable platforms such as Fitbit.

A potential workflow is:

```text
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

---

## FR-074 — Wearable Session Import

Where supported, Book Brain should be able to import:

* Start time.
* End time.
* Duration.
* Relevant activity information.
* Device/platform information where useful.

Duplicate sessions should be prevented.

---

## FR-075 — Unassigned Wearable Sessions

A wearable-generated session shall not require a book to be known at the time it begins.

Unassigned sessions shall be stored and may be associated with a book later.

---

## FR-076 — Current Book Association

Where the user has identified a current book, an imported session may be automatically associated with it.

The user shall be able to review and change the association.

The application shall not make an association where the available information is insufficient.

---

## FR-077 — Wearable Platform Independence

Core reading-session functionality shall not depend specifically on Fitbit.

Where practical, wearable integrations should use an abstraction that allows additional platforms to be added later.

Potential platforms include:

* Fitbit.
* Wear OS.
* Other supported wearable ecosystems.

---

## FR-078 — Wearable Feasibility Investigation

Before implementation, the project shall investigate:

* Developer APIs.
* Custom application support.
* Authentication.
* Synchronisation.
* Device compatibility.
* API limits.
* Privacy.
* Cost.
* Platform restrictions.

If direct integration is not feasible, alternative approaches shall be considered.

---

# 22. Web Application

The web application shall be introduced after the core application architecture is sufficiently stable.

---

## FR-079 — Web Interface

A future web interface shall provide access to appropriate Book Brain functionality.

Potential features include:

* Library view.
* Book details.
* Search.
* Filtering.
* Book management.
* Reading management.
* Session management.
* Statistics.
* Recommendations.
* AI librarian.

---

## FR-080 — Backend API

A future backend API shall expose controlled application functionality.

Potential API areas include:

```text
/books
/authors
/genres
/library
/reading
/sessions
/statistics
/recommendations
/ai
```

Business logic shall remain in application services rather than being duplicated inside API endpoints.

---

# 23. Mobile Application

---

## FR-081 — Mobile Application

A future mobile application shall provide access to the core Book Brain functionality.

Potential functionality includes:

* Library management.
* Book search.
* ISBN scanning.
* Reading status.
* Ratings.
* Reading sessions.
* Statistics.
* Recommendations.
* AI librarian.

---

## FR-082 — Shared Backend

The mobile application shall communicate with the same backend and application services used by the web application.

Core business logic shall not be duplicated independently within the mobile application.

---

# 24. Data Requirements

The data model shall support the distinction between:

```text
Book / Work
    ↓
Edition
    ↓
Library Entry
    ↓
Reading Record
    ↓
Reading Sessions
```

The final database structure shall be documented separately in:

`docs/database-design.md`

Expected entities include:

* Book/work.
* Edition.
* Author.
* Book-author relationship.
* Genre.
* Book-genre relationship.
* Library entry.
* Reading record.
* Reading session.
* Format.
* Data source/provenance where required.

The exact table structure shall be determined during database design.

---

## DR-001 — Multiple Authors

A book shall support multiple authors where appropriate.

---

## DR-002 — Multiple Genres

A book shall support multiple genres/categories.

---

## DR-003 — Multiple Editions

The data model shall support multiple editions of the same book/work.

---

## DR-004 — Multiple Formats

The data model shall support different formats/editions.

---

## DR-005 — Reading Sessions

Reading sessions shall exist independently from book associations.

---

## DR-006 — Historical Reading

The data model should preserve historical reading information even when a book is removed from the user's current library.

---

## DR-007 — Incomplete Metadata

The application shall support books with incomplete metadata.

For example, missing:

* Page count.
* Publisher.
* ISBN.
* Cover.
* Publication date.

Missing information shall not make the book unusable.

---

## DR-008 — Export

The user shall be able to export their personal data in a practical machine-readable format.

Potential formats include:

* CSV.
* JSON.
* SQLite database copy.

The final export format shall be defined during implementation.

---

# 25. Data Quality Requirements

## NFR-001 — Data Validation

The system shall validate user-provided and externally retrieved data.

Examples include:

* ISBN format.
* Rating range.
* Dates.
* Page count.
* Required fields.
* Reading-session timestamps.

---

## NFR-002 — Data Consistency

The application shall maintain referential and logical consistency between:

* Books.
* Editions.
* Authors.
* Genres.
* Library entries.
* Reading records.
* Reading sessions.

---

## NFR-003 — Missing Data

Statistics shall account for missing values rather than treating missing data as zero or otherwise producing misleading results.

---

## NFR-004 — Data Provenance

Where practical, the system should distinguish between data:

* Entered by the user.
* Imported from an external API.
* Imported from a wearable.
* Calculated by the application.
* Generated or interpreted by AI.

---

# 26. Non-Functional Requirements

## NFR-005 — Usability

The application should minimise unnecessary manual data entry.

---

## NFR-006 — Reliability

Invalid input and external service failures shall not cause data corruption.

---

## NFR-007 — Maintainability

Code shall be organised into logical components with clearly defined responsibilities.

---

## NFR-008 — Testability

Core functionality shall have automated tests.

The recommendation engine shall have tests covering:

* Different contexts.
* Ownership constraints.
* Explicit exclusions.
* Page-length constraints.
* Ranking behaviour.

External integrations should use appropriate integration tests and mocks where required.

---

## NFR-009 — Security

When remote access or user accounts are introduced:

* Authentication information shall be protected.
* Secrets shall not be committed to source control.
* API credentials shall be stored securely.
* User data shall not be publicly exposed.
* Access shall be appropriately authorised.
* Communication shall use appropriate encryption.

---

## NFR-010 — Portability

The initial application should run locally on common operating systems supported by Python and SQLite.

---

## NFR-011 — Cost

The MVP should use free software and services wherever practical.

Paid services shall not be required for core MVP functionality.

Future costs shall be evaluated before introducing paid dependencies.

---

## NFR-012 — Scalability

SQLite shall be used initially.

The architecture should permit migration to PostgreSQL if requirements such as:

* Multiple users.
* Remote access.
* Increased concurrency.
* Cloud deployment.
* Advanced database capabilities.

justify the additional complexity.

---

## NFR-013 — Privacy

Personal library information, reading history, ratings, notes, and preferences shall be private by default.

Future AI and wearable functionality shall consider whether personal data is processed locally or transmitted to external services.

---

## NFR-014 — External Service Independence

The core application shall remain functional when optional external services are unavailable.

---

# 27. Analytics Architecture Principle

Operational data and analytics/presentation concerns should be separated where practical.

The core database remains the authoritative source.

Analytics may be generated through:

```text
Database
    ↓
SQL queries
    ↓
Application statistics
    ↓
Python/Pandas
    ↓
Power BI
```

The application shall not require Power BI to calculate core statistics.

Reading-session data shall be structured so that it can be analysed alongside:

* Books.
* Editions.
* Genres.
* Authors.
* Formats.
* Ratings.
* Reading history.
* Reading status.

Recommendation information should eventually support evaluation of recommendation quality.

---

# 28. Initial Technology Direction

The following technologies represent the current direction rather than permanent commitments.

## Initial Development

* Python.
* SQLite.
* SQL.
* Git.
* GitHub.
* Python testing framework.

## Data Analysis

* Python.
* Pandas.
* SQL.
* Matplotlib where appropriate.
* Power BI.

## Future Backend

* FastAPI.
* PostgreSQL.

## Future Web Frontend

Potential technologies include:

* HTML.
* CSS.
* JavaScript.
* React.
* TypeScript.

The final frontend technology shall be selected when implementation begins.

## Future Mobile Application

Potential technology:

* React Native.

The final framework shall be selected when mobile development begins.

## Future Wearable Integration

Potential integrations include:

* Fitbit.
* Wear OS.
* Other supported wearable platforms.

The implementation shall depend on platform capabilities and restrictions.

## Future AI

Potential approaches include:

* Rule-based recommendation.
* Content-based filtering.
* Collaborative approaches where sufficient data exists.
* Embeddings.
* Semantic search.
* Local open-weight language models.
* External AI APIs.
* Retrieval-Augmented Generation.
* Tool calling.
* Hybrid recommendation systems.

AI shall be introduced only after the underlying library, database, analytics, and recommendation functionality is sufficiently mature.

---

# 29. MVP Acceptance Criteria

The MVP shall be considered complete when the user can:

1. Create the SQLite database.
2. Create and store a book/work.
3. Create and store an edition where applicable.
4. Store authors.
5. Store genres.
6. Add a book/edition to their library.
7. Retrieve library records.
8. Search for books.
9. Update book and library information.
10. Remove a book from the library.
11. Assign a reading status.
12. Record a rating.
13. Record reading dates.
14. Add reading notes.
15. Start a reading session manually.
16. End a reading session manually.
17. Store reading-session duration.
18. Associate a reading session with a book.
19. Leave a reading session unassigned.
20. Produce basic reading statistics.
21. Export personal library/reading data.
22. Run automated tests against core functionality.

The MVP shall **not** require:

* Graphical frontend.
* FastAPI.
* AI.
* Recommendation engine.
* Semantic search.
* Vector database.
* Barcode scanning.
* External book APIs.
* Wearable integration.
* User accounts.
* Cloud hosting.
* Mobile application.
* Power BI integration.

---

# 30. Future Development Milestones

The exact roadmap shall be maintained separately in:

`docs/roadmap.md`

Potential development phases include:

## Phase 1 — Project Foundation

* Repository structure.
* Documentation.
* Development environment.
* Database design.
* Testing structure.

## Phase 2 — Core Library

* SQLite database.
* Book/work records.
* Editions.
* Authors.
* Genres.
* Library entries.
* CRUD operations.
* Search.
* Reading status.
* Ratings.
* Notes.
* Tests.

## Phase 3 — Reading Tracking

* Reading records.
* Reading dates.
* Reading sessions.
* Reading-time calculations.
* Basic statistics.

## Phase 4 — External Metadata

* ISBN lookup.
* Book API integration.
* Metadata import.
* Data provenance.
* Error handling.

## Phase 5 — Analytics

* Analytical SQL.
* Python/Pandas analysis.
* Reading trends.
* Power BI dashboard.

## Phase 6 — Recommendation Engine

* Candidate generation.
* Filtering.
* Scoring.
* Ranking.
* Context-aware recommendations.
* Ownership-aware recommendations.
* Recommendation exclusions.
* Recommendation evaluation.

## Phase 7 — Semantic Search

* Embedding generation.
* Similarity search.
* Evaluation of vector-storage options.
* Integration with recommendations where useful.

## Phase 8 — AI Librarian

* Natural-language interpretation.
* Structured outputs.
* Database queries.
* Recommendation integration.
* Statistics queries.
* Tool calling.
* RAG where appropriate.
* AI provider abstraction.

## Phase 9 — Web Application

* FastAPI backend.
* Frontend.
* Authentication where required.
* Library interface.
* Analytics dashboard.
* Recommendation interface.
* AI interface.

## Phase 10 — Mobile Application

* Mobile interface.
* API integration.
* Barcode scanning.
* Reading-session controls.
* AI librarian.

## Phase 11 — Wearable Integration

* Investigate Fitbit capabilities.
* Prototype reading-session integration.
* Synchronise sessions.
* Associate sessions with current books.
* Investigate other wearable platforms.

## Phase 12 — Deployment and Scaling

* Remote deployment.
* PostgreSQL migration where justified.
* Authentication.
* Secure API access.
* Monitoring.
* Backup strategy.

---

# 31. Long-Term Vision

The long-term goal is to develop Book Brain into a complete personal reading platform.

A mature version should allow a user to:

```text
Scan a book
     ↓
Identify the ISBN
     ↓
Retrieve metadata
     ↓
Confirm/edit information
     ↓
Catalogue the book
     ↓
Add it to the library/TBR
     ↓
Select it as currently reading
     ↓
Start a reading session
     ↓
Track reading time
     ↓
Finish the book
     ↓
Rate and review it
     ↓
Analyse reading habits
     ↓
Receive personalised recommendations
     ↓
Discuss the library with an AI librarian
```

---

## 31.1 Immediate Reading

For a request such as:

> "I'm going to the beach. What should I read today?"

Book Brain should understand that the user wants something immediately available.

It should prioritise:

1. Books the user owns.
2. Books that have not been completed.
3. Suitable TBR books.
4. Books matching preferences.
5. Books appropriate to the context.
6. Shorter books where appropriate.

A preference around **100–150 pages** may be used as one ranking factor.

The system should not recommend a book requiring purchase unless the user indicates that acquisition is acceptable.

---

## 31.2 Bookshop Discovery

For a request such as:

> "I'm on my way to the bookshop. Have you got any must-buys for me?"

Book Brain should understand that acquisition is possible.

It should:

1. Analyse reading history.
2. Identify preferred genres.
3. Identify preferred authors.
4. Analyse highly rated books.
5. Consider relevant TBR information.
6. Exclude books already owned.
7. Retrieve appropriate external candidates.
8. Rank potential purchases.
9. Explain the reasons for the recommendations.

---

## 31.3 Reading Statistics

The user should eventually be able to ask:

> "What genre do I read most?"

> "How much time have I spent reading this month?"

> "Do I tend to finish shorter books?"

> "Which authors do I rate highest?"

> "Have I been reading more horror this year?"

The system should answer using authoritative application data rather than relying on the LLM's internal knowledge.

---

## 31.4 Wearable Reading

Where technically supported, the user should eventually be able to:

```text
Start Reading
      ↓
Read
      ↓
Stop Reading
```

using a supported wearable or companion device.

Book Brain would record the session and associate it with the current book where possible.

---

# 32. Project Quality and Portfolio Objectives

Book Brain is intended to demonstrate practical software engineering rather than simply function as a collection of technologies.

The project should demonstrate:

### Software Engineering

* Modular architecture.
* Separation of responsibilities.
* Business logic isolation.
* Error handling.
* Testing.
* Version control.
* Documentation.

### Database Engineering

* Relational data modelling.
* Primary and foreign keys.
* Constraints.
* Normalisation.
* Referential integrity.
* SQL queries.
* Database migrations where required.

### Data Analysis

* Analytical SQL.
* Pandas.
* Data transformation.
* Statistical summaries.
* Power BI.
* Visualisation.

### Recommendation Systems

* Candidate generation.
* Filtering.
* Ranking.
* Explainability.
* Evaluation.

### API Integration

* REST APIs.
* External metadata.
* Error handling.
* Authentication where required.
* Rate-limit handling.

### Artificial Intelligence

* Structured outputs.
* Embeddings.
* Semantic search.
* LLM integration.
* Tool calling.
* RAG.
* AI provider abstraction.

### Application Development

* Backend API.
* Web interface.
* Mobile interface.
* Barcode scanning.
* Device integration.

### Security and Privacy

* Secure secrets.
* Authentication.
* Authorisation.
* Data protection.
* Privacy-aware AI integrations.

The project should prioritise **working, well-designed functionality over the number of technologies used**.

---

# 33. Relationship to Other Documentation

This document describes **what Book Brain should do**.

Other project documentation provides complementary information:

| Document             | Purpose                                        |
| -------------------- | ---------------------------------------------- |
| `requirements.md`    | What Book Brain should do                      |
| `roadmap.md`         | When functionality is planned                  |
| `architecture.md`    | How the system is structured                   |
| `database-design.md` | How application data is stored                 |
| `development-log.md` | What has actually been implemented and learned |

These documents should remain consistent with one another.

When a requirement changes, the relevant architecture, database design, roadmap, and development documentation should be reviewed.

Major architectural or technical decisions should be recorded in the development documentation.

---

# 34. Requirements Status

Requirements in this document are not all current implementation requirements.

They fall into three broad categories:

### Current

Functionality required for the current development phase and MVP.

### Planned

Functionality intended for a later development phase.

### Exploratory

Potential functionality that requires technical investigation before being committed.

Examples of exploratory functionality include:

* Wearable integration.
* Specific AI providers.
* Specific vector databases.
* Specific frontend frameworks.
* Multi-user deployment.

This distinction is important because the long-term vision should not force premature implementation complexity into the current application.

The current implementation shall remain focused on building a reliable foundation for the later features.
