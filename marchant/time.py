from datetime import datetime


def time_get():
    current_time = datetime.now().time()
    if current_time.hour < 12:
        greet = 'Good Morining'
    elif current_time.hour < 18:
        greet = 'Good Afternoon'
    else:
        greet ='Good Evening'
 
    return greet
