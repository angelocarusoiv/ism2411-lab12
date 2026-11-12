# Lab 12: CSV Practice - Angelo Caruso

# Self Assesmtment Questions:

# 1: You've now completed a full ETL pipeline: read a CSV, transform the data, write a new CSV. How does this compare to doing the same task in Excel? What can Python do that Excel can't do easily, and vice versa?
# Python makes the ETL pipeline reproducible and easier to automate, while Excel is more convenient for quick visual inspection and manual edits.

# 2: Exercise 8 showed you append mode. Think of a real business process that would benefit from an append-mode log file — describe it and explain why append mode is the right tool.
# A real business process that would benefit from an append-mode file is an ordering system. It is the right tool because it preserves historical records by adding new entries to the bottom without overwriting past data.

# AI Disclosure:
# I used Google Gemini (High Thinking Level) to help explain how to import the CSV module, explain errors, and assist in coding for some exercises. I also used GitHub CoPilot to autofill lines.


import csv
import os
from datetime import datetime

sales_file = "data/sales.csv"

print("=== EXERCISE 2: Read and print raw rows ===")
with open(sales_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

print("=== EXERCISE 3: Skip the header ===")
with open(sales_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    print("Data rows:")
    for row in reader:
        print(row)

print("=== EXERCISE 4: Compute totals ===")
overall_total = 0.0
with open(sales_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        row_total = price * quantity
        overall_total += row_total
        print(f"{product}: {quantity} units x ${price:.2f} = ${row_total:.2f}")
print(f"Overall Total Revenue: ${overall_total:.2f}")

print("=== EXERCISE 5: Filter and write ===")
original_count = 0
written_count = 0
cleaned_rows = []

with open(sales_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    cleaned_header = header + ["total"]
    
    for row in reader:
        original_count += 1
        product, price_str, qty_str = row
        price = float(price_str)
        quantity = int(qty_str)
        row_total = price * quantity
        
        if row_total > 100:
            cleaned_rows.append([product, price, quantity, row_total])
            written_count += 1

os.makedirs("data", exist_ok=True)

with open("data/cleaned.csv", mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(cleaned_header)
    writer.writerows(cleaned_rows)

print(f"Original rows: {original_count}, Written rows (total > $100): {written_count}")

print("=== EXERCISE 6: csv.DictReader ===")
# csv.reader accesses columns by index numbers, which is simple but fragile if column positions change.
# csv.DictReader accesses columns by header names, making the code much easier to read and safer against column shifts.
dict_total = 0.0
with open(sales_file, mode="r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        price = float(row["price"])
        quantity = int(row["quantity"])
        dict_total += price * quantity
print(f"DictReader Total Revenue: ${dict_total:.2f} (Matches Exercise 4)")

print("=== EXERCISE 7: Sales summary by product ===")
product_summary = {}
with open(sales_file, mode="r", encoding="utf-8") as f:
    dict_reader = csv.DictReader(f)
    for row in dict_reader:
        product = row["product"]
        revenue = float(row["price"]) * int(row["quantity"])
        product_summary[product] = product_summary.get(product, 0.0) + revenue

for product in sorted(product_summary.keys()):
    print(f"{product}: ${product_summary[product]:.2f}")

print("=== EXERCISE 8: Append mode log ===")
total_revenue_for_log = 0.0
with open(sales_file, mode="r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        total_revenue_for_log += float(row[1]) * int(row[2])

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_entry = f"{timestamp} - Total Revenue: ${total_revenue_for_log:.2f}\n"

with open("data/run_log.txt", mode="a", encoding="utf-8") as f:
    f.write(log_entry)

print(f"Logged to data/run_log.txt: {log_entry.strip()}")