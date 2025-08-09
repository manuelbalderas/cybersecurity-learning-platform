from app.models import Course

def get_all_courses():
    return Course.query.all()

def get_course_by_alias(alias):
    return Course.query.filter_by(alias=alias).first()