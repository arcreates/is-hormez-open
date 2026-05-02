import requests
import datetime

# --- CONFIG ---
NEWS_API_KEY = "YOUR_NEWS_API_KEY" # Get a free one at newsapi.org

def get_status():
    url = f"https://newsapi.org/v2/everything?q='Strait of Hormuz'&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
        headline = articles[0]['title'] if articles else "No news... suspiciously quiet."
    except:
        headline = "Data link severed by giant squid or blockade."

    # Snark Logic
    panic_words = ["seized", "missile", "closed", "blocked", "attack", "tanker"]
    score = sum(1 for word in panic_words if word in headline.lower())

    if score >= 2:
        return "YES", "#ff4d4d", "It's a parking lot out there. Hope you like walking.", headline
    elif score >= 1:
        return "SORT OF", "#e67e22", "The vibes are rancid, but the ships are moving (fast).", headline
    else:
        return "NO", "#27ae60", "Smooth sailing. The oil is flowing like cheap coffee.", headline

status, color, vibe, news = get_status()
now = datetime.datetime.now().strftime("%Y-%m-%d %H:00:00")

# Read the template and replace placeholders
with open("template.html", "r") as f:
    html = f.read()

html = html.replace("{{COLOR}}", color)
html = html.replace("{{STATUS}}", status)
html = html.replace("{{VIBE}}", vibe)
html = html.replace("{{NEWS}}", news)
html = html.replace("{{TIME}}", now)

with open("index.html", "w") as f:
    f.write(html)