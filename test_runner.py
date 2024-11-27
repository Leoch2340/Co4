import time
import os
import xml.etree.ElementTree as ET
from subprocess import run

def run_test(command, expected_output, test_name, operation_type):
    # Запуск ассемблера
    start_time = time.time()
    process = run(command, shell=True, capture_output=True)
    end_time = time.time()

    # Проверка времени выполнения
    execution_time = end_time - start_time
    print(f"\nВремя выполнения теста '{test_name}' ({operation_type}): {execution_time:.4f} секунд")

    # Проверка наличия ошибок в процессе
    if process.returncode != 0:
        print(f"Ошибка в тесте '{test_name}' ({operation_type}): {process.stderr.decode()}")
        return False

    # Проверка правильности результата
    log_file = "log.xml"
    if os.path.exists(log_file):
        tree = ET.parse(log_file)
        root = tree.getroot()

        for instruction in root.findall("instruction"):
            instruction_type = instruction.get("type")
            instruction_text = instruction.text.strip()

            # Проверяем, что результат соответствует ожидаемому для каждой операции
            if instruction_type == operation_type and expected_output in instruction_text:
                print(f"Тест '{test_name}' ({operation_type}) прошел успешно.")
                return True
        print(f"Тест '{test_name}' ({operation_type}) не прошел: неверный вывод.")
        return False
    else:
        print(f"Ошибка: файл {log_file} не найден.")
        return False


def test_assembler():
    # Ожидаемый вывод для каждой команды в XML логе
    expected_output = {
        "LOAD_CONST": "A=39, B=695, C=1",
        "READ_MEM": "A=22, B=506, C=3, D=7",
        "WRITE_MEM": "A=22, B=603, C=7",
        "BITREVERSE": "A=0, B=6"
    }

    # Тесты для каждой операции
    operations = [
        ("python uvm.py --source=test_cases.txt --binary=program.bin --log=log.xml", expected_output["LOAD_CONST"], "Тест 1: Загрузка константы", "LOAD_CONST"),
        ("python uvm.py --source=test_cases.txt --binary=program.bin --log=log.xml", expected_output["READ_MEM"], "Тест 2: Чтение из памяти", "READ_MEM"),
        ("python uvm.py --source=test_cases.txt --binary=program.bin --log=log.xml", expected_output["WRITE_MEM"], "Тест 3: Запись в память", "WRITE_MEM"),
        ("python uvm.py --source=test_cases.txt --binary=program.bin --log=log.xml", expected_output["BITREVERSE"], "Тест 4: Операция bitreverse", "BITREVERSE")
    ]

    # Выполнение тестов для каждой операции по очереди
    for command, expected, test_name, operation_type in operations:
        print(f"\nЗапуск {test_name} ({operation_type})")
        result = run_test(command, expected, test_name, operation_type)
        if result:
            print(f"Тест '{test_name}' ({operation_type}) прошел успешно.\n")
        else:
            print(f"Тест '{test_name}' ({operation_type}) не прошел.\n")

        # Пауза между тестами с запросом на продолжение
        input("Нажмите Enter для продолжения следующего теста...")

# Запуск тестов
if __name__ == "__main__":
    test_assembler()
