# **🎓 InternHub SNG — Платформа Поиска Вакансий и Стажировок**

**InternHub SNG** — это интерактивный веб\-сервис на базе Python и Flask, разработанный для автоматизированного поиска и умного подбора стажировок и вакансий в странах СНГ. Платформа анализирует актуальные вакансии из Excel-базы, позволяет фильтровать предложения по навыкам, формату работы и специальности, а также автоматически оценивает процент соответствия кандидата (Match Score) на основе загруженного PDF-резюме.

## **🌟 Основные Возможности (Features)**

* **📄 Умный разбор PDF-резюме (PDF Parsing):** Автоматическое считывание текста из загруженного файла резюме и выявление ключевых навыков пользователя.  
* **🎯 Алгоритм Match Score (% соответствия):** Динамический расчет процента подходимости вакансии (от 0% до 100%) на основе пересечения навыков и штрафов за несоответствие формата работы.  
* **🛠 Мульти-выбор навыков (до 7 элементов):** Удобный интерфейс фильтрации с чекбоксами для точного подбора вакансий по стеку технологий.  
* **🏢 Динамическая загрузка из Excel:** Автоматический импорт актуальных вакансий напрямую из документа .xlsx.  
* **🏠 Фильтрация по формату работы:** Быстрый отбор вакансий по типам *Remote* (удаленка), *Hybrid* (гибрид) и *Office* (офис).  
* **🎨 Современно оформленный Dark/Amber UI:** Элегантный графитовый интерфейс с золотисто-янтарными акцентами, разработанный для комфортного восприятия информации.

## **📐 Логика Алгоритма Оценки (Match Score Logic)**

1. **Базовый балл:** Формируется на основе доли совпавших навыков пользователя от всех требуемых навыков вакансии.  
2. **Штраф за формат работы (-20%):** Если пользователь указал желаемый формат (например, *Remote*), а вакансия предлагает иной (*Office* / *Hybrid*), итоговый показатель снижается на 20%.  
3. **Ранжирование:** Вакансии автоматический сортируются по убыванию процента соответствия.

## **🛠 Технологический Стек (Tech Stack)**

* **Backend:** Python 3.10+, Flask  
* **Data Processing & Parsing:** Pandas, OpenPyXL, PyPDF  
* **Frontend:** HTML5, CSS3 (Flexbox, CSS Variables), JavaScript (ES6+), Jinja2  
* **WSGI Server & Deployment:** Gunicorn, Render.com, GitHub

## **📁 Структура Проекта (Directory Structure)**

internhub/  
├── templates/  
│   └── index.html                       \# Главный HTML-шаблон с поддержкой Dark UI  
├── Copy of InternHub\_SNG\_Vacancies.xlsx \# База данных вакансий  
├── site.py                              \# Backend-логика Flask и обработка PDF/Excel  
├── requirements.txt                     \# Список необходимых Python-библиотек  
├── Procfile                             \# Команда запуска для хостинга Render  
└── README.md                            \# Документация проекта

## **⚙️ Файлы Конфигурации (Configuration Files)**

### **requirements.txt**

flask  
pandas  
openpyxl  
pypdf  
gunicorn

### **Procfile**

web: gunicorn site:app

## **💻 Локальный Запуск и Установка (Local Installation)**

1. **Клонируйте репозиторий:**  
   git clone https://github.com/your-username/internhub.git  
   cd internhub

2. **Создайте и активируйте виртуальное окружение (опционально):**  
   python \-m venv venv  
   \# Для Windows:  
   venv\\Scripts\\activate  
   \# Для macOS/Linux:  
   source venv/bin/activate

3. **Установите зависимости:**  
   pip install \-r requirements.txt

4. **Запустите Flask-приложение:**  
   python site.py

5. **Откройте в браузере:**  
   Перейдите по адресу http://127.0.0.1:5000/.

## **🚀 Деплой на GitHub и Render.com**

### **Шаг 1\. Публикация в GitHub**

1. Инициализируйте Git-репозиторий и загрузите файлы:  
   git init  
   git add .  
   git commit \-m "Initial commit InternHub SNG"  
   git branch \-M main  
   git remote add origin https://github.com/your-username/internhub.git  
   git push \-u origin main

### **Шаг 2\. Деплой на Render.com**

1. Зарегистрируйтесь / войдите на [Render.com](https://render.com/?utm_source=gemini).  
2. Нажмите **New \+** \-\> **Web Service**.  
3. Подключите ваш GitHub-репозиторий internhub.  
4. Укажите параметры:  
   * **Name:** internhub-sng (или любое другое имя)  
   * **Runtime:** Python 3  
   * **Build Command:** pip install \-r requirements.txt  
   * **Start Command:** gunicorn site:app  
5. Нажмите **Create Web Service** и дождитесь завершения сборки.

## **📝 Лицензия**

Проект создан в учебных и демонстрационных целях. Все права защищены.