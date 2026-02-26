from rapidfuzz import fuzz

def log(msg: str):
    print(f"[INFO]: {msg}")

def check_fuzzy_search(text: str, target: str, threshold: int = 80) -> bool:
    text = text.lower().strip()
    target = target.lower().strip()

    verb = target.split()[0]
    
    score = fuzz.token_set_ratio(target, text)
    
    if verb not in text and fuzz.partial_ratio(verb, text) < 90:
        return False

    return score >= threshold