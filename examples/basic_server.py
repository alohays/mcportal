"""
Basic example of using MCPortal to create an MCP server with OpenAI tools
"""
import os
import sys

# Add the parent directory to the path to import mcportal in development
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mcportal import MCPServer, Tracer
from mcportal.tools import OpenAIBuiltInTools

def main():
    # Initialize a tracer
    tracer = Tracer()
    print(f"Initialized tracer with ID: {tracer.current_trace_id}")
    
    # Create a server with the tracer
    server = MCPServer(tracer=tracer)
    
    # Register some OpenAI built-in tools
    server.register_tools(OpenAIBuiltInTools.WEB_SEARCH)
    server.register_tools(OpenAIBuiltInTools.CODE_INTERPRETER)
    
    # Create a custom handler for the web search tool
    def custom_web_search_handler(params):
        query = params.get("query", "")
        print(f"Custom web search handler called with query: {query}")
        return {
            "results": [
                {
                    "title": f"Custom result for {query}",
                    "url": f"https://example.com/search?q={query}",
                    "snippet": f"This is a custom result for the query: {query}"
                }
            ]
        }
    
    # Set the custom handler for the web search tool
    OpenAIBuiltInTools.WEB_SEARCH.set_handler(custom_web_search_handler)
    
    # Start the server
    print("Starting server on 127.0.0.1:8000")
    server.start(host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
