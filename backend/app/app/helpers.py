import os


def save_content_to_file(file_name: str, content: str) -> None:
    with open(file_name, 'w') as file:
        file.write(content)


def save_binary_to_file(file_name: str, content: bytes) -> None:
    with open(file_name, 'wb') as file:
        file.write(content)


def load_content_from_file(file_name: str) -> str:
    with open(file_name, 'r') as file:
        return file.read()


def curl(link: str, domain: str):
    return os.popen(f"curl -H 'Host: {domain}' {link} -k").read()
