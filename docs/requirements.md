# Book Brain — Software Requirements Specification

**Project status:** Initial development
**Version:** 0.1
**Last updated:** August 2026

---

# 1. Project Overview

Book Brain is a personal book management, reading-tracking, analytics, recommendation, and AI librarian application.

The application is designed to help users:

* Catalogue books they own.
* Manage their TBR collection.
* Track books they are currently reading.
* Record completed books and ratings.
* Track reading dates and reading time.
* Analyse their reading habits.
* Discover books already available in their collection.
* Identify books they may wish to purchase.
* Eventually interact with an AI librarian through natural language.
* Potentially track reading sessions through wearable devices such as Fitbit.

The application will begin as a small Python and SQLite project and progressively develop into a full application with external book APIs, analytics, recommendation functionality, conversational AI, a web interface, wearable integrations, and eventually a mobile application.

The project is intended to be both a genuinely useful personal application and a professional software engineering, database, data analytics, API, AI, and integration portfolio project.

---

# 2. Project Goals

The application aims to:

1. Provide a reliable digital catalogue of books owned by the user.
2. Minimise manual data entry through ISBN lookup and barcode scanning.
3. Allow users to manage their TBR list and reading history.
4. Track ratings, reading dates, notes, formats, and reading sessions.
5. Track the amount of time spent reading.
6. Provide meaningful statistics about reading habits.
7. Allow users to explore reading habits by genre, author, length, rating, time period, and reading time.
8. Provide recommendations based on the user's actual library and reading behaviour.
9. Distinguish between books the user already owns and books they would need to acquire.
10. Provide context-aware recommendations based on what the user wants to do.
11. Develop a personalised recommendation system.
12. Eventually provide a conversational AI librarian.
13. Investigate wearable integration for automatic reading-session tracking.
14. Provide web and mobile access in future versions.
15. Demonstrate professional software engineering, database, data analysis, API, integration, and AI development practices.
16. Allow users to retain control of and export their personal library data.

---

# 3. Development Philosophy

The application shall be developed incrementally.

The project shall begin with a small, functional core rather than attempting to implement all planned functionality simultaneously.

Future functionality shall be added only after the underlying functionality is stable and tested.

The database shall be treated as the central source of truth for the user's library, reading history, and reading-session data.

The recommendation engine shall use structured application data to determine appropriate recommendation candidates.

The conversational AI shall not be treated as the authoritative source of information about the user's library.

The architecture should avoid unnecessary dependencies between core functionality and optional external services.

External integrations should be designed so that failure of an optional service does not prevent the core application from functioning.

Technical decisions that materially affect architecture, cost, privacy, security, maintainability, or future development shall be documented.

---

# 4. Scope

## 4.1 Initial MVP

The Minimum Viable Product shall provide:

* A SQLite database.
* Book creation.
* Book retrieval.
* Book updating.
* Book deletion.
* Basic book search.
* Reading status.
* Ratings.
* Reading dates.
* Reading notes.
* Basic reading statistics.
* Basic reading-session support.
* Basic automated tests.
* Basic data export.

The initial MVP will operate without:

* Graphical frontend.
* AI.
* Barcode scanning.
* External book APIs.
* Wearable integration.
* Cloud deployment.
* User accounts.
* Mobile application.
* Power BI integration.

Reading sessions in the MVP may be entered manually.

---

# 5. Book Catalogue Requirements

## FR-001 — Add Book

The system shall allow the user to add a book to their library.

A book may contain:

* ISBN
* Title
* Author
* Publisher
* Publication date
* Page count
* Description
* Cover image
* Language
* Genre/category information

---

## FR-002 — Unique Book Identification

The system shall assign each book a unique internal identifier.

Where an ISBN is available, the system shall store the ISBN as an additional identifier.

The system should prevent accidental duplication of books with the same ISBN.

Books without an ISBN shall still be supported.

The database design should allow different editions of the same title to exist where appropriate.

---

## FR-003 — View Book

The system shall allow the user to view detailed information about an individual book.

---

## FR-004 — Update Book

The system shall allow the user to modify book information.

---

## FR-005 — Delete Book

