"""
Unit tests for RAG Q&A Bot modules
"""

import unittest
from src.text_cleaner import TextCleaner
from src.crawler import WebCrawler


class TestTextCleaner(unittest.TestCase):
    """Test text cleaning and chunking"""
    
    def setUp(self):
        self.cleaner = TextCleaner(chunk_size=100, overlap=20)
    
    def test_clean_text(self):
        """Test text cleaning"""
        dirty_text = "Hello   world!!!   This   is   a   test."
        cleaned = self.cleaner.clean_text(dirty_text)
        self.assertNotIn("   ", cleaned)
        self.assertTrue(len(cleaned) > 0)
    
    def test_chunk_text(self):
        """Test text chunking"""
        text = "This is a test sentence. This is another test sentence. " * 5
        chunks = self.cleaner.chunk_text(text, chunk_size=100)
        self.assertTrue(len(chunks) > 1)
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 150)  # Allow some margin
    
    def test_process_documents(self):
        """Test document processing"""
        documents = [
            {
                'url': 'http://example.com/1',
                'title': 'Test Page 1',
                'content': 'This is test content. ' * 20
            },
            {
                'url': 'http://example.com/2',
                'title': 'Test Page 2',
                'content': 'Another test content. ' * 20
            }
        ]
        processed = self.cleaner.process_documents(documents)
        self.assertGreater(len(processed), 0)
        for doc in processed:
            self.assertIn('url', doc)
            self.assertIn('content', doc)
            self.assertIn('chunk_index', doc)


class TestWebCrawler(unittest.TestCase):
    """Test web crawler"""
    
    def setUp(self):
        self.crawler = WebCrawler('http://example.com', max_pages=5, delay=1)
    
    def test_is_valid_url(self):
        """Test URL validation"""
        # Valid URLs
        self.assertTrue(self.crawler.is_valid_url('http://example.com/page'))
        self.assertTrue(self.crawler.is_valid_url('https://example.com/about'))
        
        # Invalid URLs
        self.assertFalse(self.crawler.is_valid_url('http://other.com/page'))
        self.assertFalse(self.crawler.is_valid_url('http://example.com/logout'))
        self.assertFalse(self.crawler.is_valid_url('http://example.com/test.pdf'))


if __name__ == '__main__':
    unittest.main()
