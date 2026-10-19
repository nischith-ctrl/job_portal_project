import os

import requests

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

from flask_login import (

    LoginManager, UserMixin, login_user, login_required, logout_user, current_user

)

from werkzeug.security import generate_password_hash, check_password_hash



# ---------------------------------------------------------

# 1. APP & DATABASE CONFIGURATION

# ---------------------------------------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret-job-portal-key-2026'



# Save database directly in the project root as job_portal.db (.sqlite3 compatible)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'job_portal.sqlite3')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

login_manager.login_message_category = 'info'





# ---------------------------------------------------------

# 2. DATABASE MODELS

# ---------------------------------------------------------

class User(UserMixin, db.Model):

    """Stores Job Seekers, Employers, and Admins."""

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)

    role = db.Column(db.String(20), nullable=False, default='seeker')  # 'seeker', 'employer', 'admin'



    # Relationships

    jobs_posted = db.relationship('Job', backref='employer', lazy=True, cascade="all, delete-orphan")

    applications = db.relationship('Application', backref='applicant', lazy=True, cascade="all, delete-orphan")



    def set_password(self, password):

        self.password_hash = generate_password_hash(password)



    def check_password(self, password):

        return check_password_hash(self.password_hash, password)





class Job(db.Model):

    """Stores job listings posted by Employers or imported via API."""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120), nullable=False)

    company = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(80), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    salary = db.Column(db.String(60), nullable=False)

    description = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    employer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)



    # Relationships

    applications = db.relationship('Application', backref='job', lazy=True, cascade="all, delete-orphan")





class Application(db.Model):

    """Stores job applications submitted by Job Seekers."""

    id = db.Column(db.Integer, primary_key=True)

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    resume_link = db.Column(db.String(255), nullable=False)

    cover_letter = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(30), default='Submitted')  # Submitted, Reviewed, Shortlisted, Rejected

    applied_at = db.Column(db.DateTime, default=datetime.utcnow)





@login_manager.user_loader

def load_user(user_id):

    return db.session.get(User, int(user_id))





# ---------------------------------------------------------

# 3. PUBLIC & JOB SEARCH ROUTES

# ---------------------------------------------------------

@app.route('/')

def index():

    """Home page with multi-filter job search (location, category, company, keyword)."""

    keyword = request.args.get('keyword', '').strip()

    location = request.args.get('location', '').strip()

    category = request.args.get('category', '').strip()

    company = request.args.get('company', '').strip()



    query = Job.query



    if keyword:

        query = query.filter(Job.title.ilike(f'%{keyword}%') | Job.description.ilike(f'%{keyword}%'))

    if location:

        query = query.filter(Job.location.ilike(f'%{location}%'))

    if category:

        query = query.filter(Job.category.ilike(f'%{category}%'))

    if company:

        query = query.filter(Job.company.ilike(f'%{company}%'))



    jobs = query.order_by(Job.created_at.desc()).all()



    # Fetch distinct categories for the filter dropdown

    categories = [c[0] for c in db.session.query(Job.category).distinct().all()]

    return render_template('index.html', jobs=jobs, categories=categories)





@app.route('/job/<int:job_id>')

def job_detail(job_id):

    """Displays full details of a job and the application form."""

    job = db.session.get(Job, job_id)

    if not job:

        flash('Job listing not found.', 'danger')

        return redirect(url_for('index'))



    already_applied = False

    if current_user.is_authenticated and current_user.role == 'seeker':

        existing = Application.query.filter_by(job_id=job.id, user_id=current_user.id).first()

        already_applied = existing is not None



    return render_template('job_detail.html', job=job, already_applied=already_applied)





# ---------------------------------------------------------

# 4. AUTHENTICATION ROUTES

# ---------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])

def register():

    """Registers a new Job Seeker or Employer."""

    if current_user.is_authenticated:

        return redirect(url_for('dashboard'))



    if request.method == 'POST':

        username = request.form.get('username', '').strip()

        email = request.form.get('email', '').strip().lower()

        password = request.form.get('password', '')

        role = request.form.get('role', 'seeker')



        if role not in ['seeker', 'employer']:

            role = 'seeker'



        if User.query.filter((User.username == username) | (User.email == email)).first():

            flash('Username or email already exists. Please choose another.', 'danger')

            return redirect(url_for('register'))



        new_user = User(username=username, email=email, role=role)

        new_user.set_password(password)

        db.session.add(new_user)

        db.session.commit()



        flash('Account created successfully! Please log in.', 'success')

        return redirect(url_for('login'))



    return render_template('register.html')





@app.route('/login', methods=['GET', 'POST'])

