from transformers import pipeline

def summarize_text(text, max_length=100, min_length=30):
    """Summarize text using Hugging Face transformers"""
    
    if not text:
        return "No content available"
    
    # Limit text length to avoid API issues (max 1024 tokens)
    text = text[:1024]
    
    try:
        # Use BART model for summarization
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Generate summary
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        
        return summary[0]['summary_text']
        
    except Exception as e:
        print(f"⚠️ Summarization error: {str(e)}")
        # Fallback: return first 150 characters
        return text[:150] + "..."
