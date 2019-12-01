from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import json
from driver_funct import *
app = Flask(__name__)

# cd C:\Users\pluketina\Documents\Petar\dataflask
cache = {} # stores the webdriver
debug = True

@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'key': 'value'
    }
    if request.method == 'GET':
        return render_template('index.html', context=context)
    elif request.method == 'POST':
        data = request.get_data().decode('utf-8')
        data = json.loads(data) # JSON string to dictionary

        if data == 'something':
            return jsonify({'returned': 'A returned message for a post'})
        else:
            return jsonify({'key': 'value'})


@app.route('/webcrawler', methods=['GET', 'POST'])
def webcrawler():
    path = './static/drivers/chromedriver.exe'
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        data = json.loads(data)
        if data['message'] == 'open':
            driver = webdriver.Chrome(executable_path=path)
            cache['driver'] = driver
            driver.get(url = 'https://www.linkedin.com/')
            return jsonify({'message': 'success'})
        elif data['message'] == 'type':
            type_credentials(cache['driver'], data)
            return jsonify({'message': 'success'})
        elif data['message'] == 'visit':
            driver = cache['driver']
            driver.get(url=data['url'])
            return jsonify({'message': 'success'})
        elif data['message'] == 'start':
            path, file = start_crawling(cache['driver'])
            return send_from_directory(directory=path, as_attachment=True, filename=file)
    else:
        return render_template('webcrawler.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        print(data['name'])
        print(data['email'])
        print(data['subject'])
        print(data['message'])
        context = {
            'message': 'Your message was sent. Talk to you soon!'
        }
        return render_template('contact.html', context=context)
    else:
        return render_template('contact.html', context=None)



if __name__ == '__main__':
    app.run(debug=debug)
