#### Тестовое задание №1 (test1.py)
Код на Python, который будет отправлять заказчику среднесуточную температуру за
последние 7 суток по городам РФ. Справочник городов хранится в БД на SQL Server.
Код отправляет данные заказчику только при наличии непрерывной истории наблюдений
за последние 7 суток (включая последний имеющийся день наблюдений).
Инструмент должен использовать бесплатные источники информации.
#### Тестовое задание №3 (test3.py)
В БД есть две таблицы – общая история заправок автомобилей
(Автомобиль – Дата_и_время_заправки – Литров_заправлено) и журнал показаний одометров
автомобилей из части парка (Автомобиль – Дата_и_время – Пробег_накопительным_итогом).
Информация об остатке топлива в баках недоступна, этим показателем пренебрегаем.
Записи в журнале показаний одометров производятся через различные промежутки времени
(от «раз в 10 минут» до «раз в сутки»). Заправка автомобиля также производится в любое
время. Предложить вариант или несколько вариантов расчета и представления данных по
превышению расхода топлива (код view или хранимой процедуры). Цель – обратить внимание
пользователя финального view на автомобили с признаками явно аномального расхода. 