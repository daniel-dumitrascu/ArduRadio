import sys
import logging

class ColoredFormatter(logging.Formatter):
    """Custom formatter with ANSI color codes."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green  
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[41m',   # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        # Only add colors if output is a terminal
        if sys.stdout.isatty():
            color = self.COLORS.get(record.levelname, '')
            formatted = super().format(record)
            
            # Add color to levelname only
            if color:
                formatted = formatted.replace(
                    record.levelname, 
                    f"{color}{record.levelname}{self.RESET}"
                )
            return formatted
        else:
            return super().format(record)

def getLogger(log_name, lvl):
    log = logging.getLogger(log_name)
    log.setLevel(lvl)

    # Prevent adding multiple handlers if logger already exists
    if log.handlers:
        return log

    console_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(lvl)
    console_handler.setFormatter(console_formatter)
    log.addHandler(console_handler)
    return log