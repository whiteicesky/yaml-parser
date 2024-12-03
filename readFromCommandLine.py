import sys


class ConfigParser:
    def __init__(self):
        self.constants = {}

    def remove_comments(self, text):
        lines = text.splitlines()
        result = []
        inside_multiline_comment = False
        for line in lines:
            if inside_multiline_comment:
                if "*/" in line:
                    inside_multiline_comment = False
                continue
            if line.strip().startswith("%") or line.strip() == "":
                continue
            if "/*" in line:
                inside_multiline_comment = True
                continue
            result.append(line)
        return "\n".join(result)

    def join_multiline(self, lines):
        result = []
        buffer = ""
        open_blocks = 0

        for line in lines:
            stripped_line = line.strip()

            open_blocks += stripped_line.count("{") + stripped_line.count("[")
            open_blocks -= stripped_line.count("}") + stripped_line.count("]")

            buffer += stripped_line + " "

            if open_blocks == 0 and buffer.strip():
                result.append(buffer.strip())
                buffer = ""

        if buffer.strip():
            raise SyntaxError(f"Незавершенный блок: {buffer}")

        return result

    def parse_value(self, value):
        if value.startswith("["):
            return self.parse_array(value)
        elif value.startswith("{"):
            return self.parse_dict(value)
        elif value.isdigit():
            return int(value)
        elif value.startswith('"') and value.endswith('"'):
            return value[1:-1]  # Строка
        else:
            raise SyntaxError(f"Неизвестный формат значения: {value}")

    def parse_array(self, value):
        content = value[1:-1].strip()
        items = []
        buffer = ""
        open_blocks = 0

        for char in content:
            if char in "[{":
                open_blocks += 1
            elif char in "]}":
                open_blocks -= 1

            if char == "," and open_blocks == 0:
                items.append(buffer.strip())
                buffer = ""
            else:
                buffer += char

        if buffer.strip():
            items.append(buffer.strip())

        return [self.parse_value(item) for item in items]

    def parse_dict(self, value):
        content = value[1:-1].strip()
        items = []
        buffer = ""
        open_blocks = 0

        for char in content:
            if char in "[{":
                open_blocks += 1
            elif char in "]}":
                open_blocks -= 1

            if char == "," and open_blocks == 0:
                items.append(buffer.strip())
                buffer = ""
            else:
                buffer += char

        if buffer.strip():
            items.append(buffer.strip())

        result = {}
        for item in items:
            if "=" not in item:
                raise SyntaxError(f"Некорректный элемент словаря: {item}")
            key, val = item.split("=", 1)
            result[key.strip()] = self.parse_value(val.strip())

        return result

    def parse_constant(self, line):
        name, value = line[4:-1].split("=", 1)
        self.constants[name.strip()] = self.parse_value(value.strip())

    def parse(self, text):
        text = self.remove_comments(text)
        lines = text.split("\n")
        joined_lines = self.join_multiline(lines)

        result = {}

        for line in joined_lines:
            if line.startswith("def"):
                self.parse_constant(line)

        for line in joined_lines:
            if line.startswith("def"):
                continue  # Игнорируем строки с "def"

            if "=" not in line:
                raise SyntaxError(f"Некорректная строка: {line} (отсутствует знак =)")

            name, value = line.rstrip(";").split("=", 1)
            result[name.strip()] = self.parse_value(value.strip())

        result.update(self.constants)

        final_result = {}
        final_result.update(self.constants)
        final_result.update(result)

        return final_result


def main():
    parser = ConfigParser()

    input_text = sys.stdin.read()

    try:
        result = parser.parse(input_text)
        import yaml
        print(yaml.dump(result, default_flow_style=False, allow_unicode=True))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
