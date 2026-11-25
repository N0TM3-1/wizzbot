import copy
import logging


class DiscordColorFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: '\033[90m',     # Bright black / gray
        logging.INFO: '\033[34m',      # Blue
        logging.WARNING: '\033[33m',   # Yellow
        logging.ERROR: '\033[31m',     # Red
        logging.CRITICAL: '\033[35m',  # Magenta
    }
    NAME_COLOR = '\033[36m'            # Cyan for logger/module names
    RESET = '\033[0m'

    def __init__(
        self,
        fmt: str = '%(asctime)s %(levelname)-8s %(name)s %(message)s',
        datefmt: str = '%Y-%m-%d %H:%M:%S',
        colorize: bool = False,
        name_color: str | None = NAME_COLOR,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.colorize = colorize
        self.name_color = name_color

    def format(self, record: logging.LogRecord) -> str:
        modified = copy.copy(record)
        clean_name = modified.name.strip('_')

        if self.colorize:
            if self.name_color:
                modified.name = f'{self.name_color}{clean_name}{self.RESET}'
            else:
                modified.name = clean_name

            color = self.LEVEL_COLORS.get(modified.levelno)
            if color:
                padded = f'{modified.levelname:<8}'
                modified.levelname = f'{color}{padded}{self.RESET}'
        else:
            modified.name = clean_name

        return super().format(modified)


def setup_logging(
    level: int = logging.INFO,
    log_file: str = 'log.log',
    fmt: str = '%(asctime)s %(levelname)-8s %(name)s: %(message)s',
    datefmt: str = '%Y-%m-%d %H:%M:%S',
) -> None:
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setFormatter(DiscordColorFormatter(fmt=fmt, datefmt=datefmt, colorize=False))

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(DiscordColorFormatter(fmt=fmt, datefmt=datefmt, colorize=True))

    logging.basicConfig(
        level=level,
        handlers=[file_handler, stream_handler],
        force=True,
    )