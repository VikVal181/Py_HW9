from loader import dp, bot
from aiogram import types
from random import randint
#import game_logic

games_with = {}

@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
	await message.answer('Этот бот для игры в конфеты\n'
						 'Доступны следующие команды:\n'
						 '/start \n'
						 '/help \n'
						 '/new_game \n'
						 '/set_candy')
	
@dp.message_handler(commands=['help'])
async def mes_start(message: types.Message):
	await message.answer('Этот бот для игры в конфеты.\n'
						 'Игроки поочередно берут конфеты со стола.\n'
						 'Можно взять от 1 до 28. Выигрывает ток кто взял последнюю конфету.\n'
						 'Команда (/set_candy число) устанавливает \nначальное кол-во конфет и запускает игру.\n/new_game запускает новую игру с конфетами по умолчанию')
	
@dp.message_handler(commands=['new_game'])
async def mes_start(message: types.Message):
	global games_with
	games_with[message.from_user.id] = 150
	await message.answer(f'Привет {message.from_user.first_name}!\n'
						f'Давай начнем игру. На столе {games_with[message.from_user.id]} конфет\n'
						'Сколько конфет Ты хочешь взять?')

@dp.message_handler(commands=['set_candy'])
async def mes_start(message: types.Message):
	global games_with
	new_count = message.text.split()[1]
	if new_count.isdigit() or new_count == '':
		games_with[message.from_user.id] = int(new_count)
		await message.answer(f'Привет {message.from_user.first_name}!\n'
						f'Давай начнем игру. На столе {games_with[message.from_user.id]} конфет\n'
						'Сколько конфет Ты хочешь взять?')
	else:
		await message.answer('Введено не число')

	
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