The system shall allow the user to remove a book from their library.

The application should request confirmation before permanent deletion.

Deleting a book should not unintentionally delete unrelated reading history or other data.

---

# 6. Reading Management

## FR-006 — Reading Status

The system shall allow the user to assign a reading status.

Initial statuses shall include:

* TBR
* Currently Reading
* Read

Additional statuses may be added later.

---

## FR-007 — Rating

The system shall allow the user to rate a completed book using a five-point rating system.

Ratings shall be optional.

The system shall validate that ratings fall within the permitted range.

---

## FR-008 — Reading Dates

The system shall allow the user to record:

* Date started.
* Date finished.

These fields shall be optional.

The system should validate that reading dates are logically consistent.

---

## FR-009 — Reading Notes

The system shall allow the user to store personal notes associated with a book.

---

## FR-010 — Book Format

The system shall allow the user to record the format in which they own or read a book.

Potential values include:

* Hardback
* Paperback
* E-book
* Audiobook
* Other

The system should allow a book to have more than one format where appropriate.

---

# 7. Reading Session Tracking

Reading-session tracking shall record the amount of time a user spends reading.

## FR-011 — Start Reading Session

The system shall allow the user to start a reading session.

A reading session shall record at minimum:

* Start date and time.

A session may optionally be associated with a specific book.

---

## FR-012 — End Reading Session

The system shall allow the user to end an active reading session.

The system shall record:

* End date and time.
* Session duration.

Duration should be calculated from the recorded start and end times rather than manually entered where possible.

---

## FR-013 — Associate Reading Session With Book

A reading session should be associated with a book where the relevant book is known.

The user should be able to:

* Select the book before starting a session.
* Select or change the associated book after a session.
* Leave a session temporarily unassigned.

This allows reading time to be recorded even when the user does not identify the book at the beginning of a session.

---

## FR-014 — Reading Session History

The system shall allow the user to view previous reading sessions.

Session information may include:

* Book.
* Start time.
* End time.
* Duration.
* Format.
* Date.

---

## FR-015 — Reading Time Statistics

The application shall calculate reading-time statistics where sufficient data exists.

Possible statistics include:

* Total reading time.
* Reading time per book.
* Average reading-session duration.
* Longest reading session.
* Reading time per day.
* Reading time per week.
* Reading time per month.
* Reading time per year.
* Reading time by genre.
* Reading time by format.

---

# 8. Search and Filtering

## FR-016 — Search

The system shall allow users to search their library by:

* Title.
* Author.
* ISBN.

---

## FR-017 — Filtering

The system shall eventually allow users to filter their library by:

* Reading status.
* Genre.
* Author.
* Rating.
* Page count.
* Publication year.
* Reading year.
* Format.
* Reading time.

Additional filtering options may be introduced later.

---

# 9. External Book Metadata

## FR-018 — ISBN Lookup

The system shall eventually allow an ISBN to be submitted to an external book API.

The system shall retrieve available bibliographic information.

The specific API shall be selected based on:

* Availability.
* Data quality.
* Usage limits.
* Licensing.
* Privacy.
* Cost.
* Reliability.

---

## FR-019 — Automatic Metadata Population

Where information is available, the system should automatically populate:

* Title.
* Author.
* Publisher.
* Publication date.
* Page count.
* Description.
* Cover.
* Categories/genres.
* Language.

The user shall be able to review and modify imported information.

---

## FR-020 — External API Failure Handling

The system shall handle:

* Invalid ISBNs.
* ISBNs not found.
* API downtime.
* Network failures.
* Incomplete metadata.
* Unexpected API responses.
* API usage limits.

The application shall not lose existing user data if an external API fails.

External API functionality shall not be required to manage books manually.

---

# 10. Barcode Scanning

## FR-021 — Barcode Scanning

A future version shall allow the user to scan an ISBN barcode using a supported camera or barcode scanner.

The scanned ISBN shall be passed to the book metadata lookup process.

The user should be able to scan a book and add it with minimal manual input.

---

# 11. Reading Statistics and Analytics

Reading analytics shall be a major feature of the application.

The system shall collect sufficient structured data to allow meaningful analysis of the user's reading habits.

