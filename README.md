# Embeddings MCP Server

A Model Context Protocol (MCP) server that provides text embedding capabilities using Ollama. This server exposes tools for generating embeddings from text strings, supporting both single text inputs and batch processing.

## Features

- **Single Text Embedding**: Generate embeddings for individual text strings
- **Batch Text Embedding**: Process multiple texts efficiently in a single request
- **Ollama Integration**: Uses Ollama for local embedding model execution
- **Configurable Models**: Support for different embedding models available in Ollama
- **Type Safety**: Full type hints and validation using Pydantic
- **Error Handling**: Comprehensive error handling with informative messages

## Prerequisites

1. **Ollama**: Install and run Ollama on your system
   ```bash
   # Install Ollama (macOS)
   brew install ollama
   
   # Start Ollama service
   ollama serve
   
   # Pull an embedding model (recommended)
   ollama pull nomic-embed-text
   ```

2. **Python 3.10+**: Required for the MCP server

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd embeddings-mcp

# Install dependencies
uv sync

# Install the package
uv pip install -e .
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd embeddings-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

## Running the Server

### Direct execution
```bash
uv run embeddings-mcp
```

**Note**: The server runs and waits for MCP protocol messages on stdin/stdout. This is normal behavior for MCP servers.

### Testing the Server

You can test that the server is working correctly by sending MCP protocol messages:

```bash
# Test initialization
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}' | uv run embeddings-mcp

# Test tool listing (requires proper MCP handshake)
(echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}'; echo '{"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}'; echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}') | uv run embeddings-mcp
```

The server should respond with proper MCP protocol messages and list the available tools.

### Running Over HTTP

The server also supports HTTP transport mode for integration with web-based MCP clients:

```bash
# Start HTTP server on default port 8000
uv run embeddings-mcp --transport http

# Start HTTP server on custom host and port
uv run embeddings-mcp --transport http --host 0.0.0.0 --port 9000

# View available options
uv run embeddings-mcp --help
```

**HTTP Endpoint**: The MCP server is available at `/mcp` endpoint.

**Note**: HTTP mode requires clients to accept both `application/json` and `text/event-stream` content types.

## Available Tools

### `get_embedding`
Generate an embedding for a single text string.

**Parameters:**
- `text` (str): The text to generate an embedding for
- `model` (str, optional): The Ollama model to use (default: "nomic-embed-text")

**Returns:** List[float] - The embedding vector

### `get_embeddings_batch`
Generate embeddings for multiple text strings.

**Parameters:**
- `texts` (List[str]): A list of texts to generate embeddings for
- `model` (str, optional): The Ollama model to use (default: "nomic-embed-text")

**Returns:** List[List[float]] - A list of embedding vectors

## MCP Client Configuration

### Claude Desktop

Add the following to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "embeddings": {
      "command": "uv",
      "args": ["run", "embeddings-mcp"],
      "cwd": "/Users/lyonwj/github/johnymontana/embeddings-mcp"
    }
  }
}
```

**Note**: Replace the `cwd` path with the actual path to your embeddings-mcp directory.

**For HTTP transport** (if your client supports it):
```json
{
  "mcpServers": {
    "embeddings": {
      "command": "uv",
      "args": ["run", "embeddings-mcp", "--transport", "http", "--port", "8000"],
      "cwd": "/Users/lyonwj/github/johnymontana/embeddings-mcp"
    }
  }
}
```

### Cursor

Add to your Cursor settings:

```json
{
  "mcp.servers": {
    "embeddings": {
      "command": "uv",
      "args": ["run", "embeddings-mcp"],
      "cwd": "/Users/lyonwj/github/johnymontana/embeddings-mcp"
    }
  }
}
```

**Note**: Replace the `cwd` path with the actual path to your embeddings-mcp directory.

### Windsurf

Configure in Windsurf settings:

```json
{
  "mcp": {
    "servers": {
      "embeddings": {
        "command": "uv",
        "args": ["run", "embeddings-mcp"],
        "cwd": "/Users/lyonwj/github/johnymontana/embeddings-mcp"
      }
    }
  }
}
```

**Note**: Replace the `cwd` path with the actual path to your embeddings-mcp directory.

### Zed

Add to your Zed configuration:

```json
{
  "language_models": {
    "mcp_servers": {
      "embeddings": {
        "command": "uv",
        "args": ["run", "embeddings-mcp"],
        "cwd": "/Users/lyonwj/github/johnymontana/embeddings-mcp"
      }
    }
  }
}
```

**Note**: Replace the `cwd` path with the actual path to your embeddings-mcp directory.

### Continue.dev

Configure in your Continue.dev config:

```json
{
  "mcpServers": {
    "embeddings": {
      "command": "uv",
      "args": ["run", "embeddings-mcp"],
      "cwd": "/Users/lyonwj/github/johnymontana/embeddings-mcp"
    }
  }
}
```

**Note**: Replace the `cwd` path with the actual path to your embeddings-mcp directory.

## Testing with MCP Inspector

The MCP Inspector is a useful tool for testing MCP servers during development.

### Installation
```bash
npm install -g @modelcontextprotocol/inspector
```

### Usage
```bash
# Start the inspector
npx @modelcontextprotocol/inspector

