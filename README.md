# PySpark Data Quality Checks

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PySpark 3.3+](https://img.shields.io/badge/PySpark-3.3+-orange.svg)](https://spark.apache.org/)

Набор функций для автоматической проверки качества данных в DataFrame с выводом отчёта в JSON/HTML.

**Проблема:** В ETL-пайплайнах 30% времени уходит на ручную проверку данных (null, дубликаты, выбросы).  
**Решение:** Библиотека из 5 функций, которые за 2 строки кода дают полный отчёт о качестве.

## Возможности

- Проверка на null / NaN
- Поиск дубликатов по указанным колонкам
- Статистика типов данных (inferred vs expected)
- Выбросы через IQR или z-score
- Валидация по регулярным выражениям (email, phone)

## Быстрый старт

```bash
git clone https://github.com/Vat00/pyspark-data-quality
cd pyspark-data-quality
pip install -r requirements.txt
