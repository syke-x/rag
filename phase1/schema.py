from neo4j import GraphDatabase

URI  = "bolt://localhost:7687"
AUTH = ("neo4j", "moviepass123")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Neo4j connected successfully!")

    with driver.session(database="neo4j") as session:

        # --- Step 1: Create constraints ---
        with session.begin_transaction() as tx:
            tx.run("CREATE CONSTRAINT movie_id  IF NOT EXISTS FOR (m:Movie)  REQUIRE m.movie_id  IS UNIQUE")
            tx.run("CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.person_id IS UNIQUE")
            tx.run("CREATE CONSTRAINT genre_id  IF NOT EXISTS FOR (g:Genre)  REQUIRE g.genre_id  IS UNIQUE")
            tx.run("CREATE CONSTRAINT studio_id IF NOT EXISTS FOR (s:Studio) REQUIRE s.studio_id IS UNIQUE")
            tx.commit()                          # ← REQUIRED or nothing is saved
        print("Constraints created successfully!")

        # --- Step 2: Verify constraints exist ---
        result = session.run("SHOW CONSTRAINTS")
        print("\n--- Registered constraints ---")
        for record in result:
            print(f"  {record['name']}  |  {record['type']}")

        # --- Step 3: Seed test nodes ---
        with session.begin_transaction() as tx:
            tx.run("MERGE (m:Movie  {movie_id:1})  SET m.title = 'Inception', m.release_year = 2010, m.runtime = 148")
            tx.run("MERGE (p:Person {person_id:1}) SET p.name  = 'Christopher Nolan', p.birth_year = 1970")
            tx.run("MERGE (g:Genre  {genre_id:1})  SET g.name  = 'Sci-Fi'")
            tx.run("MATCH (p:Person {person_id:1}), (m:Movie {movie_id:1}) MERGE (p)-[:DIRECTED {year:2010}]->(m)")
            tx.run("MATCH (m:Movie  {movie_id:1}), (g:Genre {genre_id:1})  MERGE (m)-[:BELONGS_TO]->(g)")
            tx.commit()                          # ← REQUIRED
        print("\nTest data seeded successfully!")

        # --- Step 4: Traversal query — the payoff ---
        result = session.run("""
            MATCH (director:Person)-[:DIRECTED]->(movie:Movie)-[:BELONGS_TO]->(genre:Genre)
            RETURN director.name AS director, movie.title AS movie, genre.name AS genre
        """)
        print("\n--- 2-hop traversal result ---")
        for record in result:
            print(f"  {record['director']}  |  {record['movie']}  |  {record['genre']}")

        # --- Step 5: Cleanup ---
        with session.begin_transaction() as tx:
            tx.run("MATCH (n) WHERE n.person_id = 1 OR n.movie_id = 1 OR n.genre_id = 1 DETACH DELETE n")
            tx.commit()
        print("\nTest data cleaned up (DETACH DELETE)")
