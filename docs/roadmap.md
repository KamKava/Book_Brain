# Book Brain — Development Roadmap

**Project status:** Early development
**Version:** 0.2
**Last updated:** August 2026

---

# Vision

Book Brain is intended to become a personal library management, reading-tracking, analytics, recommendation, and AI librarian application.

The application will allow users to:

* Catalogue books they own.
* Store book metadata including page count and series information.
* Manage their TBR.
* Track current and completed reading.
* Record ratings, notes, dates, and formats.
* Track individual reading sessions and reading time.
* Analyse their reading habits.
* Receive context-aware recommendations.
* Discover books from external book catalogues.
* Distinguish between books they already own and books they may wish to acquire.
* Ask questions about their library using natural language.
* Eventually interact with Book Brain through web, mobile, and potentially wearable devices.

The project will be developed incrementally, with each phase producing a usable or demonstrable improvement.

The AI system will be built on top of a reliable database, application logic, and recommendation system rather than being treated as the foundation of the application.

---

# Development Architecture

The long-term architecture is expected to develop approximately as follows:

```text
                         ┌───────────────┐
                         │     User      │
                         └───────┬───────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
                    ▼                         ▼
              Web Frontend              Mobile App
                    │                         │
                    └────────────┬────────────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │   FastAPI     │
                         │    Backend    │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
        Library System     Reading System    Recommendation
                                                  Engine
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                                 ▼
                           ┌──────────┐
                           │ Database │
                           └────┬─────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 ▼              ▼              ▼
             Analytics    External Data     Embeddings
                                │              │
                                │              ▼
                                │          AI / LLM
                                │              │
                                └──────┬───────┘
                                       ▼
                                 AI Librarian
```

External book data may serve two different purposes:

```text
User entering a book
        ↓
External book search
        ↓
Select metadata
        ↓
Add to Book Brain
```

and later:

```text
User wants to buy a book
        ↓
External book catalogue
        ↓
Potential candidates
        ↓
Recommendation Engine
        ↓
AI explains recommendations
```

These are separate use cases and should not be unnecessarily coupled.

The architecture will be developed gradually. Components should not be implemented before they are required.

---

# Phase 1 — Project Foundation

**Goal:** Establish professional development practices and design the foundations of the application.

### Documentation

* [x] Create GitHub repository
* [x] Create README
* [x] Create `.gitignore`
* [x] Create `docs/` directory
* [x] Create requirements document
* [x] Create roadmap
* [x] Create architecture document
* [x] Create database design document
* [ ] Create development log
* [ ] Establish technical decision record process

### Project management

* [x] Create GitHub Project
* [x] Create initial milestone
* [x] Create initial issues
* [ ] Organise issues on project board
* [ ] Define issue naming/conventions
* [ ] Define branch/commit conventions

### Technical design

* [x] Finalise initial requirements
* [x] Define initial architecture
* [x] Design database
* [x] Create ER diagram
* [x] Identify core entities
* [x] Identify relationships
* [x] Establish testing approach
* [x] Document technical decisions

**Outcome:**

A documented and professionally structured project ready for implementation.

---

# Phase 2 — Build the Database

**Goal:** Turn the approved database design into a working SQLite database.

* [ ] Create database initialisation module
* [ ] Create `Book` table
* [ ] Create `Author` table
* [ ] Create `Genre` table
* [ ] Create `Series` table
* [ ] Create `Format` table
* [ ] Create `LibraryEntry` table
* [ ] Create `ReadingStatus` table
* [ ] Create `Rating` table
* [ ] Create `Note` table
* [ ] Create `ReadingHistory` table
* [ ] Create `ReadingSession` table
* [ ] Create junction tables
* [ ] Add primary keys
* [ ] Add foreign keys
* [ ] Add constraints
* [ ] Add indexes where appropriate
* [ ] Add initial reading statuses
* [ ] Add database seed/test data
* [ ] Test database creation
* [ ] Write database tests
* [ ] Document implementation

The database shall support:

