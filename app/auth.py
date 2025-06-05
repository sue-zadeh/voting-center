import os
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.utils import secure_filename
import mysql.connector
from flask_hashing import Hashing
from mysql.connector import connect, Error
from datetime import datetime
from app import app
import app.connect as connect


app.secret_key = 'e2e62cdb171271f0b12e5043f9f84208eba1f05c8658704e'
PASSWORD_SALT = '1234abcd'

hashing = Hashing(app)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db_connection = None

def getCursor(dictionary=False, buffered=False):
    global db_connection

    try:
        if db_connection is None or not db_connection.is_connected():
            db_connection = mysql.connector.connect(
                user=connect.dbuser,
                password=connect.dbpass,
                host=connect.dbhost,
                database=connect.dbname,
                auth_plugin='mysql_native_password',
                autocommit=True
            )
            print("Connection successful")

        cursor = db_connection.cursor(dictionary=dictionary, buffered=buffered)
        return cursor, db_connection

    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        return None, None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'assets')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def save_profile_photo(photo):
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(photo_path)
        return filename
    return None  # Return None if no photo is uploaded or the file is invalid

# ------ members, moderators, admins
# def redirect_based_on_role(html_file):
#      if "member" in session:
#          return redirect(url_for("voter"))
#      elif "moderator" in session:
#         return redirect(url_for("Scrutineer"))
#      elif "admin" in session:
#         return redirect(url_for("Admin"))
#      else:
#          return render_template(html_file)
    
def render_login_or_register(registered, toLogin, msg, username):
    if toLogin:
        return render_template('login.html', msg=msg, toLogin=toLogin, registered=registered, username=username) 
    else:
        return render_template("register.html", msg=msg, toLogin=toLogin)
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
#-- home page
@app.route("/")
def home():
    return render_template("home.html")

