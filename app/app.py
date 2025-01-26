# This will go into App direction to include __init__.py file, and imort the defined function "create_app"
import logging
from App import create_app
from colorlog import ColoredFormatter
 
# 创建一个logger
log = logging.getLogger(__name__)
 
# 配置logger的输出格式
log_format = (
    '%(asctime)s%(log_color)s%(levelname)s:%(name)s:%(message)s'
)

date_format = '%Y-%m-%d %H:%M:%S'
formatter = ColoredFormatter(
    log_format,
    datefmt=date_format,
    reset=True,
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'purple',
    }
)

# 为logger添加formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.CRITICAL)
 
log.debug("This is a debug message")
log.info("This is an info message")
log.warning("This is a warning message")
log.error("This is an error message")
log.critical("This is a critical message")

# Then, here call the function defined in “App/__init__.py”. Not only create app, but also register blueprint, which used as routers for different modules.
app = create_app()
app.config['JSON_AS_ASCII'] = False#make suire json text is not right.
# If form in models.py can't apply in templates/xxx.html, this config can help on it.
app.config['SECRET_KEY'] = 'ABC'#make suire json text is not right.
app.config['JSON_FILE_PATH'] = "App/jsonData/"
app.config['RECORD_PATH_FILE'] = "App/record"
app.config['UUID_TITLE_PATH_FILE'] = "App/uuid_title"
app.log = log
if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80)

