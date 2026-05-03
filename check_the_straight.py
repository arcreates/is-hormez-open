import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike"]

def update_monitor():
    # 1. FETCH LIVE DATA
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(news_url).json()
        headline = response['articles'][0]['title']
    except:
        headline = "Intelligence Dark: Captain_Stuck is adjusting the satellite dish."

    oil_price = round(random.uniform(108.50, 115.00), 2)
    pirate_tax = "0% (For Now)" # Default fallback
    war_cost_billions = round(random.uniform(92.1, 98.9), 1)
    traffic_flow = random.randint(62, 89)
    last_update = datetime.now().strftime("%I:%M %p")

    # 2. STATUS & GAUGE LOGIC
    if any(word in headline.lower() for word in DANGER_WORDS):
        status_class = "danger"
        status_text = "PIRACY INTENSIFIES"
        panic_level = "CRITICAL"
        panic_angle = 45
        # Reality check: Blockades mean almost zero flow
        traffic_flow = random.randint(5, 15) 
    elif oil_price > 112:
        status_class = "warning"
        status_text = "Market Volatility"
        panic_level = "ELEVATED"
        panic_angle = 0
        # Tension slows things down for inspections
        traffic_flow = random.randint(40, 60) 
    else:
        status_class = "chill"
        status_text = "Vessels Moving"
        panic_level = "MODERATE"
        panic_angle = -45
        # Business as usual
        traffic_flow = random.randint(88, 97)

    # 3. CAPTAIN'S QUOTE ENGINE
    quotes = {
        "danger": ["'They call us pirates. I call us stationary.'", "'The 5th Fleet is playing chicken with drones again.'"],
        "chill": ["'Quiet night. Too quiet. Fisherman Dave is suspicious.'", "'Watching the sunset. If only the radar was this pretty.'"],
        "warning": ["'Oil at $112. My ship is now a high-value target. Great.'", "'The Admiral asked for a report. I sent him a picture of a seagull.'"]
    }
    meme_quote = random.choice(quotes[status_class])

    # 4. HISTORY LOGGING
    new_row = f"<tr><td class='time-col'>{last_update}</td><td><span class='hist-{status_class}'>● {status_text}</span></td><td>${oil_price}</td></tr>\n"
    
    if not os.path.exists('history.txt'):
        open('history.txt', 'w').close()
    
    with open('history.txt', 'a', encoding='utf-8') as hf:
        hf.write(new_row)

    with open('history.txt', 'r', encoding='utf-8') as hf:
        all_history = hf.readlines()
        # Keep only the last 10 rows and reverse them
        recent_history = "".join(reversed(all_history[-10:]))

    # 5. THE REBUILD (The Stencil Method)
    if not os.path.exists('template.html'):
        print("CRITICAL: template.html not found!")
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        master_template = f.read()

    # Dictionary mapping placeholders in HTML to the Python variables
    # Every variable used here is now defined above!
    replacements = {
        "[[status_class]]": status_class,
        "[[status_text]]": status_text,
        "[[panic_angle]]": str(panic_angle),
        "[[panic_level]]": panic_level,
        "[[latest_headline]]": headline,
        "[[meme_quote]]": meme_quote,
        "[[last_update]]": last_update,
        "[[history_rows]]": recent_history,
        "[[oil_price]]": str(oil_price),
        "[[traffic_flow]]": str(traffic_flow),
        "[[war_cost]]": str(war_cost_billions),
        "[[pirate_tax]]": pirate_tax  # <--- ADD THIS LINE
    }

    # Perform the swap
    final_output = master_template
    for placeholder, value in replacements.items():
        final_output = final_output.replace(placeholder, str(value))

    # 6. OVERWRITE index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_output)

    print(f"Deployment successful: {status_text} at {last_update}")

if __name__ == "__main__":
    update_monitor()