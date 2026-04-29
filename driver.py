from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "moviepass123")
with GraphDatabase.driver(URI , AUTH) as driver:
    driver.verify_connectivity()

    print("Neo4j connected successfully!")



    with driver.session(database = "neo4j") as session:
        result = session.run("RETURN 'Graph RAG connected!' AS message")
        record = result.single()
        print(record["message"])

        session.run("CREATE (:TestNode {name : 'hello' , create : 1})")
        result = session.run("MATCH (n :TestNode) RETURN n.name AS name")
        for record in result:
            print(record["name"])
        session.run("MATCH (n:TestNode) DELETE n")
        print("TestNode cleaned up")