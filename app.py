# from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.utils import secure_filename
# import os
# from datetime import datetime

# app = Flask(__name__, static_folder='.', template_folder='.', static_url_path='')
# app.secret_key = 'truevex_secret_key_123'  # Change this to something very secure

# # Base directory of the application
# basedir = os.path.abspath(os.path.dirname(__file__))

# # Database Configuration
# # Using absolute path to ensure it works on all hosting environments
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
# app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB limit

# db = SQLAlchemy(app)

# # Ensure necessary folders exist
# if not os.path.exists(os.path.join(basedir, 'instance')):
#     os.makedirs(os.path.join(basedir, 'instance'))
# if not os.path.exists(app.config['UPLOAD_FOLDER']):
#     os.makedirs(app.config['UPLOAD_FOLDER'])

# # Models
# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     company = db.Column(db.String(100))
#     email = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(20))
#     service = db.Column(db.String(100))
#     message = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class Application(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     fullname = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
#     dob = db.Column(db.String(50))
#     address = db.Column(db.Text)
#     gender = db.Column(db.String(50))
#     position = db.Column(db.String(100))
#     location = db.Column(db.String(100))
#     qualification = db.Column(db.String(100))
#     passout = db.Column(db.String(50))
#     experience = db.Column(db.String(100))
#     resume_path = db.Column(db.String(200))
#     cover_letter = db.Column(db.Text)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# # Routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/<page>')
# def serve_page(page):
#     # Security: only allow specific html files or prevent directory traversal
#     if '..' in page or '/' in page or '\\' in page:
#         return redirect(url_for('index'))
    
#     if page.endswith('.html'):
#         if os.path.exists(os.path.join(basedir, page)):
#             return render_template(page)
#     return redirect(url_for('index'))

# # Database initialization (runs when the app is loaded, even in production)
# with app.app_context():
#     db.create_all()
#     # Create a default admin if none exists
#     if Admin.query.count() == 0:
#         hashed_pw = generate_password_hash('admin123') # Default password
#         default_admin = Admin(username='admin', password=hashed_pw)
#         db.session.add(default_admin)
#         db.session.commit()

# @app.route('/submit_contact', methods=['POST'])
# def submit_contact():
#     try:
#         name = request.form.get('name')
#         company = request.form.get('company')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         service = request.form.get('service')
#         message = request.form.get('message')

#         new_contact = Contact(name=name, company=company, email=email, phone=phone, service=service, message=message)
#         db.session.add(new_contact)
#         db.session.commit()
        
#         return "<script>alert('Message sent successfully!'); window.location.href='/contact.html';</script>"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# @app.route('/submit_apply', methods=['POST'])
# def submit_apply():
#     try:
#         fullname = request.form.get('fullname')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         dob = request.form.get('dob')
#         address = request.form.get('address')
#         gender = request.form.get('gender')
#         position = request.form.get('position')
#         location = request.form.get('location')
#         qualification = request.form.get('qualification')
#         passout = request.form.get('passout')
#         experience = request.form.get('experience')
#         cover_letter = request.form.get('cover_letter')
        
#         resume = request.files.get('resume')
#         resume_path = None
#         if resume and resume.filename != '':
#             filename = secure_filename(resume.filename)
#             unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
#             # Save the file
#             resume.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
#             # Store ONLY the filename in DB to avoid path separator issues
#             resume_path = unique_filename

#         new_app = Application(
#             fullname=fullname, email=email, phone=phone, dob=dob, address=address,
#             gender=gender, position=position, location=location, qualification=qualification,
#             passout=passout, experience=experience, resume_path=resume_path, cover_letter=cover_letter
#         )
#         db.session.add(new_app)
#         db.session.commit()
        
#         return "<script>alert('Application submitted successfully!'); window.location.href='/apply.html';</script>"
#     except Exception as e:
#         return f"An error occurred: {str(e)}"

# # Admin Section
# @app.route('/admin-login', methods=['GET', 'POST'])
# def admin_login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         admin = Admin.query.filter_by(username=username).first()
#         if admin and check_password_hash(admin.password, password):
#             session['admin_id'] = admin.id
#             return redirect(url_for('admin_dashboard'))
#         else:
#             flash('Invalid credentials')
#     return render_template('login.html')

