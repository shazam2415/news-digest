import os
import requests
from datetime import datetime, timedelta

def fetch_news():
    """Fetch cybersecurity AND AI news from NewsAPI"""
    
    api_key = os.getenv('NEWSAPI_KEY')
    
    if not api_key:
        raise ValueError("NEWSAPI_KEY not found in environment variables")
    
    print(f"Using API Key: {api_key[:10]}...")
    
    url = "https://newsapi.org/v2/everything"
    
    # Get articles from the last 7 days
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    from_date = week_ago.strftime('%Y-%m-%d')
    
    # Fetch CYBERSECURITY news
    print("🔒 Fetching cybersecurity news...")
    cybersec_params = {
        'q': 'cybersecurity OR hacking OR breach OR malware OR vulnerability OR infosec OR cyber attack',
        'from': from_date,
        'sortBy': 'popularity',
        'language': 'en',
        'apiKey': api_key,
        'pageSize': 50
    }
    
    # Fetch AI news
    print("🤖 Fetching AI news...")
    ai_params = {
        'q': 'artificial intelligence OR machine learning OR AI OR deep learning OR neural network OR LLM OR ChatGPT',
        'from': from_date,
        'sortBy': 'popularity',
        'language': 'en',
        'apiKey': api_key,
        'pageSize': 50
    }
    
    try:
        cybersec_response = requests.get(url, params=cybersec_params, timeout=10)
        ai_response = requests.get(url, params=ai_params, timeout=10)
        
        cybersec_response.raise_for_status()
        ai_response.raise_for_status()
        
        cybersec_data = cybersec_response.json()
        ai_data = ai_response.json()
        
        if cybersec_data['status'] != 'ok' or ai_data['status'] != 'ok':
            raise Exception("API Error")
        
        # High-quality sources
        quality_sources = {
            'wired',
            'techcrunch',
            'securityweek',
            'bleepingcomputer',
            'the hacker news',
            'zdnet',
            'arstechnica',
            'cyberscoop',
            'darkreading',
            'infosecurity-magazine',
            'cnet',
            'the verge',
            'hackaday',
            'gizmodo.com',
            'theverge',
            'venturebeat',
            'theinformation',
            'artificialintelligence'
        }
        
        all_articles = []
        
        # Process cybersec articles
        for article in cybersec_data['articles']:
            source_name = article['source']['name'].lower()
            has_content = article.get('content') or article.get('description')
            
            if any(qs in source_name for qs in quality_sources) and has_content:
                article['category'] = '🔒 Cybersecurity'
                all_articles.append(article)
        
        # Process AI articles
        for article in ai_data['articles']:
            source_name = article['source']['name'].lower()
            has_content = article.get('content') or article.get('description')
            
            if any(qs in source_name for qs in quality_sources) and has_content:
                article['category'] = '🤖 AI & Machine Learning'
                all_articles.append(article)
        
        # Remove duplicates by URL
        seen = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen:
                seen.add(article['url'])
                unique_articles.append(article)
        
        # Sort by date (newest first)
        unique_articles.sort(key=lambda x: x['publishedAt'], reverse=True)
        
        print(f"✅ Found {len(unique_articles)} total articles (Cybersec + AI)")
        
        return unique_articles
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch news: {str(e)}")
