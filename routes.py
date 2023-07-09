from flask import render_template, redirect, url_for, request, flash, session, Blueprint
from flask_login import login_required, login_manager, login_user, current_user
from models import User
import qrcode, random, string
from io import BytesIO
from functools import wraps
from database import db
from app import app
from werkzeug.security import check_password_hash
#from sqlalchemy import func


app_routes = Blueprint('app_routes', __name__)

# Route for home page
@app_routes.route('/')
def home():
    # Render the home page template
    return render_template('home.html')

# Route for user registration
@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Added email attribute
        password = request.form['password']

        if User.query.filter_by(username=username).first() is not None:
            flash('Username already exists')
            return redirect(url_for('app_routes.register'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('app_routes.login'))

    return render_template('register.html')

# Route for user login
@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data
        username = request.form['username']
        password = request.form['password']

        # Validate the user's credentials
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and if the password is correct
        if user and user.check_password(password):
            # Password is correct
            login_user(user)  # Log in the user
            session['user_id'] = user.id  # Set the user_id in the session
            flash('Logged in successfully.', 'success')
            return redirect(url_for('app_routes.dashboard'))
        else:
            # Invalid username or password
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('app_routes.login'))
    else:
        # Render the login form
        return render_template('login.html')




# Decorator function to check if a user is authorized
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('app_routes.login'))
        return f(*args, **kwargs)
    return decorated_function


# Route for the user dashboard
@app_routes.route('/dashboard')
@login_required
def dashboard():
    from models import ShortURL
    # Get the user_id from the session
    user_id = session.get('user_id')
    print('Session User ID:', user_id)
    if user_id:
        # Retrieve the user from the database
        user = User.query.get(user_id)
        print('User:', user)  # Print the user object for debugging

        # Render the dashboard template and pass the user object
        return render_template('dashboard.html', user=user)
    else:
        # Redirect to the login page if user_id is not found in the session
        return redirect(url_for('app_routes.login'))



# Route for creating a short URL
@app_routes.route('/create', methods=['POST'])
@login_required
def create_short_url():
    from models import ShortURL
    
    if 'user_id' not in session:
        return redirect(url_for('app_routes.login'))
    
    original_url = request.form.get('original_url')
    custom_url = request.form.get('custom_url')
    user_id = session['user_id']
    
    # Generate a unique short code
    short_code = generate_short_code()
    
    # Create a new ShortURL object
    short_url = ShortURL(original_url=original_url, short_code=short_code, custom_url=custom_url, user_id=user_id)
    db.session.add(short_url)
    db.session.commit()
    
    return redirect(url_for('app_routes.dashboard'))


def generate_short_code():
    from models import ShortURL
    # Generate a random alphanumeric string of length 6 for the short code
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    
    # Check if the generated short code is already in use
    while ShortURL.query.filter_by(short_code=short_code).first() is not None:
        # If the short code is already in use, generate a new one
        short_code = ''.join(random.choice(characters) for _ in range(6))
    
    return short_code

# Route for redirecting to the original URL
@app_routes.route('/<short_code>')
def redirect_to_original_url(short_code):
    from models import ShortURL, LinkAnalytics
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if short_url:
        # Create a new LinkAnalytics object
        link_analytics = LinkAnalytics(short_url_id=short_url.id, user_agent=request.user_agent.string)
        db.session.add(link_analytics)
        db.session.commit()
        
        return redirect(short_url.original_url)
    
    return render_template('404.html'), 404

# Route for displaying analytics for a short URL
@app_routes.route('/analytics/<short_code>')
@login_required
def short_url_analytics(short_code):
    from models import ShortURL, LinkAnalytics
    if 'user_id' not in session:
        return redirect(url_for('app_routes.login'))

    short_url = ShortURL.query.filter_by(short_code=short_code).first()

    if short_url:
        return render_template('analytics.html', short_url=short_url)

    return render_template('404.html'), 404

# Route for generating a QR code for a short URL
@app_routes.route('/qrcode/<short_code>')
def generate_qrcode(short_code):
    from models import ShortURL
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if short_url:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(request.host_url + short_url.short_code)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return img_io.getvalue(), 200, {'Content-Type': 'image/png'}
    
    return render_template('404.html'), 404