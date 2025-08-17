# Testing with MCP Inspector

This guide covers how to test the Embeddings MCP Server using the MCP Inspector tool.

## Prerequisites

1. **Ollama Running**: Ensure Ollama is running with an embedding model
   ```bash
   ollama serve
   ollama pull nomic-embed-text
   ```

2. **MCP Inspector**: Install the inspector tool
   ```bash
   npm install -g @modelcontextprotocol/inspector
   ```

## Step-by-Step Testing

### 1. Start the MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

This will open a web interface, typically at `http://localhost:5173`.

### 2. Configure the Server

In the inspector interface:

1. **Server Command**: `uv`
2. **Arguments**: `["run", "embeddings-mcp"]`
3. **Working Directory**: `/absolute/path/to/embeddings-mcp`
4. Click **"Connect"**

### 3. Verify Connection

Once connected, you should see:
- Server status: **Connected**
- Available tools: `get_embedding` and `get_embeddings_batch`

### 4. Test the Tools

#### Test `get_embedding`

1. Select the `get_embedding` tool
2. Fill in the parameters:
   ```json
   {
     "text": "This is a test sentence for embedding.",
     "model": "nomic-embed-text"
   }
   ```
3. Click **"Call Tool"**
4. Verify the response contains a list of floating-point numbers

#### Test `get_embeddings_batch`

1. Select the `get_embeddings_batch` tool
2. Fill in the parameters:
   ```json
   {
     "texts": [
       "First test sentence",
       "Second test sentence", 
       "Third test sentence"
     ],
     "model": "nomic-embed-text"
   }
   ```
3. Click **"Call Tool"**
4. Verify the response contains an array of embedding arrays

### 5. Test Error Cases

#### Test with Invalid Model
```json
{
  "text": "Test text",
  "model": "non-existent-model"
}
```
Should return an error message about the unavailable model.

#### Test with Empty Text
```json
{
  "text": "",
  "model": "nomic-embed-text"
}
```
Should still work and return an embedding.

## Expected Results

### Successful `get_embedding` Response
```json
{
  "content": [
    {
      "type": "text",
      "text": "[0.1234, -0.5678, 0.9012, ...]"
    }
  ],
  "isError": false
}
```

### Successful `get_embeddings_batch` Response
```json
{
  "content": [
    {
      "type": "text", 
      "text": "[[0.1234, -0.5678, ...], [0.2345, -0.6789, ...], ...]"
    }
  ],
  "isError": false
}
```

### Error Response
```json
{
  "content": [
    {
      "type": "text",
      "text": "RuntimeError: Failed to generate embedding: ..."
    }
  ],
  "isError": true
}
```

## Troubleshooting

### Common Issues

1. **"Connection refused" error**
   - Ensure Ollama is running: `ollama serve`
   - Check if the service is accessible: `curl http://localhost:11434`

2. **"Model not found" error**
   - Pull the required model: `ollama pull nomic-embed-text`
   - Verify available models: `ollama list`

3. **"Server failed to start" error**
   - Check the working directory path is correct
   - Ensure all dependencies are installed: `uv sync`
   - Verify the server can run standalone: `uv run embeddings-mcp`

### Debug Mode

For additional debugging, you can run the server with verbose logging:

```bash
# Set log level to debug
export PYTHONPATH=/path/to/embeddings-mcp/src
uv run python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from embeddings_mcp import main
main()
"
```

## Performance Notes

- **Single vs Batch**: Use `get_embeddings_batch` for multiple texts to reduce overhead
- **Model Choice**: Larger models provide better quality but slower performance
- **Caching**: Consider implementing caching for frequently requested embeddings
- **Concurrency**: The server handles one request at a time; for high throughput, consider running multiple instances