# @app.route('/uploads/<filename>')

     #------register form-------#@app.route('/register', methods=['GET', 'POST'])
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        username = request.form.get('username')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')  
        email = request.form.get('email')
        location = request.form.get('location')
        file = request.files.get('profile_image')
        profile_image = None
        
        # Check if password matches confirm password
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('register'))

        cursor, conn = getCursor()
        if not cursor or not conn:
            flash('Database connection error', 'error')
            return redirect(url_for('register'))

        if not re.match(r'^[A-Za-z\s,]+$', location):
            flash('Location must contain only letters, spaces, and commas.', 'error')
            return redirect(url_for('register'))
        
        # Save the profile image if uploaded, otherwise set to None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            profile_image = filename  # Store the filename in the database
        else:
            profile_image = None  # Set to None if no file is uploaded or file is invalid

        # Check if username already exists
        cursor.execute("SELECT * FROM User WHERE Username = %s", (username,))
        account = cursor.fetchone()

        if account:
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        # Check if email already exists
        cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
        account = cursor.fetchone()

        if account:
            flash('Email already exists!', 'error')
            return redirect(url_for('register'))

        password = hashing.hash_value(password, PASSWORD_SALT)

        cursor.execute("""
            INSERT INTO User (Username, FirstName, LastName, Email, Password, Location, Image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (username, first_name, last_name, email, password, location, profile_image))
        conn.commit()

        flash('Registration successful. Please login now.', 'success')
        return redirect(url_for('login', username=username))

    return render_template("register.html")

  
  
   #----- login------#
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        cursor, conn = getCursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            # Check if the account is inactive
            if user['status'] == 'inactive':
                flash('Your account is inactive. Please contact an admin to reactivate your account.', 'danger')
                return redirect(url_for('login'))

            # Hash the input password and compare with the stored hash
            input_password_hash = hashing.hash_value(password, PASSWORD_SALT)
            db_password_hash = user['password']

            if input_password_hash == db_password_hash:
                # Set session variables
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['role'] = user['role']

                # Redirect based on role
                if session['role'] == 'admin':
                    return redirect(url_for('admin_home'))
                elif session['role'] == 'scrutineer':
                    return redirect(url_for('scrutineer_home'))
                else:
                    return redirect(url_for('voting'))
            else:
                flash('Invalid username or password.', 'danger')
        else:
            flash('Invalid username or password.', 'danger')

        if user and hashing.check_value(user['Password'], password, PASSWORD_SALT):
            session['UserID'] = user['UserID']
            session['Username'] = user['Username']
            session['Role'] = user['Role']
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('voting'))


        return redirect(url_for('login'))

    return render_template("login.html")
  
  #------------profile----------#
  
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('UserID')
    cursor, conn = getCursor(dictionary=True)
    
    # Fetch user details from the database, including the Image field
    cursor.execute("SELECT UserID, Username, FirstName, LastName, Email, Location, Image, Status FROM User WHERE UserID = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('login'))
    
    # Render the profile page with the user data
    return render_template('profile.html', user=user)


    


#----logout---#

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))



# admin function
@app.route('/admin/home')
def admin_home():
    # Ensure the user is logged in and has the role of admin
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Access denied: Admins only.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('admin_home.html')


#Creat account

@app.route('/admin/manage_users')
@admin_required  
def manage_users():
    if session.get('username') != 'admin1':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('admin_home'))  # Redirect to another page if not super admin
    
    return render_template('manage_users.html')



@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form.get('email')
        role = request.form.get('role')
        
        if not username or not password or not email or not first_name or not last_name:
            error_message = 'All fields are required.'
            return render_template('create_account.html', error_message=error_message)

        try:
            cursor, conn = getCursor()
            # Hash the password using the specified hashing method
            hashed_password = hashing.hash_value(password, PASSWORD_SALT)
            cursor.execute(
                "INSERT INTO users (username, password, first_name, last_name, email, role) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, hashed_password, first_name, last_name, email, role)
            )
            conn.commit()
            cursor.close()
            conn.close()

            # Flash the success message and redirect to the manage_users page
            flash('Account created successfully!', 'success')
            return redirect(url_for('manage_users'))
        except Exception as e:
            error_message = f'An error occurred: {str(e)}'
            return render_template('create_account.html', error_message=error_message)

    return render_template('create_account.html')




#Manage admin account

@app.route('/admin/manage_accounts', methods=['GET', 'POST'])
@admin_required
def manage_accounts():
    cursor, conn = getCursor(dictionary=True)
    
    try:
        if request.method == 'POST':
            user_id = request.form.get('user_id')
            action = request.form.get('action')

            if action == 'deactivate':
                cursor.execute("UPDATE users SET status = 'inactive' WHERE user_id = %s AND role != 'voter'", (user_id,))
            elif action == 'reactivate':
                cursor.execute("UPDATE users SET status = 'active' WHERE user_id = %s AND role != 'voter'", (user_id,))
            elif action == 'switch_to_admin':
                cursor.execute("UPDATE users SET role = 'admin' WHERE user_id = %s AND role = 'scrutineer'", (user_id,))
            elif action == 'switch_to_scrutineer':
                cursor.execute("UPDATE users SET role = 'scrutineer' WHERE user_id = %s AND role = 'admin'", (user_id,))
            conn.commit()
            flash('Account updated successfully.', 'success')

        # Fetch all Admin and Scrutineer accounts
        cursor.execute("SELECT * FROM users WHERE role IN ('admin', 'scrutineer')")
        accounts = cursor.fetchall()

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'danger')
    finally:
        cursor.close()
        conn.close()

    return render_template('manage_accounts.html', accounts=accounts)


#Password change

@app.route('/admin/change_password', methods=['GET', 'POST'])
@admin_required  
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        # Get the current admin's details
        cursor, conn = getCursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (session['user_id'],))
        admin = cursor.fetchone()

        if not admin:
            flash('Admin not found.', 'danger')
            return redirect(url_for('admin_home'))

        # Verify current password
        current_password_hash = hashing.hash_value(current_password, PASSWORD_SALT)
        if current_password_hash != admin['password']:
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('change_password'))

        # Check if the new passwords match
        if new_password != confirm_new_password:
            flash('New passwords do not match.', 'danger')
            return redirect(url_for('change_password'))

        # Update the password in the database
        new_password_hash = hashing.hash_value(new_password, PASSWORD_SALT)
        cursor.execute("UPDATE users SET password = %s WHERE user_id = %s", (new_password_hash, admin['user_id']))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Password changed successfully!', 'success')
        return redirect(url_for('change_password'))

    return render_template('change_password.html')



#Competition create
@app.route('/admin/create_competition', methods=['GET', 'POST'])
@admin_required
def create_competition():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        status = 'Draft'  # Default status for a new competition

        # Handle the image upload
        image = request.files.get('image')
        image_filename = None
        if image and image.filename != '':
            image_filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Insert the competition into the database
        cursor, conn = getCursor()
        if cursor:
            try:
                cursor.execute("""
                    INSERT INTO competitions (name, description, start_date, end_date, status, image)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (name, description, start_date, end_date, status, image_filename))
                conn.commit()
                flash('Competition added successfully!', 'success')
                return redirect(url_for('view_competitions'))
            except Error as e:
                print(f"Error: {e}")  # Log the error
                flash(f'An error occurred while adding the competition: {str(e)}', 'danger')  # Show the actual error
            finally:
                cursor.close()
                conn.close()

    return render_template('create_competition.html')



