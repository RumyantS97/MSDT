import cv2
import requests
import time
from flask import Flask, Response

import googlemaps

from const import GOOGLE_MAPS_API_KEY, INTERVAL, API_KEY, API_URL, JSON_DATA, LAST_PLATE
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)


app = Flask(__name__)
camera = cv2.VideoCapture(0)


license_plates = [entry["suspectVehicle"]["licensePlate"]
                  for entry in JSON_DATA]


def gen_frames():
    # Set initial last_time to current time minus INTERVAL
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

                # Send frame to Plate Recognizer API
                response = requests.post(
                    API_URL,
                    files=dict(upload=frame_bytes),
                    headers={'Authorization': f'Token {API_KEY}'}
                )
                plates = response.json()  # Parse response

                # Check if any plates are detected and process
                for result in plates.get('results', []):
                    # Update LAST_PLATE coordinates
                    LAST_PLATE['x'] = result['box']['xmin']
                    LAST_PLATE['y'] = result['box']['ymin']
                    LAST_PLATE['w'] = result['box']['xmax'] - \
                        result['box']['xmin']
                    LAST_PLATE['h'] = result['box']['ymax'] - \
                        result['box']['ymin']

                    # Print only the license plate number in uppercase
                    plate_number = result.get('plate', 'N/A').upper()
                    print("Detected Plate:", plate_number)

                    # Check if detected plate is in the list from JSON data
                    if plate_number in license_plates:
                        location = gmaps.geolocate()
                        # print(f"Alert: Match found for plate {plate_number}")
                        lat, lng = location['location']['lat'], location['location']['lng']
                        print(f"Alert: Match found for plate {
                              plate_number} at location {lat}, {lng}")
                        print("Alert: Sending alert to authorities...")
                        print("____")
                        print("Alert details:")
                        print("Alert ID:", JSON_DATA[0]["alertId"])
                        print("Alert Time:", JSON_DATA[0]["alertTime"])
                        print("Alert Location:", JSON_DATA[0]["alertLocation"])
                        print("Alert Type:", JSON_DATA[0]["alertType"])
                        print("Missing Person Name:",
                              JSON_DATA[0]["missingPerson"]["name"])
                        print("Missing Person Age:",
                              JSON_DATA[0]["missingPerson"]["age"])
                        print("Alert: Alert sent!")

            # Draw rectangle around the last detected license plate
            x, y, w, h = LAST_PLATE['x'], LAST_PLATE['y'], LAST_PLATE['w'], LAST_PLATE['h']
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)  # Green color

            # Convert frame to bytes for streaming
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
