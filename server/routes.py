from flask import render_template, request
from server import app
from server.models import User, Resume, WorkExperience, Education, Skill
from server.data import getPrimaryUser, registerUser, tokenToUser, logoutUser, updateUser, updateEmail, updatePassword, loginUser, getUser, getResumes, getResume, addResume, updateResume, deleteResume, addEducation, updateEducation, deleteEducation, getEducations, getAllEducations, addWorkExperience, updateWorkExperience, deleteWorkExperience, getWorkExperiences, getAllWorkExperiences, addSkill, updateSkill, deleteSkill, getSkills, getAllSkills, getAll, createBlogPost, updateBlogPost, deleteBlogPost, getBlogPost, getBlogPosts, getAllPublishedBlogPosts, createSetting, updateSetting, deleteSetting, getSetting, getSettings, getSettingByKey, getAllowedEmails, deleteAllowedEmail, addAllowedEmail

def getToken():
  if 'x-access-token' in request.headers:
    return request.headers['x-access-token']
  return False

def isLoggedIn(token):
  if token:
    return tokenToUser(token)
  return False

def getJsonRequest():
  return request.get_json()

@app.route('/data/registerUser', methods=['POST'])
def user_register():
  return registerUser(getJsonRequest())

@app.route('/data/updateUser', methods=['POST'])
def user_update():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateUser(getJsonRequest(), user)

@app.route('/data/allowedEmails', methods=['GET'])
def allowed_emails():
  user = isLoggedIn(getToken())
  return getAllowedEmails(user)

@app.route('/data/allowedEmails/<email>', methods=['DELETE'])
def allowed_email_delete(email):
  user = isLoggedIn(getToken())
  return deleteAllowedEmail(email, user)

@app.route('/data/allowedEmails/<email>', methods=['POST'])
def allowed_email_add(email):
  user = isLoggedIn(getToken())
  return addAllowedEmail(email, user)

# @app.route('/data/updateEmail/<email>', methods=['POST'])
# def user_email_update(email):
#   user = isLoggedIn(getToken())
#   if not user:
#     return {"success": False, "message": "No token provided"}
#   return updateEmail(email, user)

@app.route('/data/updatePassword', methods=['POST'])
def user_password_update():
  user = isLoggedIn(getToken())
  details = getJsonRequest()
  if not user:
    return {"success": False, "message": "No token provided"}
  return updatePassword(details['old_password'], details['new_password'], user)

@app.route('/data/loginUser', methods=['POST'])
def user_login():
  userData = getJsonRequest()
  return loginUser(userData['email'], userData['password'])

@app.route('/data/logoutUser', methods=['GET'])
def user_logout():
  token = getToken()
  if not token:
    return {"success": False, "message": "No token provided"}
  return logoutUser(token)

@app.route('/data/user', methods=['GET'])
def user_data():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getUser(user)

@app.route('/data/resume', methods=['GET'])
def resumes_get():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getResumes(user)

@app.route('/data/resume/<int:id>', methods=['GET'])
def resume_get(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getResume(id, user)

@app.route('/data/resume', methods=['POST'])
def resume_add():
  user = isLoggedIn(getToken())
  resume = getJsonRequest()
  if not user:
    return {"success": False, "message": "No token provided"}
  return addResume(resume, user)

@app.route('/data/resume/<int:id>', methods=['POST'])
def resume_update(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateResume(id, getJsonRequest(), user)

@app.route('/data/resume/<int:id>', methods=['DELETE'])
def resume_delete(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return deleteResume(id, user)

@app.route('/data/educationAdd/<int:id>', methods=['POST'])
def education_add(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return addEducation(id, getJsonRequest(), user)

@app.route('/data/education/<int:id>', methods=['POST'])
def education_update(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateEducation(id, getJsonRequest(), user)

@app.route('/data/education/<int:id>', methods=['DELETE'])
def education_delete(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return deleteEducation(id, user)

@app.route('/data/education/<int:id>', methods=['GET'])
def education_get(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getEducations(id, user)

@app.route('/data/education', methods=['GET'])
def education_get_all():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getAllEducations(user)

@app.route('/data/workExperienceAdd/<int:id>', methods=['POST'])
def workExperience_add(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return addWorkExperience(id, getJsonRequest(), user)

@app.route('/data/workExperience/<int:id>', methods=['POST'])
def workExperience_update(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateWorkExperience(id, getJsonRequest(), user)

@app.route('/data/workExperience/<int:id>', methods=['DELETE'])
def workExperience_delete(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return deleteWorkExperience(id, user)

@app.route('/data/workExperience/<int:id>', methods=['GET'])
def workExperience_get(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getWorkExperiences(id, user)

@app.route('/data/workExperience', methods=['GET'])
def workExperience_get_all():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getAllWorkExperiences(user)

@app.route('/data/skillAdd/<int:id>', methods=['POST'])
def skill_add(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return addSkill(id, getJsonRequest(), user)

@app.route('/data/skill/<int:id>', methods=['POST'])
def skill_update(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateSkill(id, getJsonRequest(), user)

@app.route('/data/skill/<int:id>', methods=['DELETE'])
def skill_delete(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return deleteSkill(id, user)

@app.route('/data/skill/<int:id>', methods=['GET'])
def skill_get(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getSkills(id, user)

@app.route('/data/skill', methods=['GET'])
def skill_get_all():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getAllSkills(user)

@app.route('/data/all', methods=['GET'])
def resume_data():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getAll(user)

@app.route('/data/getAllPublic', methods=['GET'])
def resume_data_public():
  return getAll(getPrimaryUser())

@app.route('/data/blog', methods=['POST'])
def blog_add():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return createBlogPost(getJsonRequest(), user)

@app.route('/data/blog/<int:id>', methods=['POST'])
def blog_update(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateBlogPost(id, getJsonRequest(), user)

@app.route('/data/blog/<int:id>', methods=['DELETE'])
def blog_delete(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return deleteBlogPost(id, user)

@app.route('/data/blog/<int:id>', methods=['GET'])
def blog_get(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getBlogPost(id, user)

@app.route('/data/blog/mine', methods=['GET'])
def blog_get_mine():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return getBlogPosts(user)

@app.route('/data/blog', methods=['GET'])
def blog_get_all():
  return getAllPublishedBlogPosts()

@app.route('/data/settings', methods=['POST'])
def settings_add():
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return createSetting(getJsonRequest(), user)

@app.route('/data/settings/<int:id>', methods=['POST'])
def settings_update(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return updateSetting(id, getJsonRequest(), user)

@app.route('/data/settings/<int:id>', methods=['DELETE'])
def settings_delete(id):
  user = isLoggedIn(getToken())
  if not user:
    return {"success": False, "message": "No token provided"}
  return deleteSetting(id, user)

@app.route('/data/settings/<int:id>', methods=['GET'])
def settings_get(id):
  return getSetting(id)

@app.route('/data/settings', methods=['GET'])
def settings_get_all():
  return getSettings()

@app.route('/data/settings/<key>', methods=['GET'])
def settings_get_key(key):
  return getSettingByKey(key)

# @app.route('/<path:path>')
# @app.route('/')
# def home_page():
#   return render_template('../templates/index.html')