#  Who’s Snooping?

**Who’s Snooping** is a small, no-BS Python tool that shows you **who’s actually connected to your local network**.

No hacking.  
No packet sniffing.  
No shady stuff.

Just good old **network visibility** .. because it’s *your* house and *your* Wi-Fi.

---

## What it does

- Scans your local network using ARP
- Lists all connected devices with:
  - IP address
  - MAC address
  - Vendor (when possible)
- Helps you spot:
  - Phones
  - Laptops
  - Routers
  - IoT devices
  - Anything that doesn’t belong 👀

---

What it does *not* do

Let’s be clear:

- No spying on traffic
- No sniffing packets
- No passwords
- No intrusion

This tool only asks one question:

“Who’s currently on my network?”

That’s it.

---

Requirements

- Linux (tested on Debian / Ubuntu)
- Python 3
- `scapy` (installed system-wide)

Install Scapy:
```bash
sudo apt install python3-scapy

How to run:

Clone the Repo: git clone git@github.com:Hishamkhashman1/whos_snooping.git
cd whos_snooping

Run it: sudo python3 main.py

and thats it :D 



