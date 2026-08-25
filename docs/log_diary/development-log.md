# Book Brain — Development Log

**Project status:** Early development  
**Version:** 0.1  
**Last updated:** August 2026

---

# 1. Purpose

This document records the development history of Book Brain.

It is used to record:

- Significant development work.
- Important technical decisions.
- Problems and solutions.
- Changes to requirements or design.
- Testing and debugging.
- Lessons learned.
- Decisions that affect future development.

The log should describe what **actually happened during development**.

Project requirements, architecture, database structure and future plans are documented separately.

---

# 2. Documentation Structure

Book Brain uses the following documentation:

| Document | Purpose |
|---|---|
| `requirements.md` | What the application should do |
| `database-design.md` | What data is stored and how it relates |
| `architecture.md` | How the main system components fit together |
| `roadmap.md` | Planned development sequence |
| `development-log.md` | What happened during development |

The development log should not duplicate these documents unnecessarily.

When a development decision changes another document, that document should be updated as well.

---

# 3. Logging Principles

## Keep entries short

The log should record significant events rather than every coding action.

Useful:

> Changed the library model after discovering that ownership and bibliographic information needed to be represented separately.

Unnecessary:

> Created a Python file and added three functions.

---

## Record reasoning

For significant decisions, record:

- The problem.
- Options considered, where relevant.
- The decision.
- Why it was chosen.
- Consequences or follow-up work.

---

## Record changes

When an earlier decision changes, record:

- Previous approach.
- New approach.
- Reason for the change.
- Affected areas.

---

## Record lessons

Unexpected discoveries, mistakes and useful technical lessons should be recorded when they may help future development.

---

# 4. Development Entry Template

Use this template for significant development sessions or decisions:

## YYYY-MM-DD — Title

### Session

Brief description of what was worked on.

### Problem / Decision

What problem was encountered or what decision needed to be made?

### Options

Relevant alternatives considered.

### Decision

What was chosen?

### Reasoning

Why?

### Implementation

What was actually changed?

### Testing

How was it tested?

### Result

What happened?

### Documentation

Documents updated, if any.

### Next

What should happen next?

---

# 5. Development Entries

Chronological development notes begin here.

---

## YYYY-MM-DD — Project Started

### Session

Initial Book Brain project planning and documentation.

### Result

Established the initial project scope and development direction.

### Next

Begin implementation of the database foundation.

---

# 6. Lessons Learned

Record significant lessons discovered during development.

Examples:

- Database design lessons.
- SQL lessons.
- Python/application architecture lessons.
- Testing lessons.
- API integration lessons.
- Recommendation-system lessons.
- AI integration lessons.
- Data modelling lessons.

---

# 7. Open Decisions

Record important decisions that remain unresolved until their relevant development phase.

Examples:

- External book API selection.
- Recommendation scoring approach.
- Embedding technology.
- LLM provider.
- Web technology.
- Wearable integration feasibility.
- Deployment approach.

Once a decision is made, record it in the development log and update the relevant project documentation.

---

# 8. Current Development State

**Current phase:** Phase 2 — Database Foundation

**Current focus:**

- Finalise SQLite schema.
- Implement database creation.
- Add constraints and indexes.
- Add reference data.
- Test database integrity.

**Next major phase:**

Phase 3 — Core Library.

---

# 9. Maintenance

Update this document when:

- A significant development session is completed.
- An important technical decision is made.
- A significant problem is solved.
- Requirements or architecture change.
- A useful lesson is discovered.

Minor implementation details do not need to be recorded unless they have lasting significance.

# Book Brain — Roadmap

**Project status:** Early development  
**Version:** 0.1  
**Last updated:** August 2026

---

## 1. Purpose

This roadmap defines the planned development sequence for Book Brain.

It describes **when major capabilities are introduced**, rather than documenting their detailed requirements or implementation.

The roadmap may change as development progresses.

---

# 2. Development Phases

## Phase 1 — Project Foundation

**Status:** Complete / ongoing

- Define project goals and scope.
- Create project documentation.
- Set up Git and GitHub.
- Establish initial Python project structure.

---

## Phase 2 — Database Foundation

**Status:** Current

- Finalise database design.
- Create SQLite schema.
- Add foreign keys and constraints.
- Add indexes where required.
- Add reference data.
- Test database creation and integrity.

---

## Phase 3 — Core Library

**Status:** Next

- Implement database access layer.
- Implement book CRUD.
- Implement library-entry CRUD.
- Implement authors, genres and series.
- Add validation.
- Add search and filtering.
- Add automated tests.

**Goal:** A reliable local library-management application.

---

## Phase 4 — Reading Tracking

- Implement reading records.
- Implement reading status workflow.
- Support rereading.
- Implement reading sessions.
- Add session tracking.
- Add reading-history queries.
- Add automated tests.

**Goal:** Track not only what is owned, but what and how the user reads.

---

## Phase 5 — External Book Data

