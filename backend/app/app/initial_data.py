import logging
from app.db.init_db import init_db
from app.db.session import database, client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = database
    loop = client.get_io_loop()
    loop.run_until_complete(init_db(db=db))



def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
