import os
import requests
from datetime import datetime

def update_monitor():
    # 1. FETCH NEWS DATA
    # Fallback headlines for May 2, 2026
    api_key = os.getenv('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        news_data = response.json()
        headline = news_data['articles'][0]['title'] if news_data.get('articles') else "Naval Standoff Continues in Strait"
    except:
        headline = "Trump Not Satisfied with Iran Proposal; War Likely if Tolls Continue"

    # 2. DEFINE VIBE & DANGER LOGIC FIRST
    # We need these variables defined before we calculate the dynamic stats
    headline_low = headline.lower()
    danger_words = ["pirate", "reject", "likely", "war", "satisfied", "threat", "blockade", "sanctions", "tehran", "crush"]

    import random

# ... inside your update_monitor() function ...

# THE CAPTAIN'S QUOTE ENGINE
pirate_tweets = {
    "danger": [
        "Captain_Stuck: 'Trump called us pirates again. Thinking of changing the ship's name to The Golden Hindsight.' #NavyPirates",
        "Captain_Stuck: 'Status: 40 tankers anchored. 0 coffee left. Might start trading crude for espresso beans.'",
        "Captain_Stuck: 'Update: The Rubicon has been crossed, and my anchor is stuck. Standard Saturday.' #StraitOfHormuz",
        "Captain_Stuck: 'If I see one more carrier I’m officially claiming this tanker as a sovereign island.'",
        "Captain_Stuck: 'Admiral told us to stay alert. I told him I haven't blinked since April. Send help.'",
        "Captain_Stuck: 'Current mood: Shiver me timbers, but in a geopolitical sense.'",
        "Captain_Stuck: 'They said the Strait was open. My radar says LOL. Someone is lying.' #Hormuz2026"
    ],
    "chill": [
        "Captain_Stuck: 'Quiet night. Almost too quiet. If Fisherman Dave starts singing sea shanties, I’m jumping overboard.'",
        "Captain_Stuck: 'Oil dropped $2. Finally might be able to afford a sandwich in 2026.'",
        "Captain_Stuck: 'Just a reminder: We are still here. Please don't forget about us when you're buying your $8 gas.'",
        "Captain_Stuck: 'Saw a dolphin. It looked more confused about the blockade than we are.'",
        "Captain_Stuck: 'The sea is flat, the news is boring, and I’ve read every book on this ship twice.'"
    ],
    "oil_spike": [
        "Captain_Stuck: 'Oil at $112? My retirement plan is just selling the fuel in our backup generator.'",
        "Captain_Stuck: 'At these prices, this tanker is basically a floating Fort Knox. Where’s my cut?'",
        "Captain_Stuck: 'Price of crude up again. Price of my sanity? All-time low.' #OilPrices"
    ],
    "pirate_humor": [
        "Captain_Stuck: 'What do you call a pirate with two eyes and two legs? A rookie. Or a very lucky Ensign.'",
        "Captain_Stuck: 'Someone asked for my boarding pass. I showed them my 5-inch deck gun. They didn't laugh.'",
        "Captain_Stuck: 'Status: Arrr-gumentative. The Navy called. They want their dignity back.'"
    ]
}

# Logic to pick the right category
if status_class == "danger":
    category = "danger" if random.random() > 0.3 else "pirate_humor"
elif float(oil_price) > 110:
    category = "oil_spike"
else:
    category = "chill"

meme_quote = random.choice(pirate_tweets[category])

    # Final combined vibe check
    combined_text = (headline + meme_quote).lower()
    
    if any(word in combined_text for word in danger_words):
        panic_angle = 75
        status_text = "PIRACY INTENSIFIES"  # Even better than 'Effectively Closed'
        status_class = "danger"
        panic_level = "FULL BLACKBEARD"    # Maximum meme level
        vibe_check = "Aggressive"
    else:
        panic_angle = -75
        status_text = "OPEN"
        status_class = "success"
        panic_level = "CHILL"
        vibe_check = "Smooth"

    # 3. CALCULATE DYNAMIC STATS (Now that we have status_class!)
    # Use %I:%M %p for a real 12-hour clock (e.g., 08:45 PM)
    current_time = datetime.now().strftime("%I:%M %p")

    # Dynamic Oil (Prices spike to $112.45 if it's dangerous)
    oil_price = "112.45" if status_class == "danger" else "108.17"

    # Dynamic Traffic (Drops to 8% if closed, 85% if open)
    traffic_flow = "8" if status_class == "danger" else "85"

    # Dynamic War Cost (Calculated since start date of April 1, 2026)
    days_since_start = (datetime.now() - datetime(2026, 4, 1)).days
    war_cost = f"{50 + (days_since_start * 1.5):.1f}B"

    # 4. PERSISTENT HISTORY LOGIC
    hist_color_class = f"hist-{status_class}"
    new_row = f"""
    <tr>
        <td class="time-col">{current_time}</td>
        <td class="{hist_color_class}">● {status_text}</td>
        <td>${oil_price}</td>
        <td style="font-style: italic; color: #eee;">{vibe_check}</td>
    </tr>"""

    try:
        with open('index.html', 'r') as f:
            old_content = f.read()
        
        if "" in old_content:
            existing_history = old_content.split("")[1].split("")[0]
            # Keep top 4 rows + 1 new row
            rows = [r for r in existing_history.split('</tr>') if '<td>' in r][:4]
            history_rows = new_row + "</tr>".join(rows) + "</tr>"
        else:
            history_rows = new_row
    except:
        history_rows = new_row

    # 5. DATA MAPPING
    data = {
        "status_text": status_text,
        "status_class": status_class,
        "panic_angle": panic_angle,
        "panic_level": panic_level,
        "latest_headline": headline,
        "meme_quote": meme_quote,
        "oil_price": oil_price,
        "traffic_flow": traffic_flow,
        "war_cost": war_cost,
        "vibe_check": vibe_check,
        "last_update": current_time,
        "history_rows": history_rows
    }

    # 6. INJECTION
    with open('template.html', 'r') as f:
        template_content = f.read()

    for key, value in data.items():
        placeholder = "[[" + key + "]]"
        template_content = template_content.replace(placeholder, str(value))

    # 7. SAVE OUTPUT
    with open('index.html', 'w') as f:
        f.write(template_content)
    
    print(f"Success: {status_text} at {current_time}. Oil is ${oil_price}.")

if __name__ == "__main__":
    update_monitor()