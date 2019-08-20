import telebot;
import os
bot = telebot.TeleBot('TOKEN');

def gets(arr):
	res = ''
	for i in arr:
		res += i
		res += ' ' 
	return res

def get_list():
	file = open('users.txt', 'r')
	x = file.readlines()
	file.close()
	return x

def puts(txt, users):
	file = open('users.txt', 'a')
	if users:
		file.write(f'\n@{txt}')
	else:
		file.write(f'@{txt}')
	file.close()

def push(txt):
	file = open('users.txt', 'a')
	file.write(f'\n{txt}')
	file.close()

def refresh(x):
	with open("users.txt", "r+") as f:
		d = f.readlines()
		f.seek(0)
		for i in d:
			if i != x:
				f.write(i)
		f.truncate()

def remove_empty_lines(filename):
    if not os.path.isfile(filename):
        print("{} does not exist ".format(filename))
        return
    with open(filename) as filehandle:
        lines = filehandle.readlines()

    with open(filename, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)  

def filterr():
	file = open('users.txt', 'r')
	uss = file.readlines()
	tmp = []

	for i in uss:
		if i not in tmp and (i+'\n' not in tmp):
			tmp.append(i)
	print(tmp)

	uss = tmp

	file.close()

	file = open('users.txt', 'w')
	file.write('')
	file.close()

	for i in uss:
		push(i)

	remove_empty_lines('users.txt')


users = get_list()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if message.text == "/call@callmafbot" or message.text == '/call':
		filterr()
		users = get_list()
		if users:
			bot.send_message(message.chat.id, f'Кількість зареєстрованих: {len(users)}, зву всіх)')
			lastpos = 0
			pos = 5
			while (pos < len(users)):
				mess = gets(users[lastpos:pos])
				bot.send_message(message.chat.id, mess)
				lastpos += 5
				pos += 5

			if len(users) % 5 != 0:
				bot.send_message(message.chat.id, gets(users[lastpos:len(users)]))
			else:
				bot.send_message(message.chat.id, gets(users[lastpos:lastpos + 5]))


		else:
			bot.send_message(message.chat.id, 'Ніхто не підписався на розсилку!')

	elif message.text == '/reg@callmafbot' or message.text == '/reg':
		if message.from_user.username == None:
			bot.send_message(message.chat.id, 'У вас немає юзернейму! Реєстрація неможлива!')
		else:
			users = get_list()
			if f'@{message.from_user.username}' not in users:
				puts(message.from_user.username, users)
				bot.send_message(message.chat.id, f'Користувач @{message.from_user.username} успішно підписаний на розсилку!')
			else:
				bot.send_message(message.chat.id, f'@{message.from_user.username} уже підписаний')

	elif message.text == '/kick@callmafbot' or message.text == '/kick':
		users = get_list()
		if f'@{message.from_user.username}' not in users:
			bot.send_message(message.chat.id, f'Користувач @{message.from_user.username} ще не підписаний!')
		else:
			refresh(f'@{message.from_user.username}')
			bot.send_message(message.chat.id, f'Користувач @{message.from_user.username} відмінив підписку!')

	elif message.text == '/help@callmafbot' or message.text == '/help':
		bot.send_message(message.chat.id, '''Клікни "/reg", щоб підписатись на розсилку, або ж "/kick", щоб відмінити її''')
		bot.send_message(message.chat.id, '''Щоб позвати усіх підписаних на розсилку кляцни /call''')

	elif message.text == '/love@callmafbot' or message.text == '/love':
		bot.send_message(message.chat.id, '❤️')

bot.polling(none_stop=True, interval=0)
