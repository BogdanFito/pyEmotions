import cv2
import gdown
import numpy as np
from keras.models import load_model
from PIL import Image

# Ссылка на модель
model_url = "https://drive.google.com/uc?id=19d34gXL5gwD6gLPFDRyLZguZqyAgVhzz"

# Путь для сохранения модели
model_path = "saved_models/trained_model_res_net.h5"

# Загрузка модели с использованием ссылки из Google Drive
gdown.download(model_url, model_path, quiet=False)

# Загрузка модели из сохраненного файла
model = load_model(model_path)

# Создание словаря с соответствием индексов классам
class_names = ['angry', 'happy', 'neutral', 'sad', 'surprise']

# Загрузка каскадного классификатора лиц Haar
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Подключение камеры
cap = cv2.VideoCapture(0)

while True:
    # Захват кадра с камеры
    ret, frame = cap.read()

    # Преобразование кадра в черно-белый вид
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Обнаружение лиц в кадре
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Обрезка кадра до области с лицом
        face_image = frame[y:y+h, x:x+w]

        # Предобработка лица
        img = Image.fromarray(face_image).convert('RGB')
        img = img.resize((48, 48))
        x = np.array(img)
        x = np.expand_dims(x, axis=0)
        x = x / 255.0  # Нормализация значений пикселей

        # Классификация лица с использованием модели
        predictions = model.predict(x)
        class_index = np.argmax(predictions, axis=1)[0]
        emotion = class_names[class_index]

        # Отрисовка прямоугольника вокруг лица
        #cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 0), 2)

        # Вывод эмоции на кадре
        cv2.putText(frame, emotion, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


    # Отображение кадра
    cv2.imshow('Emotion Detection', frame)

    # Выход из цикла по нажатию клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