#Delete competitions

@app.route('/admin/confirm_delete_competition/<int:competition_id>', methods=['GET', 'POST'])
@admin_required
def confirm_delete_competition(competition_id):
    cursor, conn = getCursor(dictionary=True)
    cursor.execute("SELECT * FROM competitions WHERE competition_id = %s", (competition_id,))
    competition = cursor.fetchone()

    if request.method == 'POST':
        if 'confirm' in request.form:
            try:
                # Delete all competitors associated with this competition
                cursor.execute("DELETE FROM competitors WHERE competition_id = %s", (competition_id,))
                
                # Delete the competition itself
                cursor.execute("DELETE FROM competitions WHERE competition_id = %s", (competition_id,))
                
                conn.commit()
                flash('Competition and all associated competitors deleted successfully!', 'success')
            except Exception as e:
                print(f"Error: {e}")
                flash(f"An error occurred while deleting the competition: {str(e)}", 'danger')
            finally:
                cursor.close()
                conn.close()

            return redirect(url_for('view_competitions'))

        elif 'cancel' in request.form:
            return redirect(url_for('view_competitions'))

    return render_template('confirm_delete_competition.html', competition=competition)

#view open competition

@app.route('/admin/view_open_competitions')
@admin_required
def view_open_competitions():
    cursor, conn = getCursor()
    open_competitions = []
    
    try:
        # Updated query to include the image column
        cursor.execute("SELECT competition_id, name, start_date, end_date, status, image FROM competitions WHERE status = 'Open'")
        for comp in cursor.fetchall():
            print(comp)  # Debugging: print each row to see its structure
            open_competitions.append({
                'competition_id': comp['competition_id'],
                'name': comp['name'],
                'start_date': comp['start_date'].strftime('%Y-%m-%d'),  # Convert to string
                'end_date': comp['end_date'].strftime('%Y-%m-%d'),  # Convert to string
                'status': comp['status'],
                'image': comp['image']  # Add the image field
            })
    except Exception as e:
        print(f"Error: {e}")
        flash(f"An error occurred while retrieving open competitions: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()
    
    return render_template('view_open_competitions.html', open_competitions=open_competitions)




#View competition details
@app.route('/admin/competition/<int:competition_id>', methods=['GET'])
@admin_required
def view_competition_details(competition_id):
    cursor, conn = getCursor(dictionary=True)
    if cursor:
        try:
            cursor.execute("SELECT * FROM competitions WHERE competition_id = %s", (competition_id,))
            competition = cursor.fetchone()

            cursor.execute("SELECT * FROM competitors WHERE competition_id = %s", (competition_id,))
            competitors = cursor.fetchall()

        finally:
            cursor.close()
            conn.close()

    if not competition:
        flash("Competition not found.", "danger")
        return redirect(url_for('view_open_competitions'))

    return render_template('competition_details.html', competition=competition, competitors=competitors)



#Update Status
@app.route('/admin/update_competition_status/<int:competition_id>', methods=['GET', 'POST'])
@admin_required
def update_competition_status(competition_id):
    cursor, conn = getCursor()
    if request.method == 'POST':
        new_status = request.form.get('status')
        if cursor:
            try:
                cursor.execute("""
                    UPDATE competitions 
                    SET status = %s 
                    WHERE competition_id = %s
                """, (new_status, competition_id))
                conn.commit()
                flash(f'Competition status updated to {new_status}!', 'success')
            except Error as e:
                flash(f'Error updating competition status: {str(e)}', 'danger')
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('view_open_competitions'))
    
    cursor.execute("SELECT * FROM competitions WHERE competition_id = %s", (competition_id,))
    competition = cursor.fetchone()
    return render_template('update_competition_status.html', competition=competition)


