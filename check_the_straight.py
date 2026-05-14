import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike", "fired", "refuses", "redline", "reject", "attacked"]
PEACE_WORDS = ["avoid", "de-escalation", "end", "peace", "memorandum", "pause"]

def update_monitor():
    # 1. SET DEFAULTS (Prevents NameErrors)
    status_class, status_text = "chill", "Vessels Moving"
    panic_level, panic_angle = "MODERATE", -45
    oil_price = round(random.uniform(98.50, 102.00), 2)
    traffic_flow, hazard_pay = random.randint(45, 62), "Standard"
    vibe_data = f"{random.randint(22, 31)} Ships"
    drone_stat, zodiac_stat = "0", "0"
    t_wins, i_threats, b_count = 0, 0, 0
    trump_found, iran_found = False, False
    headline = "No new intel reported."
    recent_history = ""

    base_path = os.path.dirname(os.path.abspath(__file__))
    counter_file = os.path.join(base_path, 'counters.txt')
    history_file = os.path.join(base_path, 'history.txt')
    template_file = os.path.join(base_path, 'template.html')
    output_file = os.path.join(base_path, 'index.html')

    # 2. LOAD SAVED COUNTERS
    if os.path.exists(counter_file) and os.stat(counter_file).st_size > 0:
        with open(counter_file, 'r') as f:
            try:
                vals = f.read().strip().split('|')
                t_wins, i_threats, b_count = int(vals[0]), int(vals[1]), int(vals[2])
            except: pass

    # 3. FETCH NEWS & SCOREBOARD LOGIC
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    try:
        r = requests.get(news_url).json()
        articles = r.get('articles', [])[:20]
        if articles:
            headline = articles[0]['title']
            # Scan for counter increments
            for art in articles:
                txt = art['title'].lower()
                if not trump_found and any(w in txt for w in ["trump", "peace", "memorandum"]):
                    t_wins += 1
                    trump_found = True
                if not iran_found and any(w in txt for w in ["iran", "threat", "blockade"]):
                    i_threats += 1
                    iran_found = True
    except:
        articles = []

    # 4. DETERMINE CRISIS STATUS
    has_danger = any(word in headline.lower() for word in DANGER_WORDS)
    if has_danger:
        status_class, status_text = "danger", "PIRACY INTENSIFIES"
        panic_level, panic_angle = "CRITICAL", 45
        oil_price = round(random.uniform(110.00, 118.00), 2)
        hazard_pay = "+400% (Blood Money)"
        drone_stat = str(random.randint(15, 30))
        zodiac_stat = str(random.randint(5, 12))
        b_count += 1

    # --- TWEET DATABASE ---
    CAPTAIN_QUOTES = [
        "If you can see the drones, they can see you.",
        "Third zodiac this morning. They're starting to recognize my coffee mug.",
        "Oil is up. My blood pressure is higher.",
        "Radar is looking like a game of Tetris today.",
        "Just saw a seagull wearing a GoPro. The surveillance is getting weird.",
        "Nothing says 'Good Morning' like a shadowed transit in the Strait.",
        "Thinking about starting a podcast. 'Stuck in the Strait' has a nice ring to it.",
        "Is it a blockade or just a very aggressive parking job?",
        "Another day, another redline crossed. I'm running out of red ink.",
        "The crew is betting on the next oil price jump. I've got my money on 'Panic'."
]

    # Choose a random quote
    current_tweet = random.choice(CAPTAIN_QUOTES)
    current_time = datetime.now().strftime("%H:%M")

    # 5. LOG HISTORY
    new_row = f"<tr><td>{datetime.now().strftime('%H:%M')}</td><td>{status_text}</td><td>${oil_price}</td></tr>\n"
    with open(history_file, 'a') as hf:
        hf.write(new_row)
    with open(history_file, 'r') as hf:
        recent_history = "".join(reversed(hf.readlines()[-10:]))

    # 6. APPLY REPLACEMENTS
    if os.path.exists(template_file):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
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
            "[[meme_quote]]": random.choice(CAPTAIN_QUOTES),
            "[[history_rows]]": recent_history,
            "[[insurance_risk]]": "HIGH" if has_danger else "MODERATE",
            "[[pirate_tax]]": "$12,500" if has_danger else "$0"
            "[[last_update]]": current_time,
        # If your HTML uses a specific tag for the tweet time:
            "[[tweet_time]]": current_time,
        }

        for tag, val in replacements.items():
            content = content.replace(tag, str(val))

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        with open(counter_file, 'w') as f:
            f.write(f"{t_wins}|{i_threats}|{b_count}")

if __name__ == "__main__":
    update_monitor()