- Research suitable book APIs.
- Implement book search.
- Support ISBN/title/author lookup.
- Import selected metadata.
- Add user confirmation before saving.
- Handle API failures and incomplete data.
- Test integrations with mocked responses.

**Goal:** Reduce manual book-data entry without giving external services control over user data.

---

## Phase 6 — Analytics

- Add application-level reading statistics.
- Create analytical queries/views where useful.
- Export data for analysis.
- Introduce Pandas where useful.
- Build Power BI dashboards.

**Goal:** Understand the user's library and reading behaviour.

---

## Phase 7 — Recommendation Engine

- Define recommendation contexts.
- Implement candidate generation.
- Implement filtering rules.
- Implement scoring.
- Implement ranking.
- Add recommendation explanations/factors.
- Create automated recommendation tests.

**Goal:** Produce useful recommendations without requiring AI.

---

## Phase 8 — External Recommendation Discovery

- Search external catalogues for candidates.
- Exclude books already owned when appropriate.
- Apply user preferences and exclusions.
- Combine external candidates with the recommendation engine.
- Evaluate recommendation quality.

**Goal:** Recommend books outside the existing library.

---

## Phase 9 — Semantic Search

- Research embedding models.
- Generate book embeddings.
- Evaluate similarity search.
- Test semantic recommendations.
- Select suitable vector-storage approach if required.
- Combine semantic similarity with existing recommendation logic where useful.

**Goal:** Improve discovery and similarity-based recommendations.

---

## Phase 10 — AI Librarian

- Research LLM options.
- Introduce an LLM provider abstraction.
- Implement structured request interpretation.
- Add controlled application tools.
- Connect AI to library queries.
- Connect AI to recommendations.
- Add retrieval where useful.
- Evaluate accuracy and hallucination risks.

**Goal:** Provide a natural-language interface to Book Brain.

---

## Phase 11 — Web Application

- Design web UI.
- Introduce FastAPI.
- Expose application services through an API.
- Build frontend.
- Connect frontend to backend.
- Add authentication if required.

**Goal:** Make Book Brain accessible through a web interface.

---

## Phase 12 — Mobile Application

- Evaluate mobile technology.
- Build mobile interface.
- Connect to the existing backend.
- Add mobile reading-session controls.
- Add barcode scanning.

**Goal:** Provide convenient mobile access to Book Brain.

---

## Phase 13 — Wearable Integration

**Status:** Research / future

- Investigate Fitbit and other wearable capabilities.
- Evaluate available APIs and platform restrictions.
- Determine whether direct integration is feasible.
- Implement only if technically and practically justified.

**Goal:** Optionally automate reading-session tracking.

---

## Phase 14 — Deployment

- Evaluate hosting options.
- Introduce PostgreSQL if required.
- Configure production infrastructure.
- Secure API credentials.
- Implement authentication and authorisation.
- Configure HTTPS.
- Add monitoring and logging.
- Deploy the application.

**Goal:** Move from a local application to a remotely accessible system.

---

# 3. Simplified Development Path

The overall progression is:

```text
Foundation
    ↓
SQLite Database
    ↓
Core Library
    ↓
Reading Tracking
    ↓
External Book Data
    ↓
Analytics
    ↓
Recommendation Engine
    ↓
External Discovery
    ↓
Semantic Search
    ↓
AI Librarian
    ↓
Web Application
    ↓
Mobile Application
    ↓
Wearables
    ↓
Deployment```

4. Development Principles
Build before expanding

A phase should be sufficiently stable before major functionality from the next phase is introduced.

Avoid premature technology

Future technologies should not be introduced simply because they are planned.

Test before depending

New functionality should be tested before becoming a dependency for later phases.

Keep the core independent

Book Brain should remain useful without AI, external APIs, Power BI or wearable integration.

Reassess future phases

A planned feature may be changed, postponed or removed if development shows that it provides insufficient value.

5. Current Position
Phase 1  ██████████  Foundation
Phase 2  ██████░░░░  Database Foundation  ← CURRENT
Phase 3  ░░░░░░░░░░  Core Library
Phase 4  ░░░░░░░░░░  Reading Tracking
Phase 5  ░░░░░░░░░░  External Book Data
Phase 6  ░░░░░░░░░░  Analytics
Phase 7  ░░░░░░░░░░  Recommendation Engine
Phase 8  ░░░░░░░░░░  External Discovery
Phase 9  ░░░░░░░░░░  Semantic Search
Phase 10 ░░░░░░░░░░  AI Librarian
Phase 11 ░░░░░░░░░░  Web Application
Phase 12 ░░░░░░░░░░  Mobile Application
Phase 13 ░░░░░░░░░░  Wearable Integration
Phase 14 ░░░░░░░░░░  Deployment
6. Roadmap Maintenance

The roadmap should be updated when:

A phase is completed.
A phase changes significantly.
A phase is added or removed.
Development reveals a better sequence.
A major future technology is no longer required.

Detailed implementation decisions belong in development-log.md, not in this document.
