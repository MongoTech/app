import os


def save_content_to_file(file: str, content: str) -> None:
    with open(file, 'w') as file:
        file.write(content)

def save_binary_to_file(file: str, content: str) -> None:
    with open(file, 'wb') as file:
        file.write(content)

def load_content_from_file(file: str) -> str:
    with open(file, 'r') as file:
        return file.read()


def curl(link: str, domain: str):
    return os.popen(f"curl -H 'Host: {domain}' {link} -k").read()
