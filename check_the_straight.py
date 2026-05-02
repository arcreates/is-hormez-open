import os
import requests
from datetime import datetime

def update_monitor():
    # 1. Fetch News
    api_key = os.getenv('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        news_data = response.json()
        headline = news_data['articles'][0]['title'] if news_data.get('articles') else "Naval Standoff Continues in Strait"
    except:
        headline = "Trump Rejects Iran Peace Deal; Navy Enforces 'Pirate' Blockade"

    # 2. SATURDAY MAY 2, 2026 DATA
    oil_price = "108.17" 
    traffic_flow = "8" 
    
   # 3. BEEFED UP VIBE LOGIC (May 2, 2026 Update)
    headline_low = headline.lower()
    
    # We are adding more 'Danger' triggers based on tonight's specific news
    danger_words = ["pirate", "reject", "likely", "war", "satisfied", "threat", "blockade", "sanctions"]
    warning_words = ["negotiation", "talks", "proposal", "pakistan", "mediator"]

    if any(word in headline_low for word in danger_words):
        panic_angle = 75
        status_text = "EFFECTIVELY CLOSED"
        status_class = "danger"
        panic_level = "MAXIMUM PIRACY"
        vibe_check = "Aggressive"
        meme_quote = "Captain_Stuck: 'Trump says Navy is like pirates. I guess I need a parrot now.' #Hormuz2026"
        
    elif any(word in headline_low for word in warning_words):
        panic_angle = 0
        status_text = "RESTRICTED / TALKS"
        status_class = "warning"
        panic_level = "DIPLOMATIC GRIDLOCK"
        vibe_check = "Tense"
        meme_quote = "Consulate_Gen: 'Our memes are GOAT, your blockade is mid.' #Dhamaal"
        
    else:
        panic_angle = -75
        status_text = "OPEN"
        status_class = "success"
        panic_level = "CHILL"
        vibe_check = "Smooth"
        meme_quote = "Fisherman_Dave: 'Quiet day on the water. No carriers in sight.'"
        
    # 4. DATA DICTIONARY
    data = {
        "status_text": status_text,
        "status_class": status_class,
        "panic_angle": panic_angle,
        "panic_level": panic_level,
        "latest_headline": headline,
        "meme_quote": meme_quote,
        "oil_price": oil_price,
        "traffic_flow": traffic_flow,
        "vibe_check": vibe_check,
        "last_update": datetime.now().strftime("%H:00")
    }

    # 5. READ AND INJECT (Using Square Brackets [[ ]])
    with open('template.html', 'r') as f:
        content = f.read()

    for key, value in data.items():
        # This now looks for [[key]] instead of {{key}}
        placeholder = "[[" + key + "]]"
        content = content.replace(placeholder, str(value))

    # 6. SAVE
    with open('index.html', 'w') as f:
        f.write(content)
    
    print(f"Update successful. Status: {status_text}")

if __name__ == "__main__":
    update_monitor()