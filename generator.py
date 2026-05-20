import json
import random
from faker import Faker

fake = Faker('ru_RU') # Генерируем реалистичные российские данные
Faker.seed(42)

raw_data = []

# Создаем 100 реалистичных транзакций
for i in range(100):
    tx_id = f"TX_{1000 + i}"
    amount = round(random.uniform(100.0, 50000.0), 2)
    currency = random.choice(["RUB", "RUB", "RUB", "USD", "EUR"]) # В основном рубли
    status = random.choice(["SUCCESS", "SUCCESS", "SUCCESS", "FAILED", "PROCESSING"])
    
    # Искусственно вносим 15% брака (Data Quality аномалии)
    if random.random() < 0.15:
        anomaly_type = random.choice(["null_id", "negative_amount", "bad_status"])
        if anomaly_type == "null_id":
            tx_id = None
        elif anomaly_type == "negative_amount":
            amount = -amount
        elif anomaly_type == "bad_status":
            status = "ERROR_SYSTEM"

    record = {
        "tx_id": tx_id,
        "amount": amount,
        "meta": {
            "client_name": fake.name(),
            "currency": currency,
            "status": status
        }
    }
    raw_data = raw_data + [record]

# Записываем в файл
with open("raw_transactions.json", "w", encoding="utf-8") as f:
    for record in raw_data:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("Создан файл raw_transactions.json со 100 реалистичными транзакциями и аномалиями!")
