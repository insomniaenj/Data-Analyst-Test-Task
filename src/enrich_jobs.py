import re


def analyze_support_size(vacancies_texts):
    pattern_a = re.compile(
        r"(команда|отдел|штат|поддержк\w+)\s+(из|более|около)?\s+(\d{2,4})\s+(человек|сотрудников|операторов)")

    combined_text = " ".join(vacancies_texts).lower()
    match = pattern_a.search(combined_text)

    if match:
        size = int(match.group(3))
        if size >= 10:
            return size, f"Прямое упоминание: {match.group(0)}", "site"

    if "24/7" in combined_text or "сменный график" in combined_text:
        return 12, "Оценка на основе сменного графика и объема найма", "jobs"

    return 0, None, None