import logging
import yaml
import logging.config

class MyLogger():
    
    LVL = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    
    def __init__(self, name):
        self.name = name
        with open('etc/logger.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            self.logger = logging.getLogger(name)

    def __repr__(self):
        return "MyLogger('%s')" % (self.name)
    
    def echo(self, level, string):
        l = self.LVL[level]
        self.logger.log(l, string)

    def exception(self, string):
        self.logger.exception(string)
    
    
if __name__ == '__main__':
    logger = MyLogger('monitor')
    logger.echo("INFO", 'Monitoring is active')
    logger.echo("WARNING", 'WARNING')