import numpy as np 
import string


tabela_verdade ={}

def generate_variables(n):# função que cria a quantidade de variáveis que o usuário especificou
    variaveis = list(string.ascii_lowercase)

    del variaveis[n::]
    for x in variaveis:
        tabela_verdade[x] = []



def generate_variables_negate(tabela, expression):
    new_table = {}
    new_table.update(tabela)    
    negation_variables = ['r','s','u', 'v', 'w', 'x', 'y', 'z',]
    list_expression = list(expression)
    j = -1
    list_letters_negate =[]
    
    for i in range(len(list_expression)):

        if list_expression[i] == '!' and  list_expression[i+1] not in list_letters_negate:
            
            j+=1

            list_letters_negate.append(list_expression[i+1])

            new_table[negation_variables[j]] = []
            new_table[negation_variables[j]] = np.logical_not(new_table[list_expression[i+1]])
            expression = expression.replace(f'!{list_expression[i+1]}', negation_variables[j])
            
    return new_table , expression






def gerar_tabela_verdade(m,n,index = 1):

    bits= 2**m
    repeticoes_coluna=(bits//(2**n))*2 # Essa Varivel determina a quantidade em que um intervalo de 1 e 0 se repetirão dentro de uma coluna
    repeticoes_linha =(2**n//2)//2
    
    if m == n:
        generate_variables(n)

    indice_atual =  sorted(tabela_verdade.keys())[index]
    


    if not tabela_verdade['a']: # essa condição cria a primeira coluna da tabela verdade, a pergunta da condição é: se nada em tabela_verdade: crie primeira coluna
            for k in range(bits // 2):
                tabela_verdade['a'].append(0)
            for k in range(bits // 2):
                tabela_verdade['a'].append(1)


    for  j in range(repeticoes_coluna):
        for k in range(repeticoes_linha):
            tabela_verdade[indice_atual].append(0)
                    
                    
        for k in range(repeticoes_linha):
            tabela_verdade[indice_atual].append(1)

    if n == 2: 
        return tabela_verdade

    else:
        return gerar_tabela_verdade(m,n-1, index+1)








def show_tabela_verdade(tabela, expression='?', answers=[]):
    
    print(' '.join(tabela)+' |'+expression)
    text = ''
    for y in range(len(tabela['a'])):
        for x in tabela:
            text += f'{tabela[x][y]} '
        if len(answers) == 0:
            print(text+'|?')
        else:
            print(text+f'|{answers[y]}')
        text = ''
#Adapatar para mostrar tabelas com expressão





def test_expression(tabela, expression,n):
    new_tabela_verdade,  expression = generate_variables_negate(tabela, expression)

    answers = []
    for j in range(2**n):
        expressionx = list(expression)
        valor_logico_atual = int(new_tabela_verdade[expressionx[0]][j])

        linha=[]
        

        i =0
        while i < len(expressionx):
            if expressionx[i] == '+':
                if '*' not in expressionx[0:i]:
                    valor_logico_atual = bool(new_tabela_verdade[expressionx[i-1]][j])

                del expressionx[0:i+1]
                linha.append(valor_logico_atual)
                valor_logico_atual =  bool(new_tabela_verdade[expressionx[0]][j])
                i=0

            elif expressionx[i] =='*':
                valor_logico_atual *= bool(new_tabela_verdade[expressionx[i+1]][j])
                
            
            if i == len(expressionx)-1 :       

                if expressionx[i-1] == '+' or len(expressionx) == 1:
                    valor_logico_atual =  bool(new_tabela_verdade[expressionx[i]][j])
                
                if expressionx[i-1] == '*':
                    valor_logico_atual *= bool(new_tabela_verdade[expressionx[i]][j])

                linha.append(valor_logico_atual )
            i+=1

        if 1 in linha or True in linha:
            answers.append(1)
        else:
            answers.append(0)
    return answers


def generate_expression(tabela):
    row = ''
    expression_atual = ''
    expression = ''
    len_traveled = 0

    for y in range(len(tabela['a'])):
        len_traveled = 0
        for x in tabela:
            len_traveled+= 1

            if tabela[x][y] == 1:
                expression_atual += str(x)

            elif tabela[x][y] == 0:
                expression_atual += "!"+str(x)
                        
            if len_traveled != len(tabela):
                expression_atual +='*'

            else: 
                        expression_atual +='+'

            row += ' ' + str(tabela[x][y]) 
        answer = input('Resposta das entradas:'+row+' : ')
        
        if answer == '1':
            expression += expression_atual
        row = ''    
        expression_atual = ''
    return expression[:-1]    
    



expression = ''
n =''
options = '4'

while True:
    
    variaveis = ''

    if options == '4':
        tabela_verdade.clear()
        n = int(input('Vc precisa gerar sua Tabela Verdade, digite o número de variáveis: '))
        tabela = gerar_tabela_verdade(n,n)
        print(f'\nVc Gerou sua Tabela verdade de {n} variaveis,')

    elif options == '1':
        show_tabela_verdade(tabela)
    
    elif options == '2':
        if expression == '':
            print('Lembressse, voce só pode testar uma expressão com as variaveis: '+','.join(tabela))
            expression = input('Digite a expressão: ')
            answers = test_expression(tabela, expression, n)
            show_tabela_verdade(tabela, expression ,answers)
        else:
            answers = test_expression(tabela, expression, n)
            show_tabela_verdade(tabela, expression, answers)
        
        expression = ''

    elif options == '3':
        expression = generate_expression(tabela)
        print('Esta é a sua expressão: '+expression+'\nVocê pode testa-la apertando 2')


    elif options == '5':
        print('Obrigado por utilizar o programa!!')
        break
    
    print('Escolha:\n1 - Para mostrar a tabela verdade\n2 - Para testar uma expressão\n3 - Para Extrair uma expressão da tabela verdade\n4 - Para gerar uma nova tabela verdade\n5 - Para sair')
    options = input()

