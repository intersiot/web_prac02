from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
# 내 로컬에서 실행할 때는 밑에거
# client = MongoClient('localhost', 27017)
# 배포할 때는 밑에거
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.dbsparta_plus_week1

from datetime import datetime

@app.route('/')
def home():
    return render_template('index.html')


# GET 요청 API 코드 : 리스팅
@app.route('/diary', methods=['GET'])
def show_diary():
    diaries = list(db.diary.find({}, {'_id': False}))

    return jsonify({'all_diary': diaries})


# POST 요청 API 코드 : 저장하기(포스팅)
@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    # 파일 저장하는 코드 (서버 쪽)
    file = request.files["file_give"]

    # 파일 확장자 명: 확장자 앞에 .으로 쪼개서 변수에 저장
    # 가장 마지막거 가져와라: -1
    extension = file.filename.split('.')[-1]

    # datetime 이용해서 파일명 변경 후 저장
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    time = today.strftime('%Y.%m.%d')

    filename = f'file-{mytime}'

    save_to = f'static/{filename}.{extension}'
    file.save(save_to)

    # db에 저장하는 코드
    doc = {
        'title': title_receive,
        'content': content_receive,
        'file': f'{filename}.{extension}',
        'time': time
    }

    db.diary.insert_one(doc)

    return jsonify({'msg': '저장 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
