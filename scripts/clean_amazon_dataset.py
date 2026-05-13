import csv
import re
from pathlib import Path

INPUT_PATH = Path('datasets/amazon/data/amazon.csv')
OUTPUT_PATH = Path('datasets/amazon/data/amazon_cleaned.csv')

CATEGORY_MAPPING = [
    ('decoration', ['décor', 'decor', 'decoration', 'home decor', 'phonecharms']),
    ('technology', ['electronics', 'computers', 'accessories', 'mobiles', 'smartphones', 'headphones', 'camera', 'networking', 'printers', 'usb', 'laptop', 'tablet', 'speakers', 'projector', 'batteries', 'poweraccessories', 'cameras&photography', 'cables', 'chargers', 'gaming', 'wireless', 'hdmi', 'router']),
    ('home', ['home&kitchen', 'kitchen', 'home', 'appliances', 'vacuum', 'heater', 'fans', 'waterheaters', 'coffee', 'purifier', 'cooktop', 'iron', 'blender', 'mixer', 'jojicer', 'sewing', 'laundry', 'airpurifier', 'humidifier', 'kettle', 'cookers', 'grinder', 'toaster', 'foodprocessors', 'roomheaters', 'storage']),
    ('office', ['officeproducts', 'office', 'stationery', 'paper', 'calculators', 'pen', 'prince', 'desk', 'notebook', 'officepaperproducts']),
    ('health', ['health', 'personalcare', 'medical', 'scales', 'health monitors', 'bathroom', 'medical supplies']),
    ('automotive', ['car&motorbike', 'car accessories', 'automobile', 'auto', 'airpurifier&ionizers']),
    ('toys', ['toys', 'games', 'craft', 'drawing', 'painting', 'colouring', 'arts&crafts']),
    ('clothes', ['clothes', 'apparel', 'fashion', 'wear', 'garment', 'footwear']),
    ('sports', ['sports', 'fitness', 'gym', 'outdoor', 'cycling', 'exercise']),
    ('beauty', ['beauty', 'makeup', 'cosmetics', 'personal care']),
]

PERCENT_BINS = [0, 25, 50, 75, 100]


def clean_price(value: str) -> float:
    if value is None:
        return 0.0
    cleaned = re.sub(r'[^0-9.]', '', value)
    return float(cleaned) if cleaned else 0.0


def clean_int(value: str) -> int:
    if value is None:
        return 0
    cleaned = re.sub(r'[^0-9]', '', value)
    return int(cleaned) if cleaned else 0


def map_discount_bin(value: str) -> str:
    if not value:
        return '0%'
    numeric = clean_int(value)
    nearest = min(PERCENT_BINS, key=lambda x: abs(x - numeric))
    return f'{nearest}%'


def map_global_category(category: str) -> str:
    if not category:
        return 'other'
    normalized = category.lower().replace(' ', '').replace('&', '').replace('|', ' ').replace(',', ' ')
    for target, keywords in CATEGORY_MAPPING:
        for kw in keywords:
            if kw in normalized:
                return target
    return 'other'


def main() -> None:
    rows = []
    skipped = 0
    with INPUT_PATH.open(newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            discounted_price = clean_price(row.get('discounted_price', ''))
            actual_price = clean_price(row.get('actual_price', ''))
            if actual_price == 0 and discounted_price == 0:
                skipped += 1
                continue
            discount_bin = map_discount_bin(row.get('discount_percentage', '0%'))
            mapped_category = map_global_category(row.get('category', ''))
            try:
                rating = float(row.get('rating') or 0.0)
            except ValueError:
                skipped += 1
                continue
            rating_count = clean_int(row.get('rating_count', '0'))
            rows.append({
                'product_id': row.get('product_id', '').strip(),
                'category': mapped_category,
                'actual_price': actual_price,
                'discounted_price': discounted_price,
                'discount_percentage': discount_bin,
                'rating': rating,
                'rating_count': rating_count,
            })
    print(f'Skipped {skipped} malformed rows.')

    with OUTPUT_PATH.open('w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['product_id', 'category', 'actual_price', 'discounted_price', 'discount_percentage', 'rating', 'rating_count']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f'Cleaned dataset created at {OUTPUT_PATH} with {len(rows)} rows.')


if __name__ == '__main__':
    main()
