from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

import os

from werkzeug.utils import secure_filename

from models.career_recommender import (
    CAREER_PATHS,
    recommend_careers
)

from models.job_matcher import get_matching_jobs

from models.resume_analyzer import analyze_resume


# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "career-ai-secret-key"

UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder automatically

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================================
# HELPER FUNCTION
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        # -------------------------------------------------
        # Get form data
        # -------------------------------------------------

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        goal = request.form.get(
            "goal",
            ""
        ).strip()

        other_goal = request.form.get(
            "other_goal",
            ""
        ).strip()


        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not name:

            return render_template(
                "register.html",
                error="Please enter your name."
            )


        if not email:

            return render_template(
                "register.html",
                error="Please enter your email."
            )


        if not password:

            return render_template(
                "register.html",
                error="Please create a password."
            )


        if len(password) < 6:

            return render_template(
                "register.html",
                error=(
                    "Password must be at least "
                    "6 characters."
                )
            )


        if not goal:

            return render_template(
                "register.html",
                error=(
                    "Please select your career goal."
                )
            )


        # -------------------------------------------------
        # OTHER CAREER GOAL
        # -------------------------------------------------

        if goal == "Other":

            if not other_goal:

                return render_template(
                    "register.html",
                    error=(
                        "Please enter your "
                        "career goal."
                    )
                )

            goal = other_goal


        # -------------------------------------------------
        # SAVE REGISTERED USER
        # -------------------------------------------------

        session["registered_user"] = {

            "name": name,

            "email": email,

            "password": password,

            "goal": goal

        }


        # -------------------------------------------------
        # Clear old login/session data
        # -------------------------------------------------

        session.pop(
            "user",
            None
        )

        session.pop(
            "logged_in",
            None
        )

        session.pop(
            "resume_skills",
            None
        )

        session.pop(
            "resume_score",
            None
        )

        session.pop(
            "resume_result",
            None
        )


        # -------------------------------------------------
        # Go to LOGIN
        # -------------------------------------------------

        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        # -------------------------------------------------
        # Get login data
        # -------------------------------------------------

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()


        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        if not email:

            return render_template(
                "login.html",
                error="Please enter your email."
            )


        if not password:

            return render_template(
                "login.html",
                error="Please enter your password."
            )


        # -------------------------------------------------
        # Get registered account
        # -------------------------------------------------

        registered_user = session.get(
            "registered_user"
        )


        if not registered_user:

            return render_template(
                "login.html",
                error=(
                    "No account found. "
                    "Please create an account first."
                )
            )


        # -------------------------------------------------
        # Check email and password
        # -------------------------------------------------

        if (
            email != registered_user["email"]
            or
            password != registered_user["password"]
        ):

            return render_template(
                "login.html",
                error=(
                    "Incorrect email or password."
                )
            )


        # -------------------------------------------------
        # LOGIN SUCCESS
        # -------------------------------------------------

        session["user"] = {

            "name":
                registered_user["name"],

            "email":
                registered_user["email"],

            "goal":
                registered_user["goal"]

        }


        session["user_name"] = (
            registered_user["name"]
        )

        session["user_email"] = (
            registered_user["email"]
        )

        session["career_goal"] = (
            registered_user["goal"]
        )

        session["logged_in"] = True


        # -------------------------------------------------
        # Go to Resume
        # -------------------------------------------------

        return redirect(
            url_for("resume")
        )


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    # -----------------------------------------------------
    # Check login
    # -----------------------------------------------------

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # Get user information
    # -----------------------------------------------------

    user = session.get(
        "user",
        {}
    )


    # -----------------------------------------------------
    # Get resume information
    # -----------------------------------------------------

    resume_score = session.get(
        "resume_score",
        0
    )

    resume_skills = session.get(
        "resume_skills",
        []
    )


    # -----------------------------------------------------
    # Show profile
    # -----------------------------------------------------

    return render_template(

        "profile.html",

        user=user,

        resume_score=resume_score,

        resume_skills=resume_skills

    )


# =========================================================
# CAREER RECOMMENDATIONS
# =========================================================

@app.route("/career")
def career():

    # -----------------------------------------------------
    # Get resume skills
    # -----------------------------------------------------

    user_skills = session.get(
        "resume_skills",
        []
    )


    # -----------------------------------------------------
    # Get user's selected career goal
    # -----------------------------------------------------

    career_goal = session.get(
        "career_goal",
        ""
    )


    # -----------------------------------------------------
    # Generate personalized recommendations
    # -----------------------------------------------------

    recommendations = recommend_careers(

        user_skills,

        career_goal=career_goal,

        limit=6

    )


    # -----------------------------------------------------
    # Show career page
    # -----------------------------------------------------

    return render_template(

        "career.html",

        recommendations=recommendations,

        user_skills=user_skills,

        career_goal=career_goal

    )


# =========================================================
# JOB RECOMMENDATIONS
# =========================================================

