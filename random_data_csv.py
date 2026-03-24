import csv
import random
from datetime import datetime, timedelta

random.seed(42)

number_of_records = input("Number of recors: ")

countries = [
    "Canada",
    "UK",
    "UAE",
    "Germany",
    "Estonia",
    "Netherlands",
    "Czechoslovakia",
    "Austria",
]
plans = [
    "Free",
    "Basic",
    "Basic plus",
    "Pro",
    "Pro plus",
    "Enterprise",
    "Ultimate",
    "Chuck Norris",
]


def random_signup_date():
    start = datetime(1993, 1, 1)
    end = datetime.now()
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


unique_transaction = 0


rows = []
for i in range(1, int(number_of_records) + 1):
    age = random.randint(18, 99)
    country = random.choice(countries)
    plan = random.choice(plans)
    monthly_spend = round(random.uniform(0, 1000), 2)
    random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    device = f"device_{random.randint(1, 300)}"
    random_decimal = random.randint(0, 100)

    rows.append(
        {
            "customer_id": f"CUST{i:08d}",
            "age": age,
            "country": country,
            "plan": plan,
            "device": device,
            "monthly_spend": monthly_spend,
            "IP": random_ip,
            "singup_date": random_signup_date(),
            "transaction_id": f"TRAN_{random_decimal}{i:08d}",
        }
    )

with open("customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Saved customers.csv")
