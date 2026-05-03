import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike"]

def update_monitor():
    # 1. FETCH DATA
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(news_url).json()
        headline = response['articles'][0]['title']
    except Exception:
        headline = "Intelligence Dark: Fisherman Dave reports high static on the radio."

    oil_price = round(random.uniform(108.50, 115.00), 2)
    war_cost_billions = round(random.uniform(92.1, 98.9), 1)
    last_update = datetime.now().strftime("%I:%M %p")

    # 2. STATUS LOGIC
    status_class = "chill"
    status_text = "Vessels Moving"
    if any(word in headline.lower() for word in DANGER_WORDS):
        status_class = "danger"
        status_text = "PIRACY INTENSIFIES"

    # 3. CAPTAIN'S QUOTES
    pirate_tweets = {
        "danger": ["Captain_Stuck: 'Trump called us pirates. Where is my parrot? #NavyPirateMonitor'"],
        "chill": ["Captain_Stuck: 'Quiet night. Fisherman Dave is suspicious.'"],
        "oil_spike": ["Captain_Stuck: 'Oil at $112. My ship is now a floating Fort Knox.'"],
        "pirate_humor": ["Captain_Stuck: 'Why is the rum gone? Naval blockade, obviously.'"]
    }
    
    cat = "danger" if status_class == "danger" else ("oil_spike" if oil_price > 110 else "chill")
    meme_quote = random.choice(pirate_tweets[cat])

    # 4. DEFINE THE NEW ROW
    new_row = f"<tr><td>{last_update}</td><td><span class='dot {status_class}'>●</span> {status_text}</td><td>${oil_price}</td></tr>\n"

    # 5. HISTORY MANAGEMENT (Memory)
    if not os.path.exists('history.txt'):
        open('history.txt', 'w').close()

    with open('history.txt', 'a', encoding='utf-8') as hf:
        hf.write(new_row)

    with open('history.txt', 'r', encoding='utf-8') as hf:
        all_rows = hf.readlines()
        # Keep it short so the file doesn't explode again
        recent_history = "".join(reversed(all_rows[-10:]))

    # 6. TEMPLATE INJECTION (Source of Truth)
    if not os.path.exists('template.html'):
        print("Template missing!")
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        page_content = f.read()

    # The Big Fix: Matching your [[latest_headline]] tag
    replacements = {
        "[[status_class]]": status_class,
        "[[status_text]]": status_text,
        "[[panic_angle]]": str(panic_angle),
        "[[panic_level]]": panic_level,
        "[[latest_headline]]": headline,
        "[[meme_quote]]": meme_quote,
        "[[last_update]]": last_update,
        "[[history_rows]]": recent_history,  # Make sure this matches!
        "[[oil_price]]": str(oil_price),
        "[[traffic_flow]]": str(random.randint(60, 95)), # Add this if you want it
        "[[war_cost]]": str(war_cost_billions)
    }

    # Strict replacement loop
    final_output = page_content
    for placeholder, value in replacements.items():
        final_output = final_output.replace(placeholder, value)

    # 7. WRITE TO PUBLIC SITE
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_output)

if __name__ == "__main__":
    update_monitor()