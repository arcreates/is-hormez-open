import requests
import random
import os
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
# YOUR UPDATED DANGER LIST
DANGER_WORDS = [
    "blockade", "war", "closed", "seized", "pirate", "rubicon", 
    "rejected", "strike", "fired", "refuses", "redline", 
    "refject", "refuse", "didn't work"
]
PEACE_WORDS = ["denies", "avoid", "de-escalation", "end", "talks", "peace", "memorandum", "pause"]

def update_monitor():
    # 1. FETCH LATEST 20 HEADLINES
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(news_url).json()
        articles = response.get('articles', [])[:20]
        if articles:
            primary_headline = articles[0]['title']
        else:
            primary_headline = "Intelligence Dark: Captain_Stuck is adjusting the satellite dish."
    except:
        primary_headline = "Satellite Link Failure: Check back after the next flyover."
        articles = []

   # 2. PERSISTENT COUNTERS (With "Empty File" Protection)
    counter_file = 'counters.txt'
    
    # If file doesn't exist OR is empty, initialize it
    if not os.path.exists(counter_file) or os.stat(counter_file).st_size == 0:
        with open(counter_file, 'w') as f: 
            f.write("0|0|0")
        t_wins, i_threats, b_count = 0, 0, 0
    else:
        with open(counter_file, 'r') as f:
            content = f.read().strip()
            if '|' in content:
                t_wins, i_threats, b_count = map(int, content.split('|'))
            else:
                # Fallback if the file format is weird
                t_wins, i_threats, b_count = 0, 0, 0

    for art in articles:
        txt = art['title'].lower()
        if not trump_found and "trump" in txt and any(w in txt for w in ["victory", "peace", "memorandum", "open"]):
            t_wins += 1
            trump_found = True
        if not iran_found and "iran" in txt and any(w in txt for w in ["threat", "final", "refuse", "blockade", "procedures"]):
            i_threats += 1
            iran_found = True

    # 4. SET SAFE DEFAULTS
    oil_price = round(random.uniform(98.50, 115.00), 2) # Range expanded for peace/war volatility
    last_update = datetime.now().strftime("%I:%M %p")
    status_class = "chill"
    
    # 5. CORE STATUS LOGIC (Based on the NEWEST headline)
    has_danger = any(word in primary_headline.lower() for word in DANGER_WORDS)
    has_peace = any(word in primary_headline.lower() for word in PEACE_WORDS)

    if has_danger and not has_peace:
        status_class = "danger"
        status_text = "PIRACY INTENSIFIES"
        panic_level = "CRITICAL"
        panic_angle = 45
        traffic_flow = random.randint(4, 7)
        hazard_pay = "+400% (Blood Money)"
        vibe_data = f"{random.randint(1, 3)} Ships (AIS Ghosting)"
        drone_stat = f"{random.randint(12, 30)} (Aggressive Vibe Check)"
        zodiac_stat = f"{random.randint(8, 15)} (Circular Doughnuts)"
        b_count += 1 # The Meta-Blockade counter
    
    elif oil_price > 112 or (has_danger and has_peace):
        status_class = "warning"
        status_text = "Market Volatility"
        panic_level = "ELEVATED"
        panic_angle = 0
        traffic_flow = random.randint(18, 35) 
        hazard_pay = "+120% (Panic Pricing)"
        vibe_data = f"{random.randint(8, 14)} Ships (Tense AF)"
        drone_stat = f"{random.randint(3, 7)} (Shadowing us)"
        zodiac_stat = f"{random.randint(1, 4)} (Following us)"
    
    else:
        status_class = "chill"
        status_text = "Vessels Moving"
        panic_level = "MODERATE"
        panic_angle = -45
        traffic_flow = random.randint(45, 62)
        hazard_pay = "Standard (Boring)"
        vibe_data = f"{random.randint(22, 31)} Ships (Cautious)"
        drone_stat = f"{random.randint(0, 1)} (Probably a Seagull)"
        zodiac_stat = "0 (Everyone is Napping)"

    # Save counters back
    with open(counter_file, 'w') as f:
        f.write(f"{t_wins}|{i_threats}|{b_count}")

    # 6. CAPTAIN'S QUOTE ENGINE
    quotes = {
        "danger": ["'They call us pirates. I call us stationary.'", "'The 5th Fleet is playing chicken with drones again.'"],
        "chill": ["'Quiet night. Too quiet. Fisherman Dave is suspicious.'", "'Watching the sunset. If only the radar was this pretty.'"],
        "warning": ["'Oil at $112. My ship is now a high-value target.'", "'The Admiral asked for a report. I sent him a picture of a seagull.'"]
    }
    meme_quote = random.choice(quotes[status_class])

    # 7. HISTORY LOGGING
    new_row = f"<tr><td class='time-col'>{last_update}</td><td><span class='hist-{status_class}'>● {status_text}</span></td><td>${oil_price}</td></tr>\n"
    if not os.path.exists('history.txt'):
        open('history.txt', 'w').close()
    with open('history.txt', 'a', encoding='utf-8') as hf:
        hf.write(new_row)
    with open('history.txt', 'r', encoding='utf-8') as hf:
        all_history = hf.readlines()
        recent_history = "".join(reversed(all_history[-10:]))

    # 8. THE REBUILD
    if not os.path.exists('template.html'):
        return

    with open('template.html', 'r', encoding='utf-8') as f:
        master_template = f.read()

    replacements = {
        "[[status_class]]": status_class,
        "[[status_text]]": status_text,
        "[[panic_angle]]": str(panic_angle),
        "[[panic_level]]": panic_level,
        "[[latest_headline]]": primary_headline,
        "[[meme_quote]]": meme_quote,
        "[[last_update]]": last_update,
        "[[history_rows]]": recent_history,
        "[[oil_price]]": str(oil_price),
        "[[traffic_flow]]": str(traffic_flow),
        "[[hazard_pay]]": hazard_pay,
        "[[vibe_data]]": vibe_data,
        "[[drone_stat]]": drone_stat,
        "[[zodiac_stat]]": zodiac_stat,
        "[[t_wins]]": str(t_wins),
        "[[i_threats]]": str(i_threats),
        "[[b_count]]": str(b_count)
    }

    final_output = master_template
    for placeholder, value in replacements.items():
        final_output = final_output.replace(placeholder, str(value))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_output)

    print(f"Update Complete: {status_text} | Scoreboard: {t_wins}/{i_threats}/{b_count}")

if __name__ == "__main__":
    update_monitor()