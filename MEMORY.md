# Graph RAG Foundations — Project Memory

## Goal
Build deep foundational understanding of graph databases, vector databases,
and how Graph RAG unifies them. This is prerequisite knowledge for the
production fraud detection system.

---

## The four query types that drive all design decisions

| # | Query Type | Retrieval Strategy | Example |
|---|---|---|---|
| 1 | Relational | Pure graph traversal | "Which movies did Nolan direct that star Cillian Murphy?" |
| 2 | Semantic | Pure vector search | "What movies are similar in tone to Interstellar?" |
| 3 | Multi-hop reasoning | Graph RAG's unique strength | "Most connected directors in sci-fi through shared actors?" |
| 4 | Hybrid | Graph + semantic combined | "Like Blade Runner but lighter in tone" |

---

## Concepts mastered
<!-- Append after each phase with first-principles summary -->

### Phase 1, Step 1.1 — The JOIN Depth Problem (2026-04-28)
- **What existed before graphs:** Relational databases with normalised tables joined via foreign keys
- **The failure mode:** Each additional hop in a relationship query requires an additional JOIN.
  At 3+ hops, the database must materialise intermediate result sets that grow combinatorially.
  A 3-hop query over tables of size N can produce O(N³) intermediate rows before filtering.
- **Why this matters:** For relational questions (actors → movies → directors → other movies),
  the query plan cost explodes while a graph traversal follows physical pointers at O(1) per hop.
- **The graph solution:** Index-free adjacency — each node stores direct physical pointers to
  its neighbours. No lookup table, no index scan. Traversal cost = O(depth), not O(N^depth).

### Phase 1, Step 1.2 — The Property Graph Model (2026-04-28)
- **Four primitives:** Node (entity), Edge (named directed relationship), Property (key-value on either), Label (type tag on nodes)
- **Key insight:** An edge is a first-class citizen with its own identity and properties — not a row in a join table
- **Edge properties:** `role` on ACTED_IN, `year` on DIRECTED — data that belongs to the relationship, not either endpoint
- **Node vs property rule:** If you ever want to traverse TO it or connect other things to it → Node. If purely descriptive → Property
- **Multiple labels:** One Person node can carry both `:Actor` and `:Director` labels simultaneously

### Phase 1, Step 1.3 — Neo4j Driver + Connection (2026-04-29)
- **Driver choice:** Official `neo4j` driver over `py2neo` — py2neo abandoned (2022), neo4j 5.x incompatible, hides Cypher
- **Bolt protocol:** Binary wire protocol, not HTTP — efficient graph type serialisation + connection pooling
- **Object hierarchy:** `driver` (connection pool, long-lived) → `session` (unit of work) → `result` (cursor)
- **Transaction model:** Auto-commit (`session.run()`) vs explicit (`session.begin_transaction()` + `tx.commit()`)
- **Critical rule:** `with session.begin_transaction()` auto-ROLLBACKS on exit unless you explicitly call `tx.commit()`

### Phase 1, Step 1.4 — Schema Design (2026-04-29)
- **Design backwards from queries:** Every node type and relationship type must be justified by a query that needs it
- **Nodes:** Movie, Person, Genre, Studio — each with integer ID as canonical key (links vector DB later)
- **Relationships:** DIRECTED, ACTED_IN (with role + billing_order), BELONGS_TO, PRODUCED_BY, SEQUEL_OF
- **Constraints:** Uniqueness constraints on canonical IDs — mandatory before any ingestion
- **DETACH DELETE:** Required when deleting nodes with relationships; plain DELETE fails if edges exist
- **Genre as node not property:** Storing genre as string property prevents traversal; must be a node to enable graph queries

### Phase 2, Step 2.1 — Data Contracts & Pydantic (2026-04-30)
- **Why Pydantic:** Plain dicts don't validate structure; dataclasses don't enforce types at runtime. Pydantic guarantees data contracts between pipeline stages.
- **Fail early:** Catching bad data (e.g., missing overview) at the parsing boundary is vastly cheaper than catching it inside the database driver or embedding model.
- **Data shape:** Parsing nested JSON within CSVs requires careful handling and conversion into structured models before any DB interaction.
- **Pandas edge case:** Merging dataframes on identical column names (e.g. `title`) renames them (`title_x`, `title_y`), which requires fallback logic in the parser.

---

## Key decisions log
<!-- Append every architectural and library choice with date + rationale -->

| Date | Decision | Rationale | Rejected alternatives |
|---|---|---|---|
| 2026-04-28 | Project domain: Movies | Intuitive relationships, free data (TMDB/MovieLens), zero domain confusion | Finance (too complex for learning), Medical (domain overhead) |

---

## Tradeoffs chosen
<!-- Running log: what we chose, what we rejected, why -->

_Populated as decisions are made through phases._

---

## Failure modes discovered
<!-- Especially Phase 5 — naive RAG failures become Graph RAG motivation -->

_Populated during Phase 5._

---

## Open questions
<!-- Running list — revisit at start of each session -->

1. ChromaDB vs. Qdrant — which is better for a local learning setup? (Phase 3)
2. LangChain vs. LlamaIndex — core orchestration tradeoff for a learner? (Phase 5)
3. Louvain resolution parameter — how sensitive is community detection to this? (Phase 6)

---

## Bridge to fraud detection project
<!-- After Phase 7 — map every concept learned here to its fraud detection equivalent -->

_Populated after Phase 7._

---

## Session log

| Session | Date | Steps completed | Key insight |
|---|---|---|---|
| 1 | 2026-04-28 | 1.1 ✅ 1.2 ✅ | Property graph: nodes, edges, labels, properties — edge as first-class citizen, node vs property rule |
| 2 | 2026-04-29 | 1.3 ✅ 1.4 ✅ | neo4j driver transaction model: auto-rollback on exit; schema designed backwards from queries |
| 3 | 2026-04-30 | 2.1 ✅ | Pydantic as a strict data contract boundary before database ingestion |
