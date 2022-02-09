from datetime import datetime

class Log:
    @staticmethod
    def log(message):
        with open('logs', 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

