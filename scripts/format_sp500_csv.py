import csv
from datetime import datetime
from pathlib import Path

INPUT_PATH = Path(__file__).resolve().parent.parent / 'datasets' / 'S&P+500+Stock+Prices+2014-2017.csv' / 'S&P 500 Stock Prices 2014-2017.csv'
OUTPUT_PATH = Path(__file__).resolve().parent.parent / 'datasets' / 'S&P+500+Stock+Prices+2014-2017.csv' / 'S&P 500 Stock Prices 2014-2017_formatted.csv'

RUBRO_MAP = {
    # Technology
    'AAPL': 'tech', 'MSFT': 'tech', 'GOOGL': 'tech', 'GOOG': 'tech', 'META': 'tech', 'NVDA': 'tech',
    'INTC': 'tech', 'CSCO': 'tech', 'ORCL': 'tech', 'ADBE': 'tech', 'CRM': 'tech', 'IBM': 'tech',
    'HPQ': 'tech', 'AMAT': 'tech', 'AVGO': 'tech', 'QCOM': 'tech', 'TXN': 'tech', 'AMD': 'tech',
    'MU': 'tech', 'LRCX': 'tech', 'SWKS': 'tech', 'WDAY': 'tech', 'ANET': 'tech',
    # Finance
    'JPM': 'finance', 'BAC': 'finance', 'C': 'finance', 'WFC': 'finance', 'GS': 'finance', 'MS': 'finance',
    'AXP': 'finance', 'BRK.B': 'finance', 'SCHW': 'finance', 'USB': 'finance', 'PNC': 'finance',
    'TFC': 'finance', 'ICE': 'finance', 'SPGI': 'finance', 'MET': 'finance', 'AON': 'finance',
    'MMC': 'finance', 'BLK': 'finance', 'STT': 'finance',
    # Textile / apparel
    'PVH': 'textile', 'RL': 'textile', 'TPR': 'textile', 'GIL': 'textile', 'HBI': 'textile',
    'NKE': 'textile', 'LULU': 'textile', 'UA': 'textile', 'VFC': 'textile',
    # Healthcare
    'JNJ': 'healthcare', 'PFE': 'healthcare', 'MRK': 'healthcare', 'ABBV': 'healthcare',
    'TMO': 'healthcare', 'ABT': 'healthcare', 'BMY': 'healthcare', 'LLY': 'healthcare',
    'AMGN': 'healthcare', 'GILD': 'healthcare', 'CVS': 'healthcare', 'ANTM': 'healthcare',
    # Energy
    'XOM': 'energy', 'CVX': 'energy', 'COP': 'energy', 'SLB': 'energy', 'HAL': 'energy',
    'OXY': 'energy',
    # Consumer
    'KO': 'consumer', 'PEP': 'consumer', 'PG': 'consumer', 'WMT': 'consumer', 'COST': 'consumer',
    'MCD': 'consumer', 'SBUX': 'consumer', 'NKE': 'consumer', 'STZ': 'consumer',
    # Industrials
    'GE': 'industrial', 'BA': 'industrial', 'CAT': 'industrial', 'MMM': 'industrial',
    'LMT': 'industrial', 'RTX': 'industrial', 'HON': 'industrial', 'DE': 'industrial',
    # Communication
    'VZ': 'communication', 'T': 'communication', 'DIS': 'communication', 'NFLX': 'communication',
    'CMCSA': 'communication', 'TMUS': 'communication',
    # Materials
    'DD': 'materials', 'APD': 'materials', 'LIN': 'materials', 'ECL': 'materials',
    'CF': 'materials',
    # Utilities
    'DUK': 'utilities', 'SO': 'utilities', 'NEE': 'utilities', 'EXC': 'utilities',
    'AEP': 'utilities',
    # Real estate
    'PLD': 'real estate', 'SPG': 'real estate', 'EQR': 'real estate', 'PSA': 'real estate',
}


def season_for_month(month: int) -> str:
    if month in (12, 1, 2):
        return 'winter'
    if month in (3, 4, 5):
        return 'spring'
    if month in (6, 7, 8):
        return 'summer'
    return 'autumn'


def get_rubro(symbol: str) -> str:
    return RUBRO_MAP.get(symbol, 'other')


ENGLISH_MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]


def format_csv(input_path: Path, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with input_path.open(newline='') as src, output_path.open('w', newline='') as dst:
        reader = csv.DictReader(src)
        fieldnames = reader.fieldnames + ['Year', 'month', 'day', 'season', 'rubro']
        writer = csv.DictWriter(dst, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            date = datetime.strptime(row['date'], '%Y-%m-%d')
            row['Year'] = date.year
            row['month'] = ENGLISH_MONTHS[date.month - 1]
            row['day'] = date.strftime('%A')
            row['season'] = season_for_month(date.month)
            row['rubro'] = get_rubro(row['symbol'])
            writer.writerow(row)


if __name__ == '__main__':
    format_csv(INPUT_PATH, OUTPUT_PATH)
    print(f'Formatted CSV written to: {OUTPUT_PATH}')
