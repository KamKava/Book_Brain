# Book Brain — Development Log

**Project status:** Initial development
**Version:** 0.1
**Last updated:** August 2026

---

# 1. Purpose

This document records the development of Book Brain throughout the project.

Unlike the requirements and database design documents, which describe what the application is intended to do and how its data should be structured, this document records the actual development process.

The development log shall document:

* Major development activities.
* Important technical decisions.
* Changes to the project design.
* Problems encountered.
* Solutions implemented.
* Testing and debugging.
* Technologies and tools used.
* Lessons learned.
* Changes in scope.
* Decisions that affect future development.
* Significant deviations from the original requirements or design.

The purpose is both to provide a historical record of the project and to demonstrate the reasoning behind important engineering decisions.

---

# 2. Development Log Principles

## 2.1 Record Decisions, Not Every Keystroke

The development log should not become a diary of every small coding activity.

It should focus on decisions and events that are useful for understanding how the project developed.

For example, useful entries include:

> Decided to separate `Book` from `LibraryEntry` because bibliographic information and ownership information represent different concepts.

Less useful entries include:

> Created a Python file called `database.py`.

Unless the latter decision had an important technical consequence, it does not need to be recorded.

---

## 2.2 Record the Reasoning

Important decisions should explain **why** a particular approach was chosen.

Where appropriate, entries should document:

* Options considered.
* Advantages and disadvantages.
* Constraints.
* Final decision.
* Consequences of the decision.

---

## 2.3 Record Changes to Previous Decisions

Early decisions are not necessarily permanent.

If a later discovery requires the design to change, the development log should record:

1. What the original decision was.
2. What changed.
3. Why it changed.
4. What parts of the project were affected.

This is particularly important for:

* Database design.
* Technology choices.
* API selection.
* Recommendation architecture.
* AI architecture.
* Application architecture.

---

## 2.4 Link Development Decisions to Project Documentation

Where appropriate, development-log entries should refer to related documentation.

For example:

* `docs/requirements.md`
* `docs/database-design.md`
* `docs/architecture.md`
* `docs/roadmap.md`

If an implementation decision changes one of these documents, the relevant document should also be updated.

---

# 3. Project Starting Point

Book Brain began as an idea for a personal application to manage and analyse a home book collection.

The initial concept was to create an application capable of:

* Cataloguing books owned by the user.
* Managing a TBR collection.
* Tracking currently-read books.
* Recording completed books.
* Recording ratings and reading dates.
* Analysing reading habits.
* Eventually providing personalised recommendations.
* Eventually providing an AI librarian.
* Potentially tracking reading sessions through wearable devices.

The project was deliberately designed to start small and become progressively more sophisticated.

The initial implementation therefore focuses on a local Python and SQLite application rather than attempting to build the complete system immediately.

---

# 4. Initial Technology Decisions

## 4.1 Python

Python was selected as the initial programming language.

Reasons include:

* Existing familiarity.
* Strong support for data processing.
* SQLite integration.
* Availability of testing frameworks.
* Strong ecosystem for APIs.
* Strong ecosystem for AI and machine learning.
* Compatibility with future recommendation-system development.
* Compatibility with future analytics work.

Python also allows the initial application to remain relatively simple while providing a path towards more sophisticated functionality.

---

## 4.2 SQLite

SQLite was selected as the initial database.

Reasons include:

* No database server is required.
* Easy local development.
* Minimal setup.
* Suitable for a single-user MVP.
* Full SQL support.
* Easy backup and portability.
* Useful for learning relational database design.

SQLite is not intended to be a permanent limitation.

The database design should allow a future migration to PostgreSQL if the application eventually requires:

* Multiple users.
* Remote access.
* Increased concurrency.
* Server-side deployment.
* More advanced database functionality.

---

## 4.3 Git and GitHub

Git will be used for source control.

GitHub will be used to:

* Store the project repository.
* Track development history.
* Document the project.
* Demonstrate development practices.
* Potentially provide portfolio visibility.

Changes should be committed in logical units rather than using excessively large commits containing unrelated changes.

---

# 5. Initial Project Structure

The project documentation is expected to use a structure similar to:

