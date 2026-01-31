"""
Web Crawler Module
Crawls website pages and extracts text content
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from typing import Set, List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebCrawler:
    def __init__(self, base_url: str, max_pages: int = 50):
        """
        Initialize web crawler
        
        Args:
            base_url: Starting URL to crawl
            max_pages: Maximum number of pages to crawl
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.pages: List[Dict[str, str]] = []
        self.domain = urlparse(base_url).netloc
        
    def is_valid_url(self, url: str) -> bool:
        """Check if URL belongs to the same domain"""
        try:
            parsed = urlparse(url)
            return parsed.netloc == self.domain and parsed.scheme in ['http', 'https']
        except:
            return False
    
    def extract_text_from_html(self, html: str) -> str:
        """Extract text content from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        return text
    
    def fetch_page(self, url: str) -> tuple[str, bool]:
        """
        Fetch a page from URL
        
        Returns:
            Tuple of (content, success_flag)
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            response.raise_for_status()
            return response.text, True
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return "", False
    
    def get_links_from_page(self, html: str, page_url: str) -> List[str]:
        """Extract all links from HTML page"""
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            url = urljoin(page_url, link['href'])
            # Remove fragments
            url = url.split('#')[0]
            
            if self.is_valid_url(url) and url not in self.visited_urls:
                links.append(url)
        
        return links
    
    def crawl(self) -> List[Dict[str, str]]:
        """
        Main crawl function
        
        Returns:
            List of pages with url and content
        """
        to_visit = [self.base_url]
        
        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
            
            logger.info(f"Crawling: {url} ({len(self.visited_urls) + 1}/{self.max_pages})")
            
            html, success = self.fetch_page(url)
            if not success:
                continue
            
            self.visited_urls.add(url)
            
            # Extract text
            text = self.extract_text_from_html(html)
            
            if text.strip():
                self.pages.append({
                    'url': url,
                    'content': text
                })
            
            # Get links for further crawling
            new_links = self.get_links_from_page(html, url)
            to_visit.extend(new_links)
        
        logger.info(f"Crawling completed. Total pages: {len(self.pages)}")
        return self.pages
