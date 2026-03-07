import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    date_time_match = re.search(r'(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})', content)
    receipt_date_time = date_time_match.group(1) if date_time_match else "Not found"

    payment_match = re.search(r'([А-Яа-я\s]+):\n\s*[\d\s,]+(?=\nИТОГО)', content)
    payment_method = payment_match.group(1).strip() if payment_match else "Not found"

    product_pattern = re.compile(
        r'\d+\.\n(.*?)\n(\d+,\d+)\s*x\s*([\d\s,]+\.\d{2})\n([\d\s,]+\.\d{2})', 
        re.DOTALL
    )

    products = []
    items = product_pattern.findall(content)

    for item in items:
        name = re.sub(r'\s+', ' ', item[0].strip())
        quantity = float(item[1].replace(',', '.'))
        unit_price = float(item[2].replace(' ', '').replace(',', '.'))
        total_price = float(item[3].replace(' ', '').replace(',', '.'))

        products.append({
            "product_name": name,
            "quantity": quantity,
            "unit_price": unit_price,
            "total_line_price": total_price
        })

    total_match = re.search(r'ИТОГО:\n\s*([\d\s,]+\.\d{2})', content)
    total_amount = float(total_match.group(1).replace(' ', '').replace(',', '.')) if total_match else 0.0

    receipt_data = {
        "metadata": {
            "date_time": receipt_date_time,
            "payment_method": payment_method,
            "calculated_total": total_amount
        },
        "items": products
    }

    return receipt_data

if __name__ == "__main__":
    try:
        data = parse_receipt('raw.txt')
        
        print(f"--- Receipt Summary ---")
        print(f"Date/Time: {data['metadata']['date_time']}")
        print(f"Payment:   {data['metadata']['payment_method']}")
        print("-" * 30)
        
        for i, item in enumerate(data['items'], 1):
            print(f"{i}. {item['product_name']}")
            print(f"   {item['quantity']} x {item['unit_price']} = {item['total_line_price']}")
        
        print("-" * 30)
        print(f"TOTAL AMOUNT: {data['metadata']['calculated_total']}")
        
        with open('parsed_receipt.json', 'w', encoding='utf-8') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=4)
            
    except FileNotFoundError:
        print("Error: raw.txt not found. Please place the file in the script directory.")