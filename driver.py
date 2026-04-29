from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "moviepass123")
driver = GraphDatabase.driver(URI , auth = AUTH)

driver.verify_connectivity()

with driver.session(database = "neo4j") as session:
    result = session.run("RETURN 'Graph RAG connected!' AS message")
    record = result.single()
    print(record["message"])

    session.run("CREATE (:TestNode {name : 'hello' , create : 1})")
    result = session.run("MATCH (n:TestNode) RETURN n.name AS name")
    for record in result:
        print(record["name"])