class Usuario:
    def __init__(self):
        print('Soy un nuevo objeto')
    
    def hablar(self,mensaje):
        print(mensaje)

pedro = Usuario()
raul = Usuario()

pedro.hablar('hola')
raul.hablar('hola')

        