from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from database import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for flash messages

# Initialize database when app starts
init_db()


def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect('contacts.db')
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn


@app.route('/')
def index():
    """Render the contact form."""
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission."""
    # Get form data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Basic validation
    if not name or not email or not message:
        flash('Name, Email, and Message are required fields!', 'error')
        return redirect(url_for('index'))

    # Insert data into database
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email, phone, subject, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, phone, subject, message))
        conn.commit()
        conn.close()
        flash('Your message has been submitted successfully!', 'success')
        return redirect(url_for('success'))
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/success')
def success():
    """Render the success page."""
    return render_template('success.html')


@app.route('/contacts')
def contacts():
    """Display all submitted contacts (Admin view)."""
    conn = get_db_connection()
    all_contacts = conn.execute(
        'SELECT * FROM contacts ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return render_template('contacts.html', contacts=all_contacts)


@app.route('/delete/<int:id>')
def delete(id):
    """Delete a contact entry."""
    conn = get_db_connection()
    conn.execute('DELETE FROM contacts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Contact deleted successfully!', 'success')
    return redirect(url_for('contacts'))


if __name__ == '__main__':
    app.run(debug=True)