# In the inspector interface:
# 1. Add server with command: uv run embeddings-mcp
# 2. Set working directory to: /Users/lyonwj/github/johnymontana/embeddings-mcp
# 3. Connect to the server
# 4. Test the available tools:
#    - get_embedding
#    - get_embeddings_batch

**Note**: Replace the working directory path with the actual path to your embeddings-mcp directory.

**For HTTP testing**, you can also use the MCP Inspector with HTTP transport:
# 1. Start the server: uv run embeddings-mcp --transport http --port 8000
# 2. In the inspector, use HTTP transport mode and connect to http://127.0.0.1:8001/mcp
```

The inspector provides a web interface where you can:
- View available tools and their schemas
- Test tool calls with sample inputs
- Inspect request/response messages
- Debug server behavior

## Testing

### Run Tests
```bash
uv run pytest
```

### Run Tests with Verbose Output
```bash
uv run pytest -v
```

## Development

### Setting up Development Environment
```bash
# Clone and install in development mode
git clone <repository-url>
cd embeddings-mcp
uv sync --dev

# Run tests
uv run pytest
```

### Project Structure
```
embeddings-mcp/
  src/embeddings_mcp/
    __init__.py          # Main MCP server implementation
  tests/
    test_embeddings.py   # Test suite
  pyproject.toml           # Project configuration
  pytest.ini              # Test configuration
  README.md               # This file
```

## Supported Embedding Models

This server works with any embedding model available in Ollama. Popular options include:

- `nomic-embed-text` (default) - General purpose text embeddings
- `mxbai-embed-large` - High-quality embeddings
- `all-minilm` - Lightweight embeddings

To use a different model, ensure it's available in Ollama:
```bash
ollama list
ollama pull <model-name>
```

## Error Handling

The server includes comprehensive error handling:

- **Connection Errors**: If Ollama is not running or accessible
- **Model Errors**: If the specified model is not available
- **Input Validation**: For malformed or invalid inputs
- **Runtime Errors**: For any unexpected issues during processing

All errors are logged and returned as structured error messages to the MCP client.

## Troubleshooting

### Common Issues

1. **Server exits immediately**: This is normal behavior. The MCP server waits for input on stdin/stdout.

2. **"a coroutine was expected" error**: This was a bug in earlier versions that has been fixed. Make sure you're using the latest version.

3. **Ollama connection errors**: Ensure Ollama is running (`ollama serve`) and the specified model is available (`ollama list`).

4. **Permission errors**: Make sure you have the necessary permissions to run the server and access Ollama.

5. **Model not found**: Pull the required model first: `ollama pull nomic-embed-text`

### Verifying Installation

Run the tests to ensure everything is working:
```bash
uv run pytest
```

All tests should pass, indicating the server is properly configured.

## Example Usage

Once configured in your MCP client, you can use the tools like this:

```javascript
// Single embedding
const embedding = await get_embedding({
  text: "Hello, world!",
  model: "nomic-embed-text"
});

// Batch embeddings
const embeddings = await get_embeddings_batch({
  texts: ["First text", "Second text", "Third text"],
  model: "nomic-embed-text"
});
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.