## FR-022 — Reading Statistics

The application shall provide statistics including, where sufficient data exists:

* Total books owned.
* Total books read.
* Total books on TBR.
* Total books currently being read.
* Books finished during a selected period.
* Average rating.
* Total pages read.
* Average book length.
* Shortest book read.
* Longest book read.
* Total reading time.
* Average reading-session duration.

---

## FR-023 — Time-Based Reading Statistics

The system shall allow reading activity to be analysed by:

* Day.
* Week.
* Month.
* Quarter.
* Year.
* Custom date range.

Statistics may include:

* Books completed per month.
* Books completed per year.
* Pages read per month.
* Pages read per year.
* Reading time per month.
* Reading time per year.
* Average rating over time.

---

## FR-024 — Genre Analysis

The system shall provide statistics relating to genres/categories.

Possible statistics include:

* Number of books read per genre.
* Number of books owned per genre.
* Average rating by genre.
* Pages read by genre.
* Reading time by genre.
* Percentage of reading represented by each genre.
* Genre trends over time.

The system should support books associated with multiple genres.

---

## FR-025 — Book Length Analysis

The application shall allow users to analyse reading habits by book length.

Possible statistics include:

* Average page count.
* Median page count.
* Distribution of book lengths.
* Number of books below selected page thresholds.
* Number of books above selected page thresholds.
* Average rating by book length.
* Reading time by book length.

Possible page-length categories may include:

* Under 100 pages.
* 100–199 pages.
* 200–299 pages.
* 300–399 pages.
* 400–499 pages.
* 500+ pages.

These categories should be configurable in future versions.

---

## FR-026 — Author Statistics

The application shall provide statistics relating to authors.

Possible statistics include:

* Most-read authors.
* Number of books read per author.
* Average rating by author.
* Pages read by author.
* Reading time by author.
* Authors with the highest-rated books.

---

## FR-027 — Rating Analysis

The application shall provide statistics relating to ratings.

Possible statistics include:

* Average rating.
* Rating distribution.
* Books receiving each rating.
* Average rating by genre.
* Average rating by author.
* Average rating by publication period.
* Rating trends over time.

---

## FR-028 — Reading Pace

Where start and finish dates and/or reading-session data are available, the application should calculate:

* Days spent reading a book.
* Average days per book.
* Books completed per month.
* Average reading-session duration.
* Reading time per book.
* Estimated reading pace.

These calculations shall clearly distinguish measured data from estimates.

---

## FR-029 — Reading Trends

The application should identify changes in reading behaviour over time.

Examples include:

* Increasing or decreasing number of books read.
* Changes in average book length.
* Changes in preferred genres.
* Changes in average rating.
* Changes in reading frequency.
* Changes in reading-session duration.
* Changes in total reading time.

---

# 12. Analytics Dashboard

## FR-030 — User Statistics Dashboard

A future graphical interface shall provide an analytics dashboard presenting important reading statistics visually.

Potential visualisations include:

* Books read over time.
* Pages read over time.
* Reading time over time.
* Genre distribution.
* Rating distribution.
* Book-length distribution.
* Top authors.
* Reading status breakdown.
* Reading-session duration.
* Reading time by genre.

The dashboard should allow the user to select relevant time periods.

---

# 13. Power BI Integration

Power BI may be used as an additional analytics and portfolio component.

## FR-031 — Power BI Data Access

The application should maintain structured data in a form that can be analysed using Power BI.

Potential approaches include:

* SQLite export.
* CSV export.
* PostgreSQL connection.
* Dedicated analytical dataset.

The application shall not depend on Power BI for core functionality.

---

## FR-032 — Power BI Portfolio Dashboard

A separate Power BI dashboard may be developed to demonstrate the analytical capabilities of the application.

The dashboard may include:

* Reading trends.
* Genre analysis.
* Book-length analysis.
* Rating analysis.
* Author analysis.
* Reading-time analysis.
* Yearly reading summaries.

Power BI visualisations shall use data generated from the application rather than manually created sample data.

---

# 14. Context-Aware Recommendation System

The recommendation system is one of the core long-term features of Book Brain.

