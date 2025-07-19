from app import db, create_app
from app.models import Course, Category, Challenge
from sqlalchemy import or_, func

import yaml
from pathlib import Path

app = create_app()

base_path = Path(__file__).parent
categories_path = base_path / 'categories'
courses_path = base_path / 'courses'

def find_category(category, return_id=False, case_sensitive=True):
    if case_sensitive:
        filter_condition = or_(
            func.lower(Category.name) == func.lower(category),
            func.lower(Category.alias) == func.lower(category)
        ) 
    else:
        filter_condition = or_(
            Category.name == category,
            Category.alias == category
        )
    
    category = db.session.query(Category).filter(filter_condition).first()
    
    if return_id:
        return category.id if category else None
    else:
        return category is not None 


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

        with open(challenge, 'r') as file:
            data = yaml.safe_load(file)

        if not find_category(data['challenge_category']):
            print(f"Category {data['challenge_category']} does not exist for challenge {data['challenge_title']}.")
            return False
    
    print(f"Course structure is valid for {course_path}")
    return True

with app.app_context():
    for category_file in categories_path.rglob('*.yml'):
        with open(category_file, 'r') as file:
            data = yaml.safe_load(file)
            category = Category(
                name=data['category_name'],
                alias=data['category_alias'],
                description=data['category_description'],
                image_url=data.get('category_image_url', 'default_image.png')  # Default image if not provided
            )
            print(f"Adding category: {category.name}")
            try:
                db.session.add(category)
                db.session.commit()
                print(f"Added category: {category.name}")
            except Exception as e:
                db.session.rollback()
                print(f"Error adding category {category.name}: {e}")

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
                    image_url=data.get('course_image_url', 'default_image.png')  # Default image if not provided
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
                        files=data.get('challenge_files', ''),
                        resources=resources_str,
                        flag=data['challenge_flag'],
                        course_id=course.id,
                        category_id=find_category(data['challenge_category'], return_id=True)
                    )
                    print(f"Adding challenge: {challenge.title}")
                    try:
                        db.session.add(challenge)
                        db.session.commit()
                        print(f"Added challenge: {challenge.title}")
                    except Exception as e:
                        db.session.rollback()
                        print(f"Error adding challenge {challenge.title}: {e}")