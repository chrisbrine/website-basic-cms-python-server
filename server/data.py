from server import db
from server.models import AllowedEmail, Setting, User, BlogEnum, Blog, Resume, WorkExperience, Education, Skill
import binascii
import os
from datetime import datetime

def getPrimaryUser():
  return User.query.filter_by(id=1).first()

def login(user):
  token = binascii.hexlify(os.urandom(20)).decode()
  user.login_token = token
  db.session.commit()
  return token

def okToRegister(email):
  allowed_email = AllowedEmail.query.filter_by(email=email).first()
  if allowed_email:
    return True
  if (User.query.count() <= 0):
    return True
  return False

def okToLogin(email):
  if (User.query.count() <= 1):
    return True
  allowed_email = AllowedEmail.query.filter_by(email=email).first()
  if allowed_email:
    return True
  return False

def addAllowedEmail(email, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  allowed_email = AllowedEmail(email=email)
  db.session.add(allowed_email)
  db.session.commit()
  return {"success": True, "data": allowed_email.toObject()}  

def getAllowedEmails(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  allowed_emails = AllowedEmail.query.all()
  allowed_email_list = []
  if (allowed_emails):
    for allowed_email in allowed_emails:
      allowed_email_list.append(allowed_email.toObject())
  return {"success": True, "data": allowed_email_list}

def deleteAllowedEmail(emailId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not emailId:
    return {"success": False, "error": "Invalid email ID"}
  allowed_email = AllowedEmail.query.filter_by(id=emailId).first()
  if not allowed_email:
    return {"success": False, "error": "Invalid email"}
  db.session.delete(allowed_email)
  db.session.commit()
  return {"success": True}

def registerUser(userData):
  if not userData['email'] or not userData['password']:
    return {"success": False, "error": "Invalid user data"}
  existing_user = User.query.filter_by(email=userData['email']).first()
  if existing_user:
    return {"success": False, "error": "Email already exists"}
  if not okToRegister(userData['email']):
    return {"success": False, "error": "Not allowed to register"}
  user = User(
    email = userData['email'],
    password = userData['password']
  )
  if 'first_name' in userData:
    user.first_name = userData['first_name']
  if 'last_name' in userData:
    user.last_name = userData['last_name']
  if 'image_file' in userData:
    user.image_file = userData['image_file']
  db.session.add(user)
  db.session.commit()
  token = login(user)
  return {"success": True, "data": token}

def updateUser(userData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  user = User.query.filter_by(id=current_user.id).first()
  if 'first_name' in userData:
    user.first_name = userData['first_name']
  if 'last_name' in userData:
    user.last_name = userData['last_name']
  if 'image_file' in userData:
    user.image_file = userData['image_file']
  if 'phone_number' in userData:
    user.phone_number = userData['phone_number']
  if 'address' in userData:
    user.address = userData['address']
  if 'city' in userData:
    user.city = userData['city']
  if 'province' in userData:
    user.province = userData['province']
  if 'postalCode' in userData:
    user.postalCode = userData['postalCode']
  if 'linkedIn' in userData:
    user.linkedIn = userData['linkedIn']
  if 'github' in userData:
    user.github = userData['github']
  if 'website' in userData:
    user.website = userData['website']
  if 'facebook' in userData:
    user.facebook = userData['facebook']
  db.session.commit()
  return {"success": True, "data": user.toObject()}

def updateEmail(email, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  user = User.query.filter_by(id=current_user.id).first()
  user.email = email
  db.session.commit()
  return {"success": True}

def updatePassword(old_password, new_password, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  user = User.query.filter_by(id=current_user.id).first()
  if not user.check_password_correction(old_password):
    return {"success": False, "error": "Invalid password"}
  user.password = new_password
  db.session.commit()
  return {"success": True}

def loginUser(email_to_check, password_to_check):
  if not email_to_check or not password_to_check:
    return {"success": False, "error": "Invalid user data"}
  user = User.query.filter_by(email=email_to_check).first()
  if not user:
    return {"success": False, "error": "Invalid credentials"}
  if not okToLogin(email_to_check) and user.id != 1:
    return {"success": False, "error": "Not allowed to login"}
  if user and user.check_password_correction(password_to_check):
    token = login(user)
    return {"success": True, "data": token}
  return {"success": False, "error": "Invalid credentials"}

def tokenToUser(token):
  user = User.query.filter_by(login_token=token).first()
  if user:
    return user
  return False

def logoutUser(token):
  user = tokenToUser(token)
  if not user:
    return {"success": False, "error": "Invalid user"}
  user.login_token = None
  db.session.commit()
  return {"success": True}

def getUser(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  user = User.query.filter_by(id=current_user.id).first()
  if not user:
    return {"success": False, "error": "Invalid user"}
  return {"success": True, "data": user.toObject()}

def addResume(resumeData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}

  resume = Resume(
    user_id=current_user.id,
    title=resumeData['title'],
  )

  if 'description' in resumeData:
    resume.description = resumeData['description']
    
  db.session.add(resume)
  db.session.commit()
  return {"success": True, "data": resume.toObject()}

def updateResume(resumeId, resumeData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not resumeId:
    return {"success": False, "error": "Invalid resume ID"}
  resume = Resume.query.filter_by(id=resumeId).first()
  if resume.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  if 'title' in resumeData:
    resume.title = resumeData['title']
  if 'description' in resumeData:
    resume.description = resumeData['description']
  db.session.commit()
  return {"success": True, "data": resume.toObject()}

def deleteResume(resumeId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not resumeId:
    return {"success": False, "error": "Invalid resume ID"}
  resume = Resume.query.filter_by(id=resumeId).first()
  if resume.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  db.session.delete(resume)
  db.session.commit()
  return {"success": True}

def getResume(resumeId, current_user):
  if not resumeId:
    return {"success": False, "error": "Invalid resume ID"}
  resume = Resume.query.filter_by(id=resumeId).first()
  if resume.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  return {"success": True, "data": resume.toObject()}

def getTheResume(resumeId, current_user):
  resume = getResume(resumeId, current_user)
  if not resume["success"]:
    return False
  return resume["data"]

def getResumes(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  resumes = Resume.query.filter_by(user_id=current_user.id).all()
  resume_list = []
  if (resumes):
    for resume in resumes:
      resume_list.append(resume.toObject())
  return {"success": True, "data": resume_list}


def toDateTime(timestamp):
  return datetime.fromtimestamp(timestamp)

def strToDateTime(timestamp):
  return toDateTime(int(timestamp))

def addWorkExperience(resumeId, workExperienceData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  resume = getTheResume(resumeId, current_user)
  if not resume:
    return {"success": False, "error": "Invalid resume"}
  
  workExperience = WorkExperience(
    user_id=current_user.id,
    resume_id=resumeId,
  )
  
  if 'image_file' in workExperienceData:
    workExperience.image_file = workExperienceData['image_file']
  if 'company_name' in workExperienceData:
    workExperience.company_name = workExperienceData['company_name']
  if 'position' in workExperienceData:
    workExperience.position = workExperienceData['position']
  if 'start_date' in workExperienceData:
    if workExperienceData['start_date'] and workExperienceData['start_date'] > 0:
      workExperience.start_date = strToDateTime(workExperienceData['start_date'])
  if 'end_date' in workExperienceData:
    if workExperienceData['end_date'] and workExperienceData['end_date'] > 0:
      workExperience.end_date = strToDateTime(workExperienceData['end_date'])
  if 'description' in workExperienceData:
    workExperience.description = workExperienceData['description']
  
  db.session.add(workExperience)
  db.session.commit()
  return {"success": True, "data": workExperience.toObject()}

def updateWorkExperience(workExperienceId, workExperienceData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not workExperienceId:
    return {"success": False, "error": "Invalid work experience ID"}
  workExperience = WorkExperience.query.filter_by(id=workExperienceId).first()
  if workExperience.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  if 'image_file' in workExperienceData:
    workExperience.image_file = workExperienceData['image_file']
  if 'company_name' in workExperienceData:
    workExperience.company_name = workExperienceData['company_name']
  if 'position' in workExperienceData:
    workExperience.position = workExperienceData['position']
  if 'start_date' in workExperienceData:
    if workExperienceData['start_date'] and workExperienceData['start_date'] > 0:
      workExperience.start_date = strToDateTime(workExperienceData['start_date'])
    else:
      workExperience.start_date = None
  if 'end_date' in workExperienceData:
    if workExperienceData['end_date'] and workExperienceData['end_date'] > 0:
      workExperience.end_date = strToDateTime(workExperienceData['end_date'])
    else:
      workExperience.end_date = None
  if 'description' in workExperienceData:
    workExperience.description = workExperienceData['description']
  db.session.commit()
  return {"success": True, "data": workExperience.toObject()}

def deleteWorkExperience(workExperienceId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not workExperienceId:
    return {"success": False, "error": "Invalid work experience ID"}
  workExperience = WorkExperience.query.filter_by(id=workExperienceId).first()
  if workExperience.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  db.session.delete(workExperience)
  db.session.commit()
  return {"success": True}

def getWorkExperiences(resumeId, current_user):
  if not resumeId:
    return {"success": False, "error": "Invalid resume ID"}
  resume = getTheResume(resumeId, current_user)
  if not resume:
    return {"success": False, "error": "Invalid resume"}
  workExperiences = WorkExperience.query.filter_by(resume_id=resumeId).all()
  workExperience_list = []
  if (workExperiences):
    for workExperience in workExperiences:
      workExperience_list.append(workExperience.toObject())
  return {"success": True, "data": workExperience_list}

def getAllWorkExperiences(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  workExperiences = WorkExperience.query.filter_by(user_id=current_user.id).all()
  workExperience_list = []
  if (workExperiences):
    for workExperience in workExperiences:
      workExperience_list.append(workExperience.toObject())
  return {"success": True, "data": workExperience_list}

def addEducation(resumeId, educationData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  resume = getTheResume(resumeId, current_user)
  if not resume:
    return {"success": False, "error": "Invalid resume"}
  
  education = Education(
    user_id=current_user.id,
    resume_id=resumeId,
  )
  
  if 'image_file' in educationData:
    education.image_file = educationData['image_file']
  if 'school_name' in educationData:
    education.school_name = educationData['school_name']
  if 'degree' in educationData:
    education.degree = educationData['degree']
  if 'start_date' in educationData:
    if educationData['start_date'] and educationData['start_date'] > 0:
      education.start_date = strToDateTime(educationData['start_date'])
  if 'end_date' in educationData:
    if educationData['end_date'] and educationData['end_date'] > 0:
      education.end_date = strToDateTime(educationData['end_date'])
  if 'description' in educationData:
    education.description = educationData['description']
  
  db.session.add(education)
  db.session.commit()
  return {"success": True, "data": education.toObject()}

def updateEducation(educationId, educationData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not educationId:
    return {"success": False, "error": "Invalid education ID"}
  education = Education.query.filter_by(id=educationId).first()
  if education.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  if 'image_file' in educationData:
    education.image_file = educationData['image_file']
  if 'school_name' in educationData:
    education.school_name = educationData['school_name']
  if 'degree' in educationData:
    education.degree = educationData['degree']
  if 'start_date' in educationData:
    if educationData['start_date'] and educationData['start_date'] > 0:
      education.start_date = strToDateTime(educationData['start_date'])
    else:
      education.start_date = None
  if 'end_date' in educationData:
    if educationData['end_date'] and educationData['end_date'] > 0:
      education.end_date = strToDateTime(educationData['end_date'])
    else:
      education.end_date = None
  if 'description' in educationData:
    education.description = educationData['description']
  db.session.commit()
  return {"success": True, "data": education.toObject()}

def deleteEducation(educationId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not educationId:
    return {"success": False, "error": "Invalid education ID"}
  education = Education.query.filter_by(id=educationId).first()
  if education.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  db.session.delete(education)
  db.session.commit()
  return {"success": True}

def getEducations(resumeId, current_user):
  if not resumeId:
    return {"success": False, "error": "Invalid resume ID"}
  resume = getTheResume(resumeId, current_user)
  if not resume:
    return {"success": False, "error": "Invalid resume"}
  educations = Education.query.filter_by(resume_id=resumeId).all()
  education_list = []
  if (educations):
    for education in educations:
      education_list.append(education.toObject())
  return {"success": True, "data": education_list}

def getAllEducations(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  educations = Education.query.filter_by(user_id=current_user.id).all()
  education_list = []
  if (educations):
    for education in educations:
      education_list.append(education.toObject())
  return {"success": True, "data": education_list}

def addSkill(resumeId, skillData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  resume = getTheResume(resumeId, current_user)
  if not resume:
    return {"success": False, "error": "Invalid resume"}
  
  skill = Skill(
    user_id=current_user.id,
    resume_id=resumeId,
  )
  
  if 'skill_name' in skillData:
    skill.skill_name = skillData['skill_name']
  if 'category' in skillData:
    skill.category = skillData['category']
  if 'image_file' in skillData:
    skill.image_file = skillData['image_file']
  
  db.session.add(skill)
  db.session.commit()
  return {"success": True, "data": skill.toObject()}

def updateSkill(skillId, skillData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not skillId:
    return {"success": False, "error": "Invalid skill ID"}
  skill = Skill.query.filter_by(id=skillId).first()
  if skill.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  if 'skill_name' in skillData:
    skill.skill_name = skillData['skill_name']
  if 'category' in skillData:
    skill.category = skillData['category']
  if 'image_file' in skillData:
    skill.image_file = skillData['image_file']
  db.session.commit()
  return {"success": True, "data": skill.toObject()}

def deleteSkill(skillId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not skillId:
    return {"success": False, "error": "Invalid skill ID"}
  skill = Skill.query.filter_by(id=skillId).first()
  if skill.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  db.session.delete(skill)
  db.session.commit()
  return {"success": True}

def getSkills(resumeId, current_user):
  if not resumeId:
    return {"success": False, "error": "Invalid resume ID"}
  resume = getTheResume(resumeId, current_user)
  if not resume:
    return {"success": False, "error": "Invalid resume"}
  skills = Skill.query.filter_by(resume_id=resumeId).all()
  skill_list = []
  if (skills):
    for skill in skills:
      skill_list.append(skill.toObject())
  return {"success": True, "data": skill_list}

def getAllSkills(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  skills = Skill.query.filter_by(user_id=current_user.id).all()
  skill_list = []
  if (skills):
    for skill in skills:
      skill_list.append(skill.toObject())
  return {"success": True, "data": skill_list}

def getAll(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  user = getUser(current_user)
  resumes = getResumes(current_user)
  workExperiences = getAllWorkExperiences(current_user)
  educations = getAllEducations(current_user)
  skills = getAllSkills(current_user)
  settings = getSettings()
  blog_posts = getAllPublishedBlogPosts()
  if user["success"]:
    user = user["data"]
  else:
    user = {}
  if settings["success"]:
    settings = settings["data"]
  else:
    settings = {}
  if blog_posts["success"]:
    blog_posts = blog_posts["data"]
  else:
    blog_posts = {}
  if resumes["success"]:
    resumes = resumes["data"]
  else:
    resumes = {}
  if workExperiences["success"]:
    workExperiences = workExperiences["data"]
  else:
    workExperiences = {}
  if educations["success"]:
    educations = educations["data"]
  else:
    educations = {}
  if skills["success"]:
    skills = skills["data"]
  else:
    skills = {}
  return {
    "success": True,
    "data": {
      'user': user,
      'resumes': resumes,
      'workExperiences': workExperiences,
      'educations': educations,
      'skills': skills,
      'settings': settings,
      'blog_posts': blog_posts,
    }
  }

def createBlogPost(blogPostData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  blogPost = Blog(
    user_id=current_user.id,
    slug=blogPostData['slug'],
    title=blogPostData['title'],
    body=blogPostData['body'],
  )
  if 'category' in blogPostData:
    blogPost.category = blogPostData['category']
  if 'tags' in blogPostData:
    blogPost.tags = blogPostData['tags']
  if 'status' in blogPostData:
    blogPost.status = blogPostData['status']
  if 'edit_history' in blogPostData:
    blogPost.edit_history = blogPostData['edit_history']
  if 'image_file' in blogPostData:
    blogPost.image_file = blogPostData['image_file']
  db.session.add(blogPost)
  db.session.commit()
  return {"success": True, "data": blogPost.toObject()}

def updateBlogPost(blogPostId, blogPostData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not blogPostId:
    return {"success": False, "error": "Invalid blog post ID"}
  blogPost = Blog.query.filter_by(id=blogPostId).first()
  if blogPost.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  if 'title' in blogPostData:
    blogPost.title = blogPostData['title']
  if 'slug' in blogPostData:
    blogPost.slug = blogPostData['slug']
  if 'body' in blogPostData:
    blogPost.body = blogPostData['body']
  if 'category' in blogPostData:
    blogPost.category = blogPostData['category']
  if 'tags' in blogPostData:
    blogPost.tags = blogPostData['tags']
  if 'status' in blogPostData:
    blogPost.status = blogPostData['status']
  if 'edit_history' in blogPostData:
    blogPost.edit_history = blogPostData['edit_history']
  if 'image_file' in blogPostData:
    blogPost.image_file = blogPostData['image_file']
  db.session.commit()
  return {"success": True, "data": blogPost.toObject()}

def deleteBlogPost(blogPostId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if not blogPostId:
    return {"success": False, "error": "Invalid blog post ID"}
  blogPost = Blog.query.filter_by(id=blogPostId).first()
  if blogPost.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  db.session.delete(blogPost)
  db.session.commit()
  return {"success": True}

def getBlogPost(blogPostId, current_user):
  if not blogPostId:
    return {"success": False, "error": "Invalid blog post ID"}
  blogPost = Blog.query.filter_by(id=blogPostId).first()
  if blogPost.user_id != current_user.id:
    return {"success": False, "error": "Permission denied"}
  return {"success": True, "data": blogPost.toObject()}

def getBlogPosts(current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  blogPosts = Blog.query.filter_by(user_id=current_user.id).all()
  blogPost_list = []
  if (blogPosts):
    for blogPost in blogPosts:
      blogPost_list.append(blogPost.toObject())
  return {"success": True, "data": blogPost_list}

def getAllPublishedBlogPosts():
  blogPosts = Blog.query.filter_by(status=BlogEnum.PUBLISHED).all()
  blogPost_list = []
  if (blogPosts):
    for blogPost in blogPosts:
      blogPost_list.append(blogPost.toObject())
  return {"success": True, "data": blogPost_list}

def createSetting(settingData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if current_user.id != 1:
    return {"success": False, "error": "Permission denied"}
  if 'name' not in settingData or 'value' not in settingData:
    return {"success": False, "error": "Invalid setting data"}
  checkSetting = Setting.query.filter_by(name=settingData['name']).first()
  if checkSetting:
    return {"success": False, "error": "Setting already exists"}
  setting = Setting(
    name=settingData['name'],
    value=settingData['value'],
  )
  db.session.add(setting)
  db.session.commit()
  return {"success": True, "data": setting.toObject()}

def updateSetting(settingId, settingData, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if current_user.id != 1:
    return {"success": False, "error": "Permission denied"}
  if not settingId:
    return {"success": False, "error": "Invalid setting ID"}
  setting = Setting.query.filter_by(id=settingId).first()
  if not setting:
    return {"success": False, "error": "Invalid setting"}
  if 'name' in settingData:
    setting.name = settingData['name']
  if 'value' in settingData:
    setting.value = settingData['value']
  db.session.commit()
  return {"success": True, "data": setting.toObject()}

def deleteSetting(settingId, current_user):
  if not current_user or not current_user.id:
    return {"success": False, "error": "Invalid user"}
  if current_user.id != 1:
    return {"success": False, "error": "Permission denied"}
  if not settingId:
    return {"success": False, "error": "Invalid setting ID"}
  setting = Setting.query.filter_by(id=settingId).first()
  if not setting:
    return {"success": False, "error": "Invalid setting"}
  db.session.delete(setting)
  db.session.commit()
  return {"success": True}

def getSetting(settingId):
  if not settingId:
    return {"success": False, "error": "Invalid setting ID"}
  setting = Setting.query.filter_by(id=settingId).first()
  if not setting:
    return {"success": False, "error": "Invalid setting"}
  return {"success": True, "data": setting.toObject()}

def getSettings():
  settings = Setting.query.all()
  setting_list = []
  if (settings):
    for setting in settings:
      setting_list.append(setting.toObject())
  return {"success": True, "data": setting_list}

def getSettingByKey(settingKey):
  if not settingKey:
    return {"success": False, "error": "Invalid setting key"}
  setting = Setting.query.filter_by(name=settingKey).first()
  if not setting:
    return {"success": False, "error": "Invalid setting"}
  return {"success": True, "data": setting.toObject()}
