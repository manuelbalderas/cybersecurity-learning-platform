from flask import Blueprint, render_template, abort, render_template

from app.models import Course

courses = Blueprint('courses', __name__)

@courses.route('/')
def index():
    return render_template('courses/index.html')

@courses.route('/<course_title>')
def get_courses(course_title):
    course = Course.query.filter_by(alias=course_title).first()
    if course is None:
        abort(404)
        # Remember to delete this line and create a 404 webpage, then use render_template to that
    
    return render_template('courses/course_detail.html', course=course)