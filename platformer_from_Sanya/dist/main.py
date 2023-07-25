import pygame

# ширина и высота окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# фон
bg = pygame.image.load('background.jpg')


# Класс игрок
class Player(pygame.sprite.Sprite):
	# Изначально игрок смотрит вправо, поэтому эта переменная True
	right = True

	# Методы
	def __init__(self):
		# Стандартный конструктор класса
		# Нужно ещё конструктор родительского класса
		super().__init__()

		# изображение игрока
		self.image = pygame.image.load('player.png')

		self.rect = self.image.get_rect()

		# скорость игрока
		self.change_x = 0
		self.change_y = 0
	def calc_grav(self):
		# Здесь мы вычисляем как быстро игрок будет падать на землю под действием гравитации
		if self.change_y == 0:
			self.change_y = 1
		else:
			self.change_y += .95

	def update(self):
		# передвигаем игрока
		# устанавливаем   гравитацию
		self.calc_grav()

		# Передвигаем на право/лево
		self.rect.x += self.change_x

		# Следим ударяем ли мы объект
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		# Перебираем все возможые объекты, с которыми могли  столкнуться
		for block in block_hit_list:
			# Если мы идем направо, устанавливает нашу правую сторону на левой стороне предмета, которого мы ударили
			if self.change_x > 0:
				self.rect.right = block.rect.left
			elif self.change_x < 0:
				# если мы движемся влево, то делаем наоборот
				self.rect.left = block.rect.right

		# Передвигаемся вверх/вниз
		self.rect.y += self.change_y

		# То же самое, вот только уже для вверх/вниз
		block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		for block in block_hit_list:
			# Устанавливаем нашу позицию на основе верхней / нижней части объекта, на который мы попали
			if self.change_y > 0:
				self.rect.bottom = block.rect.top
			elif self.change_y < 0:
				self.rect.top = block.rect.bottom

			# Останавливаем  движение
			self.change_y = 0



		# Есл на земле, то ставим позицию Y как 0
		if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
			self.change_y = 0
			self.rect.y = SCREEN_HEIGHT - self.rect.height

	def jump(self):
		# Обработка прыжка. Нам нужно проверять контактируем ли мы с чем-либо
		
		self.rect.y += 10
		platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
		self.rect.y -= 10

		# Если все в порядке, прыгаем вверх
		if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
			self.change_y = -16

	# Передвижение игрока
	def go_left(self):
		self.change_x = -9 # Двигаем игрока по Х
		if(self.right): # Проверяем куда он смотрит и переворачиваем его
			self.flip()
			self.right = False

	def go_right(self):
		# то же самое, но вправо
		self.change_x = 9
		if (not self.right):
			self.flip()
			self.right = True


	def stop(self):
		# вызываем этот метод, когда не нажимаем на клавиши
		self.change_x = 0

	def flip(self):
		# переворот игрока
		self.image = pygame.transform.flip(self.image, True, False)


# Класс платформы
class Platform(pygame.sprite.Sprite):
	def __init__(self, width, height):
		# Конструктор 
		super().__init__()
		# фото платформы
		self.image = pygame.image.load('platforma.jpg')

		self.rect = self.image.get_rect()


# Класс для расстановки платформ
class Level(object):
	def __init__(self, player):
		# группа спрайтов 
		self.platform_list = pygame.sprite.Group()
		# Ссылка на основного игрока
		self.player = player

	# обновление экрана
	def update(self):
		self.platform_list.update()

	# Метод  рисования объектов
	def draw(self, screen):
		# Рисуем  фон
		screen.blit(bg, (0, 0))

		# Рисуем все платформы
		self.platform_list.draw(screen)


# Класс описывает где будут находится все платформы на определенном уровне игры
class Level_01(Level):
	def __init__(self, player):
		# Вызываем конструктор
		Level.__init__(self, player)

		# данные про платформы.
		# ширина, высота, x и y позиция
		level = [
			[210, 32, 500, 500],
			[210, 32, 200, 400],
			[210, 32, 600, 365],
		]

		# Перебираем  и добавляем каждую платформу в группу спрайтов
		for platform in level:
			block = Platform(platform[0], platform[1])
			block.rect.x = platform[2]
			block.rect.y = platform[3]
			block.player = self.player
			self.platform_list.add(block)


# Основная функция прогарммы
def main():
	# Инициализация
	pygame.init()

	# Установка высоты и ширины
	size = [SCREEN_WIDTH, SCREEN_HEIGHT]
	screen = pygame.display.set_mode(size)

	# Название 
	pygame.display.set_caption("Платформер фром саня")

	# Создаем игрока
	player = Player()

	# Создаем все уровни
	level_list = []
	level_list.append(Level_01(player))

	# Устанавливаем текущий уровень
	current_level_no = 0
	current_level = level_list[current_level_no]

	active_sprite_list = pygame.sprite.Group()
	player.level = current_level

	player.rect.x = 340
	player.rect.y = SCREEN_HEIGHT - player.rect.height
	active_sprite_list.add(player)

	# Цикл будет пока  не нажматьт кнопку закрытия
	done = False

	# Используется для управления скоростью обновления экрана
	clock = pygame.time.Clock()

	# Основной цикл программы
	while not done:
		# Отслеживание действий
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Если закрыл программу, то останавливаем цикл
				done = True

			# нажатие на кнопки
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					player.go_left()
				if event.key == pygame.K_d:
					player.go_right()
				if event.key == pygame.K_w:
					player.jump()

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_a and player.change_x < 0:
					player.stop()
				if event.key == pygame.K_d and player.change_x > 0:
					player.stop()

		# Обновляем игрока
		active_sprite_list.update()

		# Обновляем объекты на сцене
		current_level.update()

		# Если игрок приблизится к правой стороне, его не двигаем
		if player.rect.right > SCREEN_WIDTH:
			player.rect.right = SCREEN_WIDTH

		# Если игрок приблизится к левой стороне, его не двигаем
		if player.rect.left < 0:
			player.rect.left = 0

		# Рисуем объекты
		current_level.draw(screen)
		active_sprite_list.draw(screen)

		# Устанавливаем количество fps
		clock.tick(60)

		# Обновляем экран 
		pygame.display.flip()

	#  закртытие программы
	pygame.quit()

main()