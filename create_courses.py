from app import db, create_app
from app.models import Course, Challenge
from sqlalchemy import or_, func

import yaml
from pathlib import Path

import create_db

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
    courses = [course for course in courses_path.iterdir() if course.is_dir()]
    
    for i, course_path in enumerate(courses):
        if check_course_structure(course_path):
            description_file = course_path / 'description.yml'
            with open(description_file, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                
                alias = course_path.stem.replace(' ', '-').lower()
                course = Course.query.filter_by(alias=alias).first()
                
                if course:
                    course.title = data['title']
                    course.description = data['description']
                    course.image_url = data.get('image_url', 'default_image.png')
                    print(f"Updating course: {course.title}")
                else:
                    course = Course(
                        title=data['title'],
                        id=data.get('id', i),
                        alias=alias,
                        description=data['description'],
                        image_url=data.get('image_url', 'default_image.png')
                    )
                    db.session.add(course)
                    print(f"Adding new course: {course.title}")
                
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error saving course {course.title}: {e}")

            challenges_path = course_path / 'challenges'
            for challenge_file in challenges_path.rglob('*.yml'):
                with open(challenge_file, 'r', encoding='utf-8') as file:
                    data = yaml.safe_load(file)
                    resources = data.get('resources', [])
                    resources_str = ', '.join(resources) if resources else ''
                    alias = challenge_file.stem.replace(' ', '-').lower()
                    
                    challenge = Challenge.query.filter_by(alias=alias, course_id=course.id).first()
                    
                    if challenge:
                        challenge.title = data['title']
                        challenge.description = data['description']
                        challenge.category = data['category']
                        challenge.files = data.get('files', '')
                        challenge.resources = resources_str
                        challenge.format = f'dpwn{{{data.get("format", "respuesta")}}}'
                        challenge.flag = f'dpwn{{{data["flag"]}}}'
                        challenge.points = data['points']
                        print(f"Updating challenge: {challenge.title}")
                    else:
                        challenge = Challenge(
                            title=data['title'],
                            alias=alias,
                            description=data['description'],
                            category=data['category'],
                            files=data.get('files', ''),
                            resources=resources_str,
                            flag=data['flag'],
                            points=data['points'],
                            course_id=course.id,
                        )
                        db.session.add(challenge)
                        print(f"Adding new challenge: {challenge.title}")

                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error saving challenge {data['title']}: {e}")