```text
Book Brain/
│
├── docs/
│   ├── requirements.md
│   ├── roadmap.md
│   ├── architecture.md
│   ├── database-design.md
│   └── development-log.md
│
├── src/
│
├── tests/
│
├── README.md
├── .gitignore
└── LICENSE
```

The exact source-code structure will evolve as implementation progresses.

Documentation structure may also be updated when new architectural areas become significant.

---

# 6. Initial Requirements Decisions

The initial requirements were intentionally expanded beyond a simple book catalogue.

The project now treats Book Brain as a long-term application with several distinct development stages:

1. Core library management.
2. Reading tracking.
3. Reading-session tracking.
4. External metadata.
5. Analytics.
6. Recommendation engine.
7. AI librarian.
8. Web application.
9. Mobile application.
10. Wearable integration.

Not all of these features belong in the MVP.

The MVP will remain deliberately small so that the core data model and application behaviour can be implemented and tested before introducing external dependencies.

---

# 7. Database Design Decisions

## 7.1 Separate Book from LibraryEntry

One of the key database design decisions was to separate bibliographic information from the user's relationship with a book.

For example:

```text
Book
    Dracula
    Bram Stoker
    336 pages

LibraryEntry
    Owned
    Paperback
    TBR
    Added 2026-08-01
```

This allows Book Brain to distinguish the book itself from information such as:

* Ownership.
* Format.
* Reading status.
* Date added.

This separation will also support future recommendations involving books that the user does not own.

---

## 7.2 Separate ReadingRecord from ReadingSession

Another important decision was to distinguish between:

**ReadingRecord**

The overall event of reading a book, including:

* Start date.
* Finish date.
* Rating.
* Review.

and:

**ReadingSession**

An individual period spent reading, including:

* Start time.
* End time.
* Duration.

This allows Book Brain to represent a book being read over multiple sessions.

It also allows reading sessions to exist independently before being associated with a book.

This is important for future wearable integration.

---

## 7.3 Support Rereading

Reading history will not be limited to one record per book.

A user may read the same book multiple times.

Therefore, reading history is represented through separate `ReadingRecord` entries.

This allows future analysis of:

* Rereading frequency.
* Changes in ratings.
* Changes in reading speed.
* Reading behaviour over time.

---

## 7.4 Support Multiple Formats

The design separates `Book` from `Format` and `LibraryEntry`.

This allows the same underlying book to be represented in multiple formats.

For example:

```text
Dracula
│
├── Paperback
├── E-book
└── Audiobook
```

The exact rules for duplicate library entries will be confirmed during implementation.

---

## 7.5 Series Support

Series were included in the database design because they provide useful information for future recommendations.

The application should eventually be able to answer questions such as:

* Which series do I own?
* Which series have I started?
* Which books in a series have I read?
* Which books am I missing?
* What should I buy to continue a series?

Series support is therefore part of the data model even though advanced series functionality is not required for the MVP.

---

# 8. Reading Session Decision

Reading sessions were added as a first-class concept rather than storing only a total reading-time value.

This decision was made because storing individual sessions provides significantly greater analytical flexibility.

For example, individual sessions can later be used to calculate:

* Total reading time.
* Average session duration.
* Longest session.
* Reading time by day.
* Reading time by week.
* Reading time by month.
* Reading time by book.
* Reading time by genre.
* Reading time by format.

Storing only an aggregated total would make many of these analyses impossible or unreliable.

---

# 9. Unassigned Reading Sessions

The database will allow a reading session to exist without an associated book.

For example:

```text
Start: 14:10
End: 14:52
Duration: 42 minutes
Book: NULL
```

This was deliberately chosen because future reading sessions may be started through:

* Mobile devices.
* Wearables.
* Quick-access controls.

The user may not always identify the book at the exact moment a session begins.

The session can therefore be associated with a book later.

---

# 10. Context-Aware Recommendation Decision

A major change in the project scope was the decision to make recommendations context-aware.

The recommendation system should not simply ask:

> "What books does the user like?"

It should also ask:

> "What is the user trying to do right now?"

For example:

