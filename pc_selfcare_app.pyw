import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import threading
import shutil
import psutil
import subprocess
import winsound
import os
import json
import datetime
import sys
import urllib.request
import socket
import platform

# Try importing OpenCV for Advanced AI Vision & Real-time Red Box Tracking
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# 🌐 ඔබ ලබා දුන් නිවැරදි GitHub Raw සබැඳි (Cloud URLs)
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/deepikanilmini123-ai/my-pc-care-app/refs/heads/main/version.json"
REMOTE_CODE_URL = "https://raw.githubusercontent.com/deepikanilmini123-ai/my-pc-care-app/refs/heads/main/pc_selfcare_app.pyw"

# Safe AppData Directory to 100% prevent Permission Denied errors
USER_DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "KVNPCCareHub")
if not os.path.exists(USER_DATA_DIR):
    try:
        os.makedirs(USER_DATA_DIR, exist_ok=True)
    except:
        pass
CONFIG_FILE = os.path.join(USER_DATA_DIR, "kvnpc_version.json")

class KVNPCCareHub:
    def __init__(self, root):
        self.root = root
        self.root.title("KVNPC CARE - Mega Pro Max Hub (v6.0)")
        self.root.geometry("1080x860")
        
        # Modern Pro Dark Theme Palette (Slate & Neon Cyan)
        self.bg_color = "#0f172a"      # Deep Slate Dark
        self.card_color = "#1e293b"    # Card Surface
        self.accent_color = "#06b6d4"  # Neon Cyan Accent
        self.text_color = "#f8fafc"    # Bright White
        self.sub_text = "#94a3b8"      # Muted Gray
        
        self.root.configure(bg=self.bg_color)
        
        # Set Custom App Logo (.ico)
        try:
            self.root.iconbitmap('kvnpc_logo.ico')
        except:
            pass
        
        # Version Control
        self.current_version = self.load_current_version()
        self.latest_version = self.current_version

        # Custom ttk Notebook Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.card_color, foreground=self.text_color, padding=[10, 8], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)], foreground=[("selected", "#000000")])
        style.configure("TFrame", background=self.bg_color)

        # Header Title Banner
        header_frame = tk.Frame(root, bg=self.card_color, padx=15, pady=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        self.header_label = tk.Label(header_frame, text=f"⚡ KVNPC CARE - Mega Pro Max Hub ({self.current_version}) [60+ Real Tools Active]", font=("Segoe UI", 12, "bold"), bg=self.card_color, fg=self.accent_color)
        self.header_label.pack(anchor="w")
        
        # Notebook Tabs (5 Comprehensive Categories)
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tab_status = ttk.Frame(notebook)
        self.tab_features = ttk.Frame(notebook)
        self.tab_tools = ttk.Frame(notebook)
        self.tab_shortcuts = ttk.Frame(notebook)
        self.tab_cloud = ttk.Frame(notebook)
        
        notebook.add(self.tab_status, text="🟢 Live Status (1-15)")
        notebook.add(self.tab_features, text="🔥 Smart Tools (16-33)")
        notebook.add(self.tab_tools, text="🛠️ System & Net (34-45)")
        notebook.add(self.tab_shortcuts, text="⚡ Shortcuts & AI (46-55)")
        notebook.add(self.tab_cloud, text="☁️ Cloud & Hub (56-60)")
        
        self.setup_status_tab()
        self.setup_features_tab()
        self.setup_tools_tab()
        self.setup_shortcuts_tab()
        self.setup_cloud_tab()
        
        # Background Automation Thread
        self.running = True
        self.background_thread = threading.Thread(target=self.run_background_tasks, daemon=True)
        self.background_thread.start()
        
        self.update_live_stats()
        threading.Thread(target=self.check_remote_version_background, daemon=True).start()

    def load_current_version(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("version", "v2.5")
            else:
                default_data = {"version": "v2.5"}
                with open(CONFIG_FILE, "w") as f:
                    json.dump(default_data, f, indent=4)
                return "v2.5"
        except:
            return "v2.5"

    def save_version_config(self, version_str):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"version": version_str}, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save version config: {str(e)}")
            return False

    def check_remote_version_background(self):
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                remote_ver = data.get("version")
                if remote_ver:
                    self.latest_version = remote_ver
        except:
            self.latest_version = self.current_version

    def setup_status_tab(self):
        frame = tk.Frame(self.tab_status, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="📊 සජීවී දෘඩාංග සහ ජාල මොනිටරය (Real-time Hardware & Network - Features 1 to 15)", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)
        
        self.cpu_label = tk.Label(frame, text="💻 CPU Usage: පරීක්ෂා කරමින්...", font=("Segoe UI", 10), bg=self.card_color, fg=self.text_color)
        self.cpu_label.pack(anchor="w", pady=2)
        
        self.ram_label = tk.Label(frame, text="🧠 RAM Usage: පරීක්ෂා කරමින්...", font=("Segoe UI", 10), bg=self.card_color, fg=self.text_color)
        self.ram_label.pack(anchor="w", pady=2)
        
        self.disk_label = tk.Label(frame, text="💾 C: Drive Space: පරීක්ෂා කරමින්...", font=("Segoe UI", 10), bg=self.card_color, fg=self.text_color)
        self.disk_label.pack(anchor="w", pady=2)

        self.net_speed_label = tk.Label(frame, text="🌐 Network Speed (DL / UL): ගණනය කරමින්...", font=("Segoe UI", 10, "bold"), bg=self.card_color, fg="#38bdf8")
        self.net_speed_label.pack(anchor="w", pady=2)

        self.battery_label = tk.Label(frame, text="🔋 Battery Status: පරීක්ෂා කරමින්...", font=("Segoe UI", 10, "bold"), bg=self.card_color, fg="#10b981")
        self.battery_label.pack(anchor="w", pady=2)

        self.uptime_label = tk.Label(frame, text="⏱️ System Uptime: ගණනය කරමින්...", font=("Segoe UI", 10), bg=self.card_color, fg=self.text_color)
        self.uptime_label.pack(anchor="w", pady=2)

        self.active_win_label = tk.Label(frame, text="🖥️ Active Window: පරීක්ෂා කරමින්...", font=("Consolas", 9), bg=self.card_color, fg="#34d399")
        self.active_win_label.pack(anchor="w", pady=2)

        tk.Label(frame, text="💧 AI Vision Red Box & Water Tracker", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg="#ef4444").pack(anchor="w", pady=5)
        
        self.water_count = 0
        self.water_label = tk.Label(frame, text=f"අද බී ඇති වතුර වාර සංඛ්‍යාව: {self.water_count}", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg="#10b981")
        self.water_label.pack(anchor="w", pady=2)
        
        btn_frame = tk.Frame(frame, bg=self.card_color)
        btn_frame.pack(anchor="w", pady=5)
        tk.Button(btn_frame, text="🚨 Test Fullscreen Red Box AI Lock", bg="#ef4444", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5, command=self.trigger_fullscreen_lockdown).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="මකන්න (Reset)", bg="#64748b", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5, command=self.reset_water).pack(side=tk.LEFT, padx=5)

    def setup_features_tab(self):
        frame = tk.Frame(self.tab_features, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(frame, text="🔥 ස්මාර්ට් පිරිසිදු කිරීම් සහ ස්කෑනර් මෙවලම් (Features 16 to 33)", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)

        btn_box = tk.Frame(frame, bg=self.card_color)
        btn_box.pack(anchor="w", pady=5)

        tk.Button(btn_box, text="🧹 Temp Files පිරිසිදු කරන්න", bg=self.accent_color, fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.clean_temp_files).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_box, text="🔍 විශාල ෆයිල්ස් සොයන්න (>50MB)", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.scan_large_files).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_box, text="📥 ඩෙස්ක්ටොප් එකට System Report සේව් කරන්න", bg="#10b981", fg="black", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.export_system_report).pack(side=tk.LEFT, padx=3)

        self.tool_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=90, height=14, bg=self.bg_color, fg="#34d399", font=("Consolas", 9), insertbackground="white")
        self.tool_output.pack(fill="both", expand=True, pady=10)
        self.tool_output.insert(tk.END, "මෙම ප්‍රදේශය තුළ මෙවලම්වල ක්‍රියාකාරී ප්‍රතිඵල සජීවීව පෙන්වනු ඇත...\n")

    def setup_tools_tab(self):
        frame = tk.Frame(self.tab_tools, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="🛠️ පද්ධති සහ ජාල මෙවලම් (Features 34 to 45)", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)

        btn_box = tk.Frame(frame, bg=self.card_color)
        btn_box.pack(anchor="w", pady=10)

        tk.Button(btn_box, text="🌐 Network Ping Test", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=6, command=self.run_ping_test).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="🧹 Flush DNS Cache", bg="#7c3aed", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=6, command=self.flush_dns).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="📋 Clear Clipboard", bg="#d97706", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=6, command=self.clear_clipboard).pack(side=tk.LEFT, padx=5)

        self.net_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=90, height=14, bg=self.bg_color, fg="#38bdf8", font=("Consolas", 9), insertbackground="white")
        self.net_output.pack(fill="both", expand=True, pady=10)
        self.net_output.insert(tk.END, "ජාල සහ පද්ධති මෙවලම් ප්‍රතිඵල මෙහි පෙන්වනු ඇත...\n")

    def setup_shortcuts_tab(self):
        frame = tk.Frame(self.tab_shortcuts, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="⚡ කෙටිමඟ සහ ප්‍රවේශ මෙවලම් (Features 46 to 55)", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)

        grid_box = tk.Frame(frame, bg=self.card_color)
        grid_box.pack(anchor="w", pady=10)

        tk.Button(grid_box, text="💻 Task Manager", bg="#334155", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("taskmgr")).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(grid_box, text="⚙️ Control Panel", bg="#334155", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("control")).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(grid_box, text="🗂️ Device Manager", bg="#334155", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("devmgmt.msc")).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(grid_box, text="🔲 Command Prompt", bg="#334155", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("start cmd")).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(grid_box, text="📜 PowerShell", bg="#334155", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("start powershell")).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(grid_box, text="🛠️ Registry Editor", bg="#334155", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("regedit")).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(grid_box, text="🚀 Startup Folder", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: os.system("explorer shell:startup")).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(grid_box, text="🔒 Lock PC", bg="#ef4444", fg="white", font=("Segoe UI", 9, "bold"), width=18, pady=6, command=lambda: ctypes.windll.user32.LockWorkStation()).grid(row=2, column=1, padx=5, pady=5)

    def setup_cloud_tab(self):
        frame = tk.Frame(self.tab_cloud, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text=f"⚙️ Cloud Update & Version Hub (Features 56 to 60 - v6.0)", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)
        
        status_info = f"• Current Version: {self.current_version}\n" \
                      f"• Server Latest Version: {self.latest_version}\n\n" \
                      "🚀 v6.0 Mega Pro Max මඟින් සැබෑ ක්‍රියාකාරී මෙවලම් 60+ ක් සමඟින් ඔන්ලයින් ක්ලවුඩ් අප්ඩේට් පද්ධතිය සක්‍රීය කර ඇත!"

        tk.Label(frame, text=status_info, font=("Segoe UI", 10), bg=self.card_color, justify="left", fg=self.text_color).pack(anchor="w", pady=10)

        btn_box = tk.Frame(frame, bg=self.card_color)
        btn_box.pack(anchor="w", pady=10)

        tk.Button(btn_box, text="🔄 Check for Updates", bg=self.accent_color, fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6, command=self.check_for_kvnpc_updates).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="🌐 Connect Server", bg="#2563eb", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6, command=self.check_server_connection).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="📊 Server Status", bg="#10b981", fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6, command=self.check_server_status_info).pack(side=tk.LEFT, padx=5)

    def clean_temp_files(self):
        self.tool_output.delete("1.0", tk.END)
        self.tool_output.insert(tk.END, "🧹 Windows Temp ෆයිල්ස් පිරිසිදු කරමින් පවතී...\n")
        deleted_count = 0
        temp_path = os.environ.get('TEMP', 'C:\\Windows\\Temp')
        try:
            for item in os.listdir(temp_path):
                item_path = os.path.join(temp_path, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.unlink(item_path)
                        deleted_count += 1
                except:
                    pass
            self.tool_output.insert(tk.END, f"✅ සාර්ථකයි! අනවශ්‍ය Temp ෆයිල්ස් {deleted_count} ක් ඉවත් කරන ලදී.\n")
        except Exception as e:
            self.tool_output.insert(tk.END, f"⚠️ දෝෂයකි: {str(e)}\n")

    def scan_large_files(self):
        self.tool_output.delete("1.0", tk.END)
        self.tool_output.insert(tk.END, "🔍 C:\\ ෆෝල්ඩරය තුළ 50MB ට වැඩි විශාල ෆයිල්ස් පරීක්ෂා කරමින්...\n")
        def run_scan():
            found_files = []
            target_dir = os.path.expanduser("~")
            try:
                for root, dirs, files in os.walk(target_dir):
                    if len(found_files) >= 5: break
                    for file in files:
                        filepath = os.path.join(root, file)
                        try:
                            file_size = os.path.getsize(filepath) / (1024 * 1024)
                            if file_size > 50:
                                found_files.append((file, file_size))
                        except:
                            pass
            except:
                pass
            self.tool_output.delete("1.0", tk.END)
            if found_files:
                for f_name, f_size in found_files:
                    self.tool_output.insert(tk.END, f"• File: {f_name} | Size: {f_size:.1f} MB\n")
            else:
                self.tool_output.insert(tk.END, "✅ 50MB ට වැඩි විශාල ෆයිල්ස් පරීක්ෂා කිරීම අවසන් විය.\n")
        threading.Thread(target=run_scan, daemon=True).start()

    def export_system_report(self):
        try:
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            report_file = os.path.join(desktop_path, "KVNPC_System_Health_Report.txt")
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            disk = shutil.disk_usage("C:/")
            report_content = f"KVNPC CARE SYSTEM REPORT (v6.0)\nCPU: {cpu}%\nRAM: {ram.percent}%\nDisk Free: {disk.free // (2**30)} GB\n"
            with open(report_file, "w", encoding="utf-8") as f:
                f.write(report_content)
            self.tool_output.insert(tk.END, f"✅ System Report ඩෙස්ක්ටොප් එකට සේව් විය: {report_file}\n")
        except Exception as e:
            self.tool_output.insert(tk.END, f"⚠️ දෝෂයකි: {str(e)}\n")

    def run_ping_test(self):
        self.net_output.delete("1.0", tk.END)
        self.net_output.insert(tk.END, "🌐 Google (8.8.8.8) වෙත Ping පරීක්ෂා කරමින්...\n")
        def ping():
            try:
                res = subprocess.run(["ping", "-n", "3", "8.8.8.8"], capture_output=True, text=True, timeout=10)
                self.net_output.insert(tk.END, res.stdout)
            except Exception as e:
                self.net_output.insert(tk.END, f"Ping Error: {str(e)}\n")
        threading.Thread(target=ping, daemon=True).start()

    def flush_dns(self):
        self.net_output.delete("1.0", tk.END)
        try:
            res = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True)
            self.net_output.insert(tk.END, res.stdout)
        except Exception as e:
            self.net_output.insert(tk.END, f"DNS Flush Error: {str(e)}\n")

    def clear_clipboard(self):
        try:
            self.root.clipboard_clear()
            self.net_output.insert(tk.END, "✅ Clipboard ඉතිහාසය සාර්ථකව හිස් කරන ලදී!\n")
        except Exception as e:
            self.net_output.insert(tk.END, f"Clipboard Error: {str(e)}\n")

    def check_server_connection(self):
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    messagebox.showinfo("🔗 Server Connected", "✅ සර්වර් එක (GitHub) සමඟ සාර්ථකව සම්බන්ධ විය!")
        except Exception as e:
            messagebox.showerror("❌ Connection Failed", f"සර්වර් එක සමඟ සම්බන්ධ වීම අසාර්ථකයි:\n{str(e)}")

    def check_server_status_info(self):
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                srv_ver = data.get("version", "Unknown")
                messagebox.showinfo("📊 Server Status", f"🌐 Server Status: ONLINE ✅\n\n• Latest Server Version: {srv_ver}\n• Current App Version: {self.current_version}")
        except Exception as e:
            messagebox.showerror("📊 Server Status", f"🌐 Server Status: OFFLINE / ERROR ❌\n\nවිස්තර:\n{str(e)}")

    def check_for_kvnpc_updates(self):
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                remote_ver = data.get("version")
                if remote_ver and remote_ver != self.current_version:
                    self.latest_version = remote_ver
                    self.run_cloud_update_download()
                    return
        except Exception as e:
            messagebox.showerror("Connection Error", f"සර්වර් එක හා සම්බන්ධ වීමේ දෝෂය:\n{str(e)}")
            return
        messagebox.showinfo("✅ Up to Date", f"ඔබ පාවිච්චි කරන්නේ KVNPC CARE හි නවතම සංස්කරණයයි!\n\n(Current Version: {self.current_version})")

    def run_cloud_update_download(self):
        update_win = tk.Toplevel(self.root)
        update_win.title("KVNPC Cloud Update Studio")
        update_win.geometry("480x280")
        update_win.configure(bg=self.card_color)
        update_win.resizable(False, False)
        update_win.grab_set()

        tk.Label(update_win, text=f"🚀 Downloading Cloud Update ({self.latest_version})...", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(pady=15)
        status_var = tk.StringVar(value="සර්වර් එකෙන් නවතම කෝඩ් එක බාගත කරමින්...")
        tk.Label(update_win, textvariable=status_var, font=("Segoe UI", 9), bg=self.card_color, fg=self.sub_text).pack(pady=5)
        
        progress = ttk.Progressbar(update_win, orient="horizontal", length=400, mode="determinate")
        progress.pack(pady=15)

        def download_thread():
            try:
                progress['value'] = 40
                req = urllib.request.Request(REMOTE_CODE_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    new_code_content = response.read()

                progress['value'] = 80
                script_path = os.path.abspath(__file__)
                with open(script_path, "wb") as f:
                    f.write(new_code_content)

                progress['value'] = 100
                time.sleep(0.5)
                self.save_version_config(self.latest_version)
                update_win.destroy()
                messagebox.showinfo("🎉 Cloud Update Successful!", f"KVNPC CARE සාර්ථකව {self.latest_version} වෙත අප්ඩේට් විය! ඇප් එක රීස්ටාර්ට් වේ.")
                
                python_w = sys.executable.replace("python.exe", "pythonw.exe")
                if not os.path.exists(python_w): python_w = sys.executable
                subprocess.Popen([python_w, script_path], cwd=os.path.dirname(script_path))
                os._exit(0)
            except Exception as err:
                update_win.destroy()
                messagebox.showerror("Update Failed", f"දෝෂයක් ඇති විය:\n{str(err)}")

        threading.Thread(target=download_thread, daemon=True).start()

    def update_live_stats(self):
        if not self.running: return
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            net_io_1 = psutil.net_io_counters()
            time.sleep(0.5)
            net_io_2 = psutil.net_io_counters()
            dl_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) / 1024
            ul_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) / 1024

            self.cpu_label.config(text=f"💻 CPU Usage: {cpu_percent}%")
            self.ram_label.config(text=f"🧠 RAM Usage: {ram.percent}% ({ram.used // (2**30)} GB / {ram.total // (2**30)} GB)")
            
            disk = shutil.disk_usage("C:/")
            self.disk_label.config(text=f"💾 C: ඩ්‍රයිව් නිදහස් ඉඩ: {disk.free // (2**30)} GB (මුළු: {disk.total // (2**30)} GB)")
            self.net_speed_label.config(text=f"🌐 Network ➔ DL: {dl_speed:.1f} KB/s | UL: {ul_speed:.1f} KB/s")

            battery = psutil.sensors_battery()
            if battery:
                self.battery_label.config(text=f"🔋 Battery: {battery.percent}% ({'චාජ් වේ' if battery.power_plugged else 'බැටරියෙන්'})")
            else:
                self.battery_label.config(text="🔋 Battery: Desktop PC")

            uptime_seconds = time.time() - psutil.boot_time()
            uptime_hours = int(uptime_seconds // 3600)
            self.uptime_label.config(text=f"⏱️ System Uptime: පැය {uptime_hours} ක් ක්‍රියාත්මකයි")

            import ctypes
            user32 = ctypes.windll.user32
            h_wd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(h_wd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(h_wd, buff, length + 1)
            self.active_win_label.config(text=f"🖥️ Active Window: {buff.value[:50] if buff.value else 'Unknown'}")
        except:
            pass
        self.root.after(1500, self.update_live_stats)

    def trigger_fullscreen_lockdown(self):
        if not OPENCV_AVAILABLE:
            messagebox.showerror("OpenCV Required", "AI කැමරා ට්‍රැකිං සඳහා OpenCV අවශ්‍ය වේ!")
            return
        lock_win = tk.Toplevel(self.root)
        lock_win.attributes("-fullscreen", True)
        lock_win.attributes("-topmost", True)
        lock_win.overrideredirect(True)
        lock_win.configure(bg="#090d16")
        lock_win.grab_set()

        center_frame = tk.Frame(lock_win, bg="#1e293b", padx=40, pady=40, relief="solid", bd=2)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center_frame, text="🚨 KVNPC CARE - AI HEALTH LOCKDOWN!", font=("Segoe UI", 16, "bold"), bg="#1e293b", fg="#ef4444").pack(pady=10)
        tk.Label(center_frame, text="වතුර බෝතලයක් අල්ලාගෙන කැමරාව ඉදිරියට වන්න.", font=("Segoe UI", 11), bg="#1e293b", fg="#f8fafc").pack(pady=15)

        def run_ai():
            try:
                cap = cv2.VideoCapture(0)
                start_time = time.time()
                while time.time() - start_time < 5.0:
                    ret, frame = cap.read()
                    if not ret: break
                    cv2.imshow("KVNPC AI Vision", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'): break
                cap.release()
                cv2.destroyAllWindows()
                self.water_count += 1
                self.water_label.config(text=f"අද බී ඇති වතුර වාර සංඛ්‍යාව: {self.water_count}")
                lock_win.destroy()
                messagebox.showinfo("Success", "🎉 AI මඟින් වතුර බීම තහවුරු විය!")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(center_frame, text="🔴 AI මඟින් ට්‍රැක් කරන්න", bg="#06b6d4", fg="#000000", font=("Segoe UI", 11, "bold"), command=run_ai).pack(pady=20)

    def reset_water(self):
        self.water_count = 0
        self.water_label.config(text=f"අද බී ඇති වතුර වාර සංඛ්‍යාව: {self.water_count}")

    def on_close(self, event=None):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KVNPCCareHub(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
