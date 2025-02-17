# Проект: Ассемблер и интерпретатор для учебной виртуальной машины (УВМ)
Вариант 29

## 1. Общее описание

Данный проект включает в себя ассемблер и интерпретатор для учебной виртуальной машины (УВМ). УВМ поддерживает операции, такие как загрузка констант, чтение и запись значений в память, а также выполнение унарной операции `bitreverse`. Ассемблер преобразует исходный код программы в бинарный формат и лог-файл, а интерпретатор выполняет бинарные инструкции, генерируя результаты в формате XML.

Проект предоставляет инструменты для:
- Ассемблера, который конвертирует исходный код в бинарный файл и лог.
- Интерпретатора, который выполняет бинарные инструкции и записывает результаты в файл.

## 2. Описание всех функций и настроек

### Ассемблер
Ассемблер принимает на вход текстовый файл с исходным кодом программы и генерирует два файла:
- **Бинарный файл** — содержит инструкции в виде байтов.
- **Лог-файл в формате XML** — хранит информацию о каждом шаге программы и инструкциях.

Ассемблер поддерживает следующие настройки:
- `--source`: путь к исходному текстовому файлу с кодом программы.
- `--binary`: путь, по которому будет создан бинарный файл.
- `--log`: путь к файлу, в котором будет сохранен лог в формате XML.

### Интерпретатор
Интерпретатор выполняет инструкции из бинарного файла, имитируя работу учебной виртуальной машины. Результаты выполнения программы сохраняются в файл в формате XML.

Интерпретатор поддерживает следующие параметры:
- `--binary`: путь к бинарному файлу с программой.
- `--log`: путь к файлу для записи результатов работы интерпретатора.

## 3. Описание команд для сборки проекта


   Для запуска ассемблера используйте следующую команду:
```bash
python uvm.py --source=source.txt --binary=program.bin --log=log.xml

```
Для выполнения программы интерпретатором используйте следующую команду:
```bash
python uvm.py --binary=program.bin --result=result.xml --range=0-6

```

Для выполнения тестирования используйте следующую команду: 

```bash
python test_runner.py    

```

## 4. Примеры использования в виде скриншотов 

![изображение](https://github.com/user-attachments/assets/f2e5893d-660d-41f6-9389-c2fa7011bcc0)


```bash
python uvm.py --binary=program.bin --result=result.xml --range=0-6

```

![изображение](https://github.com/user-attachments/assets/e41e092c-a317-476c-86d4-bcc7ac66ef42)


```bash
python uvm.py --source=source.txt --binary=program.bin --log=log.xml

```



## 5. Результаты прогона тестов 

![изображение](https://github.com/user-attachments/assets/3159a0ab-e24b-470d-8046-b82135249a20)


```bash
python test_runner.py    

```

