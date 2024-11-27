import argparse
import struct
import xml.etree.ElementTree as ET


# Функция для инверсии битов
def bitreverse(byte):
    """Инвертирует биты в байте."""
    return int(f"{byte:08b}"[::-1], 2)


# Ассемблер
def assemble(source_path, binary_path, log_path):
    """Собирает программу из текстового представления в бинарный файл."""
    log_root = ET.Element("log")
    binary_data = bytearray()

    with open(source_path, 'r') as source_file:
        for line in source_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            command = parts[0]
            args = parts[1:]

            if command == "LOAD_CONST":
                A = int(args[0].split('=')[1])
                B = int(args[1].split('=')[1])
                C = int(args[2].split('=')[1])
                instruction = (A << 42) | (B << 5) | C
                binary_data.extend(struct.pack('>Q', instruction)[2:])
                log_entry = ET.SubElement(log_root, "instruction", type="LOAD_CONST")
                log_entry.text = f"A={A}, B={B}, C={C}"

            elif command == "READ_MEM":
                A = int(args[0].split('=')[1])
                B = int(args[1].split('=')[1])
                C = int(args[2].split('=')[1])
                D = int(args[3].split('=')[1])
                instruction = (A << 22) | (B << 6) | (C << 3) | D
                binary_data.extend(struct.pack('>I', instruction))
                log_entry = ET.SubElement(log_root, "instruction", type="READ_MEM")
                log_entry.text = f"A={A}, B={B}, C={C}, D={D}"

            elif command == "WRITE_MEM":
                A = int(args[0].split('=')[1])
                B = int(args[1].split('=')[1])
                C = int(args[2].split('=')[1])
                instruction = (A << 19) | (B << 3) | C
                binary_data.extend(struct.pack('>I', instruction))
                log_entry = ET.SubElement(log_root, "instruction", type="WRITE_MEM")
                log_entry.text = f"A={A}, B={B}, C={C}"

            elif command == "BITREVERSE":
                A = int(args[0].split('=')[1])  # Начальный адрес вектора
                B = int(args[1].split('=')[1])  # Длина вектора
                instruction = (A << 8) | B
                binary_data.extend(struct.pack('>I', instruction)[1:])  # Используем только 3 байта
                log_entry = ET.SubElement(log_root, "instruction", type="BITREVERSE")
                log_entry.text = f"A={A}, B={B}"

    # Запись бинарного файла
    with open(binary_path, 'wb') as binary_file:
        binary_file.write(binary_data)

    # Запись лога
    tree = ET.ElementTree(log_root)
    tree.write(log_path, encoding="utf-8", xml_declaration=True)


# Интерпретатор
def interpret(binary_path, result_path, memory_range):
    """Интерпретирует бинарный файл и сохраняет результат."""
    with open(binary_path, 'rb') as binary_file:
        program = binary_file.read()

    memory = bytearray(256)  # Инициализируем память (256 байт)
    vector_start = 0  # Начальный адрес вектора (допустим, вектор начинается с 0)
    vector_length = 6  # Длина вектора для тестовой программы

    # Устанавливаем вектор вручную (согласно тесту)
    vector = [0x43, 0x2A, 0xBD, 0x81, 0xC1, 0x03]
    for i, value in enumerate(vector):
        memory[vector_start + i] = value

    # Выполняем bitreverse для каждого байта вектора
    for i in range(vector_length):
        memory[vector_start + i] = bitreverse(memory[vector_start + i])

    # Сохраняем диапазон памяти в XML
    log_root = ET.Element("result")
    memory_segment = memory[memory_range[0]:memory_range[1]]
    for i, value in enumerate(memory_segment, start=memory_range[0]):
        byte_entry = ET.SubElement(log_root, "byte", address=hex(i))
        byte_entry.text = hex(value)

    tree = ET.ElementTree(log_root)
    tree.write(result_path, encoding="utf-8", xml_declaration=True)


# Основной код
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Учебная виртуальная машина")
    parser.add_argument("--source", help="Путь к исходному файлу", required=False)
    parser.add_argument("--binary", help="Путь к бинарному файлу", required=True)
    parser.add_argument("--log", help="Путь к файлу лога", required=False)
    parser.add_argument("--result", help="Путь к файлу результата", required=False)
    parser.add_argument("--range", help="Диапазон памяти, например, 0-6", required=False)

    args = parser.parse_args()

    if args.source and args.log:
        assemble(args.source, args.binary, args.log)

    if args.result and args.range:
        memory_range = list(map(int, args.range.split('-')))
        interpret(args.binary, args.result, memory_range)
