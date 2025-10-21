from datetime import datetime


def start_up():
    date_now = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    print(f'Bot started at {date_now}')


def shutdown():
    date_now = datetime.now().strftime('%H:%M:%S %d/%m/%Y')
    print(f'Bot is down at {date_now}')
