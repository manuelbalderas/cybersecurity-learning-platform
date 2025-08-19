from app.models import Course
from flask_login import current_user

def get_all_courses():
    return Course.query.all()

def get_course_by_alias(alias):
    return Course.query.filter_by(alias=alias).first()

def get_challenges_by_course(course):
    return Course.query.get(course.id).challenges if course else []

def get_started_courses():
    return {course: current_user.has_started_course(course) for course in get_all_courses()}

def get_finished_courses():
    total_courses = get_all_courses()
    total_finished_courses = {}
    for course in total_courses:
        total_challenges = len(get_challenges_by_course(course))
        completed_challenges = len(current_user.get_completed_challenges_by_course(course))
        total_finished_courses[course] = total_challenges == completed_challenges and total_challenges != 0
    return total_finished_courses

def get_calculate_percentage(course):
    total_challenges = len(get_challenges_by_course(course))
    completed_challenges = len(current_user.get_completed_challenges_by_course(course))
    return (completed_challenges / total_challenges) * 100 if completed_challenges else 0