```text
Beach today
    ↓
Need something immediately available
    ↓
Prefer owned books
    ↓
Prefer unread/TBR
    ↓
Prefer suitable genres
    ↓
Prefer shorter books
```

Whereas:

```text
Going to the bookshop
    ↓
Acquisition is possible
    ↓
Exclude books already owned
    ↓
Analyse preferences
    ↓
Search external catalogue
    ↓
Rank potential purchases
```

This distinction became an important part of the requirements and recommendation architecture.

---

# 11. Ownership-Aware Recommendations

The recommendation system will distinguish between:

* Owned books.
* TBR books.
* Currently reading.
* Completed books.
* Books not owned.

This prevents a recommendation such as:

> "Take this book to the beach."

from suggesting a book that the user does not own.

Conversely, a bookshop recommendation should be allowed to recommend books that the user does not own.

Ownership therefore becomes an important recommendation attribute rather than simply a library-management detail.

---

# 12. Short-Book Recommendation Decision

A preference for shorter books was identified as particularly useful for certain contexts.

For example, a beach-read request may favour books around:

**100–150 pages**

where suitable candidates exist.

The page range is not intended to become a rigid rule.

Instead, it should act as a recommendation weighting.

If there are no suitable books around that length, the recommendation engine should be able to consider progressively longer books.

This prevents an arbitrary page threshold from producing poor recommendations.

---

# 13. Recommendation Architecture Decision

The recommendation system should not rely entirely on an LLM.

The intended architecture is:

```text
User request
      ↓
Intent / context extraction
      ↓
Structured recommendation constraints
      ↓
Database candidate generation
      ↓
Candidate filtering
      ↓
Candidate ranking
      ↓
Recommendation results
      ↓
AI explanation
      ↓
User
```

The structured recommendation engine should remain independently testable.

For example, it should eventually be possible to provide:

```text
context = beach_read
ownership = owned
status = unread
preferred_pages = 100–150
genre_preference = high
```

and receive a ranked list without requiring an LLM.

The AI can then explain those results naturally.

---

# 14. AI Librarian Architecture Decision

The AI librarian will be treated as a conversational layer rather than the database itself.

The intended architecture is:

```text
User
 ↓
AI / LLM
 ↓
Application services
 ↓
Database
 ↓
Structured results
 ↓
AI / LLM
 ↓
User
```

The AI should not be allowed to invent information about the user's library.

For example, if the database does not contain a book as owned, the AI should not claim that the user owns it.

This separation improves:

* Reliability.
* Testability.
* Transparency.
* Data integrity.

---

# 15. Wearable Integration Decision

Wearable integration is currently considered a future feature.

The initial concept is:

```text
Start Reading
      ↓
Reading session begins
      ↓
User reads
      ↓
Stop Reading
      ↓
Session synchronised
      ↓
Book Brain
```

The session may be automatically associated with the user's currently selected book where sufficient information exists.

If no book can safely be identified, the session should remain unassigned.

Direct Fitbit integration has not yet been confirmed as technically feasible.

The project will investigate:

* Available APIs.
* Device capabilities.
* Authentication.
* Synchronisation.
* Platform restrictions.
* Privacy.
* Costs.

No implementation decision will be made until the technical feasibility is understood.

---

# 16. Analytics Decision

Analytics will be based primarily on structured underlying data rather than storing large numbers of pre-calculated statistics.

For example:

```text
ReadingRecord
ReadingSession
Book
Genre
Author
```

can be combined to calculate reading statistics when required.

This avoids storing values such as:

```text
total_books_read = 137
```

as permanent source-of-truth data when the value can be derived from the underlying records.

Pre-calculated or cached statistics may be introduced later if performance requirements justify them.

---

# 17. Power BI Decision

Power BI is considered an analytics and portfolio component rather than a core application dependency.

Book Brain should continue to function without Power BI.

Potential data access methods include:

* CSV export.
* SQLite data extraction.
* Analytical views.
* Future PostgreSQL connectivity.

The application database remains the source of truth.

---

# 18. External Book Metadata Decision

External book APIs will be introduced after the core database and CRUD functionality are stable.

The application should support manual book entry even when external APIs are unavailable.

Potential metadata sources will be evaluated based on:

