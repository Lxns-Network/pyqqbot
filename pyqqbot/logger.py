from logbook import Logger, StreamHandler
from logbook import (
    INFO,
    DEBUG
)

import logbook
import os
import sys

logbook.set_datetime_format('local')
stream_handler = StreamHandler(sys.stdout, level=INFO if not os.environ.get("DEBUG") else DEBUG)
stream_handler.format_string = '[{record.time:%Y-%m-%d %H:%M:%S}][{record.level_name}] {record.channel}: {record.message}'
stream_handler.push_application()

Event = Logger('Event', level=INFO)
Network = Logger("Network", level=DEBUG)
Session = Logger("Session", level=INFO)
Protocol = Logger("Protocol", level=INFO)