* Page counts.
* Multiple authors.
* Multiple genres.
* Book series.
* Series position.
* Multiple formats.
* Library ownership.
* Reading history.
* Reading sessions.
* Unassigned reading sessions.

**Outcome:**

Running Book Brain creates a valid SQLite database matching the approved ER diagram.

---

# Phase 3 — Core Library MVP

**Goal:** Create a functional Python application capable of managing the user's library.

### Book management

* [ ] Implement book creation
* [ ] Implement book retrieval
* [ ] Implement book updating
* [ ] Implement book deletion
* [ ] Implement book search
* [ ] Implement basic filtering

### Book metadata

* [ ] Store title
* [ ] Store ISBN
* [ ] Store page count
* [ ] Store publication information
* [ ] Store authors
* [ ] Store genres
* [ ] Store series
* [ ] Store series position
* [ ] Store formats

### Library management

* [ ] Add book to personal library
* [ ] Remove book from personal library
* [ ] Track ownership
* [ ] Implement reading status
* [ ] Implement ratings
* [ ] Implement reading dates
* [ ] Implement notes

### Quality

* [ ] Add input validation
* [ ] Add error handling
* [ ] Prevent inappropriate duplicate records
* [ ] Add automated tests
* [ ] Add basic data export

**Outcome:**

A functional local Book Brain application capable of managing a real personal book collection.

---

# Phase 4 — Reading Sessions

**Goal:** Track individual periods of time spent reading.

Reading sessions are an application feature in their own right. They are **not dependent on Fitbit**.

The initial application shall support manually starting and stopping a reading session.

### Core functionality

* [ ] Implement session creation
* [ ] Implement "Start Reading"
* [ ] Implement "Stop Reading"
* [ ] Record session start time
* [ ] Record session end time
* [ ] Calculate session duration
* [ ] Associate sessions with books
* [ ] Support unassigned sessions
* [ ] Allow sessions to be reassigned
* [ ] Display reading-session history
* [ ] Calculate total reading time
* [ ] Calculate average session duration
* [ ] Add reading-time tests

A session may originate from different sources in the future:

```text
Manual / Web / Mobile / Wearable
              ↓
       Reading Session
              ↓
           Database
```

**Outcome:**

Book Brain can track how much time the user spends reading independently of any wearable device.

---

# Phase 5 — External Book Data

**Goal:** Reduce manual data entry and improve metadata accuracy.

This phase concerns **external book data used while adding or editing books**, rather than recommendations for books the user may want to purchase later.

### Issue — Research external book data sources

* [ ] Research Google Books API
* [ ] Research Open Library API
* [ ] Research other suitable sources
* [ ] Compare title/author metadata
* [ ] Compare ISBN coverage
* [ ] Compare page-count coverage
* [ ] Compare genre/category data
* [ ] Compare cover-image availability
* [ ] Compare publication/edition information
* [ ] Compare search capabilities
* [ ] Compare usage limits
* [ ] Compare licensing
* [ ] Compare cost
* [ ] Determine primary source
* [ ] Determine fallback source if appropriate
* [ ] Document decision

### Issue — Implement external book search

The user should be able to search external book data while entering book information.

* [ ] Search by ISBN
* [ ] Search by title
* [ ] Search by author
* [ ] Support partial title searches
* [ ] Support partial author searches
* [ ] Return multiple candidates
* [ ] Return title
* [ ] Return author
* [ ] Return ISBN
* [ ] Return page count where available
* [ ] Return publication information
* [ ] Return genres/categories where available
* [ ] Return cover image where available
* [ ] Allow user to select a result
* [ ] Populate Book data from selected result
* [ ] Handle no results
* [ ] Handle API errors
* [ ] Handle incomplete metadata
* [ ] Prevent accidental duplicate books
* [ ] Add automated tests

**Outcome:**

The user can enter an ISBN, title, or author and select a matching external book record rather than manually entering all available metadata.

---

# Phase 6 — Analytics

