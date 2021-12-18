from datetime import datetime

def sample_responses(input_text):
    user_message = str(input_text).lower()
    print('este es el mensaje:  ',user_message)

    if user_message in ('hola'):
        return 'Hola que tal'
    
    if user_message in ('que tal?'):
        return 'Bien gracias'
    
    return 'No entiendo lo que dices'
