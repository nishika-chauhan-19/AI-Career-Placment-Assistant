import re


SKILLS = [
    "Python",
    "Java",
    "C",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Flask",
    "Django",
    "SQL",
    "MySQL",
    "MongoDB",
    "Git",
    "GitHub",
    "REST API",
    "Pandas",
    "NumPy",
    "Matplotlib",
    "Power BI",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Data Analysis",
    "Data Science",
    "Excel",
    "Linux",
    "AWS"
]


def clean_text(text):

    text = text.replace("\n", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            found_skills.append(skill)


    return found_skills


def calculate_resume_score(
    text,
    skills
):

    score = 0

    text_lower = text.lower()


    # Skills score

    skill_score = min(
        len(skills) * 4,
        40
    )

    score += skill_score


    # Resume sections

    sections = [

        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
        "achievements"

    ]


    section_score = 0

    for section in sections:

        if section in text_lower:

            section_score += 5


    score += min(
        section_score,
        30
    )


    # Project / experience content

    if "project" in text_lower:

        score += 10


    if "internship" in text_lower:

        score += 10


    if "experience" in text_lower:

        score += 10


    return min(
        score,
        100
    )


def get_score_label(score):

    if score >= 80:

        return "Excellent"

    elif score >= 60:

        return "Good"

    elif score >= 40:

        return "Average"

    else:

        return "Needs Improvement"


def analyze_resume(text):

    skills = extract_skills(text)

    score = calculate_resume_score(
        text,
        skills
    )

    label = get_score_label(
        score
    )


    return {

        "score": score,

        "label": label,

        "skills": skills,

        "word_count": len(
            text.split()
        )

    }