Recommendations shall consider not only what books the user likes, but also **what the user is trying to accomplish at the time of the request**.

## FR-033 — Personalised Recommendations

The system shall recommend books based on the user's:

* Reading history.
* Ratings.
* Genres.
* Authors.
* Book descriptions.
* Page counts.
* Reading time.
* TBR.
* Current reading status.
* Existing library.
* Stated preferences.

---

## FR-034 — Recommendation Context

The system shall identify relevant context from the user's request.

Possible contexts include:

* Immediate reading.
* Beach reading.
* Holiday reading.
* Short reading session.
* Long reading session.
* Bedtime reading.
* Mood-based reading.
* Bookshop visit.
* General discovery.
* "Surprise me."

The list of contexts may expand over time.

---

## FR-035 — Ownership-Aware Recommendations

The recommendation system shall distinguish between:

* Books owned by the user.
* Books on the user's TBR.
* Books currently being read.
* Books previously completed.
* Books not owned by the user.

The recommendation system shall respect ownership requirements implied by the user's request.

For example:

> "I'm going to the beach today. What should I read?"

shall prioritise books already available to the user.

---

## FR-036 — Immediate Reading Recommendations

When a user requests something to read immediately, the system shall prioritise books already available in the user's library.

The system should generally:

1. Exclude books that require acquisition.
2. Prefer appropriate TBR books.
3. Exclude books already completed unless the user requests a reread.
4. Consider currently reading books appropriately.
5. Consider the user's historical preferences.
6. Consider the requested context.
7. Consider book length and other relevant constraints.

---

## FR-037 — Short-Book / Beach-Read Recommendations

For requests such as:

> "Suggest something for a beach read today."

the system should give greater weight to:

* Books already owned.
* Books on the TBR.
* Books matching the user's preferred genres.
* Books matching the user's historical reading preferences.
* Shorter books.

A default preference may be given to books approximately **100–150 pages**, where suitable candidates exist.

The 100–150 page preference shall be treated as a recommendation weighting rather than an absolute requirement.

If no suitable books exist within this range, the system may recommend progressively longer books.

---

## FR-038 — Bookshop Recommendations

When a user requests recommendations for a bookshop visit, the recommendation system shall prioritise books the user does **not** already own.

For example:

> "I'm on my way to the bookshop. Have you got any must-buys for me?"

The system should:

1. Analyse the user's reading preferences.
2. Analyse highly rated books.
3. Analyse favourite genres and authors.
4. Consider the user's TBR where useful.
5. Exclude books already owned.
6. Identify suitable books from external book data.
7. Rank the potential purchases.
8. Explain why each book is recommended.

---

## FR-039 — Recommendation Candidate Filtering

Before generating a final recommendation, the system shall filter candidate books according to relevant constraints.

Potential constraints include:

* Ownership.
* TBR status.
* Reading status.
* Genre.
* Author.
* Book length.
* Rating history.
* User preferences.
* Reading context.
* Previously completed books.
* Availability.

---

## FR-040 — Recommendation Ranking

Candidate books shall be ranked according to their relevance to the user's request.

Different contexts may assign different weights to recommendation factors.

For example:

### Beach-read request

Potential weighting:

* Owned: very high.
* TBR: high.
* Genre compatibility: high.
* User preference: high.
* Book length: high.
* Previous ratings: medium/high.

### Bookshop request

Potential weighting:

* Not owned: very high.
* Genre compatibility: high.
* User preference: high.
* Similarity to highly rated books: high.
* Author preference: medium/high.
* Book length: context-dependent.

The exact ranking algorithm shall be developed and evaluated during the recommendation-system phase.

---

## FR-041 — Recommendation Availability

The system shall distinguish between:

### Available now

Books already accessible to the user.

### Requires acquisition

Books that the user does not currently own.

The AI should not recommend an unavailable book as an immediate reading choice unless the user has indicated that acquiring a book is acceptable.

---

## FR-042 — Recommendation Explanations

The system should explain why each recommendation was selected.

For example:

> "I'd take *Book X*. You already own it and it's on your TBR. At 137 pages, it's one of your shorter unread books, and you've rated several books in this genre highly."