**Goal:** Turn Book Brain's data into meaningful information about reading behaviour.

### Core statistics

* [ ] Total books owned
* [ ] Total books read
* [ ] Total TBR
* [ ] Currently reading
* [ ] Average rating
* [ ] Total pages read
* [ ] Average book length
* [ ] Shortest book
* [ ] Longest book
* [ ] Total reading time
* [ ] Average reading-session duration

### Genre analysis

* [ ] Books read by genre
* [ ] Books owned by genre
* [ ] Average rating by genre
* [ ] Pages read by genre
* [ ] Reading time by genre
* [ ] Genre trends

### Book-length analysis

* [ ] Average page count
* [ ] Median page count
* [ ] Book-length distribution
* [ ] Short/medium/long book categories
* [ ] Rating by book length
* [ ] Reading time by book length

### Author analysis

* [ ] Most-read authors
* [ ] Books read by author
* [ ] Average rating by author
* [ ] Reading time by author

### Series analysis

* [ ] Books read by series
* [ ] Series completion
* [ ] Series currently in progress
* [ ] Average rating by series
* [ ] Reading time by series

### Time analysis

* [ ] Books per month
* [ ] Books per year
* [ ] Pages per month
* [ ] Pages per year
* [ ] Reading time per month
* [ ] Reading time per year
* [ ] Reading trends

**Outcome:**

Book Brain can meaningfully analyse the user's reading behaviour.

---

# Phase 7 — Power BI Analytics

**Goal:** Create a professional analytical layer using Book Brain's data.

* [ ] Define analytical dataset
* [ ] Export data from SQLite
* [ ] Connect Power BI
* [ ] Build data model
* [ ] Create reading overview
* [ ] Create genre dashboard
* [ ] Create book-length analysis
* [ ] Create rating analysis
* [ ] Create author analysis
* [ ] Create series analysis
* [ ] Create reading-time analysis
* [ ] Create yearly summary
* [ ] Document analytical findings
* [ ] Add dashboard screenshots to README

Power BI shall remain an analytical layer rather than a dependency of the application.

**Outcome:**

Book Brain demonstrates both software development and professional data analytics.

---

# Phase 8 — Recommendation Engine

**Goal:** Build Book Brain's own recommendation system before introducing a conversational LLM.

The recommendation engine must be capable of producing recommendations independently of an LLM.

### Issue — Define recommendation algorithm

* [ ] Define recommendation inputs
* [ ] Define recommendation contexts
* [ ] Define candidate selection
* [ ] Define exclusion rules
* [ ] Define ranking factors
* [ ] Define scoring system
* [ ] Define context-specific weighting
* [ ] Define recommendation explanations
* [ ] Define evaluation methodology

### Issue — Implement recommendation engine

#### Candidate filtering

* [ ] Filter by ownership
* [ ] Filter by TBR status
* [ ] Filter by reading status
* [ ] Filter previously completed books where appropriate
* [ ] Filter by genre
* [ ] Filter by author
* [ ] Filter by page count
* [ ] Filter by series constraints
* [ ] Apply explicit user exclusions

#### Preference matching

* [ ] Implement genre matching
* [ ] Implement author matching
* [ ] Implement rating-based preference
* [ ] Implement page-count preferences
* [ ] Implement historical reading preference
* [ ] Implement series-aware recommendations

#### Context-aware recommendations

Support contexts including:

* [ ] General recommendation
* [ ] Beach reading
* [ ] Holiday reading
* [ ] Short reading session
* [ ] Long reading session
* [ ] Bookshop visit
* [ ] Mood-based recommendation
* [ ] Surprise me

For example, a beach-read request should prioritise:

1. Books already owned.
2. Unread/TBR books.
3. Suitable genres.
4. Historical preferences.
5. Shorter books.

A preference for approximately **100–150 pages** should be treated as a weighting rather than an absolute rule.

#### Ranking

* [ ] Rank candidate books
* [ ] Implement context-specific scoring
* [ ] Log recommendation factors
* [ ] Generate structured recommendation explanations

