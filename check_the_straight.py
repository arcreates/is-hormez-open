import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike"]
PEACE_WORDS = ["denies", "avoid", "de-escalation", "end", "talks", "peace"]

def update_monitor():
    # 1. FETCH LIVE DATA
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(news_url).json()
        headline = response['articles'][0]['title']
    except:
        headline = "Intelligence Dark: Captain_Stuck is adjusting the satellite dish."

    # 2. DEFINE DEFAULTS & BASE METRICS
    oil_price = round(random.uniform(108.50, 115.00), 2)
    war_cost_billions = round(random.uniform(92.1, 98.9), 1)
    last_update = datetime.now().strftime("%I:%M %p")
    escalation_factor = max(0, int(oil_price - 100))

    # 3. CORE STATUS LOGIC (Headline + Price Analysis)
    # Check if danger words are present
    has_danger = any(word in headline.lower() for word in DANGER_WORDS)
    # Check if peace words are also present (The Sentiment Buffer)
    has_peace = any(word in headline.lower() for word in PEACE_WORDS)

    # 3. CORE STATUS LOGIC
    if has_danger and not has_peace:
        # ... existing status_class logic ...
        hazard_pay = "+400% (Blood Money)"
        traffic_flow = random.randint(4, 7) # Matches the 5% real-world low
        ships_detected = random.randint(1, 3)
        vibe_data = f"{ships_detected} Ships (AIS Ghosting)"
        drone_stat = f"{random.randint(12, 30)} (Aggressive Vibe Check)"
        zodiac_stat = f"{random.randint(8, 15)} (Circular Doughnuts)"
    
    elif oil_price > 112 or (has_danger and has_peace):
        # ... existing status_class logic ...
        hazard_pay = "+120% (Panic Pricing)"
        traffic_flow = random.randint(18, 35) 
        ships_detected = random.randint(8, 14)
        vibe_data = f"{ships_detected} Ships (Tense AF)"
        drone_stat = f"{random.randint(3, 7)} (Shadowing us)"
        zodiac_stat = f"{random.randint(1, 4)} (Surrounding us)"
    
    else:
        # EVEN IN CHILL MODE: Throughput recovers slowly
        hazard_pay = "Standard (Boring)"
        traffic_flow = random.randint(45, 62) # Never jumps straight to 90%
        ships_detected = random.randint(22, 31)
        vibe_data = f"{ships_detected} Ships (Cautious)"
        drone_stat = f"{random.randint(0, 1)} (Probably a Seagull)"
        zodiac_stat = "0 (Everyone is Napping)"
        
        # Threat Counters
        drone_stat = f"{random.randint(0, 1)} (Probably a Seagull)"
        zodiac_stat = "0 (Everyone is Napping)"

    drone_stat = f"{drones} {vibe_suffix}"
    zodiac_stat = f"{zodiacs} Spotted"

    # 4. CAPTAIN'S QUOTE ENGINE
    quotes = {
        "danger": ["'They call us pirates. I call us stationary.'", "'The 5th Fleet is playing chicken with drones again.'"],
        "chill": ["'Quiet night. Too quiet. Fisherman Dave is suspicious.'", "'Watching the sunset. If only the radar was this pretty.'"],
        "warning": ["'Oil at $112. My ship is now a high-value target.'", "'The Admiral asked for a report. I sent him a picture of a seagull.'"]
    }
    meme_quote = random.choice(quotes[status_class])

    # 5. HISTORY LOGGING
    new_row = f"<tr><td class='time-col'>{last_update}</td><td><span class='hist-{status_class}'>● {status_text}</span></td><td>${oil_price}</td></tr>\n"
    if not os.path.exists('history.txt'):
        open('history.txt', 'w').close()
    
    with open('history.txt', 'a', encoding='utf-8') as hf:
        hf.write(new_row)

    with open('history.txt', 'r', encoding='utf-8') as hf:
        all_history = hf.readlines()
        recent_history = "".join(reversed(all_history[-10:]))

    # 6. THE REBUILD (The Stencil Method)
    if not os.path.exists('template.html'):
        print("CRITICAL: template.html not found!")
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        master_template = f.read()

    # Dictionary mapping ALL placeholders to the Python variables
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
        "[[pirate_tax]]": pirate_tax,
        "[[insurance_risk]]": insurance_risk,
        "[[hazard_pay]]": hazard_pay, # Renamed from tanker_rate
        "[[vibe_data]]": vibe_data,
        "[[drone_stat]]": drone_stat,
        "[[zodiac_stat]]": zodiac_stat
    }

    # Perform the swap
    final_output = master_template
    for placeholder, value in replacements.items():
        final_output = final_output.replace(placeholder, str(value))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_output)

    print(f"Deployment successful: {status_text} at {last_update}")

if __name__ == "__main__":
    update_monitor()