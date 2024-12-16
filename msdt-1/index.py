import time

import cv2
import requests
import googlemaps
from flask import Flask, Response

from const import (
    GOOGLE_MAPS_API_KEY,
    INTERVAL, API_KEY,
    API_URL, JSON_DATA,
    LAST_PLATE)


gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


app = Flask(__name__)
camera = cv2.VideoCapture(0)


license_plates = [entry["suspectVehicle"]["licensePlate"]
                  for entry in JSON_DATA]


def gen_frames() -> bytes:
    """
    generate video frames with license plate detection
    """
    last_time = time.time() - INTERVAL
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            current_time = time.time()
            if current_time - last_time > INTERVAL:
                last_time = current_time

                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                response = requests.post(
                    API_URL,
                    files=dict(upload=frame_bytes),
                    headers={'Authorization': f'Token {API_KEY}'}
                )
                plates = response.json()
                for result in plates.get('results', []):
                    LAST_PLATE['x'] = result['box']['xmin']
                    LAST_PLATE['y'] = result['box']['ymin']
                    LAST_PLATE['w'] = result['box']['xmax'] - \
                        result['box']['xmin']
                    LAST_PLATE['h'] = result['box']['ymax'] - \
                        result['box']['ymin']

                    plate_number = result.get('plate', 'N/A').upper()
                    print(f"Detected Plate: {plate_number}")

                    if plate_number in license_plates:
                        location = gmaps.geolocate()
                        lat, lng = location['location'][
                            'lat'
                            ], location['location']['lng']
                        print(f"Alert: Match found for plate {
                              plate_number} at location {lat}, {lng}")
                        print("Alert: Sending alert to authorities...")
                        print("____")
                        print("Alert details:")
                        print(f"Alert ID: {JSON_DATA[0]["alertId"]}")
                        print(f"Alert Time: {JSON_DATA[0]["alertTime"]}")
                        print(f"Alert Location:
                              {JSON_DATA[0]["alertLocation"]}")
                        print(f"Alert Type:", JSON_DATA[0]["alertType"])
                        print(f"Missing Person Name:
                              {JSON_DATA[0]["missingPerson"]["name"]}")
                        print(f"Missing Person Age:
                              {JSON_DATA[0]["missingPerson"]["age"]}")
                        print("Alert: Alert sent!")

            x = LAST_PLATE['x']
            y = LAST_PLATE['y']
            w = LAST_PLATE['w']
            h = LAST_PLATE['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' 
                   + frame_bytes + b'\r\n')


@app.route('/')
def video_feed() -> Response:
    """
    flask route to provide a video stream
    """
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)