def login():

    """Logs in an existing user."""

    if current_user.is_authenticated:

        return redirect(url_for('dashboard'))



    if request.method == 'POST':

        email = request.form.get('email', '').strip().lower()

        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()



        if user and user.check_password(password):

            login_user(user)

            flash(f'Welcome back, {user.username}!', 'success')

            return redirect(url_for('dashboard'))

        else:

            flash('Invalid email or password.', 'danger')



    return render_template('login.html')





@app.route('/logout')

@login_required

def logout():

    logout_user()

    flash('You have been logged out.', 'info')

    return redirect(url_for('index'))





# ---------------------------------------------------------

# 5. DASHBOARD, JOB POSTING & APPLICATION ROUTES

# ---------------------------------------------------------

@app.route('/dashboard')

@login_required

def dashboard():

    """Unified dashboard that adapts to Seeker, Employer, or Admin role."""

    if current_user.role == 'admin':

        all_users = User.query.all()

        all_jobs = Job.query.order_by(Job.created_at.desc()).all()

        all_apps = Application.query.order_by(Application.applied_at.desc()).all()

        return render_template('dashboard.html', users=all_users, jobs=all_jobs, applications=all_apps)



    elif current_user.role == 'employer':

        my_jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()

        return render_template('dashboard.html', jobs=my_jobs)



    else:  # Job Seeker

        my_apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()

        return render_template('dashboard.html', applications=my_apps)





@app.route('/post-job', methods=['POST'])

@login_required

def post_job():

    """Allows Employers and Admins to create a new job listing."""

    if current_user.role not in ['employer', 'admin']:

        flash('Only Employers and Admins can post jobs.', 'danger')

        return redirect(url_for('dashboard'))



    new_job = Job(

        title=request.form.get('title', '').strip(),

        company=request.form.get('company', '').strip(),

        category=request.form.get('category', '').strip(),

        location=request.form.get('location', '').strip(),

        salary=request.form.get('salary', '').strip(),

        description=request.form.get('description', '').strip(),

        employer_id=current_user.id

    )

    db.session.add(new_job)

    db.session.commit()

    flash('Job posted successfully!', 'success')

    return redirect(url_for('dashboard'))





@app.route('/delete-job/<int:job_id>', methods=['POST'])

@login_required

def delete_job(job_id):

    """Allows the job owner or an Admin to delete a job listing."""

    job = db.session.get(Job, job_id)

    if not job:

        flash('Job not found.', 'danger')

        return redirect(url_for('dashboard'))



    if current_user.role == 'admin' or job.employer_id == current_user.id:

        db.session.delete(job)

        db.session.commit()

        flash('Job listing deleted.', 'info')

    else:

        flash('Unauthorized action.', 'danger')



    return redirect(url_for('dashboard'))



@app.route('/edit-job/<int:job_id>', methods=['GET', 'POST'])

@login_required

def edit_job(job_id):

    """Allows the Employer who posted the job or Admin to edit a job listing."""

    job = db.session.get(Job, job_id)

    if not job or (current_user.role != 'admin' and job.employer_id != current_user.id):

        flash('Unauthorized or job not found.', 'danger')

        return redirect(url_for('dashboard'))



    if request.method == 'POST':

        job.title = request.form.get('title', '').strip()

        job.company = request.form.get('company', '').strip()

        job.category = request.form.get('category', '').strip()

        job.location = request.form.get('location', '').strip()

        job.salary = request.form.get('salary', '').strip()

        job.description = request.form.get('description', '').strip()

        db.session.commit()

        flash('Job listing updated successfully!', 'success')

        return redirect(url_for('dashboard'))



    return render_template('edit_job.html', job=job)





@app.route('/update-application/<int:app_id>', methods=['POST'])

@login_required

def update_application(app_id):

    """Allows Employers and Admins to mark an application as Shortlisted or Rejected."""

    application = db.session.get(Application, app_id)

    if application and (current_user.role == 'admin' or application.job.employer_id == current_user.id):

        application.status = request.form.get('status', 'Reviewed')

        db.session.commit()

        flash(f'Application status updated to {application.status}.', 'info')

    return redirect(url_for('dashboard'))



@app.route('/apply/<int:job_id>', methods=['POST'])

@login_required

def apply_job(job_id):

    """Allows Job Seekers to apply to a job."""

    if current_user.role != 'seeker':

        flash('Only Job Seekers can submit job applications.', 'warning')

        return redirect(url_for('job_detail', job_id=job_id))



    existing = Application.query.filter_by(job_id=job_id, user_id=current_user.id).first()

    if existing:

        flash('You have already applied for this position.', 'info')

        return redirect(url_for('job_detail', job_id=job_id))



    application = Application(

        job_id=job_id,

        user_id=current_user.id,

        resume_link=request.form.get('resume_link', '').strip(),

        cover_letter=request.form.get('cover_letter', '').strip()

    )

    db.session.add(application)

    db.session.commit()

    flash('Application submitted successfully!', 'success')

    return redirect(url_for('dashboard'))





