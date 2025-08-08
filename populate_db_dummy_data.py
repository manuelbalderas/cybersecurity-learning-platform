from app import db, create_app
from app.models import Course, Challenge

app = create_app()

with app.app_context():

    course_title = 'Reconocimiento'
    course_alias = 'reconnainsance'
    course_description = '''

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam magna dui, rhoncus at finibus ultrices, tristique eget metus. Pellentesque consectetur libero sed dolor vehicula, eu mollis nulla blandit. Donec aliquam risus vitae arcu vulputate vulputate. Integer bibendum id ligula nec lacinia. Pellentesque egestas turpis nec tincidunt volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus iaculis finibus tortor, eget varius neque semper sit amet. In volutpat ex sed felis pharetra, vitae luctus ante lacinia. In sit amet nunc eu libero pulvinar viverra eu eu odio. Mauris lobortis ullamcorper scelerisque.

    Quisque posuere condimentum massa sed interdum. Aliquam erat metus, vestibulum vitae tellus eu, scelerisque vehicula nisi. Mauris placerat non risus ac elementum. Maecenas imperdiet erat eget est commodo blandit. Nunc ut elit sit amet ex fringilla pretium. Vivamus porttitor diam quis eros interdum, et eleifend leo tincidunt. Proin auctor finibus mi, sit amet ultrices nisi. Duis pretium, est quis vestibulum vulputate, neque nibh laoreet ipsum, sed mollis enim est eget sapien. Suspendisse fringilla feugiat tempus. Nullam quam dui, mollis id mauris non, finibus gravida felis. Proin ut massa elit. Quisque vel nisi ornare, laoreet ipsum sit amet, efficitur arcu. In eget volutpat diam.

    Vestibulum tincidunt augue eu lorem porttitor lobortis. Vestibulum aliquet porta leo nec eleifend. Donec dapibus pellentesque dui, non luctus diam cursus molestie. Aliquam interdum nunc neque, id lobortis ipsum accumsan non. Phasellus in lorem egestas, imperdiet massa vitae, viverra nulla. Integer malesuada elit non feugiat ultricies. Sed rutrum turpis sed sodales maximus. Etiam volutpat, nisl et dictum varius, sapien orci finibus tellus, vel congue tellus tortor vel augue. Fusce nisi justo, vehicula et quam ac, condimentum porttitor eros. In eleifend, massa vel efficitur vulputate, tellus dui cursus est, sit amet fermentum dui tellus nec nibh. Sed lacinia ligula in justo vehicula, vel mattis turpis sodales. Sed tempus mauris eu neque consequat varius. Pellentesque tincidunt, odio eget iaculis bibendum, nibh augue gravida sapien, eget rutrum orci magna at nisi. Nulla ac elit rhoncus, dapibus nisl ut, cursus dolor. Morbi non turpis quis dui condimentum viverra. Phasellus ipsum lorem, bibendum a enim et, cursus aliquet neque. 
    '''
    image_url = 'Error3.png'

    course = Course(title=course_title, alias=course_alias, description=course_description, image_url=image_url)

    category_name = 'Buscando puertos abiertos con Nmap'

    image_url = 'Hack.png'

    challenge_title = 'Escanear aca chido mamalon'
    challenge_alias = 'scanning'
    challenge_description = '''

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam magna dui, rhoncus at finibus ultrices, tristique eget metus. Pellentesque consectetur libero sed dolor vehicula, eu mollis nulla blandit. Donec aliquam risus vitae arcu vulputate vulputate. Integer bibendum id ligula nec lacinia. Pellentesque egestas turpis nec tincidunt volutpat. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus iaculis finibus tortor, eget varius neque semper sit amet. In volutpat ex sed felis pharetra, vitae luctus ante lacinia. In sit amet nunc eu libero pulvinar viverra eu eu odio. Mauris lobortis ullamcorper scelerisque.

    Quisque posuere condimentum massa sed interdum. Aliquam erat metus, vestibulum vitae tellus eu, scelerisque vehicula nisi. Mauris placerat non risus ac elementum. Maecenas imperdiet erat eget est commodo blandit. Nunc ut elit sit amet ex fringilla pretium. Vivamus porttitor diam quis eros interdum, et eleifend leo tincidunt. Proin auctor finibus mi, sit amet ultrices nisi. Duis pretium, est quis vestibulum vulputate, neque nibh laoreet ipsum, sed mollis enim est eget sapien. Suspendisse fringilla feugiat tempus. Nullam quam dui, mollis id mauris non, finibus gravida felis. Proin ut massa elit. Quisque vel nisi ornare, laoreet ipsum sit amet, efficitur arcu. In eget volutpat diam.

    Vestibulum tincidunt augue eu lorem porttitor lobortis. Vestibulum aliquet porta leo nec eleifend. Donec dapibus pellentesque dui, non luctus diam cursus molestie. Aliquam interdum nunc neque, id lobortis ipsum accumsan non. Phasellus in lorem egestas, imperdiet massa vitae, viverra nulla. Integer malesuada elit non feugiat ultricies. Sed rutrum turpis sed sodales maximus. Etiam volutpat, nisl et dictum varius, sapien orci finibus tellus, vel congue tellus tortor vel augue. Fusce nisi justo, vehicula et quam ac, condimentum porttitor eros. In eleifend, massa vel efficitur vulputate, tellus dui cursus est, sit amet fermentum dui tellus nec nibh. Sed lacinia ligula in justo vehicula, vel mattis turpis sodales. Sed tempus mauris eu neque consequat varius. Pellentesque tincidunt, odio eget iaculis bibendum, nibh augue gravida sapien, eget rutrum orci magna at nisi. Nulla ac elit rhoncus, dapibus nisl ut, cursus dolor. Morbi non turpis quis dui condimentum viverra. Phasellus ipsum lorem, bibendum a enim et, cursus aliquet neque.
    '''
    challenge_files = 'community.svg'
    challenge_resources = 'https://google.com'
    challenge_flag = 'nca{{h4ck3d}}'

    challenge = Challenge(
        title=challenge_title,
        alias=challenge_alias,
        description=challenge_description,
        category=category_name,
        files=challenge_files,
        resources=challenge_resources,
        flag=challenge_flag,
        course_id=1,
    )

    db.session.add(course)
    db.session.add(challenge)
    db.session.commit()
    
    # courses = Course.query.all()
    # for course in courses:
    #     print(course.alias)
