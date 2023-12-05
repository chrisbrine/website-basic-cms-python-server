from server import app
from server import db
from server import bcrypt
from datetime import datetime
import enum

class Setting(db.Model):
  __tablename__ = 'setting'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False, unique=True)
  value = db.Column(db.JSON)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'Setting({self.name}, {self.value})'
  def toObject(self):
    return {
      'id': self.id,
      'name': self.name,
      'value': self.value,
    }

class AllowedEmail(db.Model):
  __tablename__ = 'allowed_email'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'AllowedEmail({self.email})'
  def toObject(self):
    return {
      'id': self.id,
      'email': self.email,
    }

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password_hash = db.Column(db.String(100), nullable=False)
  image_file = db.Column(db.JSON)
  login_token = db.Column(db.String(100))
  first_name = db.Column(db.String(100))
  last_name = db.Column(db.String(100))
  phone_number = db.Column(db.String(20))
  address = db.Column(db.String(200))
  city = db.Column(db.String(100))
  province = db.Column(db.String(100))
  postalCode = db.Column(db.String(10))
  linkedIn = db.Column(db.String(100))
  github = db.Column(db.String(100))
  website = db.Column(db.String(100))
  facebook = db.Column(db.String(100))
  settings = db.Column(db.JSON)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

  def __repr__(self):
    return f'User({self.email}, {self.first_name} {self.last_name})'

  @property
  def password(self):
    return self.password

  @password.setter
  def password(self, plain_text_password):
    self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password_hash, attempted_password)

  def toObject(self):
    return {
      'id': self.id,
      'email': self.email,
      'image_file': self.image_file,
      'login_token': self.login_token,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'phone_number': self.phone_number,
      'address': self.address,
      'city': self.city,
      'province': self.province,
      'postalCode': self.postalCode,
      'linkedIn': self.linkedIn,
      'github': self.github,
      'website': self.website,
      'facebook': self.facebook,
      'settings': self.settings,
    }

class Resume(db.Model):
  __tablename__ = 'resume'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  # education = db.relationship('Education', backref='resume', lazy=True)
  # work_experience = db.relationship('WorkExperience', backref='resume', lazy=True)
  # skills = db.relationship('Skill', backref='resume', lazy=True)
  title = db.Column(db.String(100), nullable=False, unique=True)
  description = db.Column(db.Text)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'Resume({self.user_id}, {self.title})'
  def toObject(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'title': self.title,
      'description': self.description,
    }

class Education(db.Model):
  __tablename__ = 'education'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
  image_file = db.Column(db.JSON)
  school_name = db.Column(db.String(100), nullable=False)
  degree = db.Column(db.String(100))
  start_date = db.Column(db.Date)
  end_date = db.Column(db.Date)
  description = db.Column(db.Text)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'Education({self.user_id}, {self.school_name})'
  def toObject(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'resume_id': self.resume_id,
      'image_file': self.image_file,
      'school_name': self.school_name,
      'degree': self.degree,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'description': self.description,
    }

class WorkExperience(db.Model):
  __tablename__ = 'work_experience'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
  image_file = db.Column(db.JSON)
  company_name = db.Column(db.String(100), nullable=False)
  position = db.Column(db.String(100))
  start_date = db.Column(db.Date)
  end_date = db.Column(db.Date)
  description = db.Column(db.Text)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'WorkExperience({self.user_id}, {self.company_name})'
  def toObject(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'resume_id': self.resume_id,
      'image_file': self.image_file,
      'company_name': self.company_name,
      'position': self.position,
      'start_date': self.start_date,
      'end_date': self.end_date,
      'description': self.description,
    }

class Skill(db.Model):
  __tablename__ = 'skill'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
  skill_name = db.Column(db.String(100), nullable=False, unique=True)
  image_file = db.Column(db.JSON)
  category = db.Column(db.String(100))
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'Skill({self.user_id}, {self.skill_name})'
  def toObject(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'resume_id': self.resume_id,
      'skill_name': self.skill_name,
      'image_file': self.image_file,
      'category': self.category,
    }

class BlogEnum(enum.Enum):
  DRAFT = 'DRAFT'
  PUBLISHED = 'PUBLISHED'
  DELETED = 'DELETED'
  PENDING = 'PENDING'
  FUTURE = 'FUTURE'
  PRIVATE = 'PRIVATE'

def getBlogStatus(status):
  if status == BlogEnum.DRAFT:
    return 'DRAFT'
  elif status == BlogEnum.PUBLISHED:
    return 'PUBLISHED'
  elif status == BlogEnum.DELETED:
    return 'DELETED'
  elif status == BlogEnum.PENDING:
    return 'PENDING'
  elif status == BlogEnum.FUTURE:
    return 'FUTURE'
  elif status == BlogEnum.PRIVATE:
    return 'PRIVATE'

class Blog(db.Model):
  __tablename__ = 'blog'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  image_file = db.Column(db.JSON)
  title = db.Column(db.String(100), nullable=False)
  slug = db.Column(db.String(100), nullable=False, unique=True)
  category = db.Column(db.String(100))
  tags = db.Column(db.String(200))
  status = db.Column(db.Enum(BlogEnum), default=BlogEnum.DRAFT, nullable=False)
  body = db.Column(db.Text, nullable=False)
  edit_history = db.Column(db.JSON)
  created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __repr__(self):
    return f'Blog({self.user_id}, {self.title})'
  def toObject(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'image_file': self.image_file,
      'title': self.title,
      'slug': self.slug,
      'category': self.category,
      'tags': self.tags,
      'status': getBlogStatus(self.status),
      'body': self.body,
      'edit_history': self.edit_history,
      'created_at': self.created_at,
      'updated_at': self.updated_at,
    }

with app.app_context():
  # db.drop_all()
  db.create_all()