@app.route('/delete-user/<int:user_id>', methods=['POST'])

@login_required

def delete_user(user_id):

    """Admin-only route to manage and remove users."""

    if current_user.role != 'admin':

        flash('Admin privileges required.', 'danger')

        return redirect(url_for('dashboard'))



    user = db.session.get(User, user_id)

    if user and user.id != current_user.id:

        db.session.delete(user)

        db.session.commit()

        flash(f'User {user.username} removed.', 'info')

    else:

        flash('Cannot delete your own admin account.', 'warning')



    return redirect(url_for('dashboard'))





# ---------------------------------------------------------

# 6. API INTEGRATION (EXTERNAL IMPORT + REST ENDPOINT)

# ---------------------------------------------------------

@app.route('/api/jobs', methods=['GET'])

def api_get_jobs():

    """Public REST API endpoint returning all stored job listings as JSON."""

    jobs = Job.query.order_by(Job.created_at.desc()).all()

    return jsonify([

        {

            'id': j.id,

            'title': j.title,

            'company': j.company,

            'category': j.category,

            'location': j.location,

            'salary': j.salary,

            'created_at': j.created_at.strftime('%Y-%m-%d')

        } for j in jobs

    ])





@app.route('/import-api-jobs', methods=['POST'])

@login_required

def import_api_jobs():

    """Fetches real tech job listings from the public Remotive API into the database."""

    if current_user.role not in ['employer', 'admin']:

        flash('Unauthorized.', 'danger')

        return redirect(url_for('dashboard'))



    try:

        response = requests.get('https://remotive.com/api/remote-jobs?limit=3', timeout=6)

        data = response.json()

        imported_count = 0



        for item in data.get('jobs', [])[:3]:

            job = Job(

                title=item.get('title', 'Software Engineer')[:120],

                company=item.get('company_name', 'Remote Tech')[:100],

                category=item.get('category', 'Software Development')[:80],

                location=item.get('candidate_required_location', 'Remote')[:100],

                salary=item.get('salary') or '$70,000 - $100,000',

                description=f"Imported via Remotive API. Apply or view details. Role Type: {item.get('job_type', 'Full-time')}.",

                employer_id=current_user.id

            )

            db.session.add(job)

            imported_count += 1



        db.session.commit()

        flash(f'Successfully imported {imported_count} live jobs from external API!', 'success')

    except Exception:

        flash('Could not reach external API right now. Please try again later.', 'warning')



    return redirect(url_for('dashboard'))





# ---------------------------------------------------------

# 7. DATABASE INITIALIZATION & SEED DATA

# ---------------------------------------------------------

def seed_database():

    """Creates tables and seeds default Admin, Employer, Seeker, and sample jobs."""

    db.create_all()

    if not User.query.filter_by(email='admin@jobportal.com').first():

        admin = User(username='admin', email='admin@jobportal.com', role='admin')

        admin.set_password('admin123')



        employer = User(username='techcorp_hr', email='hr@techcorp.com', role='employer')

        employer.set_password('employer123')



        seeker = User(username='john_seeker', email='john@example.com', role='seeker')

        seeker.set_password('seeker123')



        db.session.add_all([admin, employer, seeker])

        db.session.commit()



        sample_jobs = [

            Job(

                title='Python Backend Developer',

                company='TechCorp Solutions',

                category='Software Development',

                location='Bengaluru',

                salary='₹8,00,000 - ₹12,00,000 / yr',

                description='Build scalable REST APIs and web applications using Python, Flask, and SQL databases.',

                employer_id=employer.id

            ),

            Job(

                title='Frontend Web Designer',

                company='Creative Pulse Studio',

                category='Design & UI/UX',

                location='Remote',

                salary='₹5,00,000 - ₹7,50,000 / yr',

                description='Design responsive user interfaces using HTML5, CSS3, Bootstrap 5, and JavaScript.',

                employer_id=employer.id

            ),

            Job(

                title='Data Analyst Intern',

                company='DataWave Analytics',

                category='Data Science',

                location='Mangaluru',

                salary='₹25,000 / month',

                description='Analyze datasets, create dashboards, and assist with SQL reporting pipelines.',

                employer_id=employer.id

            )

        ]

        db.session.add_all(sample_jobs)

        db.session.commit()





# Run database creation & seeding outside __main__ so Gunicorn (Render/Railway) also runs it

with app.app_context():

    seed_database()



if __name__ == '__main__':

    app.run(debug=True) 