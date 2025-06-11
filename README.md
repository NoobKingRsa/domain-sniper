# 🔫 Domain Sniper Bot v1.4

> 📱 **Built on Android** • 🧪 For research & educational use only  
> ⚠️ **Free and open-source — Use responsibly!**

Domain Sniper is a powerful Python script to **scan and detect available domains** using keyword lists, WHOIS, DNS, and HTTP checks.  
Designed for mobile (Termux / Pydroid 3), it’s optimized for lightweight setups — but still packs a punch.

---

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

---

## 📥 Installation

### **Option 1 – Termux (recommended for Android):**

Copy and paste these commands **one at a time** in Termux:

```bash
pkg update
```

```bash
pkg install python git -y
```

```bash
pip install requests python-whois dnspython
```

```bash
git clone https://github.com/NoobKingRsa/domain-sniper
```

```bash
cd domain-sniper
```

```bash
python3 sniper.py
```

---

### **Option 2 – Pydroid 3 (Android):**

1. Download **Pydroid 3** from Google Play Store  
2. Open Pydroid 3 and install the following modules (use the built-in pip or pip3):  
    - `requests`  
    - `python-whois`  
    - `dnspython`  
3. Paste in the code or clone the repo to `/storage/emulated/0/Download`  
4. Run `sniper.py` in Pydroid 3  

---

## 🛠 Requirements

- **Python 3.x**
- Modules:
    - `requests`
    - `python-whois`
    - `dnspython`
- Access to your device’s `/storage/emulated/0/Download/` folder
- Basic understanding of domains & terminal usage

---

## 🧪 How to Use

1. Place a `.txt` file with keywords (one per line) into your Downloads folder  
2. Launch the script and select **"Run Domain Scan"**  
3. Choose the file and TLDs (e.g., `.com`, `.xyz`, `.app`)  
4. Let the bot scan — results are saved as `.txt` and `.csv` in Downloads

---

## ⭐ Support This Project

If this tool saved you time, helped you snipe a domain, or you just love cool open-source mobile stuff:

- ☕ [Buy Me a Coffee](https://coff.ee/noobkingrsz) — Small dev, big dreams.
- 📩 Found a bug? Got ideas?  
  Open an issue or reach out — feedback and collabs welcome!

---

## 🔮 Upcoming Features

- 🛒 Instant domain purchase integration (e.g., Namecheap API)
- 🔔 Telegram alert system (already written, currently commented out)
- 💬 Multi-language support
- 📸 Screenshot gallery & UI polish

---

## 🙋 About Me

Hey! I'm **NoobKingRSA**, a small-time developer from South Africa.  
I built this entire project on my phone using Termux and Pydroid 3, with zero funding and a lot of coffee.

I believe in tools that are lightweight, useful, and accessible to everyone — even if you don’t have a PC.

Let's keep building and learning together!  
🖤 [Support me on coffee](https://coff.ee/noobkingrsz)

---

## 📄 License

This project is licensed under the MIT License — free to use, share, and modify.  
Just **don’t be evil.** 😈

---

_Made with ☕ and Python by NoobKingRsa_
