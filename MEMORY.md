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
| 1 | 2026-04-28 | 1.1 ✅ | SQL JOIN depth → O(N^k) intermediate sets; graph uses index-free adjacency O(depth) instead |
