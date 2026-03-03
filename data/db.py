import pandas as pd
import numpy as np
from datetime import datetime
import os

class Registration:
    def __init__(self):
        self.file_name = "db.xlsx"
        # Сразу пустой DataFrame
        self.df = pd.DataFrame(columns=['ФИО', 'Возраст', 'Зарплата', 'Дата_обновления'])

    def load_data(self):
        """
        Загрузка данных из Excel-файла, если он существует
        """
        if os.path.exists(self.file_name):
            self.df = pd.read_excel(self.file_name, sheet_name="Сотрудники")
            self.fix_dtypes()
            print(f"Загружено {len(self.df)} записей")
        else:
            print('Создан новый файл базы данных')

    def save_data(self):
        """
        Сохранение данных в Excel с несколькими листами
        """
        with pd.ExcelWriter(self.file_name, engine='openpyxl') as writer:
            # Основной лист с данными
            self.df.to_excel(writer, sheet_name='Сотрудники', index=False)

            # Лист со статистикой
            if not self.df.empty:
                stats = self.get_statistics()
                stats.to_excel(writer, sheet_name='Статистика', index=False)    
                age_groups = self.group_by_age()
                age_groups.to_excel(writer, sheet_name='Возрастные группы', index=False)

    def add_user(self, message):
        """
        Парсинг сообщений с валидацией данных
        Ожидаемы формат: ФИО, возраст, ЗП
        Пример: Александр, 18, 30
        """
        try:
            # Разделяем строку и чистим пробелы 
            args = [arg.strip() for arg in message.text.split(',')]
            if len(args) != 3:
                return "Ошибка: Введите данные в формате: ФИО, возраст, зарплата"

            name, age, salary = args
            if not age.isdigit() or not salary.isdigit():
                return "Ошибка: Возраст и зарплата должны быть числами"
            age = int(age)
            salary = int(salary)

            if age < 18 or age > 100:
                return "Ошибка: Возраст должен быть от 18 до 100 лет"
            # Создаем новую запись
            new_record = pd.DataFrame({
                'ФИО':[name],
                'Возраст':[age],
                'Зарплата':[salary],
                'Дата_обновления':[datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            })

            # Добавляем к существующему DataFrame
            self.df = pd.concat([self.df, new_record], ignore_index=True)
            # Убеждаемся, что типы правильные 
            self.fix_dtypes()

            # Сохранение изменения
            self.save_data()
            return f"✅ Сотрудник {name} успешно добавлен!\nВсего сотрудников: {len(self.df)}"

        except Exception as e:
            return f"❌ Ошибка при добавлении {str(e)}"

    def delete_user(self, name):
        """
        Удаление сотрудников по ФИО с подтверждением
        """
        try:
            # Поиск сотрудника (частичное совпадение, регистрозависимый)
            mask = self.df['ФИО'].str.contains(name, case=False, na=False)

            if not mask.any():
                return f"❌ Сотрудник '{name}' не найден"
            
            # Проказываем найденных сотрудников
            found = self.df[mask]
            print("Найденные сотрудники:")
            print(found.to_string(index=False))

            # Удаляем (здесь можно добавить подтверждение)
            self.df = self.df[~mask]
            self.save_data()

            return f"✅ Удалено {mask.sum()} записей"
        except Exception as e:
            return f"❌ Ошибка при удалении: {str(e)}"
        
    def get_statistics(self):
        """
        Получение расширенной статистики по сотрудникам
        """
        if self.df.empty:
            return pd.DataFrame({"Статистика":["Нет данных"]})
        
        stats = {
            'Показатель':[
                'Всего сотрудников',
                'Средний возраст',
                'Медианный возраст',
                'Минимальный возраст',
                'Максимальный возраст',
                'Средняя зарплата',
                'Медианная зарплата',
                'Минимальная зарплата',
                'Максимальная зарплата',
                'Стандартное отклонение (возраст)',
                'Стандартное отклонение (зарплата)',
                'Сумма зарплат',
                '25-й перцентиль (возраст)',
                '75-й перцентиль (возраст)',
            ],
            'Значение': [
                len(self.df),
                round(self.df['Возраст'].mean(), 2),
                self.df['Возраст'].median(),
                self.df['Возраст'].min(),
                self.df['Возраст'].max(),
                round(self.df['Зарплата'].mean(), 2),
                self.df['Зарплата'].median(),
                self.df['Зарплата'].min(),
                self.df['Зарплата'].max(),
                round(self.df['Возраст'].std(), 2),
                round(self.df['Зарплата'].std(), 2),
                self.df['Зарплата'].sum(),
                self.df['Возраст'].quantile(0.25),
                self.df['Возраст'].quantile(0.75)
            ]
        }

        return pd.DataFrame(stats)
    
    def group_by_age(self):
        """
        Группировка сотрудников по возрастным категориям
        """
        bins = [18, 25, 35, 50, 100]
        labels = ['18-25 лет', '26-35 лет', '36-50 лет', '50+ лет']
        self.df['Возрастная_группа'] = pd.cut(self.df["Возраст"], bins=bins, labels=labels, right=False)

        grouped = self.df.groupby('Возрастная_группа').agg({
            'ФИО':'count',
            'Возраст': ['mean', 'min', 'max'],
            'Зарплата': ['mean', 'sum']
        }).round(2)

        grouped.columns = ['Количество', 'Ср.возраст', 'Мин.возраст', 'Макс.возраст', 'Ср.зарплата', 'Сумма_зарплат']
        return grouped.reset_index()
    
    def fix_dtypes(self):
        """Преобразует колонки в правильные типы данных"""
        if not self.df.empty:
            # Преобразуем Возраст и Зарплату в числовые типы
            self.df['Возраст'] = pd.to_numeric(self.df['Возраст'], errors='coerce')
            self.df['Зарплата'] = pd.to_numeric(self.df['Зарплата'], errors='coerce')
            # Удаляем строки с NaN (если были ошибки преобразования)
            self.df = self.df.dropna(subset=['Возраст', 'Зарплата'])
            # Преобразуем в int
            self.df['Возраст'] = self.df['Возраст'].astype(int)
            self.df['Зарплата'] = self.df['Зарплата'].astype(int)   

    def search_employees(self, criteria, value):
        """
        Поиск сотрудников по разным категориям
        """
        if criteria == 'age':
            # Поиск по возрасту (диапазон)
            result = self.df[self.df['Возраст'] == value]
        elif criteria == 'salary':
            # Поиск по зарплате (больше указанной)
            result = self.df[self.df['Зарплата'] >= value]
        elif criteria == 'name':
            # Поиск по имени (частичное совпадение)
            result = self.df[self.df['ФИО'].str.contains(value, case=False, na=False)]
        else:
            return None
        
        return result 
    
    def sort_employees(self, by='Зарплата', ascending=False):
        """
        Сортировка сотрудников
        """
        return self.df.sort_values(by=by, ascending=ascending)
    
    def update_salary(self, name, new_salary):
        """
        Обновление зарплаты сотрудника
        """
        mask = self.df['ФИО'].str.contains(name, case=False, na=False)
        if mask.any():
            self.df.loc[mask, 'Зарплата'] = new_salary
            self.save_data()
            return f"✅ Зарплата обновлена для {mask.sum()} сотрудников"
        return "❌ Сотрудник не найден"
    
    def get_top_earners(self, n=5):
        """
        Получение топ-N сотрудников по зарплате 
        """
        if not self.df.empty and self.df['Зарплата'].dtype == 'object':
            self.df['Зарплта'] = pd.to_numeric(self.df['Зарплата'])

        return self.df.nlargest(n, 'Зарплата')[['ФИО', 'Зарплата', 'Возраст']]
    
    def get_employee_summary(self):
        """
        Краткая сводка по сотрудникам
        """
        if self.df.empty:
            return "База данных пуста"
        
        summary = f"""
📊 СВОДКА ПО СОТРУДНИКАМ:
━━━━━━━━━━━━━━━━━━━━━
👥 Всего сотрудников: {len(self.df)}
📅 Средний возраст: {self.df['Возраст'].mean():.1f} лет
💰 Средняя зарплата: {self.df['Зарплата'].mean():.1f} тыс.руб
💵 Общий фонд ЗП: {self.df['Зарплата'].sum():.1f} тыс.руб

🏆 Топ-3 по зарплате:
{self.get_top_earners(3).to_string(index=False, header=False)}

📈 Возрастной состав:
{self.df['Возраст'].value_counts().sort_index().to_string()}
        """
        return summary
# Пример использования класса
if __name__ == "__main__":
    # Создаём экземпляр класса
    reg = Registration()
    # Загружаем существующие данные
    reg.load_data()

    # Пример добавления (имитация собщения)
    class Message:
        def __init__(self, text):
            self.text = text
        
    test_messages = [
        Message("Иван Петров, 25, 50"),
        Message("Мария Сидорова, 30, 75"),
        Message("Петр Иванов, 35, 100"),
    ]

    for msg in test_messages:
        result = reg.add_user(msg)
        print(result)

    # Выводим статистику 
    print("\n" + reg.get_employee_summary())

    # Пример класса
    print("\n🔍 Поиск сотрудников с зарплатой >= 70:")
    high_earners = reg.search_employees('salary', 70)
    if high_earners is not None and not high_earners.empty:
        print(high_earners.to_string(index=False))
    
    # Пример сортировки
    print("\n📋 Сортировка по возрасту (молодые → старшие):")
    sorted_by_age = reg.sort_employees(by='Возраст', ascending=True)
    print(sorted_by_age[['ФИО', 'Возраст', 'Зарплата']].to_string(index=False))
