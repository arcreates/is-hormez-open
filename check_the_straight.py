import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike", "fired", "refuses", "redline", "refject", "refuse", "didn't work"]
PEACE_WORDS = ["denies", "avoid", "de-escalation", "end", "talks", "peace", "memorandum", "pause"]

def update_monitor():
    # 1. INITIALIZE EVERYTHING AT THE TOP (The Fix for UnboundLocalError)
    t_wins, i_threats, b_count = 0, 0, 0
    trump_found = False
    iran_found = False
    status_class = "chill"
    last_update = datetime.now().strftime("%I:%M %p")
    
    # 2. LOAD PERSISTENT COUNTERS
    counter_file = 'counters.txt'
    if os.path.exists(counter_file) and os.stat(counter_file).st_size > 0:
        with open(counter_file, 'r') as f:
            try:
                t_wins, i_threats, b_count = map(int, f.read().strip().split('|'))
            except:
                pass # Keeps them at 0 if file is corrupted

    # 3. FETCH NEWS
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(news_url).json()
        articles = response.get('articles', [])[:20]
        primary_headline = articles[0]['title'] if articles else "Intelligence Dark."
    except:
        articles = []
        primary_headline = "Satellite Link Failure."

    # 4. MULTI-SCAN (Now safe because variables are initialized above)
    for art in articles:
        txt = art['title'].lower()
        if not trump_found and "trump" in txt and any(w in txt for w in ["victory", "peace", "memorandum", "open"]):
            t_wins += 1
            trump_found = True
        if not iran_found and "iran" in txt and any(w in txt for w in ["threat", "final", "refuse", "blockade", "procedures"]):
            i_threats += 1
            iran_found = True

    # 5. STATUS LOGIC
    oil_price = round(random.uniform(98.50, 115.00), 2)
    has_danger = any(word in primary_headline.lower() for word in DANGER_WORDS)
    has_peace = any(word in primary_headline.lower() for word in PEACE_WORDS)

    if has_danger and not has_peace:
        status_class, status_text, panic_level, panic_angle = "danger", "PIRACY INTENSIFIES", "CRITICAL", 45
        traffic_flow, hazard_pay = random.randint(4, 7), "+400% (Blood Money)"
        vibe_data = f"{random.randint(1, 3)} Ships (AIS Ghosting)"
        drone_stat = f"{random.randint(12, 30)} (Aggressive Vibe Check)"
        zodiac_stat = f"{random.randint(8, 15)} (Circular Doughnuts)"
        b_count += 1
    elif oil_price > 112 or (has_danger and has_peace):
        status_class, status_text, panic_level, panic_angle = "warning", "Market Volatility", "ELEVATED", 0
        traffic_flow, hazard_pay = random.randint(18, 35), "+120% (Panic Pricing)"
        vibe_data = f"{random.randint(8, 14)} Ships (Tense AF)"
        drone_stat = f"{random.randint(3, 7)} (Shadowing us)"
        zodiac_stat = f"{random.randint(1, 4)} (Following us)"
    else:
        status_class, status_text, panic_level, panic_angle = "chill", "Vessels Moving", "MODERATE", -45
        traffic_flow, hazard_pay = random.randint(45, 62), "Standard (Boring)"
        vibe_data = f"{random.randint(22, 31)} Ships (Cautious)"
        drone_stat = f"{random.randint(0, 1)} (Probably a Seagull)"
        zodiac_stat = "0 (Everyone is Napping)"

    # 6. SAVE & REBUILD
    with open(counter_file, 'w') as f: f.write(f"{t_wins}|{i_threats}|{b_count}")
    
    # ... (Rest of your History Logging and Template Rebuild logic goes here) ...
    # Ensure replacements includes [[t_wins]], [[i_threats]], and [[b_count]]