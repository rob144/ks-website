from flask import Flask, request, send_from_directory, render_template
import sqlite3 as lite

app = Flask(__name__)

def get_db_con():
    return lite.connect('contact.db')

con = get_db_con()
with con:
    con.cursor().execute(
        """CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_name TEXT,
            contact_email TEXT,
            contact_telephone TEXT,
            contact_message TEXT)"""
    )

@app.route('/')
def main():
    return send_from_directory('templates', 'index.html')

@app.route('/contact-msg', methods=['POST'])
def contact_msg():
    contact_name = request.form['contact-name']
    contact_email = request.form['contact-email']
    contact_telephone = request.form['contact-telephone']
    contact_message = request.form['contact-message']
    
    if(len(contact_message) > 3):
        con = get_db_con()
        with con:
            con.cursor().execute(
                """INSERT INTO messages 
                    (contact_name, contact_email, contact_telephone, contact_message)
                    VALUES (?, ?, ?, ?)""",
                    (contact_name, contact_email, contact_telephone, contact_message)
            )
        return render_template('contact-msg.html', contact_name=request.form['contact-name'])
    else:
        return render_template('index.html', error='Message was empty.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
