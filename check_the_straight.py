import os
import requests
from datetime import datetime

def update_monitor():
    # 1. Fetch News (Using your secret API Key)
    api_key = os.getenv('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        news_data = response.json()
        # Get the top headline or a default if API fails
        headline = news_data['articles'][0]['title'] if news_data.get('articles') else "Naval Standoff Continues in Strait"
    except:
        headline = "Trump Rejects Iran Peace Deal; Navy Enforces 'Pirate' Blockade"

    # 2. SATURDAY MAY 2, 2026 DATA POINTS
    # Oil spiked to $117 earlier this week, now settling near $108
    oil_price = "108.17" 
    traffic_flow = "8" # Only 8% of normal traffic is moving
    
    # 3. PANIC LOGIC & MEME GENERATOR
    headline_low = headline.lower()
    
    if any(word in headline_low for word in ["pirate", "reject", "likely", "war"]):
        panic_angle = 75 # Points to the Red
        status_text = "EFFECTIVELY CLOSED"
        status_class = "danger"
        panic_level = "MAXIMUM PIRACY"
        vibe_check = "Aggressive"
        meme_quote = "Captain_Stuck_77: 'Trump calling the Navy pirates is the vibe of the century. Still can't get my oil out though.' #Hormuz2026"
    elif "negotiation" in headline_low or "talks" in headline_low:
        panic_angle = 0 # Points to the Yellow
        status_text = "RESTRICTED"
        status_class = "warning"
        panic_level = "MEME WARFARE"
        vibe_check = "Tense"
        meme_quote = "Iranian Consulate: 'Our memes are GOAT, your blockade is mid.' #DhamaalMemes"
    else:
        panic_angle = -75 # Points to the Green
        status_text = "OPEN"
        status_class = "success"
        panic_level = "CHILL"
        vibe_check = "Smooth"
        meme_quote = "Fisherman_Dave: 'Just me and the dolphins out here. Quiet day.'"

    # 4. PREPARE THE DATA FOR TEMPLATE
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

    # 5. READ TEMPLATE AND INJECT DATA
    with open('template.html', 'r') as f:
        content = f.read()

    # Replace placeholders with real data
    for key, value in data.items():
        placeholder = "{{" + key + "}}"
        content = content.replace(placeholder, str(value))

    # 6. SAVE THE FINAL INDEX.HTML
    with open('index.html', 'w') as f:
        f.write(content)
    
    print(f"Successfully updated at {datetime.now()}. Status: {status_text}")

if __name__ == "__main__":
    update_monitor()