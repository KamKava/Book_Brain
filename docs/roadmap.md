# Book Brain — Development Roadmap

**Project status:** Early development
**Version:** 0.1
**Last updated:** August 2026

---

# Vision

Book Brain is intended to become a personal library management, reading-tracking, analytics, recommendation, and AI librarian application.

The application will allow users to:

* Catalogue books they own.
* Manage their TBR.
* Track current and completed reading.
* Record ratings, notes, dates and formats.
* Track reading sessions and reading time.
* Analyse their reading habits.
* Receive context-aware recommendations.
* Ask questions about their library using natural language.
* Eventually interact with Book Brain through web, mobile and potentially wearable devices.

The project will be developed incrementally, with each phase producing a usable or demonstrable improvement.

The AI system will be built on top of a reliable database and recommendation system rather than being treated as the foundation of the application.

---

# Development Architecture

The long-term architecture is expected to develop approximately as follows:

```
                    ┌────────────────────┐
                    │       User         │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │   Web / Mobile UI  │
                    └─────────┬──────────┘
                              │
                         Backend API
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Library System   Reading System   Recommendation
             │                │                │
             └────────────────┼────────────────┘
                              │
                         Database
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        Book Metadata     Analytics       Embeddings
                                              │
                                              ▼
                                         AI / LLM
                                              │
                                              ▼
                                        AI Librarian
```

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
* [ ] Create architecture document
* [ ] Create database design document
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

* [ ] Finalise initial requirements
* [ ] Define initial architecture
* [ ] Design database
* [ ] Create ER diagram
* [ ] Identify core entities
* [ ] Identify relationships
* [ ] Establish testing approach
* [ ] Document technical decisions

**Outcome:**

A documented and professionally structured project ready for implementation.

---

# Phase 2 — Core Database

**Goal:** Build the data foundation of Book Brain.

* [ ] Create SQLite database
* [ ] Create database schema
* [ ] Implement Book table/entity
* [ ] Implement Author relationship
* [ ] Implement Genre relationship
* [ ] Implement Library Entry
* [ ] Implement Reading Status
* [ ] Implement Rating
* [ ] Implement Reading Dates
* [ ] Implement Notes
* [ ] Implement Book Format
* [ ] Implement database constraints
* [ ] Create database seed/test data
* [ ] Write database tests

**Outcome:**

A reliable SQLite database representing a real personal book library.

---

# Phase 3 — Core Library MVP

**Goal:** Create a functional Python application capable of managing the library.

* [ ] Implement book creation
* [ ] Implement book retrieval
* [ ] Implement book updating
* [ ] Implement book deletion
* [ ] Implement book search
* [ ] Implement filtering
* [ ] Implement reading status management
* [ ] Implement rating management
* [ ] Implement reading dates
* [ ] Implement notes
* [ ] Implement format management
* [ ] Add input validation
* [ ] Add error handling
* [ ] Add automated tests
* [ ] Add basic data export

**Outcome:**

A functional local Book Brain application with no frontend required.

---

# Phase 4 — Reading Sessions

**Goal:** Introduce detailed tracking of time spent reading.

* [ ] Design reading-session data model
* [ ] Implement session creation
* [ ] Implement session start
* [ ] Implement session completion
* [ ] Calculate session duration
* [ ] Associate sessions with books
* [ ] Support unassigned sessions
* [ ] Allow sessions to be reassigned
* [ ] Display reading-session history
* [ ] Calculate total reading time
* [ ] Calculate average session duration
* [ ] Add reading-time tests

### Future consideration

* [ ] Investigate wearable integration requirements
* [ ] Investigate Fitbit developer capabilities
* [ ] Document technical feasibility

**Outcome:**

Book Brain can track not only which books the user reads, but how much time they spend reading.

---

# Phase 5 — External Book Data

**Goal:** Reduce manual data entry.

* [ ] Research free book APIs
* [ ] Compare API data quality
* [ ] Compare API limits/licensing
* [ ] Select initial API
* [ ] Implement ISBN lookup
* [ ] Retrieve book metadata
* [ ] Populate book information automatically
* [ ] Add cover images
* [ ] Handle missing/incomplete data
* [ ] Handle API errors
* [ ] Prevent API failures from affecting existing data
* [ ] Add API integration tests

**Outcome:**