#### Evaluation

* [ ] Create recommendation test cases
* [ ] Test ownership constraints
* [ ] Test exclusion rules
* [ ] Test page-length preferences
* [ ] Test genre matching
* [ ] Test series constraints
* [ ] Evaluate recommendation quality
* [ ] Document limitations

**Outcome:**

Book Brain can independently determine which books from the user's collection are appropriate recommendations.

---

# Phase 9 — External Recommendation Candidate Discovery

**Goal:** Allow Book Brain to discover books outside the user's library for situations where the user is willing to acquire a book.

This is deliberately separate from the external metadata search used when adding books.

For example:

> "I'm going to the bookshop. Have you got any must-buys for me?"

The flow should be:

```text
External book catalogue
        ↓
Potential books
        ↓
Remove books already owned
        ↓
Apply user exclusions
        ↓
Apply genre/preferences
        ↓
Compare with reading history
        ↓
Recommendation Engine
        ↓
AI explains recommendations
```

### Issue — External recommendation candidate discovery

* [ ] Define external recommendation requirements
* [ ] Search external book catalogues
* [ ] Search by relevant genres/categories
* [ ] Search by authors
* [ ] Search by keywords
* [ ] Retrieve candidate metadata
* [ ] Retrieve page counts where available
* [ ] Retrieve publication information
* [ ] Retrieve cover information
* [ ] Exclude books already owned
* [ ] Exclude books already read where appropriate
* [ ] Apply user exclusions
* [ ] Apply genre preferences
* [ ] Apply author preferences
* [ ] Apply book-length preferences
* [ ] Pass candidates to recommendation engine
* [ ] Rank candidates
* [ ] Return recommendation candidates
* [ ] Add automated tests

**Outcome:**

Book Brain can discover books that are not currently in the user's library and provide them to the recommendation engine for evaluation.

---

# Phase 10 — Semantic Search and Embeddings

**Goal:** Improve book similarity beyond simple metadata matching.

This phase introduces semantic AI without requiring a conversational LLM.

* [ ] Learn what embeddings are
* [ ] Select an embedding model
* [ ] Generate embeddings for book descriptions
* [ ] Store embeddings
* [ ] Implement similarity search
* [ ] Find books similar to highly rated books
* [ ] Compare semantic similarity with rule-based recommendations
* [ ] Evaluate results
* [ ] Document embedding architecture

Possible future technologies include:

* Local embedding models
* PostgreSQL + pgvector
* Chroma
* Qdrant

A separate vector database should not be introduced unless there is a practical reason to do so.

**Outcome:**

Book Brain can understand semantic relationships between books and use them as an additional recommendation signal.

---

# Phase 11 — AI Librarian

**Goal:** Add natural-language interaction without surrendering control of the application to the LLM.

## Issue — Design AI architecture

Before implementation:

* [ ] Define LLM responsibilities
* [ ] Define recommendation-engine responsibilities
* [ ] Define database access
* [ ] Define tools/functions available to AI
* [ ] Define safety boundaries
* [ ] Define hallucination controls
* [ ] Select initial LLM
* [ ] Document architecture

The key principle is:

```text
                     USER
                       │
                       ▼
                     LLM
                       │
              Understand request
                       │
                       ▼
              Book Brain tools
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Database    Statistics   Recommender
```

The LLM does not decide what books exist.

It asks Book Brain.

---

## Issue — Implement AI librarian

### Initial LLM integration

* [ ] Connect selected LLM
* [ ] Implement conversation handling
* [ ] Implement prompt/system instructions
* [ ] Implement structured request handling
* [ ] Test natural-language understanding

### Library queries

* [ ] Query books
* [ ] Query TBR
* [ ] Query current reading
* [ ] Query reading history
* [ ] Query ratings
* [ ] Query notes where appropriate
* [ ] Query series
* [ ] Query reading statistics

### Recommendation integration

