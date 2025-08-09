from flask import Blueprint, render_template, abort
from app.services.courses_service import get_all_courses, get_course_by_alias

courses_frontend_bp = Blueprint('courses_frontend', __name__)

@courses_frontend_bp.route('/')
def index():
    courses = get_all_courses()
    return render_template('courses/index.html', courses=courses, page_title="Cursos")

@courses_frontend_bp.route('/<course_title>')
def get_courses(course_title):
    course = get_course_by_alias(course_title)
    if course is None:
        abort(404)
    
    return render_template('courses/course_detail.html', course=course, page_title=f"{course.title}")