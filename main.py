from flask import Flask, render_template, request, Response
import cv2

import database as db

app = Flask(__name__)

camera = cv2.VideoCapture(1)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    cur = db.database.cursor()
    cur.execute("SELECT * FROM users")  
    result = cur.fetchall()

    #Convert objects to dictionary
    data = []
    columnNames = [column[0] for column in cur.description]
    for record in result:
        data.append(dict(zip(columnNames, record)))

    cur.close()

    return render_template('index.html', data=data)

@app.route('/employees')
def employees():
    return render_template('employees.html',)


@app.route('/reports')
def reports():
    return render_template('reports.html',)


@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=4000)