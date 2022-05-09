from halo import Halo

class Logger:
    def __init__(self) -> None:
        self.spinner = Halo(text_color='cyan')

    def info(self, text, color='cyan'):
        self.spinner.text_color = color
        self.spinner.info(text)

    def on(self, text, color='green'):
        self.spinner.text_color = color
        self.spinner.succeed(text)

    def off(self, text, color='red'):
        self.spinner.text_color = color
        self.spinner.succeed(text)
    
    def maintain(self, text, color='yellow'):
        self.spinner.text_color = color
        self.spinner.succeed(text)
    
    def error(self, text):
        self.spinner.fail(text)

logger = Logger()