For bookshop recommendations:

> "*Book Y* is a strong candidate because you rated three books by similar authors 4–5 stars, but you don't currently own it."

---

## FR-043 — Recommendation Transparency

The recommendation system shall be capable of identifying the factors that contributed to a recommendation.

This information should be available for:

* Debugging.
* Testing.
* Evaluation.
* Improving recommendation quality.

The user-facing explanation may be simplified.

---

## FR-044 — No Unnecessary Purchases

When a user requests a recommendation for something they can read immediately from their existing library, the system should prioritise books already available to them rather than recommending books requiring purchase.

---

## FR-045 — Recommendation Exclusions

The system should support explicit exclusions such as:

* "Don't recommend anything I've already read."
* "Nothing over 300 pages."
* "No romance."
* "Don't suggest this author."
* "Only recommend books on my TBR."
* "Only suggest physical books I own."

These exclusions should take priority over general recommendation preferences.

---

# 15. Recommendation Architecture

## FR-046 — Structured Candidate Generation

The application shall generate recommendation candidates using structured data and defined rules before asking an AI model to produce a natural-language response.

The AI model shall not independently invent the user's library contents.

---

## FR-047 — Database as Source of Truth

The application database shall remain the authoritative source for:

* Book ownership.
* Reading status.
* TBR status.
* Ratings.
* Reading history.
* Reading sessions.
* User notes.
* Other personal library information.

The AI system shall receive relevant structured information from the application.

---

## FR-048 — AI as Conversational Layer

The AI shall primarily be responsible for:

* Understanding natural-language requests.
* Identifying relevant intent and constraints.
* Communicating recommendation results naturally.
* Explaining recommendations.
* Asking clarification questions where necessary.
* Combining structured application results into useful responses.

The AI shall not be relied upon as the authoritative database of the user's books.

---

## FR-049 — Recommendation Engine Independence

The recommendation engine should remain independently testable from the conversational AI.

It should be possible to provide a structured request such as:

```text
context = beach_read
ownership = owned
status = unread
preferred_pages = 100–150
genre_preference = high
```

and receive a ranked set of candidate books without requiring an LLM.

---

# 16. AI Librarian

## FR-050 — Conversational AI

A future version shall provide a conversational interface allowing the user to ask questions about their library.

Examples:

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

## FR-051 — Library-Aware AI

The AI librarian shall be capable of distinguishing between:

* Books owned by the user.
* Books on the TBR list.
* Books currently being read.
* Books already completed.
* Books not owned by the user.

The AI shall not claim that a book is owned by the user unless that information is available from the application data.

---

## FR-052 — Statistics-Aware AI

The AI librarian should eventually be able to use the user's reading statistics when answering questions.

Examples include:

> "What genre do I read most?"

> "Have I been reading longer books this year?"

> "Which author do I rate highest?"

> "I haven't read much horror this year. What do I own?"

> "When do I usually read?"

> "How much time did I spend reading last month?"

---

## FR-053 — Context-Aware AI

The AI should use contextual information from the user's request when deciding how to formulate a recommendation.

For example:

> "I'm going to the beach today."

should be interpreted differently from:

> "I'm going to the bookshop today."

The first should prioritise immediate availability from the user's existing collection.

The second should allow recommendations for books not currently owned.

---

## FR-054 — Clarification

Where a request is ambiguous and the ambiguity materially affects the recommendation, the AI should ask an appropriate clarification question.

For example:

> "Do you want something from your existing library, or are you looking to buy something?"

The system should avoid unnecessary clarification where a reasonable interpretation is available.

---

## FR-055 — AI Provider Independence

The AI functionality should be designed so that the application is not permanently dependent on a single AI provider.

Potential approaches may include:

* Local open-weight language models.
* External AI APIs.
* Multiple interchangeable model providers.

The final AI architecture shall be selected based on:

* Capability.
* Cost.
* Privacy.
* Hardware requirements.
* Licensing.
* Maintainability.

---

# 17. Wearable Integration

Wearable integration is a future development area and shall not be required for the MVP.

## FR-056 — Wearable Reading Session Tracking

