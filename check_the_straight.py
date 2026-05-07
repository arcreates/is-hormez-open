import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike", "fired", "refuses", "redline", "refject", "refuse", "didn't work"]
PEACE_WORDS = ["denies", "avoid", "de-escalation", "end", "talks", "peace", "memorandum", "pause"]

def update_monitor():
    # 1. Initialize variables
    t_wins, i_threats, b_count = 0, 0, 0
    trump_found, iran_found = False, False
    
    # Get current path to ensure we are hitting the right files
    base_path = os.path.dirname(os.path.abspath(__file__))
    counter_file = os.path.join(base_path, 'counters.txt')
    template_file = os.path.join(base_path, 'template.html')
    output_file = os.path.join(base_path, 'index.html')

    # 2. Load counters
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as f:
            try:
                t_wins, i_threats, b_count = map(int, f.read().strip().split('|'))
            except: pass

    # 3. News Logic
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    try:
        r = requests.get(news_url).json()
        articles = r.get('articles', [])[:20]
        headline = articles[0]['title'] if articles else "No Intel Found."
    except:
        articles, headline = [], "Link Down."

    # 4. Counter Update
    for art in articles:
        txt = art['title'].lower()
        if not trump_found and "trump" in txt and any(w in txt for w in ["victory", "peace", "memorandum", "open"]):
            t_wins += 1
            trump_found = True
        if not iran_found and "iran" in txt and any(w in txt for w in ["threat", "final", "refuse", "blockade"]):
            i_threats += 1
            iran_found = True

    # 5. BUILD THE PAGE
    if os.path.exists(template_file):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # This dictionary MUST include every [[tag]] in your HTML
        replacements = {
            "[[status_class]]": status_class,
            "[[status_text]]": status_text,
            "[[panic_level]]": panic_level,
            "[[panic_angle]]": str(panic_angle),
            "[[latest_headline]]": headline,
            "[[last_update]]": datetime.now().strftime("%H:%M"),
            "[[t_wins]]": str(t_wins),
            "[[i_threats]]": str(i_threats),
            "[[b_count]]": str(b_count),
            "[[oil_price]]": str(oil_price),
            "[[traffic_flow]]": str(traffic_flow),
            "[[hazard_pay]]": hazard_pay,
            "[[vibe_data]]": vibe_data,
            "[[drone_stat]]": drone_stat,
            "[[zodiac_stat]]": zodiac_stat,
            "[[meme_quote]]": random.choice(["'They call us pirates. I call us stationary.'", "'Watching the sunset. If only the radar was this pretty.'"]),
            "[[history_rows]]": recent_history,
            "[[insurance_risk]]": "MODERATE" if oil_price < 110 else "HIGH", # Placeholder logic
            "[[pirate_tax]]": "$12,400" if status_class == "danger" else "$0" # Placeholder logic
        }

        # The Magic Loop: replaces EVERY tag automatically
        for tag, value in replacements.items():
            content = content.replace(tag, str(value))

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Save counters back
        with open(counter_file, 'w') as f:
            f.write(f"{t_wins}|{i_threats}|{b_count}")

if __name__ == "__main__":
    update_monitor()