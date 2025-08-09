from flask import Blueprint 
from app.services.courses_service import get_all_courses, get_course_by_alias

courses_api_bp = Blueprint('courses_api', __name__)

@courses_api_bp.route('/')
def index():
    courses = get_all_courses()
    return render_template('courses/index.html', courses=courses, page_title="Cursos")

@courses_api_bp.route('/<course_title>')
def get_courses(course_title):
    print('XD')
    course = Course.query.filter_by(alias=course_title).first()
    courses = Course.query.all()
    if course is None:
        abort(404)
        # Remember to delete this line and create a 404 webpage, then use render_template to that
    
    return render_template('courses/course_detail.html', course=course, page_title=f"{course.title}")