from datetime import date

# Каждый день представлен в виде кортежа: (дата, температура, осадки)
weather_data = [
    (date(2025, 1, 1), 5, 'дождь'),
    (date(2025, 4, 2), -3, 'снег'),
    (date(2025, 7, 3), 10, 'ясно'),
    (date(2025, 9, 4), 7, 'дождь'),
    (date(2025, 11, 5), 12, 'ясно'),
    (date(2025, 12, 6), 8, 'дождь'),
    # ... можно добавить больше данных, но для примера достаточно
]

# а) Средняя температура за год и количество солнечных дней
total_temp = 0
sunny_days_count = 0

for day in weather_data:
    temp = day[1]
    condition = day[2]
    total_temp += temp
    if condition == 'ясно':
        sunny_days_count += 1

average_temp = total_temp / len(weather_data) if weather_data else 0

print("а) Результаты:")
print(f"Средняя температура за год: {average_temp:.2f}°C")
print(f"Количество солнечных дней: {sunny_days_count}")

print("-" * 40)

# б) Все дни с дождём, отсортированные по температуре (по убыванию)
rainy_days = [day for day in weather_data if day[2] == 'дождь']
rainy_days_sorted = sorted(rainy_days, key=lambda x: x[1], reverse=True)

print("б) Дни с дождём, отсортированные по температуре (от самой высокой к самой низкой):")
for day in rainy_days_sorted:
    d, t, c = day
    print(f"{d}: {t}°C")