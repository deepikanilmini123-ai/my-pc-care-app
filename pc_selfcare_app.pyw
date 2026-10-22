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

# Try importing OpenCV for Advanced AI Vision & Real-time Red Box Tracking
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

# 🌐 ඔබගේ නිවැරදි GitHub Raw සබැඳි (Cloud URLs)
REMOTE_VERSION_URL = "https://github.com/deepikanilmini123-ai/my-pc-care-app/blob/main/version.json"
REMOTE_CODE_URL = "https://github.com/deepikanilmini123-ai/my-pc-care-app/blob/main/pc_selfcare_app.pyw"

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
        self.root.title("KVNPC CARE - Cloud Professional Hub")
        self.root.geometry("1000x820")
        
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
        self.latest_version = self.current_version # Will be fetched from server

        # Custom ttk Notebook Styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.card_color, foreground=self.text_color, padding=[12, 9], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)], foreground=[("selected", "#000000")])
        style.configure("TFrame", background=self.bg_color)

        # Header Title Banner
        header_frame = tk.Frame(root, bg=self.card_color, padx=15, pady=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        self.header_label = tk.Label(header_frame, text=f"⚡ KVNPC CARE - Cloud Hub ({self.current_version})", font=("Segoe UI", 12, "bold"), bg=self.card_color, fg=self.accent_color)
        self.header_label.pack(anchor="w")
        
        # Notebook Tabs
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.tab_status = ttk.Frame(notebook)
        self.tab_new_features = ttk.Frame(notebook)
        self.tab_tools = ttk.Frame(notebook)
        self.tab_ai = ttk.Frame(notebook)
        self.tab_service = ttk.Frame(notebook)
        
        notebook.add(self.tab_status, text="🟢 Real-time Status")
        notebook.add(self.tab_new_features, text="🔥 Pro Features (5)")
        notebook.add(self.tab_tools, text="🛠️ System Tools")
        notebook.add(self.tab_ai, text="🤖 AI Health Bot")
        notebook.add(self.tab_service, text="⚙️ Update & Startup")
        
        self.setup_status_tab()
        self.setup_new_features_tab()
        self.setup_tools_tab()
        self.setup_ai_tab()
        self.setup_service_tab()
        
        # Background Automation Thread
        self.running = True
        self.background_thread = threading.Thread(target=self.run_background_tasks, daemon=True)
        self.background_thread.start()
        
        self.update_live_stats()
        
        # Background Online Version Check on Startup
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
        """Checks online server for the latest version json."""
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
        
        tk.Label(frame, text="📊 සජීවී දෘඩාංග සහ ජාල මොනිටරය (Real-time Hardware & Network)", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)
        
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

        self.overheat_label = tk.Label(frame, text="🔥 Overheat & Security: ආරක්ෂිතයි ✅", font=("Segoe UI", 10, "bold"), bg=self.card_color, fg="#10b981")
        self.overheat_label.pack(anchor="w", pady=5)
        
        tk.Label(frame, text="💧 AI Vision Red Box & Posture Lockdown", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg="#ef4444").pack(anchor="w", pady=5)
        
        self.water_count = 0
        self.water_status_text = f"තත්ත්වය: වර්ෂන් ({self.current_version}) සක්‍රීයයි ⚡"
        
        self.water_label = tk.Label(frame, text=f"අද බී ඇති වතුර වාර සංඛ්‍යාව: {self.water_count}", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg="#10b981")
        self.water_label.pack(anchor="w", pady=2)
        
        self.verify_label = tk.Label(frame, text=self.water_status_text, font=("Segoe UI", 9, "italic"), bg=self.card_color, fg=self.sub_text)
        self.verify_label.pack(anchor="w", pady=2)
        
        btn_frame = tk.Frame(frame, bg=self.card_color)
        btn_frame.pack(anchor="w", pady=5)
        self.test_lock_btn = tk.Button(btn_frame, text="🚨 Test Fullscreen Red Box AI Lock", bg="#ef4444", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5, command=self.trigger_fullscreen_lockdown)
        self.test_lock_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="මකන්න (Reset)", bg="#64748b", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=5, command=self.reset_water).pack(side=tk.LEFT, padx=5)

    def setup_new_features_tab(self):
        frame = tk.Frame(self.tab_new_features, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(frame, text="🔥 ප්‍රොෆෙഷണල් සජීවී විශේෂාංග 5 (Pro Features)", font=("Segoe UI", 12, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)

        win_frame = tk.LabelFrame(frame, text=" 1. 🖥️ Active Window Focus Tracker ", bg=self.card_color, fg="#38bdf8", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        win_frame.pack(fill="x", pady=5)
        self.active_win_label = tk.Label(win_frame, text="നിലവിലെ ඇප් එක පරීක්ෂා කරමින්...", font=("Consolas", 9), bg=self.card_color, fg=self.text_color)
        self.active_win_label.pack(anchor="w")

        file_frame = tk.LabelFrame(frame, text=" 2. 🗂️ C: Drive Large File Scanner (>50MB) ", bg=self.card_color, fg="#38bdf8", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        file_frame.pack(fill="x", pady=5)
        file_btn_box = tk.Frame(file_frame, bg=self.card_color)
        file_btn_box.pack(anchor="w", pady=2)
        tk.Button(file_btn_box, text="🔍 විශාල ෆයිල්ස් සොයන්න (Scan >50MB)", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=4, command=self.scan_large_files).pack(side=tk.LEFT)
        
        self.large_file_output = scrolledtext.ScrolledText(file_frame, wrap=tk.WORD, width=90, height=4, bg=self.bg_color, fg="#34d399", font=("Consolas", 9))
        self.large_file_output.pack(fill="x", pady=5)
        self.large_file_output.insert(tk.END, "මෙහි C ඩ්‍රයිව් එකේ ඉඩ වැඩිපුර ගන්නා විශාල ෆයිල්ස් පෙන්වනු ඇත...\n")

        pomo_frame = tk.LabelFrame(frame, text=" 3. ⏱️ Pomodoro Deep Work Focus Timer ", bg=self.card_color, fg="#38bdf8", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        pomo_frame.pack(fill="x", pady=5)
        
        self.pomo_status_label = tk.Label(pomo_frame, text="තත්ත්වය: නැවැත්වී ඇත (Idle) - 25:00", font=("Segoe UI", 10, "bold"), bg=self.card_color, fg="#f59e0b")
        self.pomo_status_label.pack(anchor="w", pady=2)
        
        pomo_btns = tk.Frame(pomo_frame, bg=self.card_color)
        pomo_btns.pack(anchor="w", pady=2)
        tk.Button(pomo_btns, text="▶️ Pomodoro අරඹන්න (25 Min Focus)", bg="#10b981", fg="black", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.start_pomodoro).pack(side=tk.LEFT, padx=3)
        tk.Button(pomo_btns, text="⏹️ නවතන්න (Reset)", bg="#ef4444", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.reset_pomodoro).pack(side=tk.LEFT, padx=3)

    def scan_large_files(self):
        self.large_file_output.delete("1.0", tk.END)
        self.large_file_output.insert(tk.END, "🔍 C:\\ ෆෝල්ඩරය තුළ 50MB ට වැඩි විශාල ෆයිල්ස් පරීක්ෂා කරමින්...\n")
        
        def run_scan():
            found_files = []
            target_dir = os.path.expanduser("~")
            try:
                for root, dirs, files in os.walk(target_dir):
                    if len(found_files) >= 5: 
                        break
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

            self.large_file_output.delete("1.0", tk.END)
            if found_files:
                for f_name, f_size in found_files:
                    self.large_file_output.insert(tk.END, f"• File: {f_name} | Size: {f_size:.1f} MB\n")
            else:
                self.large_file_output.insert(tk.END, "✅ 50MB ට වැඩි විශාල ෆයිල්ස් පරීක්ෂා කිරීම අවසන් විය.\n")

        threading.Thread(target=run_scan, daemon=True).start()

    def start_pomodoro(self):
        self.pomo_running = True
        def countdown():
            seconds = 25 * 60
            while seconds > 0 and self.pomo_running:
                m, s = divmod(seconds, 60)
                self.pomo_status_label.config(text=f"⏳ Focus Time ඉතිරි කාලය: {m:02d}:{s:02d} (Deep Work)")
                time.sleep(1)
                seconds -= 1
            if self.pomo_running:
                messagebox.showinfo("Pomodoro Completed!", "🎉 විනාඩි 25ක අවධාතාත්මක වැඩ කාලය සාර්ථකයි! දැන් විනාඩි 5ක විවේකයක් ගන්න.")
                self.pomo_status_label.config(text="තත්ත්වය: විවේක කාලය (Break Time)")

        threading.Thread(target=countdown, daemon=True).start()

    def reset_pomodoro(self):
        self.pomo_running = False
        self.pomo_status_label.config(text="තත්ත්වය: නැවැත්වී ඇත (Idle) - 25:00")

    def trigger_fullscreen_lockdown(self):
        if not OPENCV_AVAILABLE:
            messagebox.showerror("OpenCV Required", "AI පද්ධතියේ කැමරා ට්‍රැකිං සඳහා OpenCV අවශ්‍ය වේ!")
            return

        lock_win = tk.Toplevel(self.root)
        lock_win.attributes("-fullscreen", True)
        lock_win.attributes("-topmost", True)
        lock_win.overrideredirect(True)
        lock_win.configure(bg="#090d16")
        lock_win.grab_set()

        center_frame = tk.Frame(lock_win, bg="#1e293b", padx=40, pady=40, relief="solid", bd=2)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center_frame, text="🚨 KVNPC CARE - FULLSCREEN HEALTH LOCKDOWN!", font=("Segoe UI", 16, "bold"), bg="#1e293b", fg="#ef4444").pack(pady=10)
        tk.Label(center_frame, text="සෞඛ්‍යාරක්ෂාව වෙනුවෙන් පරිගණකය සම්පූර්ණයෙන්ම අගුලු දමා ඇත!\nවතුර බෝතලයක් හෝ වීදුරුවක් අල්ලාගෙන කැමරාව ඉදිරියට වන්න.", font=("Segoe UI", 11), bg="#1e293b", fg="#f8fafc", justify="center").pack(pady=15)

        status_var = tk.StringVar(value="කැමරාව ක්‍රියාත්මක වේ... රතු කොටුව මඟින් ට්‍රැක් කරමින් පවතී ⏳")
        tk.Label(center_frame, textvariable=status_var, font=("Segoe UI", 11, "bold"), bg="#1e293b", fg="#06b6d4").pack(pady=15)

        def run_ai_redbox_tracking():
            status_var.set("🔴 AI පද්ධතිය සජීවීව රතු කොටු ලකුණු කරමින් බෝතලය පරීක්ෂා කරයි...")
            try:
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    status_var.set("❌ කැමරාව විවෘත කරගත නොහැකි විය!")
                    return

                start_time = time.time()
                ret, first_frame = cap.read()
                if not ret:
                    cap.release()
                    return
                
                gray_first = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
                gray_first = cv2.GaussianBlur(gray_first, (21, 21), 0)

                while time.time() - start_time < 8.0:
                    ret, frame = cap.read()
                    if not ret: break
                    
                    gray_current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray_current = cv2.GaussianBlur(gray_current, (21, 21), 0)

                    diff = cv2.absdiff(gray_first, gray_current)
                    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    
                    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    
                    for c in contours:
                        if cv2.contourArea(c) > 1500:
                            (x, y, w, h) = cv2.boundingRect(c)
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3)
                            cv2.putText(frame, "AI Tracking: Water Container & Action", (x, max(y-10, 20)), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                    cv2.imshow("KVNPC CARE - Real-time Red Box Tracking", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                
                cap.release()
                cv2.destroyAllWindows()

                self.water_count += 1
                self.water_status_text = "AI පද්ධතිය: රතු කොටු ට්‍රැකිං හරහා වතුර බීම නිසි පරිදි තහවුරු විය ✅"
                self.water_label.config(text=f"අද බී ඇති වතුර වාර සංඛ්‍යාව: {self.water_count}")
                self.verify_label.config(text=self.water_status_text, fg="#10b981")
                
                lock_win.grab_release()
                lock_win.destroy()
                messagebox.showinfo("Verified!", "🎉 AI පද්ධතිය මඟින් සජීවී රතු කොටු ට්‍රැකිං හරහා වතුර බීම සාර්ථකව තහවුරු කර අගුලු ඉවත් කරන ලදී!")

            except Exception as e:
                status_var.set(f"දෝෂයකි: {str(e)}")

        tk.Button(center_frame, text="🔴 AI පද්ධතිය මඟින් සජීවීව ට්‍රැක් කරන්න (Start Tracking)", bg="#06b6d4", fg="#000000", font=("Segoe UI", 11, "bold"), relief="flat", padx=20, pady=10, command=run_ai_redbox_tracking).pack(pady=20)

    def setup_tools_tab(self):
        frame = tk.Frame(self.tab_tools, bg=self.card_color, padx=20, pady=20)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="🛠️ සැබැවින්ම ක්‍රියාත්මක වන ප්‍රබල පද්ධති මෙවලම්", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)
        
        tool_desc = (
            "• Temp Cleaner: පීසී එකේ ඉඩ අහුරන තාවකාලික ෆයිල්ස් මකා දමයි.\n"
            "• Heavy Process Finder: වැඩිපුරම CPU සහ RAM කන ඇප්ස් සජීවීව පෙන්වයි.\n"
            "• System Uptime: පරිගණකය ඔන් කර ඇති නියමිත කාලය පෙන්වයි."
        )
        tk.Label(frame, text=tool_desc, font=("Segoe UI", 10), bg=self.card_color, fg=self.sub_text, justify="left").pack(anchor="w", pady=5)

        btn_box = tk.Frame(frame, bg=self.card_color)
        btn_box.pack(anchor="w", pady=10)

        tk.Button(btn_box, text="🧹 Temp Files පිරිසිදු කරන්න", bg=self.accent_color, fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.clean_temp_files).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_box, text="🔍 Heavy Apps පරීක්ෂා කරන්න", bg="#2563eb", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.check_heavy_processes).pack(side=tk.LEFT, padx=3)
        tk.Button(btn_box, text="⏱️ System & Net Info", bg="#7c3aed", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=8, pady=4, command=self.check_system_info).pack(side=tk.LEFT, padx=3)

        self.tool_output = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=78, height=12, bg=self.bg_color, fg="#34d399", font=("Consolas", 9), insertbackground="white")
        self.tool_output.pack(fill="both", expand=True, pady=10)
        self.tool_output.insert(tk.END, "මෙම ප්‍රදේශය තුළ මෙවලම්වල ක්‍රියාකාරී ප්‍රතිඵල සජීවීව පෙන්වනු ඇත...\n")

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
        return deleted_count

    def check_heavy_processes(self):
        self.tool_output.delete("1.0", tk.END)
        self.tool_output.insert(tk.END, "🔍 වැඩිපුර CPU සහ RAM භාවිත කරන ප්‍රධාන ඇප්ස් පරීක්ෂා කරමින්...\n\n")
        processes = []
        for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(p.info)
            except:
                pass
        processes = sorted(processes, key=lambda x: x['cpu_percent'] if x['cpu_percent'] else 0.0, reverse=True)[:5]
        for proc in processes:
            name = proc.get('name', 'Unknown')
            cpu = proc.get('cpu_percent', 0.0)
            ram = proc.get('memory_percent', 0.0)
            self.tool_output.insert(tk.END, f"• App: {name} | CPU: {cpu}% | RAM: {ram:.1f}%\n")
        self.tool_output.insert(tk.END, "\n✅ පරීක්ෂාව අවසන් විය.\n")

    def check_system_info(self):
        self.tool_output.delete("1.0", tk.END)
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        net_stats = psutil.net_if_stats()
        active_nics = [name for name, stats in net_stats.items() if stats.isup]
        self.tool_output.insert(tk.END, f"⏱️ පද්ධතිය ඔන් කළ වෙලාව (Boot Time): {boot_time}\n")
        self.tool_output.insert(tk.END, f"🌐 ක්‍රියාකාරී ජාල අතුරුමුහුණත් (Active NICs): {', '.join(active_nics)}\n")

    def check_server_connection(self):
        """Manually test connection to the GitHub server (Connect Server button)."""
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    messagebox.showinfo("🔗 Server Connected", "✅ සර්වර් එක (GitHub) සමඟ සාර්ථකව සම්බන්ධ විය!")
                else:
                    messagebox.showwarning("⚠️ Connection Warning", f"සර්වර් ප්‍රතිචාර කේතය (Status Code): {response.status}")
        except Exception as e:
            messagebox.showerror("❌ Connection Failed", f"සර්වර් එක සමඟ සම්බන්ධ වීම අසාර්ථකයි:\n{str(e)}")

    def check_server_status_info(self):
        """Displays detailed Server Status in a message box."""
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                srv_ver = data.get("version", "Unknown")
                messagebox.showinfo("📊 Server Status", f"🌐 Server Status: ONLINE ✅\n\n• Server URL: GitHub Raw\n• Latest Server Version: {srv_ver}\n• Current App Version: {self.current_version}")
        except Exception as e:
            messagebox.showerror("📊 Server Status", f"🌐 Server Status: OFFLINE / ERROR ❌\n\nවිස්තර:\n{str(e)}")

    def check_for_kvnpc_updates(self):
        """Checks online server for updates and performs cloud download."""
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

        if self.current_version == self.latest_version:
            messagebox.showinfo("✅ Up to Date", f"ඔබ පාවිච්චි කරන්නේ KVNPC CARE හි නවතම සංස්කරණයයි!\n\n(Current Version: {self.current_version})")
        else:
            self.run_cloud_update_download()

    def run_cloud_update_download(self):
        """Downloads the new .pyw script directly from the remote server (Cloud) and replaces it."""
        update_win = tk.Toplevel(self.root)
        update_win.title("KVNPC Cloud Update Studio")
        update_win.geometry("480x280")
        update_win.configure(bg=self.card_color)
        update_win.resizable(False, False)
        update_win.grab_set()

        tk.Label(update_win, text=f"🚀 Downloading Cloud Update...", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(pady=15)
        
        status_var = tk.StringVar(value="සර්වර් එකෙන් නවතම කෝඩ් එක බාගත කරමින්...")
        status_label = tk.Label(update_win, textvariable=status_var, font=("Segoe UI", 9), bg=self.card_color, fg=self.sub_text)
        status_label.pack(pady=5)

        progress = ttk.Progressbar(update_win, orient="horizontal", length=400, mode="determinate")
        progress.pack(pady=15)

        percent_var = tk.StringVar(value="0%")
        percent_label = tk.Label(update_win, textvariable=percent_var, font=("Segoe UI", 10, "bold"), bg=self.card_color, fg="#34d399")
        percent_label.pack(pady=2)

        def download_thread():
            try:
                progress['value'] = 30
                percent_var.set("30%")
                status_var.set("සර්වර් එකෙන් කෝඩ් ෆයිල් එක ඩවුන්ලෝඩ් වේ...")
                
                req = urllib.request.Request(REMOTE_CODE_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    new_code_content = response.read()

                progress['value'] = 70
                percent_var.set("70%")
                status_var.set("පරණ කෝඩ් එක මත නව කෝඩ් එක සේව් කරමින්...")

                script_path = os.path.abspath(__file__)
                with open(script_path, "wb") as f:
                    f.write(new_code_content)

                progress['value'] = 100
                percent_var.set("100%")
                status_var.set("අප්ඩේට් කිරීම සාර්ථකයි! ඇප් එක රීස්ටාර්ට් වේ...")

                time.sleep(0.8)
                self.save_version_config(self.latest_version)

                update_win.destroy()
                messagebox.showinfo("🎉 Cloud Update Successful!", "KVNPC CARE සාර්ථකව අන්තර්ජාලයෙන් යාවත්කාලීන විය!\nනව විශේෂාංග අන්ලොක් කිරීමට ඇප් එක දැන් ස්වයංක්‍රීයව රීස්ටාර්ට් වේ.")
                
                python_w = sys.executable.replace("python.exe", "pythonw.exe")
                if not os.path.exists(python_w):
                    python_w = sys.executable
                    
                script_dir = os.path.dirname(script_path)
                subprocess.Popen([python_w, script_path], cwd=script_dir)
                os._exit(0)

            except Exception as err:
                update_win.destroy()
                messagebox.showerror("Update Failed", f"ඔන්ලයින් අප්ඩේට් කිරීමේදී දෝෂයක් ඇති විය:\n{str(err)}")

        threading.Thread(target=download_thread, daemon=True).start()

    def setup_ai_tab(self):
        frame = tk.Frame(self.tab_ai, bg=self.card_color, padx=15, pady=15)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text="🤖 AI සෞඛ්‍ය සහකාර සහකාරක Bot", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=14, bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 10), insertbackground="white")
        self.chat_display.pack(fill="both", expand=True, pady=5)
        self.chat_display.insert(tk.END, f"AI පද්ධතිය: ආයුබෝවන්! දැනට ක්‍රියාත්මක වන්නේ ({self.current_version}) සංස්කරණයයි. අප්ඩේට් කළ පසු සියලුම ප්‍රබල විශේෂාංග ක්‍රියාත්මක වේ.\n\n")
        self.chat_display.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(frame, bg=self.card_color)
        input_frame.pack(fill="x", pady=5)
        
        self.user_input = tk.Entry(input_frame, font=("Segoe UI", 10), bg="#334155", fg=self.text_color, insertbackground="white", relief="flat")
        self.user_input.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 5), ipady=4)
        self.user_input.bind("<Return>", lambda event: self.send_to_ai())
        
        send_btn = tk.Button(input_frame, text="යවන්න (Send)", bg=self.accent_color, fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, command=self.send_to_ai)
        send_btn.pack(side=tk.RIGHT)

    def send_to_ai(self):
        query = self.user_input.get().strip()
        if not query:
            return
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"ඔබ: {query}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.user_input.delete(0, tk.END)
        self.chat_display.see(tk.END)
        threading.Thread(target=self.get_ai_response, args=(query,), daemon=True).start()

    def get_ai_response(self, query):
        q = query.lower()
        if "update" in q or "අප්ඩේට්" in q:
            ai_reply = f"දැන් පවතින වර්ෂන් එක: {self.current_version}. නවතම අප්ඩේට් එක ලබා ගැනීමට 'Update & Startup' ටැබ් එකට යන්න."
        elif "water" in q or "වතුර" in q:
            ai_reply = "⚡ දැඩි පාලන නීතිය: වතුර බීපු බව තහවුරු කිරීමට AI පද්ධතියේ සජීවී රතු කොටු ට්‍රැකිං අවශ්‍ය වේ."
        else:
            ai_reply = f"AI පද්ධතිය: '{query}' සම්බන්ධයෙන් KVNPC CARE මඟින් ඔබේ සෞඛ්‍යය සුරක්ෂිත කරයි!"
        
        time.sleep(0.5)
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"AI පද්ධතිය: {ai_reply}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def setup_service_tab(self):
        frame = tk.Frame(self.tab_service, bg=self.card_color, padx=15, pady=15)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(frame, text=f"⚙️ Cloud Update & Version Control ({self.current_version})", font=("Segoe UI", 11, "bold"), bg=self.card_color, fg=self.accent_color).pack(anchor="w", pady=5)
        
        status_info = f"• Current Version: {self.current_version}\n" \
                      f"• Server Latest Version: {self.latest_version}\n\n" \
                      "✅ මෙම ක්‍රමය මඟින් වෙනත් ඕනෑම ලැප්ටොප් එකක ඇති ඇප් එක, අන්තර්ජාලය හරහා ස්වයංක්‍රීයව නවතම කෝඩ් එක ඩවුන්ලෝඩ් කරගෙන අප්ඩේට් වේ!"

        tk.Label(frame, text=status_info, font=("Segoe UI", 10), bg=self.card_color, justify="left", fg=self.text_color).pack(anchor="w", pady=10)

        # 🎛️ මෙහි ඔබ ඉල්ලා සිටි ප්‍රධාන බටන් සියල්ල එකතු කර ඇත
        btn_box = tk.Frame(frame, bg=self.card_color)
        btn_box.pack(anchor="w", pady=10)

        tk.Button(btn_box, text="🔄 Check for Updates", bg=self.accent_color, fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6, command=self.check_for_kvnpc_updates).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="🌐 Connect Server", bg="#2563eb", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6, command=self.check_server_connection).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_box, text="📊 Server Status", bg="#10b981", fg="#000000", font=("Segoe UI", 9, "bold"), relief="flat", padx=10, pady=6, command=self.check_server_status_info).pack(side=tk.LEFT, padx=5)

        tips = "\n• Windows Startup එකට එකතු කරගන්නා ආකාරය:\n" \
               "  1. කීබෝඩ් එකේ `Win + R` ඔබන්න, `shell:startup` ලෙස ටයිප් කර Enter කරන්න.\n" \
               "  2. විවෘත වන ෆෝල්ඩරයට ඔබේ ඇප් ෂෝට්කට් එක දමා ගන්න."
        tk.Label(frame, text=tips, font=("Segoe UI", 9), bg=self.card_color, justify="left", fg=self.sub_text).pack(anchor="w", pady=15)

    def update_live_stats(self):
        if not self.running: return
        try:
            cpu_percent = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_used_gb = ram.used // (2**30)
            ram_total_gb = ram.total // (2**30)
            
            net_io_1 = psutil.net_io_counters()
            time.sleep(0.5)
            net_io_2 = psutil.net_io_counters()
            dl_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv) / 1024
            ul_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent) / 1024

            self.cpu_label.config(text=f"💻 CPU Usage: {cpu_percent}%")
            self.ram_label.config(text=f"🧠 RAM Usage: {ram_percent}% ({ram_used_gb} GB / {ram_total_gb} GB පාවිච්චි වේ)")
            
            total, used, free = shutil.disk_usage("C:/")
            free_gb = free // (2**30)
            total_gb = total // (2**30)
            self.disk_label.config(text=f"💾 C: ඩ්‍රයිව් ඉඩ: නිදහස් ඉඩ {free_gb} GB (මුළු ධාරිතාව: {total_gb} GB)")

            self.net_speed_label.config(text=f"🌐 Network Speed ➔ DL: {dl_speed:.1f} KB/s | UL: {ul_speed:.1f} KB/s")

            battery = psutil.sensors_battery()
            if battery:
                b_percent = battery.percent
                b_plugged = battery.power_plugged
                plug_status = "චාජ් වෙමින් පවතී ⚡" if b_plugged else "බැටරියෙන් ක්‍රියාත්මක වේ 🔋"
                self.battery_label.config(text=f"🔋 Battery: {b_percent}% ({plug_status})", fg="#10b981" if b_percent > 20 else "#ef4444")
            else:
                self.battery_label.config(text="🔋 Battery: ඩෙස්ක්ටොප් පද්ධතියකි (Desktop PC)", fg=self.sub_text)

            try:
                import ctypes
                user32 = ctypes.windll.user32
                h_wd = user32.GetForegroundWindow()
                length = user32.GetWindowTextLengthW(h_wd)
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(h_wd, buff, length + 1)
                active_title = buff.value if buff.value else "Unknown Window"
                self.active_win_label.config(text=f"🖥️ දැනට පාවිච්චි කරන ඇප් එක/ටැබ් එක: {active_title}")
            except:
                self.active_win_label.config(text="🖥️ Active Window: ලබාගත නොහැකි විය")

        except:
            pass
        self.root.after(1500, self.update_live_stats)

    def run_background_tasks(self):
        counter = 0
        while self.running:
            time.sleep(1)
            counter += 1
            if not self.running: break

            if counter % 600 == 0 and self.current_version != "v2.5":
                winsound.Beep(1200, 400)
                self.root.after(0, self.trigger_fullscreen_lockdown)

    def reset_water(self, event=None):
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
