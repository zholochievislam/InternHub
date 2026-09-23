import os
from flask import Flask, render_template, request
import pandas as pd
from pypdf import PdfReader

app = Flask(__name__)

EXCEL_FILE = "Copy of InternHub_SNG_Vacancies.xlsx"

SPECIALTY_SKILLS = {
    "Бизнес-аналитика": [
        "1С",
        "Analytical thinking",
        "Analytics",
        "Banking systems",
        "Comparative analysis",
        "Data verification",
        "Databases",
        "English B2",
        "FinTech",
        "Jira",
        "Reporting",
    ],
    "Бухгалтерский учёт и финансы": [
        "1С",
        "Accounting",
        "Analysis",
        "English B2",
        "ERP",
        "Excel",
        "Finance",
        "FP&A",
        "Power BI",
        "Power Query",
        "Source documentation",
        "Tax accounting",
    ],
    "Финансы аналтитика": [
        "1С",
        "Accounting",
        "CFA / CP3P Preparation",
        "Controlling principles",
        "English B2",
        "Excel",
        "Financial analysis",
        "IFRS (МСФО)",
        "Power Point",
        "Power Query",
        "Proficient PC knowledge",
        "Tax regulations",
        "Word",
    ],
    "Маркетинг": [
        "Airtable",
        "Canva",
        "ClickUp",
        "English B2",
        "Figma",
        "Notion",
        "Problem solving",
        "Trello",
    ],
    "Консалтинг": [
        "Communication",
        "Consulting",
        "English B2",
        "Math",
        "Proficient English speaker",
        "Russian",
        "Softskills",
        "Tech-savvy",
    ],
    "Анализ данных": [
        "English B2",
        "English Intermediate+",
        "Excel",
        "Fundamentals of Statistics",
        "NumPy",
        "Pandas",
        "Power BI / Tableau",
        "Power Point",
        "Proficient PC knowledge",
        "Python",
        "R",
        "SQL",
        "Uzbek / Russian",
    ],
    "Engineering": [
        ".NET Foundation",
        "1С",
        "AI agents & Agile frameworks",
        "Algorithms",
        "CSS / HTML",
        "English B2",
        "Java / JavaScript",
        "OOP",
        "Python",
        "QA & Functional Testing",
        "SQL",
        "Test Documentation & Analysis",
    ],
}


def load_vacancies():
    if not os.path.exists(EXCEL_FILE):
        return []
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name="📋 Вакансии")
        df = df.dropna(subset=["💼 Вакансия"]).fillna("Не указано")
        vacancies = []
        for idx, row in df.iterrows():
            vacancies.append(
                {
                    "id": idx + 1,
                    "title": str(row.get("💼 Вакансия", "")),
                    "company": str(row.get("🏢 Компания", "")),
                    "field": str(row.get("🎓 Специальность", "")),
                    "city": str(row.get("📍 Город", "")),
                    "format": str(row.get("🏠 Формат", "")),
                    "experience": str(row.get("⏳ Опыт", "")),
                    "skills": str(row.get("Skills", "")),
                    "salary": str(row.get("💰 Зарплата", "")),
                    "link": str(row.get("🔗 Ссылка", "#")),
                    "status": str(row.get("Статус", "")),
                    "why_fits": str(row.get("💡 Почему подходит", "")),
                }
            )
        return vacancies
    except Exception as e:
        print(f"Ошибка при чтении Excel: {e}")
        return []


def extract_skills_from_pdf(pdf_file):
    """Извлекает текст из PDF-резюме и определяет имеющиеся навыки."""
    text = ""
    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + " "
    except Exception as e:
        print(f"Ошибка при считывании PDF: {e}")

    text_lower = text.lower()
    found_skills = set()

    # Собираем все известные навыки
    all_known_skills = set()
    for lst in SPECIALTY_SKILLS.values():
        all_known_skills.update(lst)

    for skill in all_known_skills:
        if skill.lower() in text_lower:
            found_skills.add(skill)

    # Проверка формата в резюме
    detected_format = ""
    if "remote" in text_lower or "удален" in text_lower:
        detected_format = "Remote"
    elif "hybrid" in text_lower or "гибрид" in text_lower:
        detected_format = "Hybrid"
    elif "office" in text_lower or "офис" in text_lower:
        detected_format = "Office"

    return list(found_skills)[:7], detected_format, text


def calculate_match_score(item, selected_skills, selected_format):
    score = 100

    if selected_skills:
        item_text = (item["skills"] + " " + item["title"]).lower()
        matched_count = sum(
            1 for sk in selected_skills if sk.lower() in item_text
        )
        skill_ratio = matched_count / len(selected_skills)
        score = int(skill_ratio * 100)

    if selected_format and item["format"].lower() != selected_format.lower():
        score = max(0, score - 20)

    return score


@app.route("/", methods=["GET", "POST"])
def index():
    resume_filename = None
    resume_extracted_skills = []

    if request.method == "POST":
        # Если загружено резюме
        if "resume" in request.files:
            file = request.files["resume"]
            if file and file.filename.endswith(".pdf"):
                resume_filename = file.filename
                extracted_skills, detected_fmt, _ = extract_skills_from_pdf(
                    file
                )
                resume_extracted_skills = extracted_skills

                # Берем данные из параметров формы или найденные из PDF
                selected_field = request.form.get("field", "").strip()
                selected_skills = extracted_skills[:7]
                selected_format = (
                    request.form.get("format", "").strip() or detected_fmt
                )
                query = request.form.get("query", "").strip().lower()
            else:
                query = ""
                selected_field = ""
                selected_skills = []
                selected_format = ""
        else:
            query = ""
            selected_field = ""
            selected_skills = []
            selected_format = ""
    else:
        query = request.args.get("query", "").strip().lower()
        selected_field = request.args.get("field", "").strip()
        selected_skills = request.args.getlist("skills")[:7]
        selected_format = request.args.get("format", "").strip()

    internships = load_vacancies()
    internships = [
        item for item in internships if item["status"].lower() == "active"
    ]

    fields = sorted(
        list(
            set(
                item["field"]
                for item in internships
                if item["field"] and item["field"] != "Не указано"
            )
        )
    )
    formats = sorted(
        list(
            set(
                item["format"]
                for item in internships
                if item["format"] and item["format"] != "Не указано"
            )
        )
    )

    if query:
        internships = [
            item
            for item in internships
            if query in item["title"].lower()
            or query in item["company"].lower()
            or query in item["city"].lower()
        ]

    if selected_field:
        internships = [
            item for item in internships if item["field"] == selected_field
        ]

    # Расчет процента соответствия
    for item in internships:
        item["match_score"] = calculate_match_score(
            item, selected_skills, selected_format
        )

    if selected_skills or selected_format:
        internships.sort(key=lambda x: x["match_score"], reverse=True)

    return render_template(
        "index.html",
        internships=internships,
        fields=fields,
        formats=formats,
        specialty_skills=SPECIALTY_SKILLS,
        query=query,
        selected_field=selected_field,
        selected_skills=selected_skills,
        selected_format=selected_format,
        resume_filename=resume_filename,
        resume_extracted_skills=resume_extracted_skills,
    )


if __name__ == "__main__":
    app.run(debug=True)