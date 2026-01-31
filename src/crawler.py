"""
Web Crawler Module
Crawls website pages and extracts content
"""
import json
import time
from typing import Set, List, Dict
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebCrawler:
    """
    Crawls website pages and extracts content
    """
    
    def __init__(self, base_url: str, max_pages: int = 50, delay: float = 1):
        """
        Initialize crawler
        
        Args:
            base_url: Starting URL to crawl
            max_pages: Maximum number of pages to crawl
            delay: Delay between requests in seconds
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.delay = delay
        self.visited_urls: Set[str] = set()
        self.crawled_data: List[Dict] = []
        self.base_domain = urlparse(base_url).netloc
        
    def is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid and belongs to the same domain
        """
        try:
            parsed = urlparse(url)
            # Check if domain matches
            if parsed.netloc != self.base_domain:
                return False
            # Exclude common non-content pages
            exclude_patterns = ['.pdf', '.zip', '.exe', 'logout', 'login', '#']
            for pattern in exclude_patterns:
                if pattern in url.lower():
                    return False
            return parsed.scheme in ['http', 'https']
        except:
            return False
    
    def extract_content(self, html: str, url: str) -> Dict:
        """
        Extract text content from HTML
        
        Args:
            html: HTML content
            url: URL of the page
            
        Returns:
            Dictionary with title, content, and metadata
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'footer']):
            script.decompose()
        
        # Extract title
        title = soup.title.string if soup.title else "No Title"
        
        # Extract main content
        # Try to find main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
        
        return {
            'url': url,
            'title': title,
            'content': text,
            'timestamp': time.time()
        }
    
    def crawl(self) -> List[Dict]:
        """
        Crawl the website
        
        Returns:
            List of crawled pages with content
        """
        to_visit = [self.base_url]
        
        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            self.visited_urls.add(url)
            
            try:
                logger.info(f"Crawling: {url}")
                
                # Fetch page
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Extract content
                page_data = self.extract_content(response.text, url)
                self.crawled_data.append(page_data)
                
                # Extract and queue new URLs
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    
                    # Remove fragments
                    absolute_url = absolute_url.split('#')[0]
                    
                    if self.is_valid_url(absolute_url) and absolute_url not in self.visited_urls:
                        to_visit.append(absolute_url)
                
                # Respect crawl delay
                time.sleep(self.delay)
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error crawling {url}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error for {url}: {e}")
        
        logger.info(f"Crawling completed. Pages crawled: {len(self.crawled_data)}")
        return self.crawled_data
    
    def save_to_file(self, filepath: str):
        """
        Save crawled data to JSON file
        """
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.crawled_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Data saved to {filepath}")


def crawl_website(url: str, max_pages: int = 50, delay: float = 1) -> List[Dict]:
    """
    Convenience function to crawl a website
    """
    crawler = WebCrawler(url, max_pages, delay)
    return crawler.crawl()
