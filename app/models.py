from app import db, login

from datetime import datetime, timedelta, date

from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow) 
    
    current_streak = db.Column(db.Integer, default=0)
    last_streak_date = db.Column(db.Date, default=None)
    longest_streak = db.Column(db.Integer, default=0)
    
    completed_challenges = db.relationship('UserChallenge', back_populates='user')
    
    def __repr__(self):
        return '<Username %r>' % self.username

    def update_streak(self):
        today = date.today()

        if self.has_done_streak_today:
           return
       
        elif self.last_streak_date == today - timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
            
        self.last_streak_date = today
        self.longest_streak = max(self.longest_streak, self.current_streak)
    
    def check_and_reset_streak(self):
        if not self.streak_is_broken:
            return
        
        self.current_streak = 0
        self.last_streak_date = None
        
    @property
    def streak_is_broken(self):
        return self.last_streak_date is not None and self.last_streak_date < date.today() - timedelta(days=1)
        
    @property
    def has_done_streak_today(self):
        return self.last_streak_date == date.today()

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))

    challenges = db.relationship('Challenge', back_populates='course')

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(25), nullable=False)
    category = db.Column(db.String(255), nullable=False) 
    description = db.Column(db.Text)
    files = db.Column(db.String(255))
    resources = db.Column(db.String(255))
    points = db.Column(db.Integer, default=0)
    flag = db.Column(db.String(30), nullable=False)

    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course = db.relationship('Course', back_populates='challenges')
    
    completions = db.relationship('UserChallenge', back_populates='challenge')

    
class UserChallenge(db.Model):
    __tablename__ = 'user_challenge'

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), primary_key=True)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='completed_challenges')
    challenge = db.relationship('Challenge', back_populates='completions')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    role = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)