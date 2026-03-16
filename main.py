import os
import html
from dotenv import load_dotenv
from news_fetcher import fetch_news
from translator import translate_text
from summarizer import summarize_text
from notifier import send_telegram_message

# Load environment variables
load_dotenv()

def main():
    """Main function to orchestrate the news digest workflow"""
    
    print("🚀 Haber Özeti Süreci Başlatılıyor...")
    
    try:
        # Step 1: Fetch news
        print("📰 Haberler Getiriliyor...")
        articles = fetch_news()
        
        if not articles:
            print("❌ Haber Bulunamadı")
            return
        
        print(f"✅ {len(articles)} Haber Bulundu")
        
        # Step 2: Summarize and Translate articles
        print("🤖 Haberler Özetleniyor ve Çeviriliyor...")
        summaries = []
        for i, article in enumerate(articles[:8], 1):  # Top 10 articles
            print(f"   Haber {i} İşleniyor...")
            
            # Get content
            content = article['content'] or article['description']
            
            # Summarize in English first (model is English-only)
            print(f"      Özetleniyor...")
            summary_en = summarize_text(content)
            
            # Translate summary to Turkish
            print(f"      Türkçeye çeviriliyor...")
            summary_tr = translate_text(summary_en, target_lang='tr')
            
            # Translate title to Turkish
            translated_title = translate_text(article['title'], target_lang='tr')
            
            summaries.append({
                'title': translated_title,
                'source': article['source']['name'],
                'url': article['url'],
                'summary': summary_tr,
                'category': article.get('category', '📰 Haber')
            })
        
        # Step 3: Format and send via Telegram
        print("📱 Telegram'a Gönderiliyor...")
        message = format_digest(summaries)
        send_telegram_message(message)
        
        print("✅ Haber Özeti Başarıyla Gönderildi!")
        
    except Exception as e:
        print(f"❌ Hata: {str(e)}")
        error_message = f"❌ Haber Özeti Hatası:\n{str(e)}"
        send_telegram_message(error_message)

def format_digest(summaries):
    """Format summaries into a nice Telegram message in Turkish"""
    message = "📰 *Teknoloji Haber Özeti*\n"
    message += "=" * 20 + "\n"
    message += f"Tarihi: Bugün\n"
    message += "=" * 20 + "\n\n"
    
    current_category = None
    for i, item in enumerate(summaries, 1):
        # Add category header if it changed
        if item['category'] != current_category:
            current_category = item['category']
            # Translate category
            if '🔒' in current_category:
                message += "\n🔒 Siber Güvenlik\n"
            elif '🤖' in current_category:
                message += "\n🤖 Yapay Zeka ve Makine Öğrenmesi\n"
            else:
                message += f"\n{current_category}\n"
            message += "-" * 20 + "\n\n"
        
        # Clean text
        title = clean_text(item['title'])
        source = clean_text(item['source'])
        summary = clean_text(item['summary'][:150])
        
        message += f"{i}. {title}\n"
        message += f"Kaynak: {source}\n"
        message += f"Özet: {summary}...\n"
        message += f"Bağlantı: {item['url']}\n\n"
    
    return message

def clean_text(text):
    """Clean text by removing escape characters and HTML entities"""
    if not text:
        return ""
    
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove backslashes before special characters
    text = text.replace('\\.', '.')
    text = text.replace('\\-', '-')
    text = text.replace('\\*', '*')
    text = text.replace('\\[', '[')
    text = text.replace('\\]', ']')
    text = text.replace('\\(', '(')
    text = text.replace('\\)', ')')
    text = text.replace('\\!', '!')
    text = text.replace('\\#', '#')
    text = text.replace("\\'", "'")
    text = text.replace('\\"', '"')
    
    # Remove extra spaces
    text = ' '.join(text.split())
    
    return text

if __name__ == "__main__":
    main()
