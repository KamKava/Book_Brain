# Book Brain — Requirements

**Status:** Active development  
**Version:** 0.1  
**Last updated:** August 2026

---

# 1. Purpose

Book Brain is a personal book-library and reading-management application.

Its core purpose is to manage the user's books and reading history, provide useful analysis, and eventually support personalised, context-aware recommendations and an AI librarian.

Development will be incremental. The core application must remain useful without AI or external services.

---

# 2. MVP

The MVP focuses on reliable local management of books, library records and reading data.

## 2.1 Library

The user should be able to:

- Add, view, edit and delete books.
- Record title, author, ISBN and relevant bibliographic information.
- Record genres and series.
- Record ownership.
- Record format.
- Record source and price where applicable.
- Search and filter the library.

## 2.2 Reading

The user should be able to:

- Track books as TBR, currently reading or read.
- Record reading history.
- Record multiple reading events for the same book.
- Record reading and completion dates.
- Record ratings.
- Add notes.
- Start and stop reading sessions.
- Associate reading sessions with books.
- Leave sessions unassigned when the book is unknown.

## 2.3 Basic Analysis

Book Brain should be able to derive basic statistics from stored data, including:

- Books read.
- Pages read.
- Reading time.
- Reading activity over time.
- Ratings.
- Basic library composition.

The core application must not depend on Power BI or AI.

---

# 3. Book and Library Information

Book Brain must distinguish between information about a book and information about the user's relationship with that book.

### Book information

May include:

- Title
- Author
- ISBN
- Page count
- Publication information
- Publisher
- Series
- Genre
- Edition information

### Library information

May include:

- Ownership
- Format
- Source
- Price
- Date added
- Reading status

The user's library data is authoritative.

External sources may provide metadata, but must not silently overwrite user data.

---

# 4. Reading Sessions

Reading sessions represent individual periods of reading.

The system should support sessions from different sources, including:

- Manual
- Web
- Mobile
- Wearable
- Imported

The MVP only requires manual session tracking.

Sessions may be associated with a book or remain unassigned.

The stored session data should support analysis of reading duration and activity.

---

# 5. Recommendations

The future recommendation system should:

- Use the user's library and reading history where appropriate.
- Support books owned by the user and books discovered externally.
- Consider the user's current context.
- Apply explicit constraints and exclusions.
- Score and rank candidates.
- Provide structured reasons for recommendations.
- Operate independently of an LLM.

Potential recommendation factors include:

- Ownership
- Reading status
- Genre
- Author
- Series
- Book length
- Ratings
- Reading history
- User preferences
- Current context

Example contexts include:

- Beach reading.
- Short reading session.
- Bookshop visit.
- General recommendation.

---

# 6. External Book Data

External book services may eventually provide:

### Metadata lookup

Used when adding or updating books.

Possible information includes:

- Title
- Author
- ISBN
- Page count
- Publication information
- Genres
- Series
- Cover
- Description

### External discovery

Used to find books that are not already in the user's library.

External candidates must remain separate from the user's library until the user chooses to add them.

Manual library management must continue to work if external services are unavailable.

---

# 7. AI Librarian

The AI librarian is a future capability allowing natural-language interaction with Book Brain.

It should be able to interpret requests such as:

> "What should I read this weekend?"

> "How many books did I read this year?"

> "Which books I own are similar to books I've rated highly?"

The AI should use Book Brain's application functionality to obtain factual information and recommendations.

It must not invent or override information about the user's library.

AI functionality should remain replaceable between different models or providers.

---

# 8. Analytics

Book Brain should retain sufficient structured data to support analysis of:

- Library composition.
- Reading history.
- Reading sessions.
- Ratings.
- Genres.
- Authors.
- Series.
- Book length.
- Reading trends.

Power BI may later provide advanced visualisation and portfolio analysis.

Power BI is not required for the core application.

---

# 9. Future Capabilities

The following are outside the initial MVP:

- External book APIs.
- Barcode / ISBN scanning.
- Advanced recommendation engine.
- Semantic search and embeddings.
- AI librarian.
- Web application.
- Mobile application.
- Wearable integration.
- PostgreSQL.
- Cloud deployment.

Future capabilities should build on the existing application and data rather than creating separate systems.

---

# 10. Non-Functional Requirements

Book Brain should be:

### Reliable
User data should not be silently lost or overwritten.

### Testable
Core functionality and recommendation logic should be independently testable.

### Maintainable
Responsibilities should remain separated as the application grows.

### Extensible
Future databases, interfaces, external services and AI models should be replaceable without requiring a complete redesign.

### Privacy-conscious
Personal library and reading data should remain under the user's control.

### Incremental
Technologies and functionality should be introduced when justified by the current development stage.

---

# 11. Document Boundaries

This document describes **what Book Brain should do**.

Other documents define:

- `database.md` — data model, relationships and database schema.
- `architecture.md` — system structure and component responsibilities.
- `roadmap.md` — development phases and sequence.
- `development-log.md` — actual development, decisions, problems and lessons learned.