* Data quality.
* ISBN coverage.
* Usage limits.
* Reliability.
* Licensing.
* Cost.
* Privacy.

The final API choice will be documented when implementation begins.

---

# 19. Data Provenance Decision

The database design recognises that information may originate from different sources.

Potential sources include:

```text
Manual user input
External book API
Wearable/device
Application calculation
AI-generated information
```

Where practical, the source of important information should be distinguishable.

This is particularly useful when external metadata is incomplete or incorrect.

The exact provenance implementation will be determined during schema implementation.

---

# 20. Testing Strategy

Testing will be introduced alongside development rather than being left until the end.

Core functionality should have automated tests covering:

* Database creation.
* Book creation.
* Book retrieval.
* Book updates.
* Book deletion.
* ISBN handling.
* Author relationships.
* Genre relationships.
* Series relationships.
* Library entries.
* Reading records.
* Reading sessions.
* Validation.
* Search.
* Statistics.

The recommendation engine should eventually have tests covering different contexts and constraints.

External integrations should use mocked responses where appropriate so that core tests do not depend on live external services.

---

# 21. Current Development Stage

At the current stage, the project has completed the initial conceptual requirements and database design.

The current documentation defines:

* Project goals.
* MVP scope.
* Core requirements.
* Future functionality.
* Database entities.
* Relationships.
* Recommendation principles.
* AI architecture principles.
* Wearable integration concepts.
* Future technology direction.

The next implementation stage is to convert the database design into an actual SQLite schema.

---

# 22. Next Development Steps

The immediate development sequence is expected to be:

1. Review requirements against database design.
2. Finalise the table-by-table database specification.
3. Define column types and constraints.
4. Define foreign-key behaviour.
5. Define indexes.
6. Create SQLite schema.
7. Create initial reference data.
8. Test database creation.
9. Implement database access layer.
10. Implement basic CRUD operations.
11. Add automated tests.
12. Record implementation decisions in this development log.

---

# 23. Development Entry Template

Future significant development activities should be recorded using the following structure:

## [DATE] — [TITLE]

### Context

What was being worked on and why?

### Problem / Decision

What problem was encountered or what decision needed to be made?

### Options Considered

What approaches were considered?

### Decision

What approach was selected?

### Reasoning

Why was this approach selected?

### Implementation

What was changed or implemented?

### Testing

How was the change tested?

### Result

What was the outcome?

### Documentation Updated

Which project documents were affected?

### Follow-Up

Are there any future tasks resulting from this decision?

---

# 24. Development Entries

Development entries will be added below as the project progresses.

---

## [August 2026] — Project Requirements Review

### Context

The initial requirements document was reviewed before beginning database implementation.

### Problem / Decision

The original project concept contained several future features that could affect the database design, including:

* Reading sessions.
* Context-aware recommendations.
* Series-aware recommendations.
* AI librarian functionality.
* Wearable integration.
* Power BI analytics.

The database needed to accommodate these future requirements without unnecessarily implementing them in the MVP.

### Decision

The database was designed around a normalised relational structure with the following major concepts:

```text
Book
Author
Genre
Series
LibraryEntry
Format
ReadingRecord
ReadingSession
Note
```

Relationship tables were introduced where many-to-many relationships were required.

### Result

The database design can support the MVP while providing a foundation for later recommendation, analytics, AI, and wearable functionality.

### Documentation Updated

* `docs/requirements.md`
* `docs/database-design.md`
* `docs/development-log.md`

### Follow-Up

Convert the conceptual design into an actual SQLite schema.

---

## [August 2026] — Separation of Book and LibraryEntry

### Context

The database design needed to distinguish bibliographic information from information specific to the user's collection.

### Decision

`Book` and `LibraryEntry` were separated.

### Reasoning

A book's title, author, page count and publication information describe the book itself.

Ownership, format, reading status and date added describe the user's relationship with that book.

Separating these concepts also supports future recommendations for books that the user does not own.

### Result

The database can distinguish:

```text
Book
    Dracula

LibraryEntry
    Owned
    Paperback
    TBR
```

### Documentation Updated

* `docs/database-design.md`
* `docs/requirements.md`

