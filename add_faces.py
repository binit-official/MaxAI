import face_recognition
import pickle
import cv2
import os


def add_face(name, image_path):
    """Encodes the face from the image and adds it to the list of known faces."""
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if len(face_encodings) == 0:
        print(f"No face found in the image: {image_path}")
        return None

    return face_encodings[0]


def save_face_data(known_face_encodings, known_face_names):
    """Saves the known face encodings and names to a file."""
    with open("known_faces.pkl", "wb") as f:
        pickle.dump((known_face_encodings, known_face_names), f)
    print("Face data saved to known_faces.pkl")


def load_face_data():
    """Loads known face encodings and names from a file."""
    if os.path.exists("known_faces.pkl"):
        with open("known_faces.pkl", "rb") as f:
            return pickle.load(f)
    else:
        return [], []


def main():
    known_face_encodings, known_face_names = load_face_data()

    while True:
        name = input("Enter the name of the person (or 'quit' to exit): ")
        if name.lower() == 'quit':
            break
        image_path = input("Enter the path to the image file: ")
        face_encoding = add_face(name, image_path)

        if face_encoding is not None:
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)
            save_face_data(known_face_encodings, known_face_names)


if __name__ == "__main__":
    main()
