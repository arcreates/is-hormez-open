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
    
   # 3. UPDATED VIBE LOGIC (May 2, 2026 Night Update)
    # Check BOTH the headline and the meme for danger
    combined_text = (headline + meme_quote).lower()
    
    danger_words = ["pirate", "reject", "likely", "war", "satisfied", "threat", "blockade", "sanctions", "tehran"]
    
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

    # 4.5 LOGIC FOR HISTORY ROWS
    new_row = f"""
    <tr style="border-bottom: 1px solid #444;">
        <td style="padding: 10px;">{datetime.now().strftime("%H:00")}</td>
        <td>{status_text}</td>
        <td>${oil_price}</td>
        <td>{vibe_check}</td>
    </tr>
    """

    # Try to keep the last 5 rows from the existing page
    try:
        with open('index.html', 'r') as f:
            old_page = f.read()
        # This is a bit 'hacky' but works for a single-file site:
        # We grab everything between the first <tr> and the last </tr>
        if "" in old_page:
            existing_history = old_page.split("")[1].split("")[0]
            # Keep only the last 4 rows to avoid the page getting too long
            rows = existing_history.split('</tr>')[:4]
            history_rows = new_row + "</tr>".join(rows) + "</tr>"
        else:
            history_rows = new_row
    except:
        history_rows = new_row

    # Add this to your data dictionary
    data["history_rows"] = history_rows

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