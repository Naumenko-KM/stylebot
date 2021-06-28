
import asyncio
from config import TOKEN
from PIL import Image
from aiogram import Bot, Dispatcher, executor, filters, types
import os
from pprint import pprint
import style_transfer_bot
import time


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
content = False
cur_dir = os.getcwd()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет, ты можешь загрузить фото и выбрать один из предоставленных стилей или загрузить дополнительное фото, стиль которого надо перенести. \n /help")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Загрузи фото и выбери одну из команд: \n /ukiyoe \n /vangogh \n /monet \n /cezanne \n Или загрузи второе фото со своим стилем и нажми: \n /mystyle \n Примеры стилей: /styles")


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
	global content
	if content == False:
		await message["photo"][-1].download(cur_dir + r"\images\content.jpg")
		await bot.send_message(message.from_user.id, 'Контент изображение загружено!')
		content = True
	else:
		await message["photo"][-1].download(cur_dir + r"\images\style.jpg")
		await bot.send_message(message.from_user.id, 'Изображение со стилем загружено! \n /mystyle')
		content = False


@dp.message_handler(commands=['mystyle'])
async def return_img(message: types.Message):
	global content
	content = False
	await bot.send_message(message.from_user.id, 'Придется подождать несколько минут...')
	style_img = style_transfer_bot.image_loader(cur_dir + r"\images\style.jpg")# as well as here
	content_img = style_transfer_bot.image_loader(cur_dir + r"\images\content.jpg")#измените путь на тот который у вас.

	style_transfer = style_transfer_bot.StyleTransfer()
	output_img = style_transfer.run_style_transfer(content_img, style_img)
	style_transfer_bot.imsave(output_img, name="images/output.png")
	await bot.send_photo(message.from_user.id, photo=open("images/output.png", "rb"))


@dp.message_handler(commands=['ukiyoe', 'vangogh', 'monet', 'cezanne'])
async def return_img(message: types.Message):
	global content
	content = False
	style = msg.text[1:]
	await bot.send_message(message.from_user.id, 'Придется немного подождать...')
	os.chdir('cyclegan')
	os.system("python test.py --dataroot ../images --name style_"+style+"_pretrained --model test --no_dropout")
	os.chdir('..')
	await bot.send_photo(message.from_user.id, photo=open(r"cyclegan\results\style_"+style+r"_pretrained\test_latest\images\content_fake.png", "rb"), caption=style)

@dp.message_handler(commands=['styles'])
async def return_img(message: types.Message):
	media = types.MediaGroup()
	media.attach_photo(types.InputFile('StyleImages/1.jpg'))
	media.attach_photo(types.InputFile('StyleImages/2.jpg'))
	media.attach_photo(types.InputFile('StyleImages/3.jpg'))
	media.attach_photo(types.InputFile('StyleImages/4.jpg'))
	await bot.send_media_group(message.from_user.id, media=media)
	

@dp.message_handler()
async def echo_message(msg: types.Message):
	try:
		x = int(msg.text)/10
		await bot.send_message(msg.from_user.id, x)
	except:
		await bot.send_message(msg.from_user.id, msg.text)
	
	

if __name__ == '__main__':
	executor.start_polling(dp)
	
	
	
	