# @app.route('/admin-dashboard')
# def admin_dashboard():
#     if 'admin_id' not in session:
#         return redirect(url_for('admin_login'))
#     contacts = Contact.query.order_by(Contact.created_at.desc()).all()
#     applications = Application.query.order_by(Application.created_at.desc()).all()
#     return render_template('admin_dashboard.html', contacts=contacts, applications=applications)

# @app.route('/admin/delete-contact/<int:id>')
# def delete_contact(id):
#     if 'admin_id' not in session: return redirect(url_for('admin_login'))
#     contact = Contact.query.get_or_404(id)
#     db.session.delete(contact)
#     db.session.commit()
#     return redirect(url_for('admin_dashboard'))

# @app.route('/admin/delete-app/<int:id>')
# def delete_app(id):
#     if 'admin_id' not in session: return redirect(url_for('admin_login'))
#     app_data = Application.query.get_or_404(id)
#     if app_data.resume_path:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], app_data.resume_path)
#         if os.path.exists(file_path):
#             os.remove(file_path)
#     db.session.delete(app_data)
#     db.session.commit()
#     return redirect(url_for('admin_dashboard'))

# @app.route('/logout')
# def logout():
#     session.pop('admin_id', None)
#     return redirect(url_for('admin_login'))

# @app.route('/view-resume/<path:filename>')
# def view_resume(filename):
#     if 'admin_id' not in session: return "Access Denied"
#     # Clean up the filename: remove 'uploads/' prefix and handle both slash types
#     clean_filename = filename.replace('uploads/', '').replace('uploads\\', '').replace('\\', '/')
#     # If the path actually exists in uploads, serve it
#     return send_from_directory(app.config['UPLOAD_FOLDER'], clean_filename, mimetype='application/pdf')

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# =========================
# APP SETUP
# =========================
app = Flask(__name__)
CORS(app)

app.secret_key = os.environ.get("SECRET_KEY", "truevex_secret_key_123")
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =========================
# DATABASE CONFIG
# =========================
if os.environ.get("RENDER"):
    # Production (Render) → MySQL
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    )
else:
    # Local development → SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "sqlite:///" + os.path.join(BASE_DIR, "local.db")
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# =========================
# UPLOAD CONFIG
# =========================
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

# =========================
# MODELS
# =========================
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    service = db.Column(db.String(100))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(50))
    address = db.Column(db.Text)
    gender = db.Column(db.String(50))
    position = db.Column(db.String(100))
    location = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    passout = db.Column(db.String(50))
    experience = db.Column(db.String(100))
    resume_path = db.Column(db.String(200))
    cover_letter = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# =========================
# INIT DATABASE
# =========================
with app.app_context():
    db.create_all()
    if Admin.query.count() == 0:
        admin = Admin(
            username="admin",
            password=generate_password_hash("admin123")
        )
        db.session.add(admin)
        db.session.commit()

# =========================
# API ROUTES
# =========================
@app.route("/", methods=["GET"])
def root():
    return jsonify({"status": "Truevex backend running"}), 200

@app.route("/api/contact", methods=["POST"])
def submit_contact():
    data = request.json

    contact = Contact(
        name=data.get("name"),
        company=data.get("company"),
        email=data.get("email"),
        phone=data.get("phone"),
        service=data.get("service"),
        message=data.get("message")
    )
    db.session.add(contact)
    db.session.commit()

    return jsonify({"message": "Message sent successfully"}), 200

@app.route("/api/apply", methods=["POST"])
def submit_apply():
    data = request.form
    resume = request.files.get("resume")

    resume_filename = None
    if resume and resume.filename:
        filename = secure_filename(resume.filename)
        resume_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
        resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))

    application = Application(
        fullname=data.get("fullname"),
        email=data.get("email"),
        phone=data.get("phone"),
        dob=data.get("dob"),
        address=data.get("address"),
        gender=data.get("gender"),
        position=data.get("position"),
        location=data.get("location"),
        qualification=data.get("qualification"),
        passout=data.get("passout"),
        experience=data.get("experience"),
        cover_letter=data.get("cover_letter"),
        resume_path=resume_filename
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application submitted successfully"}), 200

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

# =========================
# RUN LOCAL
# =========================
if __name__ == "__main__":
    app.run(debug=True)
