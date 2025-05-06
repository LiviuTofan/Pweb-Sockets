def format_json(json_str: str) -> str:
    formatted = []
    indent_level = 0
    in_quotes = False

    for char in json_str:
        if char == '"' and not in_quotes:
            in_quotes = True
            formatted.append(char)
        elif char == '"' and in_quotes:
            in_quotes = False
            formatted.append(char)
        elif not in_quotes and char in '{[':
            indent_level += 1
            formatted.append(char)
            formatted.append('\n')
            formatted.append(' ' * (indent_level * 2))
        elif not in_quotes and char in '}]':
            indent_level -= 1
            formatted.append('\n')
            formatted.append(' ' * (indent_level * 2))
            formatted.append(char)
        elif not in_quotes and char == ',':
            formatted.append(char)
            formatted.append('\n')
            formatted.append(' ' * (indent_level * 2))
        elif not in_quotes and char == ':':
            formatted.append(char)
            formatted.append(' ')
        else:
            formatted.append(char)

    return ''.join(formatted)