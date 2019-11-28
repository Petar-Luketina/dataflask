from flask import Flask, render_template, request, jsonify, send_file
import requests
import json
from driver_funct import *
from storage_funct import *
app = Flask(__name__)

# cd C:\Users\pluketina\Documents\Petar\dataflask
cache = {}

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
    path = './static/chromedriver.exe'
    if request.method == 'POST':
        print(1)
        data = request.get_data().decode('utf-8')
        data = json.loads(data)
        print(data)
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
            temp_image = start_crawling(cache['driver'])
            response = send_file(temp_image, as_attachment=True, attachment_filename='wordcloud.jpg')
            return response
    else:
        return render_template('webcrawler.html')


if __name__ == '__main__':
    app.run(debug=True)