The application should investigate integration with wearable platforms such as Fitbit to allow users to start and stop reading sessions from a supported wearable device.

A potential interaction could be:

1. User selects **Start Reading** on their wearable.
2. The wearable records the session start time.
3. User reads their book.
4. User selects **Stop Reading**.
5. The wearable records the session end time.
6. Book Brain receives or imports the reading session.
7. Book Brain associates the session with a book where possible.

The exact implementation shall depend on the capabilities and restrictions of the selected wearable platform.

---

## FR-057 — Wearable Reading Session Import

Where supported by the wearable platform, Book Brain should be able to import:

* Session start time.
* Session end time.
* Session duration.
* Relevant activity information.
* Associated device/platform information where useful.

The system should prevent duplicate sessions from being imported.

---

## FR-058 — Unassigned Wearable Sessions

A wearable-generated reading session shall not require a book to be known when the session begins.

If no book is associated with the session, Book Brain shall store it as an unassigned reading session.

The user should subsequently be able to associate the session with a book.

Example:

> **45-minute reading session — Which book were you reading?**

The user may then select the relevant book.

---

## FR-059 — Current Book Association

The system should allow the user to designate a book as currently being read.

Where a single current book is selected, an imported reading session may be automatically associated with that book.

The user shall be able to review or change the association.

The system shall not assume a book when the available information is insufficient.

---

## FR-060 — Wearable Platform Independence

Wearable integration should be designed so that core Book Brain reading-session functionality is not dependent on Fitbit specifically.

Where practical, the architecture should allow additional wearable platforms to be integrated in the future.

Potential platforms may include:

* Fitbit.
* Wear OS.
* Other supported wearable ecosystems.

---

## FR-061 — Wearable Integration Feasibility

Before implementing wearable functionality, the project shall investigate:

* Available developer APIs.
* Custom application/activity support.
* Bluetooth capabilities.
* Data synchronisation mechanisms.
* Authentication requirements.
* Device compatibility.
* API usage limits.
* Privacy implications.
* Cost.
* Platform restrictions.

If direct wearable integration is not technically or commercially feasible, the project should investigate alternatives such as a companion mobile application or standard wearable activity data.

---

# 18. Web Application

## FR-062 — Web Interface

A future version shall provide a web-based interface for managing the library.

The interface should provide:

* Library view.
* Book details.
* Search.
* Filtering.
* Book addition.
* Reading status management.
* Reading-session management.
* Statistics dashboard.
* Recommendation interface.
* AI librarian.

---

# 19. Mobile Application

## FR-063 — Mobile Application

A future version shall provide a mobile application.

The mobile application should allow users to:

* View their library.
* Add books.
* Scan ISBN barcodes.
* Update reading status.
* Rate books.
* Start and stop reading sessions.
* View statistics.
* Receive recommendations.
* Interact with the AI librarian.

The mobile application shall communicate with the backend through an API.

---

# 20. Data Requirements

The application shall maintain structured data suitable for both transactional application use and future analytics.

The initial data model is expected to include entities such as:

* Book.
* Author.
* Genre.
* Library entry.
* Reading status.
* Rating.
* Reading session/history.
* Book format.

The final database structure shall be determined during database design.

The database should avoid unnecessary duplication and maintain appropriate relationships between entities.

The data model should support:

* Multiple genres per book.
* Multiple authors where appropriate.
* Multiple formats.
* Different editions.
* Reading sessions.
* Unassigned reading sessions.
* Historical reading data.
* Future recommendation data.

Reading sessions shall be stored independently from books so that sessions can exist before being associated with a particular book.

---

# 21. Data Quality

## NFR-001 — Data Validation

The system shall validate user-provided and externally retrieved data.

Examples include:

* ISBN format.
* Rating range.
* Valid dates.
* Page count.
* Required fields.
* Reading-session start and end times.

---

## NFR-002 — Data Consistency

The system shall maintain consistent relationships between books, authors, genres, and reading records.

---

## NFR-003 — Missing Data

The application shall support incomplete metadata.

For example, a book without a page count should still be usable.

Statistics shall account for missing data rather than producing misleading results.

---

## NFR-004 — Data Provenance