A user can provide an ISBN and automatically retrieve available book information.

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
* [ ] Total reading time
* [ ] Average reading-session duration

### Genre analysis

* [ ] Books read by genre
* [ ] Books owned by genre
* [ ] Average rating by genre
* [ ] Pages by genre
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

**Goal:** Set analythics in the application.

* [ ] Define analytical dataset
* [ ] Export data from SQLite
* [ ] Connect Power BI
* [ ] Build data model
* [ ] Create reading overview
* [ ] Create genre dashboard
* [ ] Create book-length analysis
* [ ] Create rating analysis
* [ ] Create author analysis
* [ ] Create reading-time analysis
* [ ] Create yearly summary
* [ ] Document analytical findings
* [ ] Add dashboard screenshots to README

Power BI shall remain an analytical layer rather than a dependency of the application.

**Outcome:**

Book Brain demonstrates both software development and professional data analytics.

---

# Phase 8 — Recommendation Engine

**Goal:** Build Book Brain's own recommendation system before introducing an LLM.

This phase is particularly important.

The recommendation engine should be capable of producing recommendations without an AI language model.

### Step 1 — Rule-Based Recommendations

* [ ] Define recommendation inputs
* [ ] Define recommendation contexts
* [ ] Implement genre matching
* [ ] Implement author matching
* [ ] Implement rating-based preference
* [ ] Implement ownership filtering
* [ ] Implement TBR filtering
* [ ] Implement reading-status filtering
* [ ] Implement page-count preferences
* [ ] Implement exclusion rules

### Step 2 — Context-Aware Recommendations

Implement different recommendation behaviour for contexts such as:

* [ ] General recommendation
* [ ] Beach reading
* [ ] Holiday reading
* [ ] Short reading session
* [ ] Long reading session
* [ ] Bookshop visit
* [ ] Mood-based recommendation

### Step 3 — Recommendation Ranking

* [ ] Create scoring system
* [ ] Weight recommendation factors
* [ ] Rank candidate books
* [ ] Implement context-specific weighting
* [ ] Generate recommendation explanations
* [ ] Log recommendation factors

### Step 4 — Evaluation

* [ ] Create recommendation test cases
* [ ] Test ownership constraints
* [ ] Test exclusion rules
* [ ] Test page-length preferences
* [ ] Test genre matching
* [ ] Evaluate recommendation quality
* [ ] Document limitations

**Outcome:**

Book Brain can independently determine which books are appropriate recommendations.

---

# Phase 9 — Semantic Search and Embeddings

**Goal:** Allow Book Brain to understand similarity between books beyond simple genre labels.

This phase introduces a new form of AI without yet requiring a conversational LLM.

* [ ] Learn what embeddings are
* [ ] Select an embedding model
* [ ] Generate embeddings for book descriptions
* [ ] Store embeddings
* [ ] Implement similarity search
* [ ] Find books similar to highly rated books
* [ ] Compare semantic similarity with rule-based recommendations
* [ ] Evaluate results
* [ ] Document embedding architecture

### Possible future technologies

* Local embedding models
* PostgreSQL + pgvector
* Chroma
* Qdrant

The project should not introduce a separate vector database unless there is a practical reason to do so.

**Outcome:**

Book Brain can understand semantic relationships between books and use them in recommendations.

---

# Phase 10 — AI Librarian

**Goal:** Add natural-language interaction without surrendering control of the application to the LLM.

### LLM research

* [ ] Research local LLMs
* [ ] Research external LLM APIs
* [ ] Compare model capabilities
* [ ] Compare cost
* [ ] Compare privacy
* [ ] Compare hardware requirements
* [ ] Select initial model/provider
* [ ] Document decision

### Initial LLM integration

* [ ] Set up selected LLM
* [ ] Implement basic prompts
* [ ] Implement structured responses
* [ ] Test natural-language understanding

### Library-aware AI

* [ ] Connect LLM to application data
* [ ] Implement natural-language library queries
* [ ] Implement statistics queries
* [ ] Implement recommendation queries
* [ ] Prevent hallucinated library information

### Context extraction

The LLM should be able to transform requests such as:

> "I'm going to the beach today. Give me something short and dark."

into structured constraints such as:

```text
context = beach
availability = owned
status = unread
preferred_length = short
genre_preference = dark
```

### AI recommendation flow