* [ ] Pass user intent to recommendation engine
* [ ] Pass constraints to recommendation engine
* [ ] Retrieve ranked recommendations
* [ ] Allow LLM to explain recommendations
* [ ] Prevent LLM from inventing recommendation candidates

### Context understanding

The LLM should be able to transform:

> "I'm going to the beach today. Give me something short and dark."

into structured constraints such as:

```text
context = beach
availability = owned
status = unread
preferred_length = short
genre_preference = dark
```

### Clarification

* [ ] Detect materially ambiguous requests
* [ ] Ask appropriate clarification questions
* [ ] Avoid unnecessary clarification

### Evaluation

* [ ] Test factual accuracy
* [ ] Test ownership awareness
* [ ] Test recommendation constraints
* [ ] Test hallucination resistance
* [ ] Test tool failures
* [ ] Evaluate response quality
* [ ] Document limitations

**Outcome:**

The user can talk naturally to Book Brain while the application remains responsible for factual library data and recommendation logic.

---

# Phase 12 — RAG and Tool Calling

**Goal:** Turn the LLM into a controlled AI interface for Book Brain.

RAG and tool calling should only be introduced where they provide a practical benefit.

### Retrieval

* [ ] Identify information requiring retrieval
* [ ] Implement retrieval of relevant library data
* [ ] Implement statistics retrieval
* [ ] Implement recommendation retrieval
* [ ] Investigate RAG architecture
* [ ] Compare RAG with direct structured queries
* [ ] Determine where semantic retrieval is useful

### Tools

Potential tools include:

```text
search_library()
get_book()
get_current_book()
get_reading_statistics()
find_books_by_genre()
find_books_under_pages()
get_recommendations()
get_tbr()
start_reading_session()
stop_reading_session()
search_external_books()
```

* [ ] Define tool interfaces
* [ ] Implement controlled tool access
* [ ] Validate tool arguments
* [ ] Restrict destructive actions
* [ ] Log tool calls
* [ ] Test tool failures
* [ ] Test hallucination resistance

**Outcome:**

Book Brain has a controlled AI assistant capable of retrieving information and using approved application functionality.

---

# Phase 13 — Web Application

**Goal:** Make Book Brain accessible through a proper user interface.

The FastAPI backend should become the shared interface between Book Brain's data/business logic and future clients.

## Issue — Build FastAPI backend

* [ ] Design REST API
* [ ] Implement FastAPI application
* [ ] Configure database access
* [ ] Create book endpoints
* [ ] Create library endpoints
* [ ] Create reading endpoints
* [ ] Create reading-session endpoints
* [ ] Create search endpoints
* [ ] Create statistics endpoints
* [ ] Create recommendation endpoints
* [ ] Create AI endpoints
* [ ] Add API validation
* [ ] Handle API errors
* [ ] Add API tests
* [ ] Add API documentation

**Outcome:**

Book Brain has a functional backend API that can be used by web and future mobile clients.

---

## Issue — Build web frontend

* [ ] Design application layout
* [ ] Create library view
* [ ] Create book details
* [ ] Create book creation/editing
* [ ] Create search
* [ ] Create filters
* [ ] Create TBR interface
* [ ] Create reading-status controls
* [ ] Create reading-session controls
* [ ] Create statistics dashboard
* [ ] Create recommendation interface
* [ ] Create AI librarian interface
* [ ] Connect frontend to FastAPI
* [ ] Implement responsive design
* [ ] Test frontend/backend integration

Potential technologies:

* HTML
* CSS
* JavaScript
* React
* TypeScript

The final frontend technology will be selected when this phase begins.

**Outcome:**

Book Brain becomes a genuinely usable web application.

---

# Phase 14 — Mobile Application

**Goal:** Make Book Brain practical when physically browsing books.

* [ ] Design mobile interface
* [ ] Select mobile framework
* [ ] Implement mobile client
* [ ] Connect mobile app to FastAPI
* [ ] Implement library
* [ ] Implement book search
* [ ] Implement barcode scanning
* [ ] Implement book addition
* [ ] Implement TBR
* [ ] Implement reading status
* [ ] Implement reading sessions
* [ ] Implement statistics
* [ ] Implement recommendations
* [ ] Implement AI librarian
* [ ] Test mobile/backend integration

