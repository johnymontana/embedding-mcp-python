import asyncio
import logging
import argparse
from typing import Any, List

import ollama
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("embeddings-mcp")

logger = logging.getLogger(__name__)


@mcp.tool()
def get_embedding(text: str, model: str = "nomic-embed-text") -> List[float]:
    """
    Generate an embedding for a single text string using Ollama.
    
    Args:
        text: The text to generate an embedding for
        model: The Ollama model to use (default: nomic-embed-text)
    
    Returns:
        A list of floating point numbers representing the embedding vector
    """
    try:
        response = ollama.embeddings(model=model, prompt=text)
        return response["embedding"]
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise RuntimeError(f"Failed to generate embedding: {str(e)}")


@mcp.tool()
def get_embeddings_batch(texts: List[str], model: str = "nomic-embed-text") -> List[List[float]]:
    """
    Generate embeddings for multiple text strings using Ollama.
    
    Args:
        texts: A list of texts to generate embeddings for
        model: The Ollama model to use (default: nomic-embed-text)
    
    Returns:
        A list of embedding vectors, one for each input text
    """
    try:
        embeddings = []
        for text in texts:
            response = ollama.embeddings(model=model, prompt=text)
            embeddings.append(response["embedding"])
        return embeddings
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {e}")
        raise RuntimeError(f"Failed to generate batch embeddings: {str(e)}")


def main() -> None:
    """Run the MCP server."""
    parser = argparse.ArgumentParser(description="Embeddings MCP Server")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "http"], 
        default="stdio",
        help="Transport mode: stdio (default) or http"
    )
    parser.add_argument(
        "--host", 
        default="127.0.0.1",
        help="Host for HTTP server (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for HTTP server (default: 8000)"
    )
    
    args = parser.parse_args()
    
    if args.transport == "http":
        logger.info(f"Starting HTTP server on {args.host}:{args.port}")
        import uvicorn
        app = mcp.streamable_http_app()
        uvicorn.run(app, host=args.host, port=args.port)
    else:
        logger.info("Starting stdio server")
        mcp.run()
