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
    except:
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
        "danger": ["Captain_Stuck: 'Trump called us pirates. Where’s my parrot? #NavyPirateMonitor'", "Captain_Stuck: 'The Rubicon has been crossed. I’m just trying to cross the lane.'"],
        "chill": ["Captain_Stuck: 'Quiet night. Too quiet. Fisherman Dave is suspicious.'", "Captain_Stuck: 'Saw a dolphin. It looked more confused than the 5th Fleet.'"],
        "oil_spike": ["Captain_Stuck: 'Oil at $112. My ship is now a floating Fort Knox.'"],
        "pirate_humor": ["Captain_Stuck: 'Why is the rum gone? Naval blockade, obviously.'"]
    }
    
    cat = "danger" if status_class == "danger" else ("oil_spike" if oil_price > 110 else "chill")
    meme_quote = random.choice(pirate_tweets[cat])

    # 4. DEFINE THE NEW ROW (Crucial to do this BEFORE writing to history)
    new_row = f"<tr><td>{last_update}</td><td><span class='dot {status_class}'>●</span> {status_text}</td><td>${oil_price}</td></tr>\n"

    # 5. PERSISTENT HISTORY MANAGEMENT
    # Ensure history.txt exists
    if not os.path.exists('history.txt'):
        open('history.txt', 'w').close()

    # Append new row
    with open('history.txt', 'a') as hf:
        hf.write(new_row)

    # Read and reverse history (limit to 15 rows)
    with open('history.txt', 'r') as hf:
        all_rows = hf.readlines()
        recent_history = "".join(reversed(all_rows[-15:]))

    # 6. INJECT INTO TEMPLATE
    with open('template.html', 'r') as f:
        content = f.read()

    # Use a dictionary for cleaner replacements
    replacements = {
        "[[headline]]": str(headline),
        "[[oil_price]]": str(oil_price),
        "[[war_cost]]": str(war_cost_billions),
        "[[status_class]]": str(status_class),
        "[[status_text]]": str(status_text),
        "[[panic_level]]": str(panic_level),
        "[[panic_angle]]": str(panic_angle),
        "[[meme_quote]]": str(meme_quote),
        "[[last_update]]": str(last_update),
        "": str(recent_history)
    }

    # IMPORTANT: Always start with the fresh template content
    final_output = content
    for placeholder, value in replacements.items():
        final_output = final_output.replace(placeholder, value)

    # Write to index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_output)

if __name__ == "__main__":
    update_monitor()