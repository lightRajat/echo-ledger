from rapidfuzz import fuzz

def log(msg: str, debug=False):
    if debug:
        print(f"[DEBUG]: {msg}")
    else:
        print(f"[INFO]: {msg}")

def check_fuzzy_search(text: str, target: str, threshold: int = 80) -> bool:
    text = text.lower().strip()
    target_words = target.lower().split()
    
    for word in target_words:
        word_score = fuzz.partial_ratio(word, text)
        
        if word_score < threshold:
            return False
            
    return True