Where practical, the system should distinguish between information:

* Entered manually by the user.
* Retrieved from an external API.
* Imported from a wearable.
* Calculated by the application.
* Generated by an AI system.

This will improve transparency and make inaccurate metadata easier to identify and correct.

---

# 22. Non-Functional Requirements

## NFR-005 — Usability

The application should minimise unnecessary manual data entry.

---

## NFR-006 — Reliability

The application should handle invalid input and external API or wearable failures without crashing or corrupting existing data.

---

## NFR-007 — Maintainability

The code shall be organised into logical components with clearly defined responsibilities.

---

## NFR-008 — Testability

Core functionality shall have automated tests.

External integrations should have appropriate integration tests and/or mocked tests where live services are unavailable.

The recommendation engine shall have tests covering different recommendation contexts and constraints.

---

## NFR-009 — Security

When user accounts or remote access are introduced:

* Authentication information shall be protected.
* Secrets shall not be stored in source code.
* Personal library data shall not be publicly exposed.
* API keys shall be stored securely.
* Access to user data shall be appropriately controlled.

---

## NFR-010 — Portability

The application should be capable of running in a local development environment on common operating systems.

---

## NFR-011 — Cost

The MVP should be developed using free software and services wherever practical.

Paid services should not be required for the initial version.

Future paid services shall be evaluated based on their value and ongoing cost.

---

## NFR-012 — Scalability

The initial application may use SQLite.

The architecture should allow migration to PostgreSQL if multiple users, remote access, increased concurrency, or other requirements justify a server-based database.

---

## NFR-013 — Privacy

Personal library information, reading history, ratings, notes, and other user-generated data should remain private by default.

Future AI and wearable functionality should consider whether user data is processed locally or transmitted to external services.

---

# 23. Analytics Architecture Principle

The application shall separate operational data from analytics and presentation where practical.

The core database shall remain the authoritative source of information.

Analytics may be generated through:

1. SQL queries.
2. Python data processing.
3. Application-generated statistics.
4. Power BI.
5. Future analytics services.

Reading-session data shall be structured so it can be analysed alongside:

* Books.
* Genres.
* Authors.
* Formats.
* Ratings.
* Reading history.
* Reading status.

Recommendation data shall also be structured sufficiently to allow evaluation of recommendation quality in the future.

---

# 24. Initial Technology Direction

The following technologies represent the current development direction rather than permanent technology commitments.

### Initial development

* Python.
* SQLite.
* SQL.
* Git.
* GitHub.

### Data analysis

* Python.
* Pandas.
* SQL.
* Matplotlib where appropriate.
* Power BI.

### Future backend

* FastAPI.
* PostgreSQL.

### Future web frontend

Potential technologies include:

* HTML.
* CSS.
* JavaScript.
* React.
* TypeScript.

The final frontend technology shall be selected based on project requirements and learning and portfolio value.

### Future mobile application

Potential technology:

* React Native.

The final mobile framework shall be selected when mobile development begins.

### Future wearable integration

Potential integrations include:

* Fitbit APIs/platform.
* Wear OS.
* Other supported wearable platforms.

The final implementation shall depend on the capabilities and restrictions of the selected platforms.

### AI

Potential approaches include:

* Custom recommendation algorithms.
* Rule-based recommendation.
* Content-based filtering.
* Embeddings and semantic search.
* Local open-weight language models.
* External AI APIs.
* Retrieval-Augmented Generation.
* Hybrid recommendation systems.

The AI approach shall be selected after the core library, database, analytics, and recommendation functionality have been implemented.

---

# 25. MVP Acceptance Criteria

The MVP shall be considered complete when the user can:

1. Create the SQLite database.
2. Add a book.
3. Store book metadata.
4. Retrieve books.
5. Search for books.
6. Update book information.
7. Delete a book.
8. Assign a reading status.
9. Record a rating.
10. Record reading dates.
11. Add notes.
12. Start a reading session manually.
13. End a reading session manually.
14. Store reading-session duration.
15. Associate a reading session with a book.
16. Produce basic reading statistics.
17. Export library and reading data.
18. Run automated tests against core functionality.

