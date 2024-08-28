import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    if isinstance(text, list):
        text = " ".join(text)

    doc = nlp(text)
    noun_chunks = [chunk.text for chunk in doc.noun_chunks]

    if not noun_chunks:
        return []
    
        
    keywords = [chunk.text for chunk in doc.noun_chunks]
    return keywords
