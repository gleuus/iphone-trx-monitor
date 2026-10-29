"""Experimental public-page stock check; third-party indications are NOT Apple confirmation."""
import os
import re
import sys
from datetime import datetime, timezone
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

URL = 'https://instockradar.com/my/store/exchangetrx/iphone-duo'
APPLE = 'https://www.apple.com/my/shop/buy-iphone/iphone-duo'
BOT = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT = os.getenv('TELEGRAM_CHAT_ID')

CONFIGS = [(capacity, color) for capacity in ('512GB', '1TB') for color in ('Star White', 'Night Sky')]


def read_status(text, capacity, color):
    # Require an exact configuration name and a nearby *standalone* stock status.
    storage = r'512\s*GB' if capacity == '512GB' else r'(?:1\s*TB|1024\s*GB)'
    pattern = re.compile(rf'(?<!\w){storage}\s+{re.escape(color)}\b', re.I)
    statuses = []
    for match in pattern.finditer(text):
        lines = [s.strip() for s in text[match.end():match.end()+180].splitlines() if s.strip()]
        if lines and re.match(r'^(?:MYR|RM)\s*[\d,]+(?:\.\d\d)?$', lines[0], re.I):
            lines.pop(0)
        if lines and re.fullmatch(r'(?:In stock|Available)', lines[0], re.I):
            statuses.append('in_stock')
        elif lines and re.fullmatch(r'(?:Sold out|Out of stock|Unavailable)', lines[0], re.I):
            statuses.append('sold_out')
    # Don't notify on missing/conflicting/ambiguous rows.
    return statuses[0] if len(statuses) == 1 else 'unverified'


def main():
    r = requests.get(URL, timeout=25, headers={'User-Agent': 'Mozilla/5.0 (compatible; PersonalStockChecker/1.0)'})
    r.raise_for_status()
    page_text = BeautifulSoup(r.text, 'html.parser').get_text('\n', strip=True)
    statuses = {(capacity, color): read_status(page_text, capacity, color) for capacity, color in CONFIGS}
    print('Third-party statuses:', statuses)
    available = [(capacity, color) for (capacity, color), status in statuses.items() if status == 'in_stock']
    if not available:
        print('No matching public-page stock indication; no alert.')
        return
    if not BOT or not CHAT:
        sys.exit('Indicated stock, but Telegram secrets are missing; no alert.')
    when = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [f'Possible iPhone Duo stock at Apple The Exchange TRX ({when}):',
             *[f'• {capacity} {color}' for capacity, color in available],
             'UNVERIFIED third-party listing. Check Apple pickup availability before traveling.',
             'Apple: ' + APPLE,
             'Listing: ' + URL]
    resp = requests.post(f'https://api.telegram.org/bot{BOT}/sendMessage', data={'chat_id': CHAT, 'text': '\n'.join(lines)}, timeout=15)
    resp.raise_for_status()
    print('Tentative third-party stock indication sent to Telegram.')


if __name__ == '__main__':
    main()
