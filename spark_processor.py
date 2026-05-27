import os
import sys

os.environ["JAVA_HOME"] = r"C:\Program Files\java_17\jdk-17.0.12"
os.environ["PYSPARK_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("DataQualityPipeline") \
    .master("local[*]") \
    .config("spark.ui.showConsoleProgress", "false") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

df = spark.read.json("raw_transactions.json")

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

os.makedirs("analytics_vault", exist_ok=True)

good_data.toPandas().to_csv("analytics_vault/clean_transactions.csv", index=False, encoding="utf-8")
print("\n[УСПЕХ] Чистые данные успешно сохранены в файл clean_transactions.csv!")

if bad_data.count() > 0:
    print("\n--- ПОДОЗРИТЕЛЬНЫЕ ДАННЫЕ (НАЙДЕН БРАК) ---")
    bad_data.show(5)

spark.stop()
