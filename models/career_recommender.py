# =========================================================
# CAREER PATHS
# =========================================================

CAREER_PATHS = [

    {
        "title": "Python Developer",

        "description":
            "Build backend applications, APIs and web solutions using Python.",

        "skills": [
            "Python",
            "Flask",
            "SQL",
            "Git",
            "REST API"
        ],

        "roles": [
            "Python Developer",
            "Backend Developer",
            "Flask Developer"
        ],

        "goals": [
            "Python Development",
            "Backend Development",
            "Software Development"
        ]
    },


    {
        "title": "Data Analyst",

        "description":
            "Analyze datasets and create insights, reports and dashboards.",

        "skills": [
            "Python",
            "Pandas",
            "NumPy",
            "SQL",
            "Power BI"
        ],

        "roles": [
            "Data Analyst",
            "Business Analyst",
            "Junior Data Analyst"
        ],

        "goals": [
            "Data Analytics",
            "Data Science"
        ]
    },


    {
        "title": "Machine Learning Engineer",

        "description":
            "Develop machine learning models and intelligent applications.",

        "skills": [
            "Python",
            "NumPy",
            "Pandas",
            "Scikit-learn",
            "Machine Learning"
        ],

        "roles": [
            "ML Engineer",
            "Machine Learning Intern",
            "AI Engineer"
        ],

        "goals": [
            "Machine Learning",
            "Artificial Intelligence",
            "Data Science"
        ]
    },


    {
        "title": "Frontend Developer",

        "description":
            "Create responsive and interactive user interfaces for web applications.",

        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ],

        "roles": [
            "Frontend Developer",
            "Web Developer",
            "UI Developer"
        ],

        "goals": [
            "Web Development",
            "Frontend Development"
        ]
    },


    {
        "title": "Full Stack Developer",

        "description":
            "Build complete web applications across frontend and backend technologies.",

        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Python",
            "Flask",
            "SQL",
            "Git"
        ],

        "roles": [
            "Full Stack Developer",
            "Web Developer",
            "Software Developer"
        ],

        "goals": [
            "Web Development",
            "Full Stack Development",
            "Software Development"
        ]
    },


    {
        "title": "Data Scientist",

        "description":
            "Use statistics, programming and machine learning to solve data problems.",

        "skills": [
            "Python",
            "Pandas",
            "NumPy",
            "Machine Learning",
            "Scikit-learn",
            "SQL"
        ],

        "roles": [
            "Data Scientist",
            "Junior Data Scientist",
            "Data Science Intern"
        ],

        "goals": [
            "Data Science",
            "Machine Learning",
            "Artificial Intelligence"
        ]
    }

]


# =========================================================
# NORMALIZE SKILL
# =========================================================

def normalize_skill(skill):

    return skill.strip().lower()


# =========================================================
# CALCULATE SKILL MATCH
# =========================================================

def calculate_career_match(
    user_skills,
    career_skills
):

    user_skills_normalized = {
        normalize_skill(skill)
        for skill in user_skills
    }

    career_skills_normalized = {
        normalize_skill(skill)
        for skill in career_skills
    }

    if not career_skills_normalized:
        return 0

    matched_skills = (
        user_skills_normalized
        &
        career_skills_normalized
    )

    percentage = (
        len(matched_skills)
        /
        len(career_skills_normalized)
    ) * 100

    return round(percentage)


# =========================================================
# GET MISSING SKILLS
# =========================================================

def get_skill_gap(
    user_skills,
    career_skills
):

    user_skills_normalized = {
        normalize_skill(skill)
        for skill in user_skills
    }

    missing_skills = []

    for skill in career_skills:

        if normalize_skill(skill) not in user_skills_normalized:

            missing_skills.append(skill)

    return missing_skills


# =========================================================
# GET MATCHED SKILLS
# =========================================================

def get_matched_skills(
    user_skills,
    career_skills
):

    user_skills_normalized = {
        normalize_skill(skill)
        for skill in user_skills
    }

    matched_skills = []

    for skill in career_skills:

        if normalize_skill(skill) in user_skills_normalized:

            matched_skills.append(skill)

    return matched_skills


# =========================================================
# CAREER GOAL MATCH
# =========================================================

def calculate_goal_match(
    career,
    career_goal
):

    if not career_goal:

        return 0

    user_goal = normalize_skill(
        career_goal
    )

    career_goals = {

        normalize_skill(goal)

        for goal in career.get(
            "goals",
            []
        )
    }

    if user_goal in career_goals:

        return 100

    return 0


# =========================================================
# RECOMMEND CAREERS
# =========================================================

def recommend_careers(
    user_skills,
    career_goal=None,
    limit=6
):

    recommendations = []

    for career in CAREER_PATHS:

        # ---------------------------------------------
        # Skill Match
        # ---------------------------------------------

        skill_match = calculate_career_match(

            user_skills,

            career["skills"]

        )


        # ---------------------------------------------
        # Goal Match
        # ---------------------------------------------

        goal_match = calculate_goal_match(

            career,

            career_goal

        )


        # ---------------------------------------------
        # FINAL SCORE
        # ---------------------------------------------
        #
        # Career goal = 40%
        # Resume skills = 60%
        #
        # This makes the recommendation
        # personalized to the selected goal.
        # ---------------------------------------------

        final_match = round(

            (
                skill_match * 0.60
            )
            +
            (
                goal_match * 0.40
            )

        )


        # ---------------------------------------------
        # Matched skills
        # ---------------------------------------------

        matched_skills = get_matched_skills(

            user_skills,

            career["skills"]

        )


        # ---------------------------------------------
        # Missing skills
        # ---------------------------------------------

        missing_skills = get_skill_gap(

            user_skills,

            career["skills"]

        )


        # ---------------------------------------------
        # Create result
        # ---------------------------------------------

        recommendation = {

            "title":
                career["title"],

            "description":
                career["description"],

            "roles":
                career["roles"],

            "required_skills":
                career["skills"],

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills,

            "match":
                final_match,

            "skill_match":
                skill_match,

            "goal_match":
                goal_match

        }


        recommendations.append(
            recommendation
        )


    # =====================================================
    # SORT
    # =====================================================

    recommendations.sort(

        key=lambda career:
            career["match"],

        reverse=True

    )


    return recommendations[:limit]


# =========================================================
# TOP CAREER
# =========================================================

def get_top_career(
    user_skills,
    career_goal=None
):

    recommendations = recommend_careers(

        user_skills,

        career_goal,

        limit=1

    )

    if recommendations:

        return recommendations[0]

    return None