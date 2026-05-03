# 🚢 Is Hormuz Open? (2026 Crisis Monitor)

**Live URL:** [https://arcreates.github.io/is-hormez-open/](https://arcreates.github.io/is-hormez-open/)

An automated, data-driven dashboard tracking the status of the Strait of Hormuz during the 2026 blockade crisis. This tool monitors global news, oil prices, and maritime traffic to provide a real-time "Panic Meter" and geopolitical vibe check.

## 📡 Features
* **Real-time Intelligence:** Automatically scrapes News API for updates regarding naval blockades and diplomatic standoffs.
* **Dynamic Gauge:** A visual needle that swings between **CHILL** and **MAXIMUM PIRACY** based on headline sentiment.
* **24-Hour Trend Log:** A persistent history table that tracks hourly status changes, oil price fluctuations, and geopolitical vibes.
* **Zero-Maintenance:** Fully powered by GitHub Actions—updating every hour on the hour without human intervention.

## 🛠️ Tech Stack
* **Python 3.x:** The "brain" of the operation. Handles data scraping, sentiment logic, and HTML injection.
* **GitHub Actions:** The "engine." Executes the Python script every 60 minutes.
* **HTML5/CSS3:** A custom "War Room" UI inspired by Bloomberg terminals and naval command centers.

## 🤖 How It Works
1. The **GitHub Action** wakes up at `:00` past the hour.
2. The `check_the_strait.py` script fetches headlines and checks for "Danger Words" (e.g., *Pirate, Reject, Blockade*).
3. The script reads `template.html`, injects the new data, and updates the `index.html`.
4. The change is committed back to the repository, and GitHub Pages redeploys the site instantly.

## 📜 Setup
To run this locally or fork your own:
1. Clone the repo.
2. Add your `NEWS_API_KEY` to your GitHub Repository Secrets.
3. Push a change to trigger the first build!

---
*Disclaimer: This is a project tracking the fictional/projected events of 2026 for research and educational purposes.*
