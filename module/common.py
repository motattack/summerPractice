import csv
import hashlib
import json
import os
import time


def stopwatch(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"[Watch] Execution time: {execution_time:.4f} seconds")
        return result

    return wrapper


def save_json(json_name, res):
    with open(json_name, "w", encoding="utf-8") as json_file:
        json.dump(res, json_file, indent=4, ensure_ascii=False)


def load_json(json_name):
    with open(json_name, "r", encoding="utf-8") as json_file:
        return json.load(json_file)


def delete_cvs():
    if os.path.exists("products.csv"):
        os.remove("products.csv")


def to_csv(res, fieldnames):
    with open('products.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(res)


def clear_price(price: str):
    if price is not None:
        return price.replace('₽', '').replace(' ', '').replace('\xa0', '')


def calculate_hash(data):
    hash_object = hashlib.md5(data.encode())
    return int(hash_object.hexdigest(), 16)