@app.route("/jobs")
def jobs():

    # -----------------------------------------------------
    # Get resume skills
    # -----------------------------------------------------

    user_skills = session.get(
        "resume_skills",
        []
    )


    # -----------------------------------------------------
    # Get matching jobs
    # -----------------------------------------------------

    jobs = get_matching_jobs(
        user_skills
    )


    # -----------------------------------------------------
    # Show jobs
    # -----------------------------------------------------

    return render_template(

        "jobs.html",

        jobs=jobs,

        user_skills=user_skills

    )


# =========================================================
# JOB OPPORTUNITY DETAILS
# =========================================================

@app.route(
    "/job/<int:job_id>"
)
def job_detail(job_id):

    # -----------------------------------------------------
    # Check login
    # -----------------------------------------------------

    if "user" not in session:

        return redirect(
            url_for("login")
        )


    # -----------------------------------------------------
    # Get resume skills
    # -----------------------------------------------------

    user_skills = session.get(
        "resume_skills",
        []
    )


    # -----------------------------------------------------
    # Get matching jobs
    # -----------------------------------------------------

    matched_jobs = get_matching_jobs(
        user_skills
    )


    selected_job = None


    # -----------------------------------------------------
    # Find selected job
    # -----------------------------------------------------

    for job in matched_jobs:

        if job["id"] == job_id:

            selected_job = job

            break


    # -----------------------------------------------------
    # Job not found
    # -----------------------------------------------------

    if selected_job is None:

        return redirect(
            url_for("jobs")
        )


    # -----------------------------------------------------
    # Show job details
    # -----------------------------------------------------

    return render_template(

        "job_detail.html",

        job=selected_job

    )


# =========================================================
# RESUME UPLOAD + ANALYSIS
# =========================================================

@app.route(
    "/resume",
    methods=["GET", "POST"]
)
def resume():

    # -----------------------------------------------------
    # Check login
    # -----------------------------------------------------

    if not session.get("logged_in"):

        return redirect(
            url_for("login")
        )


    if request.method == "POST":

        # -------------------------------------------------
        # Get uploaded file
        # -------------------------------------------------

        file = request.files.get(
            "resume"
        )


        if file is None:

            return render_template(

                "resume.html",

                error=(
                    "Please select a resume."
                )

            )


        if file.filename == "":

            return render_template(

                "resume.html",

                error=(
                    "Please select a resume."
                )

            )


        # -------------------------------------------------
        # Check file extension
        # -------------------------------------------------

        if not allowed_file(
            file.filename
        ):

            return render_template(

                "resume.html",

                error=(
                    "Only PDF files are supported."
                )

            )


        # -------------------------------------------------
        # Secure filename
        # -------------------------------------------------

        filename = secure_filename(
            file.filename
        )


        filepath = os.path.join(

            app.config["UPLOAD_FOLDER"],

            filename

        )


        # -------------------------------------------------
        # Save file
        # -------------------------------------------------

        file.save(
            filepath
        )


        # -------------------------------------------------
        # Extract PDF text
        # -------------------------------------------------

        try:

            from PyPDF2 import PdfReader


            reader = PdfReader(
                filepath
            )


            text = ""


            for page in reader.pages:

                page_text = (
                    page.extract_text()
                )


                if page_text:

                    text += (
                        page_text
                        + "\n"
                    )


        except Exception as error:

            return render_template(

                "resume.html",

                error=(

                    "Unable to read the PDF. "

                    f"Error: {error}"

                )

            )


        # -------------------------------------------------
        # Check extracted text
        # -------------------------------------------------

        if not text.strip():

            return render_template(

                "resume.html",

                error=(

                    "No readable text was found "
                    "in this PDF."

                )

            )


        # -------------------------------------------------
        # Analyze resume
        # -------------------------------------------------

        try:

            result = analyze_resume(
                text
            )


        except Exception as error:

            return render_template(

                "resume.html",

                error=(

                    "Unable to analyze the resume. "

                    f"Error: {error}"

                )

            )


        # -------------------------------------------------
        # Save skills
        # -------------------------------------------------

        session[
            "resume_skills"
        ] = result.get(
            "skills",
            []
        )


        # -------------------------------------------------
        # Save score
        # -------------------------------------------------

        session[
            "resume_score"
        ] = result.get(
            "score",
            0
        )


        # -------------------------------------------------
        # Save complete resume result
        # -------------------------------------------------

        session[
            "resume_result"
        ] = result


        # -------------------------------------------------
        # Show result
        # -------------------------------------------------

        return render_template(

            "resume_result.html",

            result=result

        )


    return render_template(
        "resume.html"
    )


# =========================================================
# CLEAR RESUME DATA
# =========================================================

@app.route("/clear-resume")
def clear_resume():

    session.pop(
        "resume_skills",
        None
    )


    session.pop(
        "resume_score",
        None
    )


    session.pop(
        "resume_result",
        None
    )


    return redirect(
        url_for("resume")
    )


# =========================================================
# ERROR HANDLER
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "index.html"
    ), 404


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )