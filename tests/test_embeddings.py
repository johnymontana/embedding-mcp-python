import pytest
from unittest.mock import Mock, patch
from embeddings_mcp import get_embedding, get_embeddings_batch


class TestEmbeddings:
    """Test cases for embedding functionality."""
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embedding_success(self, mock_embeddings):
        """Test successful single embedding generation."""
        mock_response = {"embedding": [0.1, 0.2, 0.3, 0.4, 0.5]}
        mock_embeddings.return_value = mock_response
        
        result = get_embedding("test text")
        
        assert result == [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_embeddings.assert_called_once_with(model="nomic-embed-text", prompt="test text")
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embedding_custom_model(self, mock_embeddings):
        """Test embedding generation with custom model."""
        mock_response = {"embedding": [0.1, 0.2, 0.3]}
        mock_embeddings.return_value = mock_response
        
        result = get_embedding("test text", model="custom-model")
        
        assert result == [0.1, 0.2, 0.3]
        mock_embeddings.assert_called_once_with(model="custom-model", prompt="test text")
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embedding_error(self, mock_embeddings):
        """Test error handling in single embedding generation."""
        mock_embeddings.side_effect = Exception("Ollama connection error")
        
        with pytest.raises(RuntimeError, match="Failed to generate embedding"):
            get_embedding("test text")
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embeddings_batch_success(self, mock_embeddings):
        """Test successful batch embedding generation."""
        mock_responses = [
            {"embedding": [0.1, 0.2, 0.3]},
            {"embedding": [0.4, 0.5, 0.6]},
            {"embedding": [0.7, 0.8, 0.9]}
        ]
        mock_embeddings.side_effect = mock_responses
        
        texts = ["text1", "text2", "text3"]
        result = get_embeddings_batch(texts)
        
        expected = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]]
        assert result == expected
        assert mock_embeddings.call_count == 3
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embeddings_batch_custom_model(self, mock_embeddings):
        """Test batch embedding generation with custom model."""
        mock_responses = [
            {"embedding": [0.1, 0.2]},
            {"embedding": [0.3, 0.4]}
        ]
        mock_embeddings.side_effect = mock_responses
        
        texts = ["text1", "text2"]
        result = get_embeddings_batch(texts, model="custom-model")
        
        expected = [[0.1, 0.2], [0.3, 0.4]]
        assert result == expected
        mock_embeddings.assert_any_call(model="custom-model", prompt="text1")
        mock_embeddings.assert_any_call(model="custom-model", prompt="text2")
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embeddings_batch_error(self, mock_embeddings):
        """Test error handling in batch embedding generation."""
        mock_embeddings.side_effect = Exception("Ollama connection error")
        
        with pytest.raises(RuntimeError, match="Failed to generate batch embeddings"):
            get_embeddings_batch(["text1", "text2"])
    
    def test_get_embeddings_batch_empty_list(self):
        """Test batch embedding generation with empty input."""
        result = get_embeddings_batch([])
        assert result == []
    
    @patch('embeddings_mcp.ollama.embeddings')
    def test_get_embeddings_batch_single_item(self, mock_embeddings):
        """Test batch embedding generation with single item."""
        mock_response = {"embedding": [0.1, 0.2, 0.3]}
        mock_embeddings.return_value = mock_response
        
        result = get_embeddings_batch(["single text"])
        
        assert result == [[0.1, 0.2, 0.3]]
        mock_embeddings.assert_called_once_with(model="nomic-embed-text", prompt="single text")


class TestInputValidation:
    """Test cases for input validation."""
    
    def test_get_embedding_empty_string(self):
        """Test embedding generation with empty string."""
        with patch('embeddings_mcp.ollama.embeddings') as mock_embeddings:
            mock_response = {"embedding": [0.0, 0.0, 0.0]}
            mock_embeddings.return_value = mock_response
            
            result = get_embedding("")
            assert result == [0.0, 0.0, 0.0]
    
    def test_get_embedding_very_long_text(self):
        """Test embedding generation with very long text."""
        long_text = "A" * 10000
        with patch('embeddings_mcp.ollama.embeddings') as mock_embeddings:
            mock_response = {"embedding": [0.1, 0.2, 0.3]}
            mock_embeddings.return_value = mock_response
            
            result = get_embedding(long_text)
            assert result == [0.1, 0.2, 0.3]