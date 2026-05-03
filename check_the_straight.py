import os
import requests
from datetime import datetime

def update_monitor():
    # 1. FETCH NEWS DATA
    # Using a fallback for Saturday Night, May 2, 2026 intel
    api_key = os.getenv('NEWS_API_KEY')
    url = f'https://newsapi.org/v2/everything?q=Strait+of+Hormuz+OR+Iran+Blockade&sortBy=publishedAt&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        news_data = response.json()
        headline = news_data['articles'][0]['title'] if news_data.get('articles') else "Naval Standoff Continues in Strait"
    except:
        headline = "Trump Not Satisfied with Iran Proposal; War Likely if Tolls Continue"

    # 2. DYNAMIC STATS (MAY 2, 2026)
    # Fetch real Oil Price (Using a fallback if the API is down)
    try:
        # Placeholder for a real Oil Price API like AlphaVantage or OilPriceAPI
        # For now, let's keep it 'Spicy' based on the headline
        if "war" in headline.lower() or "blockade" in headline.lower():
            oil_price = "112.45" # Prices spike during conflict
        else:
            oil_price = "108.17"
    except:
        oil_price = "108.17"

    # Dynamic Traffic Flow based on Panic Level
    # If the status is 'Danger', traffic is naturally lower
    if status_class == "danger":
        traffic_flow = "5" if "pirate" in combined_text else "12"
    else:
        traffic_flow = "85" # Normal flow

    # THE TIME FIX: Use %I:%M %p for 12-hour format (e.g. 08:30 PM)
    current_time = datetime.now().strftime("%I:%M %p")
    
    # 3. DEFINE QUOTE & DANGER LOGIC
    # We define the quote first so it's available for the 'combined_text' check
    headline_low = headline.lower()
    danger_words = ["pirate", "reject", "likely", "war", "satisfied", "threat", "blockade", "sanctions", "tehran", "crush"]

    if any(word in headline_low for word in danger_words):
        meme_quote = "Captain_Stuck: 'Trump calling the Navy pirates is a mood.' #Hormuz2026"
    else:
        meme_quote = "Fisherman_Dave: 'Quiet day on the water. No carriers in sight.'"

    # Check BOTH for a total 'Vibe Check'
    combined_text = (headline + meme_quote).lower()
    
    if any(word in combined_text for word in danger_words):
        panic_angle = 75
        status_text = "EFFECTIVELY CLOSED"
        status_class = "danger"
        panic_level = "MAXIMUM PIRACY"
        vibe_check = "Aggressive"
    else:
        panic_angle = -75
        status_text = "OPEN"
        status_class = "success"
        panic_level = "CHILL"
        vibe_check = "Smooth"

    # 4. UPDATED PERSISTENT HISTORY LOGIC
    # Map the status_class to a history color class
    hist_color_class = f"hist-{status_class}"

    new_row = f"""
    <tr>
        <td class="time-col">{current_time}</td>
        <td class="{hist_color_class}">● {status_text}</td>
        <td>${oil_price}</td>
        <td style="font-style: italic; color: #eee;">{vibe_check}</td>
    </tr>"""

    # ... rest of your history merge logic ...

    try:
        with open('index.html', 'r') as f:
            old_content = f.read()
        
        if "" in old_content:
            # Extract existing rows between the markers
            existing_history = old_content.split("")[1].split("")[0]
            # Keep top 4 old rows + the 1 new row (Total 5)
            rows = [r for r in existing_history.split('</tr>') if '<td>' in r][:4]
            history_rows = new_row + "</tr>".join(rows) + "</tr>"
        else:
            history_rows = new_row
    except Exception as e:
        print(f"History Merge Failed: {e}")
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
        "vibe_check": vibe_check,
        "last_update": current_time,
        "history_rows": history_rows
    }

    # 6. INJECTION
    with open('template.html', 'r') as f:
        content = f.read()

    for key, value in data.items():
        placeholder = "[[" + key + "]]"
        content = content.replace(placeholder, str(value))

    # 7. SAVE OUTPUT
    with open('index.html', 'w') as f:
        f.write(content)
    
    print(f"Deployment Successful: {status_text} at {current_time}")

if __name__ == "__main__":
    update_monitor()