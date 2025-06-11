# 🔫 Domain Sniper Bot v1.4

> 📱 Built on Android • 🧪 For research & educational use only  
> ⚠️ Free and open-source — Use responsibly!

Domain Sniper is a powerful Python script that helps you **scan and detect available domains** using keyword lists, WHOIS, DNS, and HTTP checks. Designed for mobile (Termux / Pydroid 3), it’s optimized for lightweight setups — but still packs a punch.


## 🚀 Features

- ✅ Fast WHOIS + DNS + HTTP + Advanced DNS scans
- 🔄 Retry handling with error logging
- 📦 Saves TXT + CSV outputs with timestamped results
- 📈 Keyword expansion with prefixes/suffixes
- 🔔 (Optional) Telegram bot notification [commented out for now]
- 🧼 Auto log rotation (7-day cleanup)
- 🎨 User-friendly CLI interface
- 📁 Uses your Android **Download** folder for input/output
- ✨ No PC required!



## 📥 Installation

**Option 1 – Termux (recommended for Android):**

```bash
pkg update && pkg install python git -y
pip install requests python-whois dnspython
git clone https://github.com/NoobKingRsa/domain-sniper
cd domain-sniper
python3 sniper.py
```bash


Option 2 – Pydroid 3 (Android):

Download from Google Play Store

Open Pydroid 3 and install the following modules:

requests

python-whois

dnspython


Paste in the code or clone the repo to /storage/emulated/0/Download

Run sniper.py




🛠 Requirements

Python 3.x

Modules:

requests

python-whois

dnspython


Access to your device’s /storage/emulated/0/Download/ folder

Basic understanding of domains & terminal usage


🧪 How to Use

1. Place a .txt file with keywords (one per line) into your Downloads folder


2. Launch the script and select "Run Domain Scan"


3. Choose the file and TLDs (e.g., .com, .xyz, .app)


4. Let the bot scan — results are saved as .txt and .csv


⭐ Support This Project

If this tool saved you time, helped you snipe a domain, or you just love cool open-source mobile stuff:

☕ Buy Me a Coffee — Small dev, big dreams.

📩 Found a bug? Got ideas?
Open an issue or reach out — feedback and collabs welcome!


🔮 Upcoming Features

🛒 Instant domain purchase integration (e.g., Namecheap API)

🔔 Telegram alert system (already written, currently commented out)

💬 Multi-language support

📸 Screenshot gallery & UI polish



🙋 About Me

Hey! I'm NoobKingRSA, a small-time developer from South Africa.
I built this entire project on my phone using Termux and Pydroid 3, with zero funding and a lot of coffee.

I believe in tools that are lightweight, useful, and accessible to everyone — even if you don’t have a PC.

Let's keep building and learning together!
🖤 https://coff.ee/noobkingrsz



📄 License

This project is licensed under the MIT License — free to use, share, and modify.
Just don’t be evil. 😈


Made with ☕ and Python by NoobKingRsa
