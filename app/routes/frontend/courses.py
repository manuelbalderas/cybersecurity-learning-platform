from flask import Blueprint, render_template, abort
from flask_login import current_user
from app.services.courses_service import get_all_courses, get_course_by_alias, get_started_courses, get_finished_courses, get_calculate_percentage

courses_frontend_bp = Blueprint('courses_frontend', __name__)

@courses_frontend_bp.route('/')
def index():
    courses = get_all_courses()
    if current_user.is_authenticated:
        started_courses = get_started_courses()
        finished_courses = get_finished_courses()
        total_percentage = {course: get_calculate_percentage(course) for course in courses}
        print(finished_courses)
        return render_template(
            'courses/index.html',
            courses=courses, 
            started_courses=started_courses,
            finished_courses=finished_courses,
            total_percentage=total_percentage,
            page_title="Cursos"
        )
    return render_template('courses/index.html', courses=courses, page_title="Cursos")

@courses_frontend_bp.route('/<course_title>')
def get_courses(course_title):
    course = get_course_by_alias(course_title)
    if course is None:
        abort(404)
    
    return render_template('courses/course_detail.html', course=course, page_title=f"{course.title}")