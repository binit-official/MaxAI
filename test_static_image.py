import face_recognition

# Replace with the path to your image
image_path = "binit.jpg"
image = face_recognition.load_image_file(image_path)
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

print(f"Face locations: {face_locations}")
print(f"Face encodings: {face_encodings}")
