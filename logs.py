import logging

def get_logger():
    ''' No parameters, returns logger object for logging'''
    path = Path('..')
    cwd = path.cwd()
    log_path = str(cwd) + '\\' + 'logs'
    # create logger
    logger = logging.getLogger(get_appName())
    ch = logging.StreamHandler()
    if get_env() == 'DEV':
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    fl = logging.FileHandler(log_path + '\\' + get_appName() + '.log', mode='w')

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch AND fl 
    ch.setFormatter(formatter)
    fl.setFormatter(formatter)

    # add ch and fl to logger
    logger.addHandler(ch)
    logger.addHandler(fl)
    return logger 