* [ ] LLM interprets request
* [ ] Application validates constraints
* [ ] Recommendation engine searches candidates
* [ ] Recommendation engine ranks candidates
* [ ] LLM explains results
* [ ] Test complete conversation flow

**Outcome:**

The user can talk naturally to Book Brain while the application remains responsible for factual library data and recommendation logic.

---

# Phase 11 — RAG and Tool Calling

**Goal:** Turn the LLM into a controlled AI interface for Book Brain.

### Retrieval

* [ ] Implement retrieval of relevant library data
* [ ] Implement statistics retrieval
* [ ] Implement recommendation retrieval
* [ ] Investigate RAG architecture
* [ ] Evaluate when RAG is useful versus direct SQL

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

Book Brain has a controlled AI assistant capable of retrieving information and using application functionality.

---

# Phase 12 — Web Application

**Goal:** Make Book Brain accessible through a proper user interface.

### Backend

* [ ] Design REST API
* [ ] Implement FastAPI
* [ ] Create book endpoints
* [ ] Create reading endpoints
* [ ] Create statistics endpoints
* [ ] Create recommendation endpoints
* [ ] Create AI endpoints
* [ ] Add API validation
* [ ] Add API tests

### Frontend

* [ ] Design interface
* [ ] Create library view
* [ ] Create book details
* [ ] Create search
* [ ] Create filters
* [ ] Create TBR interface
* [ ] Create reading tracker
* [ ] Create statistics dashboard
* [ ] Create recommendation interface
* [ ] Create AI librarian interface
* [ ] Implement responsive design

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

# Phase 13 — Mobile Application

**Goal:** Make Book Brain practical when physically browsing books.

* [ ] Design mobile interface
* [ ] Select mobile framework
* [ ] Implement mobile client
* [ ] Connect mobile app to backend
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

Potential technology:

* React Native

**Outcome:**

Book Brain can be used conveniently from a phone.

---

# Phase 14 — Wearable Integration

**Goal:** Investigate and potentially implement automatic reading-session tracking.

### Research

* [ ] Investigate Fitbit developer platform
* [ ] Investigate available APIs
* [ ] Investigate custom wearable applications
* [ ] Investigate Bluetooth capabilities
* [ ] Investigate authentication
* [ ] Investigate data synchronisation
* [ ] Investigate platform restrictions
* [ ] Investigate privacy implications
* [ ] Determine technical feasibility

### Prototype

If technically feasible:

* [ ] Create wearable reading activity
* [ ] Implement Start Reading
* [ ] Implement Stop Reading
* [ ] Record start time
* [ ] Record end time
* [ ] Synchronise with Book Brain
* [ ] Detect duplicate sessions
* [ ] Associate with current book
* [ ] Support unassigned sessions

### Fallback

If direct Fitbit integration is not practical:

* [ ] Investigate mobile companion approach
* [ ] Investigate importing wearable activity data
* [ ] Investigate alternative wearable platforms

**Outcome:**

Book Brain can potentially track reading time through a wearable without requiring the user to manually enter sessions.

---

# Phase 15 — Deployment

**Goal:** Make Book Brain accessible outside the development environment.

* [ ] Select free/low-cost hosting
* [ ] Deploy backend
* [ ] Deploy frontend
* [ ] Configure production database
* [ ] Configure secrets
* [ ] Implement backups
* [ ] Configure logging
* [ ] Configure monitoring
* [ ] Implement error handling
* [ ] Document deployment
* [ ] Create production README
* [ ] Test production environment

The initial deployment should prioritise free or very low-cost services.

**Outcome:**

Book Brain is accessible remotely.

---

# Phase 16 — Portfolio Release

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
* [ ] Mood-based recommendations
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
Prioritise books not already owned
```

The recommendation engine should explicitly model these differences rather than expecting the LLM to handle them implicitly.

---

## Principle 7 — Don't Overengineer Early

SQLite is sufficient for the initial application.

A vector database, PostgreSQL, cloud infrastructure, mobile application, wearable integration, and sophisticated AI agent should only be introduced when the project actually needs them.

---

## Principle 8 — Every Major Feature Should Teach Something

Book Brain is both a useful application and a learning project.

Development should progressively demonstrate:

```text
Python
  ↓
SQL
  ↓
Database design
  ↓
APIs
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
RAG
  ↓
Tool calling
  ↓
AI agents
  ↓
Web development
  ↓
Mobile development
  ↓
Device integration
```
