from app import db, create_app
from app.models import Course, Challenge
from sqlalchemy import or_, func

import yaml
from pathlib import Path

app = create_app()

base_path = Path(__file__).parent
courses_path = base_path / 'courses'

def check_course_structure(course_path):
    description_file = course_path / 'description.yml'
    challenges_path = course_path / 'challenges'
    
    if not description_file.is_file():
        print(f"Description file not found in {course_path}")
        return False
    
    if not challenges_path.is_dir():
        print(f"Challenges directory not found in {course_path}")
        return False
    
    for challenge in challenges_path.glob('*.yml'):
        if not challenge.is_file():
            print(f"Challenge file {challenge} is not a valid file.")
            return False

    print(f"Course structure is valid for {course_path}")
    return True

with app.app_context():
    try:
        db.session.query(Course).delete()  # Deletes all entries in the Course table
        db.session.query(Challenge).delete()  # Deletes all entries in the Challenge table
        db.session.commit()
        print("Deleted all courses and challenges from the database.")
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting existing records: {e}")
    courses = [course for course in courses_path.iterdir() if course.is_dir()]
    for course_path in courses:
        if check_course_structure(course_path):
            description_file = course_path / 'description.yml'
            with open(description_file, 'r') as file:
                data = yaml.safe_load(file)
                course = Course(
                    title=data['course_title'],
                    alias=data['course_alias'],
                    description=data['course_description'],
                    image_url=data.get('image_url', 'default_image.png')  # Default image if not provided
                )
                print(f"Adding course: {course.title}")
                try:
                    db.session.add(course)
                    db.session.commit()
                    print(f"Added course: {course.title}")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error adding course {course.title}: {e}")

            challenges_path = course_path / 'challenges'
            for challenge_file in challenges_path.rglob('*.yml'):
                with open(challenge_file, 'r') as file:
                    data = yaml.safe_load(file)
                    resources = data.get('challenge_resources', [])
                    resources_str = ', '.join(resources) if resources else ''
                    challenge = Challenge(
                        title=data['challenge_title'],
                        alias=data['challenge_alias'],
                        description=data['challenge_description'],
                        category=data['challenge_category'],
                        files=data.get('challenge_files', ''),
                        resources=resources_str,
                        flag=data['challenge_flag'],
                        points=data['challenge_points'],
                        course_id=course.id,
                    )
                    print(f"Adding challenge: {challenge.title}")
                    try:
                        db.session.add(challenge)
                        db.session.commit()
                        print(f"Added challenge: {challenge.title}")
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error adding challenge {challenge.title}: {e}")