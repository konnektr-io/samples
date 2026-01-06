import os
import asyncio
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

# 1. Configuration
MCP_SERVER_URL = os.getenv("KONNEKTR_MCP_URL")  # Or your local/hosted endpoint

# 2. Define the MCP Toolset
# This automatically discovers tools exposed by your Konnektr MCP Server
# e.g., 'query_graph', 'search_vectors', 'get_neighbors'
konnektr_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_SERVER_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    ),
    # Optional: Whitelist specific tools if you don't want to expose everything
    # tool_filter=["query_graph", "find_path", "get_node_details"]
)

# 3. Define the Agent
# We give Gemini strict instructions to rely on the graph for factual queries.
graph_agent = Agent(
    model="gemini-2.0-flash",  # Fast, multimodal model
    name="konnektr_memory_agent",
    description="An AI assistant with structured graph memory.",
    instruction="""
    You are an AI Agent with Structured Graph Memory. You use the Konnektr MCP server to manage knowledge.

    MEMORY STORAGE RULES:
    1. SEMANTIC GRAPH: All knowledge is stored as entities (with properties) and relationships in a graph database. Only data aligned with the ontology can be stored.
    2. ONTOLOGY: Use existing ontology (use 'list_models' and 'get_model' for more details) or create/extend existing ontology as needed ('create_model').
    3. NEW ENTITIES: When you learn about a new entity (e.g., "New pump installed"), use 'create_or_replace_digital_twin' to add it to the graph and use 
        'create_or_replace_relationship' to add relationships.
    4. FACTUAL STORAGE: When you learn a new fact about an existing entity (e.g., "Pump-01 is vibrating"), use 'update_digital_twin' with a patch.
    5. CONTEXTUAL STORAGE: Use the 'embedding_properties' parameter (on 'create_or_replace_digital_twin' or 'async def update_digital_twin_embeddings') 
        to store contextual embeddings (the server will handle vectorization).

    MEMORY RETRIEVAL & REASONING RULES:
    1. ONTOLOGY EXPLORATION: Use 'list_models' and 'get_model' to understand the structure of the knowledge graph.
    2. SEARCH: When the user asks a fuzzy question (e.g., "What's wrong with the cooling?"), use 'search_twins' or 'search_models'.
    3. REASONING: After a search, use 'query_graph' to see how the results are connected.

    
    Example:
    User: "Who maintains the cooling pump?"
    You: [Call query_graph("MATCH (p:Pump)-[:MAINTAINED_BY]->(t:Team) WHERE p.name='Cooling' RETURN t")]
    """,
    tools=[konnektr_tools],
)


# 4. Run the Agent (Local Test)
async def main():
    print(f"🔗 Connecting to Konnektr MCP at {MCP_SERVER_URL}...")

    # Start a session
    session = await graph_agent.start_session()

    query = "What dependencies will break if I restart Server-01?"
    print(f"\nUser: {query}")

    async for event in session.send(query):
        if event.text:
            print(f"Agent: {event.text}")
        if event.tool_call:
            print(f"🛠️ Tool Call: {event.tool_call.name} -> {event.tool_call.args}")


if __name__ == "__main__":
    asyncio.run(main())
