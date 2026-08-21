JOBS = [

    {
        "id": 1,
        "title": "Python Developer Intern",
        "company": "TechNova Solutions",
        "location": "Remote",
        "type": "Internship",
        "skills": [
            "Python",
            "Flask",
            "SQL",
            "Git"
        ],
        "salary": "₹15,000 - ₹25,000 / month"
    },

    {
        "id": 2,
        "title": "Data Analyst Intern",
        "company": "DataSphere Analytics",
        "location": "Delhi",
        "type": "Internship",
        "skills": [
            "Python",
            "Pandas",
            "SQL",
            "Power BI"
        ],
        "salary": "₹18,000 - ₹30,000 / month"
    },

    {
        "id": 3,
        "title": "Frontend Developer",
        "company": "WebCraft Technologies",
        "location": "Bangalore",
        "type": "Full Time",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ],
        "salary": "₹4 - ₹7 LPA"
    },

    {
        "id": 4,
        "title": "Machine Learning Intern",
        "company": "AI Labs India",
        "location": "Hyderabad",
        "type": "Internship",
        "skills": [
            "Python",
            "NumPy",
            "Pandas",
            "Machine Learning",
            "Scikit-learn"
        ],
        "salary": "₹20,000 - ₹35,000 / month"
    },

    {
        "id": 5,
        "title": "Full Stack Developer",
        "company": "CodeMatrix",
        "location": "Pune",
        "type": "Full Time",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Flask",
            "SQL",
            "Git"
        ],
        "salary": "₹5 - ₹9 LPA"
    },

    {
        "id": 6,
        "title": "Junior Data Scientist",
        "company": "InsightAI",
        "location": "Mumbai",
        "type": "Full Time",
        "skills": [
            "Python",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "SQL"
        ],
        "salary": "₹6 - ₹10 LPA"
    }

]


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):

    return skill.strip().lower()


# =========================================================
# CALCULATE MATCH
# =========================================================

def calculate_job_match(
    user_skills,
    job_skills
):

    user_skill_set = {

        normalize_skill(skill)

        for skill in user_skills
    }

    job_skill_set = {

        normalize_skill(skill)

        for skill in job_skills
    }


    if not job_skill_set:

        return 0


    matched = (
        user_skill_set
        &
        job_skill_set
    )


    score = (

        len(matched)
        /
        len(job_skill_set)

    ) * 100


    return round(score)


# =========================================================
# GET MATCHING JOBS
# =========================================================

def get_matching_jobs(user_skills):

    results = []


    user_skill_set = {

        normalize_skill(skill)

        for skill in user_skills
    }


    for job in JOBS:

        match = calculate_job_match(

            user_skills,

            job["skills"]
        )


        # ---------------------------------------------
        # IMPORTANT
        # Only show jobs having at least ONE
        # matching skill
        # ---------------------------------------------

        if match <= 0:

            continue


        matched_skills = []

        missing_skills = []


        for skill in job["skills"]:

            if normalize_skill(skill) in user_skill_set:

                matched_skills.append(
                    skill
                )

            else:

                missing_skills.append(
                    skill
                )


        job_result = job.copy()


        job_result["match"] = match


        job_result[
            "matched_skills"
        ] = matched_skills


        job_result[
            "missing_skills"
        ] = missing_skills


        results.append(
            job_result
        )


    # ---------------------------------------------
    # Best matching jobs first
    # ---------------------------------------------

    results.sort(

        key=lambda job:
        job["match"],

        reverse=True
    )


    return results