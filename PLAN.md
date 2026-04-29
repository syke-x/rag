# Graph RAG Foundations — Project Plan

Status legend: [ ] todo  [~] in progress  [x] done

---

## PHASE 1 — What is a graph database and why does it exist?

  Concepts to master:
  - The relational database and the JOIN problem at depth
  - The property graph model: nodes, edges, properties, labels
  - Index-free adjacency and why it matters for traversal performance
  - Neo4j's storage model vs. row-store vs. column-store

  Steps:
  - [x] 1.1 — Understand the JOIN depth problem with a concrete example
              Goal: Model movies/directors/actors in SQL, count JOINs needed
              for a 3-hop query. Feel the combinatorial explosion firsthand.
              Concept taught: JOIN depth, intermediate result sets, O(n) vs O(n^k)
              Key decision: when relational breaks down and why graph is the answer

  - [x] 1.2 — Learn the property graph model
              Goal: Understand nodes, edges, properties, labels
              Concept taught: relationship as first-class citizen vs. foreign key
              Key decision: what makes an entity a node vs. a property?

  - [x] 1.3 — Install Neo4j via Docker and connect with the Python driver
              Goal: Running Neo4j instance, basic Python connectivity verified
              Concept taught: neo4j driver vs. py2neo — which and why?
              Key decision: driver choice rationale

  - [~] 1.4 — Design the movie knowledge graph schema
              Goal: Finalize node types (Movie, Person, Genre, Studio) and
              edge types (DIRECTED, ACTED_IN, BELONGS_TO, PRODUCED_BY)
              Concept taught: schema design in a schemaless world
              Key decision: what lives on a node vs. an edge vs. a property?

  Key tradeoff: When is a graph database WRONG to use?

---

## PHASE 2 — Building the graph: ingestion and Cypher

  Concepts to master:
  - Cypher query language from first principles
  - Entity resolution: same entity, different names
  - Idempotent ingestion: MERGE vs. CREATE
  - Batch ingestion vs. row-by-row: the N+1 problem

  Steps:
  - [ ] 2.1 — Parse and clean raw dataset (MovieLens or TMDB CSV)
              Goal: Clean, typed Pydantic models for each entity type
              Concept taught: data contracts, Pydantic over dicts/dataclasses
              Key decision: which dataset and why?

  - [ ] 2.2 — Write the ingestion pipeline
              Goal: CSV → Pydantic models → Cypher MERGE → Neo4j
              Concept taught: MERGE semantics, idempotency
              Key decision: batch size, transaction boundaries

  - [ ] 2.3 — First traversal queries in Cypher
              Goal: Find actors in a movie, movies by a director, co-actors
              Concept taught: declarative pattern matching vs. imperative traversal
              Key decision: Cypher syntax choices

  - [ ] 2.4 — Multi-hop query: directors connected through shared actors (2 hops)
              Goal: Observe query time vs. equivalent SQL
              Concept taught: index-free adjacency in action
              Key decision: query optimisation strategies in Cypher

  Key tradeoff: MERGE vs. CREATE — idempotency cost in write performance

---

## PHASE 3 — What is a vector database and why does it exist?

  Concepts to master:
  - Why keyword search (BM25, TF-IDF) fails for semantic similarity
  - What an embedding is from first principles (distributional hypothesis)
  - Cosine similarity vs. Euclidean distance for text
  - ANN (Approximate Nearest Neighbour): HNSW and what it sacrifices
  - Vector index is NOT a database — ACID, durability, persistence

  Steps:
  - [ ] 3.1 — Hands-on embedding exercise
              Goal: Embed 10 movie titles+descriptions, compute cosine similarity,
              verify semantic clusters form
              Concept taught: embedding geometry, vector space intuition
              Key decision: which similarity metric and why?

  - [ ] 3.2 — Set up ChromaDB or Qdrant locally via Docker
              Goal: Running vector store, connected from Python
              Concept taught: ChromaDB vs. Qdrant tradeoffs for local learning
              Key decision: which vector DB and why?

  - [ ] 3.3 — Embed movie descriptions, store with metadata
              Goal: movie_id, title, genre stored as metadata alongside vectors
              Concept taught: metadata filtering, the linking key concept
              Key decision: what metadata to store and why?

  - [ ] 3.4 — Semantic search function
              Goal: query → embedding → top-K neighbours → movie titles returned
              Concept taught: the full retrieval loop
              Key decision: what K to use and why?

  Key tradeoff: embedding model size vs. quality vs. speed

---

