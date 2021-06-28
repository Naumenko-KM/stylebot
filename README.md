# stylebot
Telegram Bot with style transfer

This Bot uses both NST and Cyclegan networks.

- /start - запуск бота (хотя он и без этой команды уже работает)
- /help - выводит подсказки
- /ukiyoe /vangogh /monet /cezanne - применяет один из стилей на загруженное изображение с помощью cyclegan
- /mystyle - применяет стиль второго загруженного изображения на первое с помощью NST (работает пару минут)
- /styles - примеры изображений со стилем

Реализация cyclegan взята оригинальная https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix, код не изменялся, вызов cyclegan происходит через команду в командной строке
`os.system("python test.py --dataroot ../images --name style_"+style+"_pretrained --model test --no_dropout")`, веса обученных четырех моделей загружены заранее в папку cyclegan/checkpoints. Размер иоговых изображений 256х256 не изменялся. 

Реализация NST взята из семинара по style transfer. Функциии перенесены в класс, который вызывает бот, размер изображений взят 512х512.

Для бота использован асинхронная библиотека aiogram, deploy бота на сервер не получился.

* Для полноценной работы бота надо скачать веса vgg19 и поместить в корневую папку бота https://download.pytorch.org/models/vgg19-dcbb9e9d.pth
* Бот будет работать некоторое время на моем компьютере
* Косяков невероятное количество, но основной функционал работает
