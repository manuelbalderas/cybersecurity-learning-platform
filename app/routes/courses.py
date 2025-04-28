from flask import Blueprint, render_template, abort

from app.models import Course

courses = Blueprint('courses', __name__)

@courses.route('/')
def index():
    courses = Course.query.all()
    return render_template('courses/index.html', courses=courses, page_title="Cursos")

@courses.route('/<course_title>')
def get_courses(course_title):
    course = Course.query.filter_by(alias=course_title).first()
    courses = Course.query.all()
    for c in courses:
        print(c)
        for challenge in c.challenges:
            print(challenge.category.name)
    if course is None:
        abort(404)
        # Remember to delete this line and create a 404 webpage, then use render_template to that
    
    return render_template('courses/course_detail.html', course=course, page_title=f"{course.title}")