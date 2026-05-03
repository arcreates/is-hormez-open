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
    except Exception as e:
        headline = "Intelligence Dark: Fisherman Dave reports high static on the radio."

    oil_price = round(random.uniform(108.50, 115.00), 2)
    war_cost_billions = round(random.uniform(92.1, 98.9), 1)
    last_update = datetime.now().strftime("%I:%M %p")

    # 2. STATUS LOGIC
    status_class = "chill"
    status_text = "Vessels Moving"
    panic_level = "MODERATE"
    panic_angle = 15

    if any(word in headline.lower() for word in DANGER_WORDS):
        status_class = "danger"
        status_text = "PIRACY INTENSIFIES"
        panic_level = "FULL BLACKBEARD"
        panic_angle = 75

    # 3. CAPTAIN'S QUOTES
    pirate_tweets = {
        "danger": ["Captain_Stuck: 'Trump called us pirates. Where’s my parrot? #NavyPirateMonitor'", "Captain_Stuck: 'Current status: Blockaded. Again.'"],
        "chill": ["Captain_Stuck: 'Quiet night. Too quiet. Fisherman Dave is suspicious.'", "Captain_Stuck: 'Saw a dolphin. It looked confused.'"],
        "oil_spike": ["Captain_Stuck: 'Oil at $112. My ship is now a floating Fort Knox.'"],
        "pirate_humor": ["Captain_Stuck: 'Why is the rum gone? Naval blockade, obviously.'"]
    }
    
    cat = "danger" if status_class == "danger" else ("oil_spike" if oil_price > 110 else "chill")
    meme_quote = random.choice(pirate_tweets[cat])

    # 4. DEFINE THE NEW ROW
    new_row = f"<tr><td>{last_update}</td><td><span class='dot {status_class}'>●</span> {status_text}</td><td>${oil_price}</td></tr>\n"

    # 5. HISTORY MANAGEMENT
    if not os.path.exists('history.txt'):
        with open('history.txt', 'w') as f: f.write("")

    with open('history.txt', 'a', encoding='utf-8') as hf:
        hf.write(new_row)

    with open('history.txt', 'r', encoding='utf-8') as hf:
        all_rows = hf.readlines()
        recent_history = "".join(reversed(all_rows[-15:]))

    # 6. TEMPLATE INJECTION (Updated with your correct tag)
    if not os.path.exists('template.html'):
        print("CRITICAL: template.html is missing!")
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        page_content = f.read()

    replacements = {
        "[[latest_headline]]": str(headline),  # MATCHED TO YOUR TAG
        "[[oil_price]]": str(oil_price),
        "[[war_cost]]": str(war_cost_billions),
        "[[status_class]]": str(status_class),
        "[[status_text]]": str(status_text),
        "[[panic_level]]": str(panic_level),
        "[[panic_angle]]": str(panic_angle),
        "[[meme_quote]]": str(meme_quote),
        "[[last_update]]": str(last_update),
        "": recent_history
    }

    for placeholder, value in replacements.items():
        page_content = page_content.replace(placeholder, value)

    # 7. FINAL OUTPUT
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(page_content)

if __name__ == "__main__":
    update_monitor()