#submit_for_approval
@app.route('/admin/submit_for_approval/<int:competition_id>', methods=['POST'])
@admin_required
def submit_for_approval(competition_id):
    cursor, conn = getCursor()
    if cursor:
        try:
            cursor.execute("""
                UPDATE competitions 
                SET status = 'Submit for Approval' 
                WHERE competition_id = %s
            """, (competition_id,))
            conn.commit()
            flash('Competition submitted for approval!', 'success')
        except Error as e:
            print(f"Error: {e}")
            flash(f'An error occurred while submitting the competition: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('manage_competitions'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)






@app.route('/admin/manage-competitions')
@admin_required
def manage_competitions():
    # Logic for managing competitions
    return render_template('manage_competitions.html')

#View competitions
@app.route('/admin/competitions', methods=['GET'])
@admin_required
def view_competitions():
    cursor, conn = getCursor(dictionary=True)
    cursor.execute("SELECT * FROM competitions WHERE end_date > CURDATE()")
    competitions = cursor.fetchall()
    return render_template('view_competitions.html', competitions=competitions)


#Open competitions (Status: open)
@app.route('/admin/open_competition/<int:competition_id>', methods=['POST'])
@admin_required
def open_competition(competition_id):
    cursor, conn = getCursor()
    if cursor:
        try:
            cursor.execute("""
                UPDATE competitions 
                SET status = 'Open' 
                WHERE competition_id = %s
            """, (competition_id,))
            conn.commit()
            flash('Competition is now open!', 'success')
        except Error as e:
            flash(f'An error occurred while opening the competition: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('edit_competition', competition_id=competition_id))






#Edit competitions
@app.route('/admin/competitions/edit/<int:competition_id>', methods=['GET', 'POST'])
@admin_required
def edit_competition(competition_id):
    cursor, conn = getCursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        try:
            cursor.execute("""
                UPDATE competitions 
                SET name = %s, description = %s, start_date = %s, end_date = %s 
                WHERE competition_id = %s
            """, (name, description, start_date, end_date, competition_id))
            conn.commit()
            flash('Competition updated successfully!', 'success')
            return redirect(url_for('view_competitions'))
        except Error as e:
            print(f"Error: {e}")
            flash(f'An error occurred while updating the competition: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    
    cursor.execute("SELECT * FROM competitions WHERE competition_id = %s", (competition_id,))
    competition = cursor.fetchone()

    if not competition:
        flash('Competition not found.', 'danger')
        return redirect(url_for('view_competitions'))

    return render_template('edit_competition.html', competition=competition)

# Publish competitions
@app.route('/admin/competitions/publish/<int:competition_id>', methods=['POST'])
@admin_required
def publish_competition(competition_id):
    cursor, conn = getCursor()
    if cursor:
        try:
            cursor.execute("""
                UPDATE competitions 
                SET status = 'Published' 
                WHERE competition_id = %s
            """, (competition_id,))
            conn.commit()
            flash('Competition is now published!', 'success')
        except Error as e:
            flash(f'Error publishing competition: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('edit_competition', competition_id=competition_id))


#Manage competitions
@app.route('/admin/competition/<int:competition_id>/competitors')
@admin_required
def manage_competitors(competition_id):
    cursor, conn = getCursor(dictionary=True)
    cursor.execute("SELECT * FROM competitions WHERE competition_id=%s", (competition_id,))
    competition = cursor.fetchone()

    cursor.execute("SELECT * FROM competitors WHERE competition_id=%s", (competition_id,))
    competitors = cursor.fetchall()

    return render_template('manage_competitors.html', competition=competition, competitors=competitors)


#Delete
@app.route('/admin/competition/<int:competition_id>/delete', methods=['POST'])
@admin_required
def delete_competition(competition_id):
    cursor, conn = getCursor()
    cursor.execute("DELETE FROM competitions WHERE competition_id=%s", (competition_id,))
    conn.commit()

    flash('Competition and all related competitors deleted successfully.', 'success')
    return redirect(url_for('view_competitions'))






#Managing Competitors

#View_competitors
@app.route('/admin/competitions/<int:competition_id>/competitors')
@admin_required
def view_competitors(competition_id):
    # Pass dictionary=True to getCursor to get a DictCursor
    cursor, conn = getCursor(dictionary=True)
    try:
        # Fetch competitors for the given competition_id
        cursor.execute("SELECT * FROM competitors WHERE competition_id = %s", (competition_id,))
        competitors = cursor.fetchall()
        
        # Fetch the competition name
        cursor.execute("SELECT name FROM competitions WHERE competition_id = %s", (competition_id,))
        competition_name = cursor.fetchone()['name']
    except Exception as e:
        print(f"Error: {e}")
        flash(f"An error occurred while retrieving competitors: {str(e)}", "danger")
        competitors = []
        competition_name = ""
    finally:
        cursor.close()
        conn.close()

    # Render the template with the fetched data
    return render_template('view_competitors.html', competitors=competitors, competition_name=competition_name)






#Add competitor
@app.route('/admin/competitions/<int:competition_id>/competitors/add', methods=['GET', 'POST'])
@admin_required
def add_competitor(competition_id):
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        image = request.files.get('image')
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None  # Or handle the case when no image is uploaded
        
        cursor, conn = getCursor()
        try:
            cursor.execute("""
                INSERT INTO competitors (competition_id, name, description, image, created_by)
                VALUES (%s, %s, %s, %s, %s)
            """, (competition_id, name, description, filename, session['user_id']))
            conn.commit()
            flash('Competitor added successfully!', 'success')
            return redirect(url_for('view_competitors', competition_id=competition_id))  # Redirect to view competitors page
        except Error as e:
            print(f"Error: {e}")
            flash(f'An error occurred while adding the competitor: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('add_competitor.html', competition_id=competition_id)


#Edit competitor
@app.route('/admin/competitors/<int:competitor_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_competitor(competitor_id):
    cursor, conn = getCursor()
    try:
        cursor.execute("SELECT * FROM competitors WHERE competitor_id = %s", (competitor_id,))
        competitor = cursor.fetchone()

        if not competitor:
            flash("Competitor not found.", "danger")
            return redirect(url_for('admin_home'))  # Redirect to a relevant page

        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            image = request.files.get('image')

            # Update competitor details in the database
            cursor.execute("""
                UPDATE competitors SET name = %s, description = %s WHERE competitor_id = %s
            """, (name, description, competitor_id))

            if image and image.filename != '':
                if allowed_file(image.filename):
                    # Use secure_filename to sanitize the image filename
                    image_filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
                    
                    # Update the database with the new image filename
                    cursor.execute("""
                        UPDATE competitors SET image = %s WHERE competitor_id = %s
                    """, (image_filename, competitor_id))
                else:
                    flash("File type not allowed. Please upload a PNG, JPG, JPEG, or GIF file.", "danger")
                    return redirect(request.url)
            else:
                # If no new image is uploaded, keep the existing one
                cursor.execute("SELECT image FROM competitors WHERE competitor_id = %s", (competitor_id,))
                image_filename = cursor.fetchone()['image']

            conn.commit()
            flash("Competitor updated successfully!", "success")
            return redirect(url_for('view_competitors', competition_id=competitor['competition_id']))

    except Exception as e:
        print(f"Error: {e}")
        flash(f"An error occurred while updating competitor: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return render_template('edit_competitors.html', competitor=competitor)






#Delete Competitor
@app.route('/admin/competitors/<int:competitor_id>/delete', methods=['POST'])
@admin_required
def delete_competitor(competitor_id):
    cursor, conn = getCursor()
    try:
        # Get the competition_id before deleting the competitor
        cursor.execute("SELECT competition_id FROM competitors WHERE competitor_id = %s", (competitor_id,))
        competitor = cursor.fetchone()

        if not competitor:
            flash("Competitor not found.", "danger")
            return redirect(url_for('admin_home'))

        competition_id = competitor['competition_id']

        # Delete the competitor
        cursor.execute("DELETE FROM competitors WHERE competitor_id = %s", (competitor_id,))
        conn.commit()

        flash("Competitor deleted successfully!", "success")
        return redirect(url_for('view_competitors', competition_id=competition_id))
    
    except Exception as e:
        print(f"Error: {e}")
        flash(f"An error occurred while deleting competitor: {str(e)}", "danger")
        return redirect(url_for('admin_home'))
    
    finally:
        cursor.close()
        conn.close()



#scrutineer
#scrutineer decorated
def scrutineer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session or session['role'] != 'scrutineer':
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for('login'))  # Redirect to login or another appropriate page
        return f(*args, **kwargs)
    return decorated_function

#Define scrutineer home
@app.route('/scrutineer/home')
@scrutineer_required 
def scrutineer_home():
    return render_template('scrutineer_home.html')



#scrutineer approval function
@app.route('/scrutineer/approve_decline_competitions')
@scrutineer_required
def approve_decline_competitions():
    cursor, conn = getCursor()
    try:
        # Fetch competitions that are pending approval
        cursor.execute("SELECT * FROM competitions WHERE status = 'Pending'")
        competitions = cursor.fetchall()
    except Exception as e:
        flash(f"An error occurred while fetching competitions: {str(e)}", "danger")
        competitions = []
    finally:
        cursor.close()
        conn.close()

    return render_template('approve_decline_competitions.html', competitions=competitions)


@app.route('/scrutineer/competition/<int:competition_id>/approve', methods=['POST'])
@scrutineer_required
def approve_competition(competition_id):
    cursor, conn = getCursor()
    try:
        cursor.execute("UPDATE competitions SET status = 'Approved' WHERE competition_id = %s", (competition_id,))
        conn.commit()
        flash("Competition approved successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while approving the competition: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('approve_decline_competitions'))


@app.route('/scrutineer/competition/<int:competition_id>/decline', methods=['POST'])
@scrutineer_required
def decline_competition(competition_id):
    cursor, conn = getCursor()
    try:
        cursor.execute("UPDATE competitions SET status = 'Declined' WHERE competition_id = %s", (competition_id,))
        conn.commit()
        flash("Competition declined successfully!", "success")
    except Exception as e:
        flash(f"An error occurred while declining the competition: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('approve_decline_competitions'))




#track daily vote function

@app.route('/scrutineer/track_daily_votes')
@scrutineer_required
def track_daily_votes():
    cursor, conn = getCursor()
    try:
        # Fetch daily vote counts
        cursor.execute("""
            SELECT DATE(vote_time) as vote_date, COUNT(*) as vote_count
            FROM votes
            GROUP BY vote_date
            ORDER BY vote_date DESC
        """)
        daily_votes = cursor.fetchall()
    except Exception as e:
        flash(f"An error occurred while tracking daily votes: {str(e)}", "danger")
        daily_votes = []
    finally:
        cursor.close()
        conn.close()

    return render_template('track_daily_votes.html', daily_votes=daily_votes)

#Review votes
@app.route('/scrutineer/review_validate_votes', methods=['GET', 'POST'])
@scrutineer_required
def review_validate_votes():
    cursor, conn = getCursor(dictionary=True)
    votes = []  # Initialize votes to an empty list
    
    try:
        if request.method == 'POST':
            # Retrieve the vote ID and validation action (validate/invalidate)
            vote_id = request.form.get('vote_id')
            action = request.form.get('action')

            if action == 'validate':
                cursor.execute("UPDATE votes SET is_valid = 1 WHERE vote_id = %s", (vote_id,))
            elif action == 'invalidate':
                cursor.execute("UPDATE votes SET is_valid = 0 WHERE vote_id = %s", (vote_id,))
            
            conn.commit()
            flash(f'Vote {action}d successfully.', 'success')

        # Fetch all votes for the current competition
        cursor.execute("SELECT vote_id, voter_id, competitor_id, competition_id, vote_time, ip_address, is_valid FROM votes")
        votes = cursor.fetchall()

    except Exception as e:
        print(f"Error: {e}")
        flash(f"An error occurred while retrieving or updating votes: {str(e)}", "danger")
    finally:
        cursor.close()
        conn.close()

    return render_template('review_validate_votes.html', votes=votes)




@app.route('/scrutineer/finalize_competition_results')
@scrutineer_required
def finalize_competition_results():
    # need to be completed
    pass



#check ip
@app.route('/scrutineer/invalidate_votes_ip', methods=['GET', 'POST'])
@scrutineer_required
def invalidate_votes_ip():
    cursor, conn = getCursor()

    if request.method == 'POST':
        ip_address = request.form.get('ip_address')

        try:
            # Update the votes table to mark votes from the specified IP address as invalid
            cursor.execute("UPDATE votes SET is_valid = 0 WHERE ip_address = %s", (ip_address,))
            conn.commit()
            flash(f'Votes from IP address {ip_address} have been invalidated.', 'success')
        except Exception as e:
            print(f"Error: {e}")
            flash(f"An error occurred while invalidating votes: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template('invalidate_votes_ip.html')

    return redirect(url_for('home')
                    
if __name__ == '__main__':
    app.run(debug=True)
