```markdown
# WPBruteGUI v1.2  
Modern & Colourful WordPress Bruteforce Tool  
GUI + CLI • Real-Time Success Counter • Optional Shell Upload

> Coded by **M4DI~UciH4**  
> [GitHub](https://github.com/RizkyEvory) • [Telegram](https://t.me/madiganzz)

---

## 📸 Preview
Dark-themed, resizable GUI with live **Success Counter** and animated progress-bar.  
(Upload your own `icon.ico` / `icon.png` to `assets/` to customize branding.)

---

## ✨ Features
| Feature | Description |
|---------|-------------|
| **Dual Mode** | Full **GUI** (Tkinter) + optional **CLI** (`--cli`) |
| **Attack Vectors** | `xmlrpc.php` **and** `/wp-login.php` |
| **Realtime Counter** | `[SUCCESS #N]` in CLI & live label in GUI |
| **Dynamic Wordlist** | Placeholders: `[DOMAIN]`, `[YEAR]`, `[WPLOGIN]`, etc. |
| **Shell Upload** | Auto-upload plugin / theme ZIP after valid login |
| **Cross-Platform** | Windows, Linux, macOS, **Termux** |
| **SSL Bypass** | Works with self-signed / expired certificates |

---

## 🚀 Quick Start

### 1. Clone
```bash
git clone https://github.com/RizkyEvory/WPBruteGUI.git
cd WPBruteGUI
```

2. Install Dependencies

```bash
pip install -r requirements.txt
```

3. Launch

Mode	Command	
GUI	`python main.py`	
CLI	`python main.py --cli`	

---

📋 Requirements

```
httpx
colorama
pillow   # for icons / PNG support
```

---

📁 File Structure

```
WPBruteGUI/
├── main.py                 # Main script (GUI + CLI)
├── assets/
│   ├── icon.ico            # Windows icon
│   └── icon.png            # Linux / macOS icon
├── requirements.txt
├── README.md
├── example/
│   ├── targets.txt         # sample target list
│   └── passwords.txt       # sample password list
├── success.txt             # found credentials (auto-created)
├── plugins.txt             # uploaded plugin shells (auto-created)
├── themes.txt              # uploaded theme shells (auto-created)
```

---

🎯 Usage Guide

1. Prepare Lists
targets.txt

```
http://target1.com
https://target2.net
```

passwords.txt

```
123456
[DOMAIN]2024
[WPLOGIN]123
```

2. GUI Flow
1. Target list → select `.txt`  
2. Password list → select `.txt`  
3. Plugin / Theme ZIP (optional) → pick your shell ZIPs  
4. Click 🚀 Start Bruteforce  
5. Watch Success Counter and Log update live.

3. CLI Flow

```bash
python main.py --cli
# Follow interactive prompts
```

---

🔐 Dynamic Wordlist Placeholders

Placeholder	Replaced With	
`[WPLOGIN]`	username	
`[DOMAIN]`	first part of domain	
`[DDOMAIN]`	full domain	
`[YEAR]`	current year	
`[UPPERLOGIN]`	username.upper()	
`[REVERSE]`	username reversed	
… (full list in source)	

---

📱 Termux Guide
No DLL required – runs natively.

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/RizkyEvory/WPBruteGUI.git
cd WPBruteGUI
pip install httpx colorama
python main.py --cli
```

> GUI on Termux: install X11-repo & VNC if you want the GUI.

---

🧪 Example Session

```
[SUCCESS #1] http://victim.com -> admin:admin123
[UPLOAD SUCCESS] Plugin: http://victim.com/wp-content/plugins/abcd1234/gepas.php
```

All results appended to `success.txt`, `plugins.txt`, `themes.txt`.

---

⚠️ Legal Notice
Use only on systems you own or have explicit authorization to test.

Developer (RizkyEvory / M4DIUciH4) not responsible for misuse.

---

🛠️ Contributing
1. Fork this repo  
2. Create feature branch: `git checkout -b feature-name`  
3. Push & open Pull Request

---

🐛 Issues & Requests
Open an [Issue](https://github.com/RizkyEvory/WPBruteGUI/issues) or contact via [Telegram](https://t.me/madiganz).

---

📜 License
MIT – see [LICENSE](LICENSE).

---

⬇️ Download
Latest release:

👉 [https://github.com/RizkyEvory/WPBruteGUI/releases](https://github.com/RizkyEvory/WPBruteGUI/releases)

```