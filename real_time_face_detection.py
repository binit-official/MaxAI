import cv2
import face_recognition

def main():
    # Open the webcam
    video_capture = cv2.VideoCapture(0)

    # Load known faces and their encodings
    known_face_encodings = []
    known_face_names = []

    # Example: Load a sample picture and learn how to recognize it
    image_of_person = face_recognition.load_image_file("binit.jpg")
    person_face_encoding = face_recognition.face_encodings(image_of_person)[0]

    # Add the face encoding and name to the lists
    known_face_encodings.append(person_face_encoding)
    known_face_names.append("Binit")

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Convert the image from BGR to RGB
        rgb_frame = frame[:, :, ::-1]

        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop over each face found in the current frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any of the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Display the name of the person
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
