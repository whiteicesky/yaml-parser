import re
import sys
import yaml


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def remove_comments(self, text):
        """Удаляет однострочные и многострочные комментарии."""
        text = re.sub(r"%.*", "", text)  # Удаляем однострочные комментарии
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)  # Удаляем многострочные комментарии
        return text.strip()

    def join_multiline(self, lines):
        """Объединяет строки для многострочных структур (словари, массивы)."""
        result = []
        buffer = []
        open_brackets = 0

        for line in lines:
            line = line.strip()
            if not line:
                continue

            open_brackets += line.count("{") + line.count("[")
            open_brackets -= line.count("}") + line.count("]")

            buffer.append(line)
            if open_brackets == 0:  # Структура завершена
                result.append(" ".join(buffer))
                buffer = []

        if buffer:  # Если остались незавершённые строки
            raise SyntaxError("Unmatched brackets in input.")
        return result

    def split_top_level(self, text, delimiter):
        """Разделяет строку на элементы по делимитеру, учитывая вложенность."""
        parts = []
        bracket_stack = []
        current = []
        for char in text:
            if char in "[{":
                bracket_stack.append(char)
            elif char in "]}":
                if not bracket_stack:
                    raise SyntaxError(f"Несовпадающие скобки в тексте: {text}")
                bracket_stack.pop()
            elif char == delimiter and not bracket_stack:
                parts.append("".join(current).strip())
                current = []
                continue
            current.append(char)
        parts.append("".join(current).strip())
        return parts

    def parse_value(self, value):
        """Рекурсивный разбор значений."""
        value = value.strip()
        if value.isdigit():  # Числа
            return int(value)
        elif value.startswith('"') and value.endswith('"'):  # Строки
            return value.strip('"')
        elif value.startswith("[") and value.endswith("]"):  # Массивы
            elements = self.split_top_level(value[1:-1], ",")
            return [self.parse_value(e) for e in elements]
        elif value.startswith("{") and value.endswith("}"):  # Словари
            pairs = self.split_top_level(value[1:-1], ",")
            result = {}
            for pair in pairs:
                if "=" not in pair:
                    raise SyntaxError(f"Некорректная запись словаря: {pair}")
                name, val = pair.split("=", 1)
                result[name.strip()] = self.parse_value(val.strip())
            return result
        elif value.startswith("^(") and value.endswith(")"):  # Вычисление константы
            name = value[2:-1].strip()
            if name not in self.constants:
                raise ValueError(f"Константа '{name}' не определена.")
            return self.constants[name]
        else:
            raise SyntaxError(f"Неизвестный формат значения: {value}")

    def parse_constant(self, line):
        """Разбирает объявление константы."""
        match = re.match(r"def\s+([_A-Za-z][_A-Za-z0-9]*)\s*=\s*(.+);", line)
        if not match:
            raise SyntaxError(f"Некорректное объявление константы: {line}")
        name, value = match.groups()
        self.constants[name] = self.parse_value(value)

    def parse(self, text):
        """Парсит текст и возвращает данные."""
        text = self.remove_comments(text)
        lines = text.split("\n")
        joined_lines = self.join_multiline(lines)  # Объединяем многострочные структуры

        result = {}

        # Сначала добавляем константы
        for line in joined_lines:
            if line.startswith("def"):
                self.parse_constant(line)

        # Теперь добавляем остальные значения, игнорируя строку с "def"
        for line in joined_lines:
            if line.startswith("def"):
                continue  # Игнорируем строки с "def"

            # Добавим проверку для некорректных строк
            if "=" not in line:
                raise SyntaxError(f"Некорректная строка: {line} (отсутствует знак =)")

            if not line.endswith(";"):
                raise SyntaxError(f"Некорректная строка: {line} (не завершена точкой с запятой)")

            name, value = line[:-1].split("=", 1)
            result[name.strip()] = self.parse_value(value.strip())

        # Обновляем результат константами
        result.update(self.constants)

        # Константы в начале
        final_result = {}
        final_result.update(self.constants)  # Сначала константы
        final_result.update(result)  # Затем остальная конфигурация

        return final_result


def main():
    parser = ConfigParser()
    input_text = sys.stdin.read()
    try:
        data = parser.parse(input_text)
        yaml_output = yaml.dump(data, sort_keys=False, allow_unicode=True)
        sys.stdout.write(yaml_output)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
