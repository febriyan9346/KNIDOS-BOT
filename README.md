<div align="center">

<img src="https://img.shields.io/badge/KNIDOS-BOT-00d4ff?style=for-the-badge&logo=ethereum&logoColor=white" alt="KNIDOS BOT"/>

# 🤖 KNIDOS BOT

**Automated bot for [Knidos Testnet](https://testnet.knidos.xyz/) — daily check-in, auto game play, multi-account & proxy support.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Web3](https://img.shields.io/badge/Web3.py-Enabled-F16822?style=flat-square&logo=ethereum&logoColor=white)](https://web3py.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Testnet](https://img.shields.io/badge/Knidos-Testnet-purple?style=flat-square)](https://testnet.knidos.xyz/)

> 🌐 **Website:** https://testnet.knidos.xyz/
>
> 💬 **Don't have the code? Find it on Discord:** https://t.co/qV48ONcjO1

</div>

---

## ✨ Features

| Feature | Description |
|:---:|---|
| 🔐 **Auto Login** | Signs in using wallet private key + EIP-712 signature |
| ✅ **Daily Check-in** | Automatically claims daily check-in rewards |
| 🎮 **Auto Play Game** | Plays `game_1` and claims points every session |
| 👥 **Multi-Account** | Process unlimited accounts from `accounts.txt` |
| 🌐 **Proxy Support** | Rotate proxies per account from `proxy.txt` |
| 🔄 **Auto Cycle** | Automatically repeats every 24 hours |
| 🎨 **Colored Logs** | Clean, color-coded terminal output with timestamps |

---

## 📋 Requirements

- Python **3.8+**
- pip packages listed in `requirements.txt`

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/febriyan9346/KNIDOS-BOT.git
cd KNIDOS-BOT
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup your accounts

Create `accounts.txt` and add your private keys (one per line):

```
your_private_key_1
your_private_key_2
your_private_key_3
```

> ⚠️ **Never share your private keys with anyone!**

### 4. (Optional) Setup proxies

Create `proxy.txt` and add proxies (one per line):

```
http://user:pass@ip:port
http://ip:port
socks5://user:pass@ip:port
```

### 5. Run the bot

```bash
python bot.py
```

---

## 🖥️ Usage

When you run the bot, you'll be prompted to select a mode:

```
============================================================
Select Mode:
1. Run with proxy
2. Run without proxy
============================================================
Enter your choice (1/2):
```

The bot will then:
1. Loop through all accounts in `accounts.txt`
2. Login using wallet signature
3. Perform daily check-in
4. Play game session and claim points
5. Wait 24 hours, then repeat

---

## 📁 File Structure

```
KNIDOS-BOT/
├── bot.py           # Main bot script
├── accounts.txt     # Your private keys (create this)
├── proxy.txt        # Your proxies (optional)
├── requirements.txt # Python dependencies
└── README.md
```

---

## 📦 Dependencies

```
requests
web3
eth-account
colorama
pytz
```

---

## ⚠️ Disclaimer

> This bot is provided for **educational purposes only**.
> Use it responsibly and at your own risk.
> The author is not responsible for any misuse, bans, or loss of funds.

---

## 💰 Support Us with Cryptocurrency

If you find this project helpful, consider supporting the developer:

<table>
  <tr>
    <th>Network</th>
    <th>Wallet Address</th>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/EVM-ETH%20%7C%20BSC%20%7C%20etc-627EEA?style=flat-square&logo=ethereum&logoColor=white"/></td>
    <td><code>0x216e9b3a5428543c31e659eb8fea3b4bf770bdfd</code></td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/TON-Telegram-0088CC?style=flat-square&logo=telegram&logoColor=white"/></td>
    <td><code>UQCEzXLDalfKKySAHuCtBZBARCYnMc0QsTYwN4qda3fE6tto</code></td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/SOL-Solana-9945FF?style=flat-square&logo=solana&logoColor=white"/></td>
    <td><code>9XgbPg8fndBquuYXkGpNYKHHhymdmVhmF6nMkPxhXTki</code></td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/SUI-Sui%20Network-4DA2FF?style=flat-square&logoColor=white"/></td>
    <td><code>0x8c3632ddd46c984571bf28f784f7c7aeca3b8371f146c4024f01add025f993bf</code></td>
  </tr>
</table>

---

<div align="center">

Made with ❤️ by **FEBRIYAN**

⭐ **Star this repo if it helped you!**

</div>