Potential technology:

* React Native

**Outcome:**

Book Brain can be used conveniently from a phone.

---

# Phase 15 — Wearable Integration

**Goal:** Investigate and potentially implement wearable-based reading-session tracking.

Wearable functionality is an **additional source of Reading Session data**, not the foundation of reading-session tracking.

The application should already support:

```text
Manual Start/Stop
        ↓
Reading Session
```

before wearable integration is attempted.

A wearable would provide an additional path:

```text
Fitbit Start/Stop
        ↓
Reading Session
```

## Issue — Investigate wearable integration

* [ ] Investigate Fitbit developer platform
* [ ] Investigate available APIs
* [ ] Investigate custom wearable applications
* [ ] Investigate Bluetooth capabilities
* [ ] Investigate authentication
* [ ] Investigate data synchronisation
* [ ] Investigate platform restrictions
* [ ] Investigate privacy implications
* [ ] Determine whether custom Start/Stop Reading functionality is possible
* [ ] Determine whether direct communication with Book Brain is possible
* [ ] Determine whether a mobile companion application is required
* [ ] Determine how sessions would be associated with books
* [ ] Determine how unassigned sessions would work
* [ ] Determine duplicate-session handling
* [ ] Determine technical feasibility
* [ ] Document decision

## Issue — Implement wearable reading sessions

Only proceed if the investigation determines that implementation is practical.

* [ ] Create wearable reading activity
* [ ] Implement Start Reading
* [ ] Implement Stop Reading
* [ ] Record session start
* [ ] Record session end
* [ ] Calculate duration
* [ ] Synchronise session with Book Brain
* [ ] Identify session source
* [ ] Associate session with current book where possible
* [ ] Support unassigned sessions
* [ ] Prevent duplicate sessions
* [ ] Allow session correction
* [ ] Add integration tests

## Fallback

If direct Fitbit integration is not practical:

* [ ] Investigate mobile companion approach
* [ ] Investigate importing wearable activity data
* [ ] Investigate alternative wearable platforms

**Outcome:**

Book Brain can potentially track reading time through a wearable without requiring the user to manually enter sessions.

---

# Phase 16 — Deployment

**Goal:** Make Book Brain accessible outside the development environment.

* [ ] Select free/low-cost hosting
* [ ] Deploy backend
* [ ] Deploy frontend
* [ ] Configure production database
* [ ] Configure secrets
* [ ] Implement backups
* [ ] Configure logging
* [ ] Configure monitoring
* [ ] Implement production error handling
* [ ] Document deployment
* [ ] Create production README
* [ ] Test production environment

The initial deployment should prioritise free or very low-cost services.

**Outcome:**

Book Brain is accessible remotely.

---

# Phase 17 — Portfolio Release

**Goal:** Turn Book Brain into a polished professional portfolio project.

* [ ] Finalise README
* [ ] Add architecture diagram
* [ ] Add database ER diagram
* [ ] Document API
* [ ] Document AI architecture
* [ ] Document recommendation methodology
* [ ] Document testing strategy
* [ ] Document deployment
* [ ] Add screenshots
* [ ] Add demonstration video/GIF
* [ ] Add Power BI dashboard
* [ ] Document technical decisions
* [ ] Document challenges and solutions
* [ ] Document future improvements
* [ ] Clean GitHub issues
* [ ] Close completed milestones
* [ ] Create release
* [ ] Create project demonstration

**Outcome:**

A polished, publicly demonstrable software project suitable for inclusion in job applications and interviews.

---

# Long-Term Ideas

These features are intentionally outside the current development roadmap.

