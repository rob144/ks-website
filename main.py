from flask import Flask, request, url_for, redirect, send_from_directory, render_template
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

@app.route('/', methods=['GET','POST'])
def main():
    if request.method != 'POST':
        return render_template('index.html')
    else: 
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
            return redirect(url_for('contact', contact_name=contact_name))
        else:
            return render_template('index.html', error='Message was empty.')

@app.route('/contact', methods=['GET'])
def contact():
    if(request.referrer):
        return render_template('contact-msg.html',contact_name=request.args.get('contact_name'))
    else:
        return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