---

## [August 2026] — Reading Sessions Added

### Context

The project requirements were expanded to include tracking time spent reading.

### Decision

Reading sessions were introduced as a separate entity.

### Reasoning

Individual sessions provide more useful information than storing only an aggregate reading-time value.

They allow future analysis of:

* Total reading time.
* Session duration.
* Reading time over time.
* Reading time by book.
* Reading time by genre.
* Reading behaviour.

### Result

`ReadingSession` is separate from `ReadingRecord`.

A session can also remain unassigned to a book.

### Documentation Updated

* `docs/requirements.md`
* `docs/database-design.md`

---

## [August 2026] — Context-Aware Recommendations

### Context

The recommendation system was expanded from simple personalised recommendations to context-aware recommendations.

### Decision

Recommendation requests should be interpreted according to the user's immediate goal.

### Example

A beach-read request should prioritise:

```text
Owned
+
Unread/TBR
+
Suitable genre
+
Shorter books
```

A bookshop request should instead prioritise:

```text
Not owned
+
Strong preference match
+
Suitable external candidates
```

### Result

Ownership is now a significant recommendation attribute.

The recommendation engine will eventually use structured constraints before ranking candidates.

### Documentation Updated

* `docs/requirements.md`
* `docs/database-design.md`

---

## [August 2026] — AI Separated from Recommendation Logic

### Context

The project will eventually include a conversational AI librarian.

### Decision

The LLM should act primarily as a conversational interface and should not independently determine the user's library contents.

### Architecture

```text
User
 ↓
LLM
 ↓
Application services
 ↓
Database / Recommendation Engine
 ↓
Structured results
 ↓
LLM
 ↓
User
```

### Reasoning

This provides better:

* Data accuracy.
* Testability.
* Control.
* Explainability.
* Separation of responsibilities.

The recommendation engine can therefore be tested independently of the AI model.

### Documentation Updated

* `docs/requirements.md`
* `docs/database-design.md`
* `docs/development-log.md`

---

# 25. Lessons Learned

This section will be updated throughout development.

Potential topics include:

* Database normalisation.
* SQL design.
* Foreign-key behaviour.
* API integration.
* Testing.
* Recommendation-system design.
* AI integration.
* Data modelling.
* Analytics architecture.
* Software architecture.
* Privacy and security.
* Deployment.

The purpose is to capture lessons that may be useful when developing future applications.

---

# 26. Known Open Questions

The following decisions remain intentionally open:

### Database

* Exact SQLite column definitions.
* Foreign-key deletion behaviour.
* Whether multiple `LibraryEntry` records for the same format should be permitted.
* Final rating precision.
* Provenance implementation.
* Exact constraints and indexes.

### External metadata

* Which book API will be used.
* How conflicting metadata sources will be handled.
* How cover images will be stored or referenced.

### Recommendations

* Final scoring algorithm.
* Exact weighting of recommendation factors.
* Content-based versus collaborative approaches.
* Embedding requirements.
* Recommendation evaluation methodology.

### AI

* AI provider.
* Local versus external model.
* Tool/function architecture.
* RAG implementation.
* Cost controls.
* Privacy architecture.

### Wearables

* Fitbit API capabilities.
* Direct wearable integration feasibility.
* Mobile intermediary requirements.
* Supported platforms.

### Application architecture

* Final web framework.
* Authentication approach.
* API architecture.
* Deployment platform.
* PostgreSQL migration requirements.

These questions should be resolved as the relevant development phases are reached rather than prematurely adding unnecessary complexity to the MVP.

---

# 27. Document Maintenance

This document should be updated whenever a significant development decision is made.

It should not be updated for every minor code change.

The development log should remain a concise historical record of the project's evolution.

Major changes to requirements or architecture should also be reflected in the relevant project documentation.

The development log therefore complements, rather than replaces:

* `requirements.md`
* `database-design.md`
* `architecture.md`
* `roadmap.md`

Together, these documents should provide a clear record of:

```text
Requirements
     ↓
Architecture
     ↓
Database Design
     ↓
Development Decisions
     ↓
Implementation
     ↓
Testing
     ↓
Future Development
```