* [ ] Goodreads/StoryGraph import
* [ ] Book lending tracking
* [ ] Reading goals
* [ ] Reading challenges
* [ ] Reading streaks
* [ ] AI-generated reading lists
* [ ] Public/private libraries
* [ ] Multiple users
* [ ] Multiple libraries
* [ ] Book price tracking
* [ ] OCR
* [ ] Cover recognition
* [ ] Local AI running directly on mobile
* [ ] Offline mobile functionality
* [ ] Additional wearable platforms
* [ ] Cloud synchronisation
* [ ] Movie Brain
* [ ] Other collection-management applications

---

# Development Principles

Book Brain will be developed incrementally.

New functionality should not be added simply because it is technically interesting.

Features should be prioritised according to:

1. **Usefulness to the user**
2. **Learning value**
3. **Portfolio value**
4. **Development effort**
5. **Cost**
6. **Architectural importance**

The project should favour completing small, functional increments over building large unfinished features.

---

## Principle 1 — Build the Foundation Before the AI

The database and core application must be reliable before AI functionality is introduced.

The AI should enhance Book Brain rather than compensate for weaknesses in the underlying system.

---

## Principle 2 — Keep AI Replaceable

The application should not be permanently dependent on a particular LLM provider.

Where practical, AI functionality should be implemented behind an abstraction layer so that models can be replaced.

---

## Principle 3 — Keep Recommendations Testable

The recommendation engine should be capable of operating without an LLM.

This makes it possible to test:

```text
Input → Candidate selection → Ranking → Result
```

independently of AI-generated language.

---

## Principle 4 — Database Is the Source of Truth

The database is authoritative for:

* Books.
* Ownership.
* TBR.
* Reading status.
* Ratings.
* Reading history.
* Reading sessions.
* User data.

The LLM must not invent or override these facts.

---

## Principle 5 — AI Is an Interface, Not the Database

The AI should interpret user requests and communicate results.

It should retrieve factual information from Book Brain rather than relying on its own knowledge of the user's library.

---

## Principle 6 — Context Matters

A recommendation should depend on what the user is trying to do.

For example:

```text
"I'm going to the beach."
        ↓
Prioritise books already owned
```

while:

```text
"I'm going to the bookshop."
        ↓
Allow recommendations for books not already owned
```

The recommendation engine should explicitly model these differences rather than expecting the LLM to handle them implicitly.

---

## Principle 7 — External Data Has Multiple Roles

External book data serves more than one purpose.

### Book entry

External data helps the user:

```text
Type title / author / ISBN
        ↓
Find matching books
        ↓
Select correct edition
        ↓
Populate metadata
```

### Book discovery

Later, external data can help:

```text
User wants to buy a book
        ↓
Search external catalogue
        ↓
Find candidates
        ↓
Exclude owned books
        ↓
Recommendation Engine
```

These functions should remain logically separate.

---

## Principle 8 — Don't Overengineer Early

SQLite is sufficient for the initial application.

A vector database, PostgreSQL, cloud infrastructure, mobile application, wearable integration, and sophisticated AI agent should only be introduced when the project actually needs them.

---

## Principle 9 — Every Major Feature Should Teach Something

Book Brain is both a useful application and a learning project.

Development should progressively demonstrate:

```text
Python
  ↓
SQL
  ↓
Database design
  ↓
Testing
  ↓
APIs
  ↓
External data integration
  ↓
Data analysis
  ↓
Power BI
  ↓
Recommendation systems
  ↓
Embeddings
  ↓
LLMs
  ↓
RAG / retrieval
  ↓
Tool calling
  ↓
AI agents
  ↓
FastAPI
  ↓
Web development
  ↓
Mobile development
  ↓
Device integration
  ↓
Deployment
```

---

# Definition of Progress

Book Brain should be considered successful at each stage when the corresponding functionality is **working, tested, documented, and demonstrable**, rather than merely designed.

The project should therefore favour:

```text
Design
   ↓
Implement
   ↓
Test
   ↓
Document
   ↓
Demonstrate
   ↓
Move forward
```

rather than continuously expanding the scope before earlier functionality is complete.
