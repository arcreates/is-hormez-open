import requests
import random
from datetime import datetime

# --- CONFIGURATION ---
NEWS_API_KEY = "YOUR_NEWS_API_KEY"  # Or use os.getenv('NEWS_API_KEY')
DANGER_WORDS = ["blockade", "war", "closed", "seized", "pirate", "rubicon", "rejected", "strike"]

def update_monitor():
    # 1. FETCH HEADLINE
    # We use language=en to avoid the Korean "Rubicon" glitch!
    news_url = f"https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    try:
        response = requests.get(news_url).json()
        headline = response['articles'][0]['title']
    except:
        headline = "Intelligence Dark: Fisherman Dave reports high static on the radio."

    # 2. FETCH OIL PRICE (Simulating May 2026 volatility)
    # Tonight's baseline: $112.45
    oil_price = round(random.uniform(108.50, 115.00), 2)
    war_cost_billions = round(random.uniform(92.1, 98.9), 1)

    # 3. DETERMINE THE STATUS (This MUST come before the quotes)
    status_class = "chill"
    status_text = "Vessels Moving"
    panic_level = "MODERATE"
    panic_angle = 15

    if any(word in headline.lower() for word in DANGER_WORDS):
        status_class = "danger"
        status_text = "PIRACY INTENSIFIES"
        panic_level = "FULL BLACKBEARD"
        panic_angle = 75

    # 4. CAPTAIN STUCK'S QUOTE ENGINE
    pirate_tweets = {
        "danger": [
            "Captain_Stuck: 'Trump called us pirates. If that's the case, where’s my parrot and my 20% cut of the oil? #NavyPirateMonitor'",
            "Captain_Stuck: 'Current status: Blockaded. Again. It’s like a parking lot, but with more cruise missiles.'",
            "Captain_Stuck: 'They crossed the Rubicon. I’m just trying to cross the shipping lane without hitting a mine.'",
            "Captain_Stuck: 'The 5th Fleet is acting like a bouncer at a club that no one wants to enter anyway.'",
            "Captain_Stuck: 'Tehran says the ball is in the US court. I just saw a drone on the radar. Ball? Drone? Same thing.'",
            "Captain_Stuck: 'Status: Anchored. Vibe: Maximum Piracy. Coffee: Extinct.'"
        ],
        "chill": [
            "Captain_Stuck: 'Quiet night. I can actually hear the waves instead of the jet engines. Slightly suspicious.'",
            "Captain_Stuck: 'Fisherman Dave says the fish aren't biting because of the sonar. I think they're protesting gas prices.'",
            "Captain_Stuck: 'Saw a Shadow Fleet tanker fly a smiley face flag today. Points for creativity.'",
            "Captain_Stuck: 'The sea is calm. The politicians are not. I know which one I’d rather deal with.'"
        ],
        "oil_spike": [
            "Captain_Stuck: 'Oil at $112.45. My ship is now worth more than a small European country. Don't tell the IRS.'",
            "Captain_Stuck: 'Watching crude prices spike while sitting on 2 million barrels of it is a special kind of torture.'",
            "Captain_Stuck: 'At these prices, I’m not a captain, I’m a high-value asset. I’ll be in my bunk.' #OilStrait"
        ],
        "pirate_humor": [
            "Captain_Stuck: 'Someone asked for my boarding pass. I showed them my 5-inch deck gun. They didn't laugh.'",
            "Captain_Stuck: 'Why is the rum always gone? Because the Navy blocked the supply ships, that’s why.'",
            "Captain_Stuck: 'Status: Arrr-gumentative. The Admiral tried to motivate us. I asked for a peg leg.'"
        ]
    }

    # Pick the right category based on status
    if status_class == "danger":
        category = "danger" if random.random() > 0.3 else "pirate_humor"
    elif oil_price > 110:
        category = "oil_spike"
    else:
        category = "chill"

    meme_quote = random.choice(pirate_tweets[category])
    last_update = datetime.now().strftime("%I:%M %p")

    # 5. READ INDEX.HTML AND INJECT UPDATES
    with open('index.html', 'r') as f:
        content = f.read()

    # Create the history row
    new_row = f"<tr><td>{last_update}</td><td><span class='dot {status_class}'>●</span> {status_text}</td><td>${oil_price}</td></tr>\n"
    
    # Injection Logic
    content = content.replace("[[headline]]", headline)
    content = content.replace("[[oil_price]]", str(oil_price))
    content = content.replace("[[war_cost]]", str(war_cost_billions))
    content = content.replace("[[status_class]]", status_class)
    content = content.replace("[[status_text]]", status_text)
    content = content.replace("[[panic_level]]", panic_level)
    content = content.replace("[[panic_angle]]", str(panic_angle))
    content = content.replace("[[meme_quote]]", meme_quote)
    content = content.replace("[[last_update]]", last_update)
    content = content.replace("", f"\n{new_row}")

    with open('index.html', 'w') as f:
        f.write(content)

    print(f"Update Successful: {status_text} at {oil_price}")

if __name__ == "__main__":
    update_monitor()