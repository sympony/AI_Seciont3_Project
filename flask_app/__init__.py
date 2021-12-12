from flask import Flask, render_template, request
# from flask_app.routes import user_routes
import joblib
import math

app = Flask(__name__)
model = joblib.load('bike_predict.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # 모델 value 받아오기
    Month = request.form['Month']
    Day = request.form['Day']
    Hour = request.form['Hour']
    Temperature = request.form['Temperature']
    Humidity = request.form['Humidity']
    # 이슬점(dewpoint)
    b = 17.62
    c = 243.12
    gamma = (float(b) * float(Temperature) /(float(c) + float(Temperature))) + math.log(float(Humidity) / 100.0)
    dewpoint = (c * gamma) / (b - gamma)
    WIndspeed = request.form['WIndspeed']
    Visibility = request.form['Visibility']
    Visibility = float(Visibility) * 20 
    weather = request.form['weather']
    Holiday = request.form['Holiday']

    list = [[int(Hour), float(Temperature), float(Humidity), float(WIndspeed), int(Visibility), float(dewpoint), 0, 0, int(weather), float(Month), int(Day)]]
    
    # 휴일 유무에 따른 값을 재 입력
    if (Holiday == '1'):
        list[0][6] = 1
    elif (Holiday == '0'):
        list[0][7] = 1
    else:
        pass
    
    predict = int(model.predict(list))

    return render_template('predict.html', predict = predict)
# f'요청 하신 날의 자전거 대여 수는 {predict}대 입니다'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)