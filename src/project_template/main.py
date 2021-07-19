import config
from utils.logger import log


def main():
    log.info("Hello world")
    log.debug(config.POSTGRES_DATABASE_URL)
    raise KeyError


if __name__ == "__main__":
    main()
