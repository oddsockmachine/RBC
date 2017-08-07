from contextlib import contextmanager
from datetime import datetime
from json import dumps

@contextmanager
def log_catch(node):
    try:
        yield
    except Exception as e:
        print(e)
        msg = dumps({'timestamp': str(datetime.now()), 'error': str(e), 'node': node.name})
        node.log_error(msg)
        pass
