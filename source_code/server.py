# --- Peserta Blueprint: Bulk Upload & Single Entry ---
# This section adds a new Flask Blueprint for managing participants (peserta).
# It provides:
#   - Viewing all peserta
#   - Bulk upload via Excel (.xlsx)
#   - Single entry form
#   - OSCE attempt tracking
#
# How it works:
#   - Admin can visit /peserta to see all peserta
#   - Admin can upload an Excel file at /peserta/upload
#   - Admin can add a single peserta at /peserta/add
#
# Required columns in Excel: id_peserta, nama, universitas, email, no_telp
#
# Make sure you have the HTML templates: peserta_list.html, peserta_upload.html, peserta_add.html

# All imports at the top
from flask import Blueprint, request, render_template, redirect, url_for, flash, Flask, session, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from module.database import Database
import pandas as pd
import pymysql
import os
from datetime import datetime

# Create a Blueprint for peserta management
peserta_bp = Blueprint('peserta', __name__, url_prefix='/peserta')

# --- View all peserta ---
@peserta_bp.route('/', methods=['GET'])
def peserta_list():
    # Connect to MySQL database
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'aplikasi-kolegium-mysql'),
        user=os.getenv('DB_USER', 'dev'),
        password=os.getenv('DB_PASSWORD', 'dev'),
        db=os.getenv('DB_NAME', 'crud_flask'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    # Fetch all peserta records with university names and attempt info
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT p.*, u.nama_universitas,
                   CASE WHEN op.id_peserta IS NOT NULL THEN 'Second Attempt' ELSE 'First Attempt' END as attempt_status
            FROM peserta p 
            LEFT JOIN university u ON p.universitas = u.id_universitas
            LEFT JOIN osce_peserta op ON p.id_peserta = op.id_peserta
            ORDER BY p.created_at DESC
        ''')
        peserta = cursor.fetchall()
    conn.close()
    return render_template('peserta_list.html', peserta=peserta)

# --- Bulk upload peserta via Excel ---
# GET /peserta/upload: Show upload form
# POST /peserta/upload: Process uploaded Excel file
@peserta_bp.route('/upload', methods=['GET', 'POST'])
def peserta_upload():
    if request.method == 'POST':
        # Check if this is the confirmation step
        if request.form.get('confirm_upload'):
            selected_indices = request.form.getlist('selected_records')
            if not selected_indices:
                flash('No records selected for upload', 'warning')
                return redirect(url_for('peserta.peserta_upload'))
            
            # Get the stored data from session
            upload_data = session.get('upload_data')
            if not upload_data:
                flash('Upload session expired. Please upload the file again.', 'error')
                return redirect(url_for('peserta.peserta_upload'))
            
            # Process selected records
            conn = pymysql.connect(
                host=os.getenv('DB_HOST', 'aplikasi-kolegium-mysql'),
                user=os.getenv('DB_USER', 'dev'),
                password=os.getenv('DB_PASSWORD', 'dev'),
                db=os.getenv('DB_NAME', 'crud_flask'),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            
            inserted, errors = 0, []
            for idx in selected_indices:
                row = upload_data[int(idx)]
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            'INSERT INTO peserta (id_peserta, nama, universitas, email, no_telp) VALUES (%s, %s, %s, %s, %s)',
                            (row.get('id_peserta'), row.get('nama'), row.get('universitas'), row.get('email'), row.get('no_telp'))
                        )
                    conn.commit()
                    inserted += 1
                except Exception as e:
                    errors.append(f"Row {int(idx)+1}: {str(e)}")
            
            conn.close()
            
            # Clear session data
            session.pop('upload_data', None)
            
            if errors:
                flash(f'Successfully inserted {inserted} records. Errors: {" | ".join(errors)}', 'warning')
            else:
                flash(f'Successfully inserted all {inserted} records!', 'success')
            
            return redirect(url_for('peserta.peserta_list'))
        
        # File upload step
        file = request.files.get('file')
        if not file:
            flash('No file selected', 'error')
            return redirect(url_for('peserta.peserta_upload'))
        
        # Determine file type and read into pandas DataFrame
        filename = file.filename.lower()
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                flash('Unsupported file format. Please upload .csv or .xlsx', 'error')
                return redirect(url_for('peserta.peserta_upload'))
        except Exception as e:
            flash(f'Error reading file: {e}', 'error')
            return redirect(url_for('peserta.peserta_upload'))
        
        # Convert DataFrame to list of dicts for session storage
        upload_data = df.to_dict('records')
        
        # Store in session for the confirmation step
        session['upload_data'] = upload_data
        
        # Validate data and show preview
        validation_errors = []
        for i, row in enumerate(upload_data):
            if not row.get('id_peserta'):
                validation_errors.append(f"Row {i+1}: Missing ID Peserta")
            if not row.get('nama'):
                validation_errors.append(f"Row {i+1}: Missing Nama")
            if not row.get('email'):
                validation_errors.append(f"Row {i+1}: Missing Email")
            if not row.get('universitas'):
                validation_errors.append(f"Row {i+1}: Missing Universitas")
        
        return render_template('peserta_upload.html', 
                             upload_data=upload_data, 
                             validation_errors=validation_errors,
                             show_preview=True)
    
    # Clear any existing upload data
    session.pop('upload_data', None)
    return render_template('peserta_upload.html')

# --- Add a single peserta ---
# GET /peserta/add: Show entry form
# POST /peserta/add: Insert new peserta
@peserta_bp.route('/add', methods=['GET', 'POST'])
def peserta_add():
    # Connect to database to get universitas list
    conn = pymysql.connect(
        host=os.getenv('DB_HOST', 'aplikasi-kolegium-mysql'),
        user=os.getenv('DB_USER', 'dev'),
        password=os.getenv('DB_PASSWORD', 'dev'),
        db=os.getenv('DB_NAME', 'crud_flask'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    universitas_list = []
    with conn.cursor() as cursor:
        cursor.execute('SELECT id_universitas, nama_universitas FROM university ORDER BY nama_universitas ASC')
        universitas_list = cursor.fetchall()
    if request.method == 'POST':
        # Get form data
        id_peserta = request.form.get('id_peserta')
        nama = request.form.get('nama')
        universitas = request.form.get('universitas')
        email = request.form.get('email')
        no_telp = request.form.get('no_telp')
        try:
            with conn.cursor() as cursor:
                # Insert new peserta
                cursor.execute(
                    'INSERT INTO peserta (id_peserta, nama, universitas, email, no_telp) VALUES (%s, %s, %s, %s, %s)',
                    (id_peserta, nama, universitas, email, no_telp)
                )
            conn.commit()
            flash('Peserta added successfully', 'success')
        except Exception as e:
            # Show error if insert fails
            flash(str(e), 'error')
        conn.close()
        return redirect(url_for('peserta.peserta_list'))
    conn.close()
    # Render the single entry form template, pass universitas_list
    return render_template('peserta_add.html', universitas_list=universitas_list)

@peserta_bp.route('/statistics', methods=['GET'])
@login_required
def peserta_statistics():
    """Display OSCE statistics by university and attempt status"""
    db = Database()
    university_stats = db.get_osce_statistics_by_university()
    
    # Get attempt status breakdown  
    first_attempt_list = db.get_peserta_by_attempt_status('First Attempt')
    second_attempt_list = db.get_peserta_by_attempt_status('Second Attempt')
    
    return render_template('peserta_statistics.html', 
                         university_stats=university_stats,
                         first_attempt_count=len(first_attempt_list),
                         second_attempt_count=len(second_attempt_list))

@peserta_bp.route('/osce-sessions', methods=['GET'])  
@login_required
def osce_sessions():
    """Display all OSCE sessions with participant counts"""
    db = Database()
    sessions = db.get_osce_sessions()
    
    return render_template('osce_sessions.html', sessions=sessions)

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

# Register peserta blueprint so /peserta routes are available
app.register_blueprint(peserta_bp)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Dummy user class and user store (replace with DB integration as needed)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Example user list with hashed password from environment variables
admin_username = os.getenv('ADMIN_USERNAME', 'admin')
admin_password = os.getenv('ADMIN_PASSWORD', 'adminpass')
hashed_password = generate_password_hash(admin_password)
users = [User(1, admin_username, hashed_password)]

@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if str(user.id) == str(user_id):
            return user
    return None

@app.route('/')
@login_required
def index():
    """Dashboard showing peserta statistics and overview"""
    stats = db.get_peserta_stats()
    recent_peserta = db.get_recent_peserta(5)
    return render_template('index.html', stats=stats, recent_peserta=recent_peserta)

@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""
    return {'status': 'healthy', 'timestamp': str(datetime.now())}, 200

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error.html')

# --- Flask-Login routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u.username == username), None)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully.')
            # Get next page from form
            next_page = request.form.get('next')
            # Safety check - if next_page is invalid, go to index
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')
            # Handle special case when 'next' is just 'index'
            if next_page == 'index':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login', _external=True))

@app.route('/download-template/<file_type>')
def download_template(file_type):
    """Download template files for bulk upload"""
    if file_type == 'excel':
        filename = 'peserta_upload_template.xlsx'
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    elif file_type == 'csv':
        filename = 'peserta_upload_template.csv'
        mimetype = 'text/csv'
    else:
        flash('Invalid template type', 'error')
        return redirect(url_for('peserta.peserta_upload'))
    
    template_path = os.path.join(app.root_path, 'templates', filename)
    if not os.path.exists(template_path):
        flash('Template file not found', 'error')
        return redirect(url_for('peserta.peserta_upload'))
    
    return send_file(template_path, as_attachment=True, download_name=filename, mimetype=mimetype)

# --- Protect resources ---
@app.before_request
def require_login():
    # Allow access to login page, static files, health check, and template downloads without authentication
    allowed_paths = ['/login', '/static', '/health', '/download-template/']
    
    for allowed_path in allowed_paths:
        if request.path.startswith(allowed_path):
            return
    
    # Require authentication for all other routes
    if not current_user.is_authenticated:
        return redirect(url_for('login', next=request.endpoint))

if __name__ == '__main__':
    app.run(port=8181, host="0.0.0.0")
