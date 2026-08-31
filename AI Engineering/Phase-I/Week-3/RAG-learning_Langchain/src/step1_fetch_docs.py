"""
STEP 1: Document Fetching
Same as before - LangChain doesn't handle web scraping.
"""

import httpx
from bs4 import BeautifulSoup
from pathlib import Path
import time

def fetch_page(url: str) -> str:
    """Fetch a single web page."""
    print(f"📥 Fetching: {url}")
    
    response = httpx.get(url, timeout=10.0)
    
    if response.status_code == 200:
        print(f"✅ Success! Got {len(response.text)} characters")
        return response.text
    else:
        print(f"❌ Failed with status {response.status_code}")
        return ""

def extract_text_from_html(html: str) -> str:
    """Extract clean text from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove unwanted elements
    for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
        element.decompose()
    
    # Get text from main content
    main_content = soup.find('main') or soup.find('article') or soup.body
    
    if main_content:
        text = main_content.get_text(separator='\n', strip=True)
        return text
    
    return ""

def save_document(url: str, text: str, output_dir: Path, index: int):
    """Save document to disk."""
    filename = f"doc_{index:03d}.txt"
    filepath = output_dir / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"SOURCE: {url}\n")
        f.write("=" * 80 + "\n\n")
        f.write(text)
    
    print(f"💾 Saved to: {filename}")
    print(f"📊 Length: {len(text)} characters\n")

def main():
    print("=" * 80)
    print("STEP 1: Document Fetching")
    print("=" * 80)
    print()
    
    # Create output directory
    output_dir = Path("RAG-learning_Langchain/data/step1")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Spark documentation URLs
    urls = [
        "https://spark.apache.org/docs/latest/rdd-programming-guide.html",
        "https://spark.apache.org/docs/latest/sql-programming-guide.html",
        "https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html",
        "https://spark.apache.org/docs/latest/configuration.html",
        "https://spark.apache.org/docs/latest/tuning.html",
        "https://spark.apache.org/docs/latest/api/python/getting_started/quickstart.html",
        "https://spark.apache.org/docs/latest/sql-getting-started.html",
        "https://spark.apache.org/docs/latest/spark-standalone.html",
        "https://spark.apache.org/docs/latest/submitting-applications.html",
        "https://spark.apache.org/docs/latest/streaming-programming-guide.html"
    ]
    
    print(f"📚 Will fetch {len(urls)} pages\n")
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]")
        
        html = fetch_page(url)
        if not html:
            continue
        
        text = extract_text_from_html(html)
        if not text:
            continue
        
        save_document(url, text, output_dir, i)
        
        if i < len(urls):
            time.sleep(1)  # Be nice to the server
    
    print("=" * 80)
    print("✅ COMPLETE!")
    print("=" * 80)
    print(f"\n📁 Documents saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    main()