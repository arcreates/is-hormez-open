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

    if any(word in headline_low for word in danger_words):
        meme_quote = "Captain_Stuck: 'Trump calling the Navy pirates is a mood.' #Hormuz2026"
    else:
        meme_quote = "Fisherman_Dave: 'Quiet day on the water. No carriers in sight.'"

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