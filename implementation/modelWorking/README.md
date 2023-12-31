# Режим распознавания эмоций с использованием модуля Артинтрек

Здесь представлена программа `startEmoMode.ino`, которая запускает режим распознавания эмоций на модуле Артинтрек. Программа загружается в контроллер Trackduino, который подключается к модулю Артинтрек через uart. Взаимодействие между контроллером и модулем осуществляется с использованием библиотеки TrackCV.

## Функции

Программа содержит две основные функции:

### `ArtintrackInit(port)`

Функция `ArtintrackInit` устанавливает соединение с модулем Артинтрек через указанный порт `port`. Это позволяет контроллеру Trackduino обмениваться данными с модулем.

### `ArtintrackUpdate(script)`

Функция `ArtintrackUpdate` запускает указанный скрипт `script` на модуле Артинтрек. В данном случае, скрипт отвечает за распознавание эмоций.

# Работа программы

После успешного подключения к модулю Артинтрек, на экране модуля отображается изображение с USB-камеры. В случае обнаружения лица на изображении, происходит распознавание текущей эмоции человека, которая отображается в окне на модуле Артинтрек.

# Демонстрация

По следующей ссылке вы можете посмотреть видеоматериал, демонстрирующий работу режима распознавания эмоций с использованием модуля Артинтрек.

[Ссылка на видеоматериал](https://drive.google.com/file/d/1WebrR__Klz07UQtUrCm4auOJauLq9ogT/view?usp=sharing)
