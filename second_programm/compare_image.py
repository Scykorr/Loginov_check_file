from PIL import Image


img1 = Image.open('1.png') # Открываем первое изображение
im1 = img1.load() # Загружаем первое изображение для доступа к пикселям

img2 = Image.open('2.png') # Открываем второе изображение
im2 = img2.load() # Загружаем второе изображение для доступа к пикселям

i = 0 # Счетчик пикселей, которые не совпадают

if (img1.size == img2.size): # Проверяем, что размер изображений совпадают
  x1,y1 = img1.size # Через атрибут size получаем кортеж с двумя элементами (размер изображения по x и y)

  # Проходимся последовательно по каждому пикселю картинок
  for x in range(0,x1):
    for y in range(0,y1):
      if im1[x,y] != im2[x,y]: # Если пиксель первой картинки по координатах [x,y] не совпадает
        # с пикселем второй картинки по координатах [x,y], тогда:
        i = i + 1 # Увеличиваем счетчик на 1
        print(f'Координаты: x={x}, y={y} Изображение 1={im1[x,y]} - Изображение 2={im2[x,y]}')
  print(f"Количество разных пикселей: {i}")
else:
  print("Размер изображений не совпадают!")