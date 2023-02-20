from loader import dp, bot
from aiogram import types
from random import randint
#import game_logic

games_with = {}
games_set = {}

@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
	global games_with
	await message.answer('Этот бот для игры в конфеты\n'
						 'Доступны следующие команды:\n'
						 '/start \n'
						 '/help \n'
						 '/set_candy "new_count"\n'
						 '/new_game \n'
						 '/stop \n'
						 '/restart')
	print(f'Пользователь {message.from_user.first_name} присоеденился!')

	
@dp.message_handler(commands=['help'])
async def mes_start(message: types.Message):
	await message.answer('Этот бот для игры в конфеты.\n'
						 'Игроки поочередно берут конфеты со стола.\n'
						 'Можно взять от 1 до 28. Выигрывает ток кто взял последнюю конфету.\n'
						 '/start - присоедениться к боту\n'
						 '/help  - вывод текущей подсказки\n'
						 '/set_candy "new_count" - установить число конфет\n'
						 '/new_game - начать новую игру \n'
						 '/stop - остановить игру\n'
						 '/restart - начать игру заново')
	
@dp.message_handler(commands=['stop'])
async def mes_start(message: types.Message):
	global games_with
	# Если игра уже запущена, то на сообщаем об этом пользователю
	if message.from_user.id in games_with:
		del games_with[message.from_user.id]
		await message.answer('Игра остановлена. \n'
							'Для настройки кол-ва конфен используй /set_candy\n'
							'Для начала игры /new_game')
	else:
		await message.answer('Игра не запущена. \n')
		
@dp.message_handler(commands=['restart'])
async def mes_start(message: types.Message):
	global games_with
	# Если игра уже запущена, то на сообщаем об этом пользователю
	if message.from_user.id in games_with:
		await start_game(message)
	else:
		await message.answer('Игра не запущена. \n')
	


@dp.message_handler(commands=['new_game'])
async def mes_start(message: types.Message):
	global games_with
	# Если игра уже запущена, то на сообщаем об этом пользователю
	if message.from_user.id in games_with:
		await message.answer(f'Игра уже запущена!\n'
					   'Продолжай играть\n или воспользуйся следующими командами:\n'
					   '/stop - остановить игру\n'
					   '/restart - запустить игру с начала')
		return
	
	await start_game(message)
	#if message.from_user.id in games_set:
		#games_with[message.from_user.id] = games_set[message.from_user.id] # Если пользователь есть в списке пользователей с настройками, то берем конфеты из настроек
	#else:
		#games_with[message.from_user.id] = 150 # Конфеты по умолчанию
	#await message.answer(f'Привет {message.from_user.first_name}!\n'
						#f'Давай начнем игру. На столе {games_with[message.from_user.id]} конфет\n'
						#'Сколько конфет Ты хочешь взять?')

async def start_game(message: types.Message):
	global games_with
	global games_set
	if message.from_user.id in games_set:
		games_with[message.from_user.id] = games_set[message.from_user.id] # Если пользователь есть в списке пользователей с настройками, то берем конфеты из настроек
	else:
		games_with[message.from_user.id] = 150 # Конфеты по умолчанию
	await message.answer(f'Привет {message.from_user.first_name}!\n'
						f'Давай начнем игру. На столе {games_with[message.from_user.id]} конфет\n'
						'Сколько конфет Ты хочешь взять?')
	

@dp.message_handler(commands=['set_candy'])
async def mes_start(message: types.Message):
	global games_with
	global games_set
	if message.from_user.id in games_with:
		await message.answer('Нельзя менять количество конфет во время игры!')
		return

	new_count = message.text.split()
	if len(new_count) == 2 and new_count[1].isdigit():
		games_set[message.from_user.id] = int(new_count[1])
		await message.answer(f'Привет {message.from_user.first_name}!\n'
						f'На столе {games_set[message.from_user.id]} конфет.\n'
						'Для начала игры используй /new_game')
	else:
		await message.answer('Введите число конфет')

	
@dp.message_handler()
async def mes_start(message: types.Message):
	global games_with
	if message.from_user.id in games_with:
		total = games_with[message.from_user.id]
		if message.text.isdigit():
			bring_candy = int(message.text)
			#print(f'bring_candy = {bring_candy}')
			if bring_candy < 1 or bring_candy > 28:
				await bot.send_message(message.from_user.id, 'Введено не верное число')
				return
			elif bring_candy > total:
				await bot.send_message(message.from_user.id, 'На столе меньше конфет')
				return
			else:
				total -= bring_candy
				if check_win(total):
					await bot.send_message(message.from_user.id, f'Игорок {message.from_user.first_name} победил!')
					del games_with[message.from_user.id]
					return
			
			bot_candy = bot_bring(total)
			await bot.send_message(message.from_user.id, f'Бот Сергей взял {bot_candy} конфет')
			total -= bot_candy
			if check_win(total):
				await bot.send_message(message.from_user.id, f'Игорок бот Сергей победил!')
				del games_with[message.from_user.id]
				return
			else:
				games_with[message.from_user.id] = total
				
			await bot.send_message(message.from_user.id, 'На столе'
						  f' {games_with[message.from_user.id]} конфет\n'
						   'Сколько конфет Ты хочешь взять?')
		else:
			await bot.send_message(message.from_user.id, 'Неизвестная команда')
	else:
		await bot.send_message(message.from_user.id, 'Начнем новую игру?\n/new_game')


def check_win(candy):
	if candy == 0:
		return True
	return False

def bot_bring(candy):
    max_turn = 28
    if max_turn > candy:
        max_turn = candy
    bot_candy = candy - (candy // (max_turn + 1) * (max_turn + 1))
    if bot_candy == 0:
        bot_candy = randint(1, max_turn)
    return bot_candy