The MVP shall **not** require:

* Graphical frontend.
* AI.
* Recommendation engine.
* Barcode scanning.
* External book APIs.
* Wearable integration.
* User accounts.
* Cloud hosting.
* Mobile application.
* Power BI integration.

These features will be introduced through later milestones.

---

# 26. Future Development Milestones

The exact roadmap shall be maintained separately in `docs/roadmap.md`.

Potential development phases include:

### Phase 1 — Core Library

* SQLite database.
* Database schema.
* CRUD operations.
* Search.
* Reading status.
* Ratings.
* Notes.
* Tests.

### Phase 2 — Reading Tracking

* Reading dates.
* Reading sessions.
* Reading-time calculations.
* Basic statistics.

### Phase 3 — External Metadata

* ISBN lookup.
* Book API integration.
* Automatic metadata population.
* Error handling.

### Phase 4 — Analytics

* Advanced SQL queries.
* Python analytics.
* Power BI dashboard.
* Reading trends.

### Phase 5 — Recommendation Engine

* Recommendation rules.
* Candidate filtering.
* Ranking.
* Context-aware recommendation.
* Recommendation evaluation.

### Phase 6 — AI Librarian

* Natural-language queries.
* Intent detection.
* Structured database queries.
* Recommendation explanations.
* Statistics-aware conversation.
* RAG/LLM integration where appropriate.

### Phase 7 — Web Application

* Backend API.
* Frontend.
* Authentication where required.
* Library interface.
* Dashboard.
* AI interface.

### Phase 8 — Mobile Application

* Mobile interface.
* Barcode scanning.
* Reading-session controls.
* Mobile AI librarian.

### Phase 9 — Wearable Integration

* Investigate Fitbit developer capabilities.
* Prototype wearable reading session.
* Synchronise sessions.
* Associate sessions with current books.
* Evaluate other wearable platforms.

---

# 27. Long-Term Vision

The long-term goal is to develop Book Brain into a complete personal reading platform.

A mature version should allow a user to:

> **Scan a book → automatically catalogue it → add it to the TBR → select it as currently reading → start a reading session → track reading time → finish the book → analyse reading habits → receive personalised recommendations → discuss their library with an AI librarian.**

For example:

### At the beach

> **User:**
> "I'm going to the beach. What should I read today?"

Book Brain should understand that the user wants something immediately available.

It should prioritise:

1. Books the user owns.
2. Books they have not finished.
3. TBR books.
4. Books matching their preferences.
5. Books matching the requested context.
6. Shorter books, with approximately 100–150 pages preferred where suitable.

It should not recommend a book requiring a trip to the bookshop unless the user asks for purchasing recommendations.

---

### At the bookshop

> **User:**
> "I'm on my way to the bookshop. Have you got any must-buys for me?"

Book Brain should understand that acquisition is now possible.

It should:

1. Analyse the user's reading history.
2. Identify genres and authors they enjoy.
3. Identify highly rated books.
4. Consider their TBR and existing preferences.
5. Exclude books already owned.
6. Search appropriate external book data.
7. Rank potential purchases.
8. Explain why each book is a good match.

---

### Statistics

The user should eventually be able to ask:

> "What genre do I read most?"

> "How much time have I spent reading this month?"

> "Do I tend to finish shorter books?"

> "Which authors do I rate highest?"

> "Have I been reading more horror this year?"

---

### Wearable integration

Where technically supported, the user should eventually be able to:

> **Start Reading → read → Stop Reading**

using a wearable device.

Book Brain would then record the reading session and associate it with the user's current book where possible.

---

The mature application should be accessible through web and mobile interfaces while maintaining a shared backend and database.

The project should remain genuinely useful to its creator while demonstrating professional skills in:

* Software engineering.
* Database design.
* SQL.
* Data engineering.
* Data analytics.
* Recommendation systems.
* API integration.
* Wearable/device integration.
* Web development.
* Mobile development.
* Artificial intelligence.
* Testing.
* Deployment.
* Technical documentation.
* Data privacy and security.

The architecture should remain sufficiently modular that the underlying concepts can potentially be adapted for other personal collection-management applications in the future.
