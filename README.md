```markdown
<!-- markdownlint-disable MD033 -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=WPBruteGUI&fontSize=60&fontColor=fff&animation=fadeIn" width="100%"/>
</p>

<p align="center">
  <a href="https://github.com/RizkyEvory/WPBruteGUI/releases/latest"><img src="https://img.shields.io/github/v/release/RizkyEvory/WPBruteGUI?style=flat-square&labelColor=1e1e2f&color=7b68ee&logo=github&label=Latest"/></a>
  <a href="https://github.com/RizkyEvory/WPBruteGUI/stargazers"><img src="https://img.shields.io/github/stars/RizkyEvory/WPBruteGUI?style=flat-square&labelColor=1e1e2f&color=ff69b4&logo=star"/></a>
  <a href="https://github.com/RizkyEvory/WPBruteGUI/issues"><img src="https://img.shields.io/github/issues-raw/RizkyEvory/WPBruteGUI?style=flat-square&labelColor=1e1e2f&color=00e054&logo=github"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Platform-Win%20%7C%20Linux%20%7C%20macOS%20%7C%20Termux-blue?style=flat-square&labelColor=1e1e2f"/></a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&pause=1000&color=7b68ee&center=true&vCenter=true&width=600&lines=Dark+GUI+for+WordPress+Bruteforce%2C+XMLRPC+%26+wp-login" />
</p>

---

## 🔥 Highlights
| | |
|---|---|
| **🎨 Modern GUI** | Dark Tkinter theme with live counter & progress-bar |
| **⚡ Dual Engine** | Attacks `xmlrpc.php` **and** `/wp-login.php` |
| **🎯 Smart Wordlist** | Placeholders like `[DOMAIN]`, `[YEAR]`, `[UPPERLOGIN]` |
| **📦 Shell Upload** | Auto-upload plugin / theme ZIP after valid login |
| **📱 Termux Ready** | Zero DLL, pure Python, run on Android |

---

## 🚀 30-Second Install
```bash
git clone https://github.com/RizkyEvory/WPBruteGUI.git
cd WPBruteGUI
pip install -r requirements.txt
python main.py        # GUI
python main.py --cli  # CLI
```

---

🖥️ GUI Preview

---

🛠️ Usage Flow

1. Target list (`targets.txt`)  
   
```
   http://victim1.com
   https://site2.org
   ```

2. Password list (`passwords.txt`)  
   
```
   123456
   [DOMAIN]2024
   [WPLOGIN]123!
   ```

3. Shell ZIPs (optional)  
   - `plugin.zip`  
   - `theme.zip`

4. Run  
   - GUI → click 🚀 Start Bruteforce  
   - CLI → `python main.py --cli`

---

📱 Termux

```bash
pkg update && pkg install python git -y
git clone https://github.com/RizkyEvory/WPBruteGUI.git
cd WPBruteGUI && pip install httpx colorama
python main.py --cli
```

> For GUI on Termux install `x11-repo` & VNC.

---

📊 Real-time Stats

Output	File	
Found credentials	`success.txt`	
Plugin shells	`plugins.txt`	
Theme shells	`themes.txt`	

---

🎨 Color Palette

Hex	Usage	
`#1e1e2f`	background	
`#7b68ee`	accent / buttons	
`#c7c7ff`	text	

---

🛡️ Legal
Use only on systems you own or have written permission to test.

Developer not responsible for misuse.

---

🤝 Contributing
1. Fork  
2. `git checkout -b feature-name`  
3. Pull Request

---

📜 License
MIT ‑ see [LICENSE](LICENSE)

---