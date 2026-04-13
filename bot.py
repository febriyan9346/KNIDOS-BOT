import os
import sys
import time
import random
import requests
import json
import pytz
import itertools
from datetime import datetime
from web3 import Web3
from eth_account.messages import encode_defunct
from colorama import Fore, Style, init

os.system('clear' if os.name == 'posix' else 'cls')

import warnings
warnings.filterwarnings('ignore')

if not sys.warnoptions:
    os.environ["PYTHONWARNINGS"] = "ignore"

init(autoreset=True)
w3 = Web3()

class KnidosBot:
    def __init__(self):
        self.target_game = "game_1"
        self.max_retries = 3
    
    def get_wib_time(self):
        wib = pytz.timezone('Asia/Jakarta')
        return datetime.now(wib).strftime('%H:%M:%S')
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN}KNIDOS BOT{Style.RESET_ALL}
{Fore.WHITE}By: FEBRIYAN{Style.RESET_ALL}
{Fore.CYAN}============================================================{Style.RESET_ALL}
"""
        print(banner)
    
    def log(self, message, level="INFO"):
        time_str = self.get_wib_time()
        
        if level == "INFO":
            color = Fore.CYAN
            symbol = "[INFO]"
        elif level == "SUCCESS":
            color = Fore.GREEN
            symbol = "[SUCCESS]"
        elif level == "ERROR":
            color = Fore.RED
            symbol = "[ERROR]"
        elif level == "WARNING":
            color = Fore.YELLOW
            symbol = "[WARNING]"
        elif level == "CYCLE":
            color = Fore.MAGENTA
            symbol = "[CYCLE]"
        else:
            color = Fore.WHITE
            symbol = "[LOG]"
        
        print(f"[{time_str}] {color}{symbol} {message}{Style.RESET_ALL}")
    
    def random_delay(self, min_sec=1, max_sec=5):
        delay = random.randint(min_sec, max_sec)
        self.log(f"Delay {delay} seconds...", "INFO")
        time.sleep(delay)
    
    def show_menu(self):
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}1. Run with proxy")
        print(f"2. Run without proxy{Style.RESET_ALL}")
        print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}")
        
        while True:
            try:
                choice = input(f"{Fore.GREEN}Enter your choice (1/2): {Style.RESET_ALL}").strip()
                if choice in ['1', '2']:
                    return choice
                else:
                    print(f"{Fore.RED}Invalid choice! Please enter 1 or 2.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                exit(0)
    
    def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            hours = i // 3600
            minutes = (i % 3600) // 60
            secs = i % 60
            print(f"\r[COUNTDOWN] Next cycle in: {hours:02d}:{minutes:02d}:{secs:02d} ", end="", flush=True)
            time.sleep(1)
        print("\r" + " " * 60 + "\r", end="", flush=True)

    def read_file(self, filename):
        try:
            with open(filename, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            self.log(f"File {filename} not found.", "ERROR")
            return []

    def extract_message(self, data):
        if isinstance(data, str) and "Knidos Testnet Wallet Verification" in data:
            return data
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and "Knidos Testnet Wallet Verification" in value:
                    return value
                if isinstance(value, dict):
                    res = self.extract_message(value)
                    if res:
                        return res
        return None

    def login_account(self, private_key, proxy):
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key
            
        account = w3.eth.account.from_key(private_key)
        wallet_address = account.address

        for attempt in range(1, self.max_retries + 1):
            try:
                session = requests.Session()
                if proxy:
                    session.proxies = {"http": proxy, "https": proxy}

                headers = {
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br, zstd",
                    "content-type": "application/json",
                    "origin": "https://testnet.knidos.xyz",
                    "referer": "https://testnet.knidos.xyz/login",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
                }
                session.headers.update(headers)

                self.log("Fetching login challenge...", "INFO")
                res_challenge = session.post("https://testnet.knidos.xyz/api/wallet/challenge", json={"wallet": wallet_address, "challenge_type": "wallet_login"}, timeout=15)
                
                if res_challenge.status_code not in [200, 201]:
                    self.log(f"Challenge failed (Code: {res_challenge.status_code})", "WARNING")
                    time.sleep(3)
                    continue

                message_to_sign = self.extract_message(res_challenge.json())
                if not message_to_sign:
                    return None

                signable_message = encode_defunct(text=message_to_sign)
                signed_message = w3.eth.account.sign_message(signable_message, private_key=private_key)
                signature = signed_message.signature.hex()

                res_login = session.post("https://testnet.knidos.xyz/api/session/login/wallet", json={"wallet": wallet_address, "signature": signature}, timeout=15)

                if res_login.status_code in [200, 201]:
                    time_str = self.get_wib_time()
                    print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Login successful!{Style.RESET_ALL}")
                    return session
                else:
                    self.log("Login rejected by server.", "WARNING")
                    time.sleep(3)

            except Exception as e:
                self.log(f"Connection Error: {str(e)[:50]}", "WARNING")
                time.sleep(3)
                
        self.log("Skipping this account due to server unresponsiveness.", "ERROR")
        return None

    def daily_checkin(self, session):
        session.headers.update({"referer": "https://testnet.knidos.xyz/dashboard"})
        try:
            self.log("Processing Task: Daily Check-in", "INFO")
            res = session.post("https://testnet.knidos.xyz/api/checkin", timeout=15)
            data = res.json()
            
            if data.get("ok"):
                awarded = data.get("awarded_points", 0)
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Check-in Success! Reward: +{awarded} Points{Style.RESET_ALL}")
            else:
                self.log("Check-in already claimed today or failed", "WARNING")
        except Exception as e:
            self.log(f"Check-in Error: {str(e)[:50]}", "ERROR")

    def play_game(self, session):
        session.headers.update({"referer": f"https://testnet.knidos.xyz/dashboard?menu=games&game={self.target_game}"})
        
        try:
            self.log(f"Processing Task: Play Game {self.target_game}", "INFO")
            res_start = session.post("https://testnet.knidos.xyz/api/games/session", json={"game_key": self.target_game}, timeout=15)
            data_start = res_start.json()
            
            if not data_start.get("ok"):
                self.log("Failed to start session (Limit might be reached)", "ERROR")
                return None
                
            session_token = data_start["session_token"]
            payload = {"game_key": self.target_game, "session_token": session_token}
            
            TARGET_PING = 7 
            self.log("Playing game session...", "INFO")
            
            for i in range(TARGET_PING):
                try:
                    session.post("https://testnet.knidos.xyz/api/games/progress", json=payload, timeout=10)
                    self.log(f"Progress {i+1}/{TARGET_PING} sent", "INFO")
                except Exception:
                    pass
                
                time.sleep(random.uniform(12.0, 15.0))

            self.log("Time reached. Claiming points...", "INFO")
            time.sleep(random.uniform(2.0, 3.5)) 

            res_comp = session.post("https://testnet.knidos.xyz/api/games/complete", json=payload, timeout=15)
            data_comp = res_comp.json()

            if data_comp.get("ok"):
                awarded = data_comp.get("awarded_points", 0)
                total = data_comp.get("total_points", 0)
                time_str = self.get_wib_time()
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Claim Success! Reward: +{awarded} Points{Style.RESET_ALL}")
                print(f"[{time_str}] {Fore.GREEN}[SUCCESS] Total Points: {total} | Today: +{awarded}{Style.RESET_ALL}")
                return total
            else:
                self.log(f"Claim Failed: {data_comp.get('error', 'Unknown')}", "ERROR")
                return None

        except Exception as e:
            self.log(f"Game Error: {str(e)[:50]}", "ERROR")
            return None

    def run(self):
        self.print_banner()
        
        choice = self.show_menu()
        
        if choice == '1':
            self.log("Running with proxy", "INFO")
            proxies = self.read_file('proxy.txt')
        else:
            self.log("Running without proxy", "INFO")
            proxies = []
            
        private_keys = self.read_file('accounts.txt')
        
        if not private_keys:
            self.log("File accounts.txt is empty. Program terminated.", "ERROR")
            return
            
        total_accounts = len(private_keys)
        self.log(f"Loaded {total_accounts} accounts successfully", "INFO")
        
        print(f"\n{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
        
        proxy_cycle = itertools.cycle(proxies) if proxies else itertools.repeat(None)
        cycle = 1
        
        while True:
            self.log(f"Cycle #{cycle} Started", "CYCLE")
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            
            success_count = 0
            
            for i, pk in enumerate(private_keys):
                self.log(f"Account #{i+1}/{total_accounts}", "INFO")
                proxy = next(proxy_cycle)
                
                if proxy:
                    self.log(f"Proxy: {proxy}", "INFO")
                else:
                    self.log("Proxy: No Proxy", "INFO")
                
                account_address = w3.eth.account.from_key(pk if pk.startswith('0x') else '0x' + pk).address
                self.log(f"{account_address}", "INFO")
                
                self.random_delay()
                
                session = self.login_account(pk, proxy)
                if session:
                    self.daily_checkin(session)
                    self.random_delay()
                    
                    poin_akhir = self.play_game(session)
                    
                    if poin_akhir is not None:
                        success_count += 1
                
                if i < total_accounts - 1:
                    print(f"{Fore.WHITE}............................................................{Style.RESET_ALL}")
                    time.sleep(2)
            
            print(f"{Fore.CYAN}------------------------------------------------------------{Style.RESET_ALL}")
            self.log(f"Cycle #{cycle} Complete | Success: {success_count}/{total_accounts}", "CYCLE")
            print(f"{Fore.CYAN}============================================================{Style.RESET_ALL}\n")
            
            cycle += 1
            self.countdown(86400)

if __name__ == "__main__":
    try:
        bot = KnidosBot()
        bot.run()
    except KeyboardInterrupt:
        exit(0)
