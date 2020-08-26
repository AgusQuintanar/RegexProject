class Reemplazador_REGEX():

    def __init__(self):
        self.cadena = 'abaaaabaaanbbb'
        self.expresion_regular = 'aba * + bbb *'
        self.expresion_regular = self.simplificar_er()

        self.cadena_reemplazadora = 'R'

        self.cr = list(self.cadena_reemplazadora)
        self.er = list(self.expresion_regular)

    def simplificar_er(self, x: int=0):
        er = self.expresion_regular.split(" ")
        while x < len(er):
            if er[x] == '+':
                if er[x-1] == er[x+1]:
                    er = er[:x] + er[x+2:]
                    x = 0
            x += 1
        return " ".join(er)

    def encontrar_concatenacion(self, cadena: list, er: list, x: int=0):
        while x <= len(cadena) - len(er):
            if cadena[x] == er[0]:
                if cadena[x:x+len(er)] == er:
                    cadena = cadena[:x] + self.cr + cadena[x+len(er):]
                    x += len(self.cr) - 1
            x += 1
        return cadena

    def encontrar_union(self, cadena: list, er1: list, er2: list, x: int=0):
        er_mas_chica = len(er1) if len(er1) < len(er2) else len(er2)

        while x <= len(cadena) - er_mas_chica:
            if cadena[x] == er1[0]:
                if cadena[x:x+len(er2)] != er2 or len(er2) < len(er1):
                    cadena = cadena[:x] + self.encontrar_concatenacion(cadena[x:x+len(er1)], er1) + cadena[x+len(er1):]
                    x += len(self.cr) - 1
            if cadena[x] == er2[0]:
                cadena = cadena[:x] + self.encontrar_concatenacion(cadena[x:x+len(er2)], er2) + cadena[x+len(er2):]
                x += len(self.cr) - 1
            x += 1
        return cadena

    def encontrar_cerradura(self, cadena: list, er: list, x: int=0):
        while x <= len(cadena) - len(er):
            if cadena[x] == er[0]:
                if cadena[x:x+len(er)-1] == er[:-1]:
                    limite_match = x + len(er)-1
                    while  limite_match  < len(cadena):
                        if cadena[limite_match] == er[-1]:
                            limite_match += 1
                        else:
                            break;

                    if limite_match + 1 < len(cadena):
                        cadena = cadena[:x] + self.cr + cadena[limite_match:]
                    else:
                        cadena = cadena[:x] + self.cr

                    x += len(self.cr) - 1
            x += 1
        return cadena
                    

class RPN(): #Reverse Polish Notation
    def __init__(self):
        self.regex = Reemplazador_REGEX()
        self.expresion_infija = self.regex.expresion_regular
        self.expresion_postfijo = ''

        print("Cadena Original:", self.regex.cadena)
        print("Expresion Regular:", self.regex.expresion_regular)
        print('Cadena Rempazadora:', self.regex.cadena_reemplazadora)

        if len(self.regex.expresion_regular.split()) == 1:
            self.cadena = "".join(self.regex.encontrar_concatenacion(list(self.regex.cadena), self.regex.er))
        else:
            self.generar_expresion_postfijo()
            self.evaluar_expresion()
        
        print("Cadena Final",self.regex.cadena)

    def evaluar_expresion(self):
        lista_expr_post = self.expresion_postfijo.split()
        indice = 1
        cadena = list(self.regex.cadena)
        while len(lista_expr_post) > 1:
            dato = lista_expr_post[indice]

            if not dato in list('*+·'):
                indice += 1
            else:
                if dato == '+':

                    if len(lista_expr_post) - indice > 2:
                        if lista_expr_post[indice + 2] == "·":
                            lista_expr_post[indice-2] = lista_expr_post[indice-2] + lista_expr_post[indice+1]
                            lista_expr_post[indice-1] = lista_expr_post[indice-1] + lista_expr_post[indice+1]
                            lista_expr_post.pop(indice+1)
                            lista_expr_post.pop(indice+1)
                            indice = 1
                        else:
                            cadena = self.regex.encontrar_union(cadena, list(lista_expr_post[indice-2]), list(lista_expr_post[indice-1]))  
                            lista_expr_post = lista_expr_post[3:]
                            indice = 1
                    
                    elif len(lista_expr_post) - indice > 1:
                        if lista_expr_post[indice + 1] == "·":
                            temp = lista_expr_post[indice-3]
                            lista_expr_post[indice-3] = temp + lista_expr_post[indice-2]
                            lista_expr_post[indice-2] = temp + lista_expr_post[indice-1]
                            lista_expr_post.pop(indice-1)
                            lista_expr_post.pop(indice)
                            indice = 1
                        else:
                            cadena = self.regex.encontrar_union(cadena, list(lista_expr_post[indice-2]), list(lista_expr_post[indice-1]))  
                            lista_expr_post = lista_expr_post[3:]
                            indice = 1
                    else:
                        cadena = self.regex.encontrar_union(cadena, list(lista_expr_post[indice-2]), list(lista_expr_post[indice-1]))  
                        lista_expr_post = lista_expr_post[3:]
                        indice = 1

                elif dato == '*':
                    if indice + 1 > len(lista_expr_post):
                        cadena = self.regex.encontrar_cerradura(cadena, list(lista_expr_post[indice-1]))
                        lista_expr_post = lista_expr_post[2:]
                        indice = 1

                        if not lista_expr_post[indice+1] in list('+·*'):
                            cadena = self.regex.encontrar_cerradura(cadena, list(lista_expr_post[indice-1]))
                            lista_expr_post = lista_expr_post[2:]
                            indice = 1
                        else:
                            cadena = self.regex.encontrar_cerradura(cadena, list(lista_expr_post[indice-1]))
                            lista_expr_post.pop(indice)
                            indice = 1
                    else:
                        cadena = self.regex.encontrar_cerradura(cadena, list(lista_expr_post[indice-1]))
                        lista_expr_post.pop(indice)
                        indice = 1

              
                
                elif dato == '·':
                    lista_expr_post[indice] = lista_expr_post[indice-2] + lista_expr_post[indice-1]
                    lista_expr_post = lista_expr_post[2:]
                    indice = 1

     
        if len(lista_expr_post) == 1:
            if not lista_expr_post[0] in list('*+·'):
                cadena = "".join(self.regex.encontrar_concatenacion(list(cadena), list(lista_expr_post[0])))

        self.regex.cadena = "".join(cadena)         

    def generar_expresion_postfijo(self):
        exInfArr = self.expresion_infija.split(" ")
        operadores = {"(":0, "+":1, "·":2, "*":3}
        pila = []
        lista = []

        for x in exInfArr:
            if not x in list('()*+·'):
                lista.append(x)
            elif x == '(' or len(pila) == 0:
                pila.append(x)
            elif x == ')':
                while pila[-1] != '(':
                    lista.append(pila.pop())
                pila.pop()
            else:
                while len(pila) != 0 and operadores[x] <= operadores[pila[-1]]:
                    lista.append(pila.pop())
                pila.append(x)
        while len(pila) != 0:
            lista.append(pila.pop())

        self.expresion_postfijo = " ".join(lista)

rpn = RPN()

print("REGEX Polaco:", rpn.expresion_postfijo)





