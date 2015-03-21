from flask import Flask, request, send_from_directory, render_template
app = Flask(__name__)

@app.route('/')
def main():
    return send_from_directory('templates', 'index.html')

@app.route('/contact-msg', methods=['POST'])
def contact_msg():
    return render_template('contact-msg.html', contact_name=request.form['contact-name'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
