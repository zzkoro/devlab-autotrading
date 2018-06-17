import logging, os, sys
from logging.handlers import RotatingFileHandler

cur_dir = os.path.abspath(os.curdir)
sys.path.append(cur_dir)
PROJECT_HOME=cur_dir

def get_logger(name):
    """

    :param name: 생성할 log 파일명
    :return: 생성된 logger 객체를 반환한다.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    rotate_handler = RotatingFileHandler(PROJECT_HOME+"/logs/"+name+".log", 'a', 1024*1024*5, 5)
    formatter = logging.Formatter('[%(levelname)s]-%(asctime)s:%(lineno)s:%(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    rotate_handler.setFormatter(formatter)
    logger.addHandler(rotate_handler)
    return logger