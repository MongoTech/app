from app.core.config import settings
from app.ssh_module import connect


def test_ssh_connection() -> None:
    connection = connect.Connection(
        settings.SSH_HOSTNAME,
        username=settings.SSH_USERNAME,
        key_filename=settings.SSH_KEY,
    )
    connection.sending_commands("echo 'test' > test.txt")  # nosec
    assert "test.txt" in connection.sending_commands("ls")  # nosec
    assert "test" in connection.sending_commands("cat test.txt")  # nosec
