import os
import sys

# 1. Указываем ваш точный путь к архивной Java 17
os.environ["JAVA_HOME"] = r"C:\Program Files\java_17\jdk-17.0.12"
os.environ["PYSPARK_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# 2. Стартуем локальную сессию Spark (теперь без лишних флагов)
spark = SparkSession.builder \
    .appName("DataQualityPipeline") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

# Скрываем лишний системный мусор в логах
spark.sparkContext.setLogLevel("WARN")

# 3. Читаем JSON, который сгенерировал первый скрипт
df = spark.read.json("raw_transactions.json")

# 4. Распаковываем вложенную структуру meta
flat_df = df.select(
    col("tx_id"),
    col("amount"),
    col("meta.client_name").alias("client"),
    col("meta.currency").alias("currency"),
    col("meta.status").alias("status")
)

print("\n" + "="*40)
print("--- ПЕРВЫЕ 5 СТРОК ИСХОДНЫХ ДАННЫХ ---")
print("="*40)
flat_df.show(5)

# 5. Контроль качества данных (Data Quality)
valid_condition = (
    col("tx_id").isNotNull() & 
    (col("amount") > 0) & 
    (col("status") != "ERROR_SYSTEM")
)

good_data = flat_df.filter(valid_condition)
bad_data = flat_df.filter(~valid_condition)

print("\n" + "="*40)
print(f"[ОТЧЕТ DQ] Всего: {flat_df.count()} | Успешных: {good_data.count()} | Брак: {bad_data.count()}")
print("="*40)
# Автоматически создаем папку, если её нет на диске
os.makedirs("analytics_vault", exist_ok=True)

# Записываем чистые данные в CSV
good_data.toPandas().to_csv("analytics_vault/clean_transactions.csv", index=False, encoding="utf-8")
print("\n[УСПЕХ] Чистые данные успешно сохранены в файл clean_transactions.csv!")

# 7. Выводим бракованные строки для анализа
if bad_data.count() > 0:
    print("\n--- ПОДОЗРИТЕЛЬНЫЕ ДАННЫЕ (НАЙДЕН БРАК) ---")
    bad_data.show(5)

spark.stop()
