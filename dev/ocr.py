# import cv2
# import pytesseract
# from PIL import Image, ImageEnhance, ImageFilter

# # Открытие изображения
# image_path = 'C:\\Users\\decco\\OneDrive\\Изображения\\Saved Pictures\\загруженное.png'
# image = Image.open(image_path)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# # Преобразование в черно-белое изображение
# image = image.convert('L')

# # Увеличение контраста
# enhancer = ImageEnhance.Contrast(image)
# image = enhancer.enhance(2)

# # Применение фильтра для уменьшения шума
# image = image.filter(ImageFilter.MedianFilter(size=3))

# # Сохранение временного файла для обработки
# temp_image_path = 'temp_image.png'
# image.save(temp_image_path)

# # Использование OpenCV для дальнейшей обработки (бинаризация)
# image_cv = cv2.imread(temp_image_path)
# gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

# # Использование адаптивной бинаризации с разным блоком и C-значением
# binary_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)

# # Применение морфологических операций для удаления шума и улучшения качества изображения
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
# binary_image = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

# # Увеличение резкости изображения
# binary_image = cv2.GaussianBlur(binary_image, (1, 1), 0)

# # Сохранение промежуточного изображения для проверки
# processed_image_path = 'processed_image.png'
# cv2.imwrite(processed_image_path, binary_image)

# # Использование Tesseract для извлечения текста
# custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
# text = pytesseract.image_to_string(binary_image, config=custom_config)

# print("Распознанные цифры:", text)
import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# Откройте изображение
image_path = 'C:\\Users\\decco\\OneDrive\\Изображения\\Saved Pictures\\загруженное.png'
image = Image.open(image_path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Преобразование в черно-белое изображение
image = image.convert('L')

# Увеличение контраста
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(1000)

# Применение фильтра для улучшения качества изображения
# image = image.filter(ImageFilter.MedianFilter())

# Сохранение временного файла для обработки
temp_image_path = 'temp_image.png'
image.save(temp_image_path)

# Используйте OpenCV для дальнейшей обработки (бинаризация)
image_cv = cv2.imread(temp_image_path)
gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
_, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Сохранение промежуточного изображения для проверки
processed_image_path = 'processed_image.png'
cv2.imwrite(processed_image_path, binary_image)

# Используйте Tesseract для извлечения текста
text = pytesseract.image_to_string(binary_image, config='outputbase digits')

print("Распознанные цифры:", text)