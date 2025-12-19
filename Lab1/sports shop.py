# Пример списка покупок
# Каждая покупка - это кортеж: (наименование, количество, цена за единицу)
purchases = [
    ("мяч", 3, 500),
    ("скакалка", 10, 150),
    ("гантели", 4, 2000),
    ("мяч", 2, 500),
    ("скакалка", 7, 150),
    ("мяч", 6, 550),
]

# а) Подсчет общего количества и общей выручки по каждому наименованию
sales_summary = {}

for item, quantity, price in purchases:
    if item not in sales_summary:
        sales_summary[item] = {"total_quantity": 0, "total_revenue": 0}
    
    sales_summary[item]["total_quantity"] += quantity
    sales_summary[item]["total_revenue"] += quantity * price

print("а) Отчет по продажам:")
for item, data in sales_summary.items():
    print(f"Товар: {item}, Общее количество: {data['total_quantity']}, Общая выручка: {data['total_revenue']}")

print("-" * 40)

# б) Найти товар с максимальным количеством проданных единиц
max_item = None
max_quantity = 0

for item, data in sales_summary.items():
    if data["total_quantity"] > max_quantity:
        max_quantity = data["total_quantity"]
        max_item = item

if max_item:
    print(f"б) Товар, проданный в наибольшем количестве: {max_item} ({max_quantity} шт.)")
else:
    print("б) Покупок не было.")