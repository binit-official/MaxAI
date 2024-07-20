import cv2
import face_recognition
from fer import FER


def recognize_face(known_face_encodings, known_face_names):
    video_capture = cv2.VideoCapture(0)
    face_recognition_model = FER()

    while True:
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        # Emotion detection
        emotion_results = face_recognition_model.detect_emotions(frame)
        if emotion_results:
            emotions = emotion_results[0]['emotions']
            for (emotion, score) in emotions.items():
                cv2.putText(frame, f"{emotion}: {score:.2f}",
                            (10, 30 + 20 * list(emotions.keys()).index(emotion)),
                            cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


# Example usage:
image_of_person_1 = face_recognition.load_image_file("binit.jpg")
person_1_face_encoding = face_recognition.face_encodings(image_of_person_1)[0]

image_of_person_2 = face_recognition.load_image_file("path_to_image_of_person_2.jpg")
person_2_face_encoding = face_recognition.face_encodings(image_of_person_2)[0]

known_face_encodings = [
    person_1_face_encoding,
    person_2_face_encoding
]

known_face_names = [
    "Binit",
    "Person 2"
]

recognize_face(known_face_encodings, known_face_names)
