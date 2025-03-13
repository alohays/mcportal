"""
Command-line interface for MCPortal
"""
import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from mcportal import MCPServer, Tracer
from mcportal.tools import OpenAIBuiltInTools

app = typer.Typer(help="MCPortal - Bridge between MCP protocol and OpenAI tools")
console = Console()

@app.command("server")
def start_server(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on"),
    tracing: bool = typer.Option(True, "--tracing/--no-tracing", help="Enable tracing"),
    tools: str = typer.Option("web_search", "--tools", "-t", help="Comma-separated list of tools to enable"),
):
    """Start the MCPortal server."""
    console.print(Panel.fit("Starting MCPortal Server", title="MCPortal"))
    
    # Set up tracing if enabled
    tracer = None
    if tracing:
        tracer = Tracer()
        console.print(f"[green]Tracing enabled with ID:[/green] {tracer.current_trace_id}")
    
    # Create the server
    server = MCPServer(tracer=tracer)
    
    # Register the requested tools
    tool_list = tools.split(",")
    for tool_name in tool_list:
        tool_name = tool_name.strip().upper()
        try:
            tool = getattr(OpenAIBuiltInTools, tool_name)
            server.register_tools(tool)
            console.print(f"[green]Registered tool:[/green] {tool_name}")
        except AttributeError:
            console.print(f"[red]Unknown tool:[/red] {tool_name}")
    
    # Start the server
    console.print(f"[green]Starting server on[/green] {host}:{port}")
    server.start(host=host, port=port)

@app.command("dashboard")
def start_dashboard(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    port: int = typer.Option(3000, "--port", "-p", help="Port to listen on"),
):
    """Start the MCPortal visualization dashboard."""
    console.print(Panel.fit("Starting MCPortal Dashboard", title="MCPortal"))
    console.print(f"[green]Dashboard available at:[/green] http://{host}:{port}")
    console.print("[yellow]Note:[/yellow] This is a placeholder for the actual dashboard implementation")
    
    # This would launch the visualization dashboard in the actual implementation
    console.print("\nPlaceholder for dashboard. Press Ctrl+C to exit.")
    try:
        # Keep the process running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[green]Dashboard stopped[/green]")

@app.command("version")
def version():
    """Show the MCPortal version."""
    from mcportal import __version__
    console.print(f"MCPortal version: {__version__}")

if __name__ == "__main__":
    app()
