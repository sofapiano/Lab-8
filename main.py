import cv2


def process_image():
    image_path = 'images/variant-10.jpg'

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('haha car goes vroom vroom', thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return thresh


def track_marker():
    cap = cv2.VideoCapture(0)
    
    # Проверка успешности открытия камеры
    if not cap.isOpened():
        print("Ошибка при открытии камеры")
        return
    
    frame_size = (640, 480)
    center_box_size = 150
    frame_center_x, frame_center_y = frame_size[0] // 2, frame_size[1] // 2

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Не удалось захватить кадр с камеры")
            break

        frame = cv2.resize(frame, frame_size, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            center_x, center_y = x + w // 2, y + h // 2
            if abs(center_x - frame_center_x) < center_box_size // 2 and abs(center_y - frame_center_y) < center_box_size // 2:
                frame = cv2.flip(frame, 1)

        cv2.imshow('vidosik', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    process_image()
    track_marker()