## PHASE 4 — Connecting graph and vector: the dual-store pattern

  Concepts to master:
  - Why you need BOTH stores (graph blind to semantics, vector blind to relationships)
  - The linking key: connecting vector DB result to Neo4j node
  - Hybrid retrieval: sequential vs. parallel strategy
  - The consistency problem: out-of-sync stores

  Steps:
  - [ ] 4.1 — Design the linking architecture
              Goal: neo4j_node_id stored as metadata on every vector DB entry
              Concept taught: foreign key equivalent in a dual-store system
              Key decision: which ID to use as the canonical key?

  - [ ] 4.2 — Graph-enriched semantic search
              Goal: query → vector search → top-K IDs → Neo4j enrichment → results
              Concept taught: sequential hybrid retrieval
              Key decision: how many hops to traverse after vector lookup?

  - [ ] 4.3 — Semantically-filtered graph traversal
              Goal: actor → graph (all their movies) → re-rank by semantic similarity
              Concept taught: graph-first, vector-second retrieval
              Key decision: re-ranking strategy

  - [ ] 4.4 — Query router
              Goal: Decide which retrieval path to take based on query structure
              Concept taught: query intent classification
              Key decision: rule-based vs. model-based routing?

  Key tradeoff: dual-store consistency — what breaks and how to detect it

---

## PHASE 5 — Naive RAG: build it and find its failure modes

  Concepts to master:
  - Full naive RAG pipeline: document → chunk → embed → store → query → retrieve → generate
  - Chunking strategy tradeoffs (fixed-size, sentence, semantic)
  - "Lost in the middle" problem
  - Hallucination in RAG: when LLM ignores retrieved context
  - Context window as a budget

  Steps:
  - [ ] 5.1 — Build naive RAG over movie descriptions
              Goal: Full working pipeline: chunk → embed → retrieve top-K → generate
              Concept taught: the naive RAG loop end-to-end
              Key decision: chunk size and overlap

  - [ ] 5.2 — Test against all four query types
              Goal: Baseline results for all four query categories
              Concept taught: retrieval vs. reasoning distinction
              Key decision: evaluation criteria

  - [ ] 5.3 — Document every failure mode
              Goal: Annotated failure log for each query type
              Concept taught: why naive RAG fails at relational questions
              Key decision: failure categorisation taxonomy

  - [ ] 5.4 — Calculate "relationship blindness" failure rate
              Goal: Quantified metric: % wrong because of missed relationships
              Concept taught: precision vs. recall in RAG evaluation
              Key decision: what counts as a "relationship miss"?

  Key tradeoff: more chunks = higher recall, worse precision, higher LLM cost

---

## PHASE 6 — Graph RAG: fix what naive RAG broke

  Concepts to master:
  - Microsoft GraphRAG: community detection + hierarchical summarisation
  - Louvain algorithm: what it does and why it creates better retrieval units
  - Local search vs. global search
  - Subgraph serialisation: graph → text for LLM reasoning

  Steps:
  - [ ] 6.1 — Community detection on the movie graph
              Goal: NetworkX Louvain on Neo4j snapshot, communities identified
              Concept taught: graph clustering, why communities = retrieval units
              Key decision: resolution parameter for Louvain

  - [ ] 6.2 — Generate community summaries
              Goal: LLM-written paragraph per community cluster
              Concept taught: index build step, pre-computation cost vs. query gain
              Key decision: summary length, prompt design

  - [ ] 6.3 — Implement local search
              Goal: entity in query → graph traversal → subgraph → prompt → answer
              Concept taught: entity-anchored retrieval
              Key decision: subgraph depth and serialisation format

  - [ ] 6.4 — Implement global search
              Goal: thematic query → community summaries → map-reduce → answer
              Concept taught: hierarchical summarisation for global questions
              Key decision: map-reduce implementation strategy

  - [ ] 6.5 — Re-run all four query types, compare to Phase 5
              Goal: Quantified improvement over naive RAG
              Concept taught: evaluation methodology, before/after analysis
              Key decision: what metrics to use?

  Key tradeoff: community summary pre-computation cost vs. query-time gain

---

## PHASE 7 — Hybrid retrieval and query routing

  Concepts to master:
  - When to traverse graph / search vectors / do both
  - Query classification from natural language
  - Reranking after retrieval
  - The full Graph RAG pipeline as a unified system

  Steps:
  - [ ] 7.1 — Query classifier
              Goal: Rule-based then LLM-based router: graph / vector / hybrid
              Concept taught: intent detection, routing strategy
              Key decision: rule-based vs. LLM-based — when to upgrade?

  - [ ] 7.2 — Hybrid retrieval
              Goal: Graph + vector results → merged, deduplicated, reranked
              Concept taught: result fusion strategies (RRF, score normalisation)
              Key decision: fusion algorithm choice

  - [ ] 7.3 — Reranker
              Goal: Cross-encoder or LLM-as-judge scores retrieved context
              Concept taught: retrieval ≠ relevance, two-stage retrieval
              Key decision: cross-encoder vs. LLM-as-judge tradeoff

  - [ ] 7.4 — Final evaluation: all four query types × all three retrieval modes
              Goal: Full comparison matrix of answer quality
              Concept taught: systematic evaluation design
              Key decision: evaluation metric (RAGAS, human eval, LLM eval?)

  - [ ] 7.5 — Postmortem: what graph adds that vector alone cannot
              Goal: Written mental model — maps directly to fraud detection project
              Concept taught: when to reach for Graph RAG in production
              Key decision: which lessons transfer to fraud detection and how?

  Key tradeoff: system complexity vs. answer quality — where is the knee of the curve?

---
