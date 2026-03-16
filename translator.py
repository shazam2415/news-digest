import translators as ts

def translate_text(text, target_lang='tr', source_lang='en'):
    """Translate text to target language"""
    
    if not text:
        return ""
    
    # Limit text length
    text = text[:500]
    
    try:
        # Use translators library
        translation = ts.translate_text(text, from_language=source_lang, to_language=target_lang)
        return translation
    except Exception as e:
        print(f"⚠️ Translation error: {str(e)}")
        return text  # Return original if translation fails
