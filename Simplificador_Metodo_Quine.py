import collections

class Simplicador():

    def __init__(self,expression_to_reduce):
        self.expression_to_reduce = expression_to_reduce
        self.groups = []
 
    def binary_to_decimal(self, list_binary):
        self.decimals = []
        all_binary = []
        for x in list_binary:
                all_binary.append(list(reversed(list_binary[x])))
        for x in range(len(all_binary)):
            current_decimal = 0
            for j in range(len(all_binary[x])):
                current_decimal +=2**j*int(all_binary[x][j])
            self.decimals.append(str(current_decimal))
        return self.decimals

    def transforme_in_linhas(self): #transformar em uma função default
        self.list_linhas = {}
        list_expression = self.expression_to_reduce.split('+')
        counter = 0
        letters = [] 
        for x in list_expression: 
            x = x.replace('*', '')
            self.list_linhas['l'+str(counter)] = []
            i = 0
            while i in range(len(x)):
                if x[i] !="'" and x[i] !='+' and x[i] !='*':
                    letters.append(x[i])
                    letters = sorted(set(letters))
                
                if i == (len(x)-1) or x[i+1] !="'" :
                    self.list_linhas['l'+str(counter)].append(1)
                    i+=1
                else:
                    self.list_linhas['l'+str(counter)].append(0)
                    i+=2
            print(self.list_linhas)
            counter+=1

        return self.list_linhas, letters
                
    def first_group(self, table): #converter pro modelo class
        maximum = -1
        for x in table:
            if maximum < sum(table[x]):    
                maximum = sum(table[x])
            maximum+=1
    
        self.first_group = {}

        for i in range(maximum): #cria o máximo de agrupamento POSSÍVEIS''
            self.first_group['g'+str(i)] = [] 

            
        for x in table: #faz os agrupamentos
            dict = 'g'+str(sum(table[x]))
            self.first_group[dict].append(table[x])

            
        for x in list(self.first_group.keys()):

            if self.first_group[x] == []:
                del self.first_group[x]
        self.first_group['index'] = []
        keys = list(self.first_group.keys())
        if 'index' in keys:
            keys.remove('index')

               
        self.first_group['index'] = self.decimals
        self.groups.append(self.first_group)
        return self.first_group #table_Quinne[0]

    def news_groups(self,last_group):
        self.last_group = last_group


        def set_index(last_group, elements):
            
            values = []
            new_index =[]
            keys = list(last_group.keys())
            if 'result' in keys:
                keys.remove('result')
            if 'index' in keys:
                keys.remove('index')
            for k in keys:
                values += last_group[k]

            for e in elements:

                # if values.count(e)>1:
                #     print('aaaaaaaaa')
                index_value = values.index(e)
                new_index.append(str(last_group['index'][index_value]))

            return new_index
                        
        def match_generator (colum, next_colum, dict_list, last_group):
            dict = dict_list[0]+'|'+dict_list[1]
            keys = list(last_group.keys())
            match = {}
            new_index = []

            

            
            for x in range (len(next_colum)):
                linha = []
                variations = 0
                for y in range(len(next_colum[x])):
                    

                    if next_colum[x][y] != colum[y]:
                        linha.append('-')
                        variations +=1
                    else:
                        linha.append(next_colum[x][y])
                    
                if variations == 1:
                    # index.append(i1+','+i2)
                    if dict not in match:
                        match[dict] = []
                    match[dict].append(linha)
                    elements = []
                    elements.append(colum)
                    elements.append(next_colum[x])
                    set_result(elements, last_group)
                    new_index.append(','.join(set_index(last_group, elements)))
                    
                if x == (len(next_colum)-1):   
                               
                    return match,new_index
 
        def set_result(elements , last_group):
            values = []
            keys = list(last_group.keys())
            if 'result' in keys:
                    keys.remove('result')

            if 'index' in keys:
                keys.remove('index')

            for x in keys:
                values += last_group[x]

            if 'result' not in last_group:
                last_group['result'] = []
                for i in range(len(values)):
                    last_group['result'].append(0)
            
            for e in elements:

                position = values.index(e)
                last_group['result'][position] = 1

        #ORGANIZAR ISSO
        current_group = {
            'index':[]
        }

        keys = list(self.last_group.keys())
        if 'result' in keys:
            keys.remove('result')

        if 'index' in keys:
            keys.remove('index')
        for k in range(0,(len(keys)-1)):
            x  = keys[k]
            k2 = k + 1
            dict_list = []
            if (k2) < len(self.last_group): 
                x2 = keys[k2]
                pedaco_group = self.last_group[x2] # melhorar nome
                
                dict_list.append(x)
                dict_list.append(x2)

                dict =  '|'.join(dict_list) 
                
            for y  in range(len(self.last_group[x])):

                match,index = match_generator(self.last_group[x][y], pedaco_group, dict_list , self.last_group)

                for ind in index:
                    current_group['index'].append(ind)

                if match != None and match!={} : 
                    
                    if dict not in current_group:
                        current_group.update(match)

                    else: 
                        for j in match[dict]:
                            current_group[dict].append(j)

        if current_group not in self.groups and current_group['index']!=[]:
            self.groups.append(current_group)
            
            return self.news_groups(current_group)
        else:
            return self.groups
        # if current_group in self.groups:
        #         return self.groups

    def generate_final_table(self,AllTables,letters):
        def transforme_binary_to_expression(letters, term):
            expression = ''
            for x in range(len(term)):
                
                    if term[x] ==1: 
                        expression+= letters[x]
                    elif term[x] == 0:
                            expression+= letters[x]+"'"

            return expression

        self.AllTables =AllTables

        final_table = {}
        
        for alt in range(len(AllTables)):
            keys = list(AllTables[alt].keys())
            position = 0
            values  = []
            if 'result' in keys:
                keys.remove('result')
            if 'index' in keys:
                keys.remove('index')
            for x in keys:
                values+=AllTables[alt][x]
            if 'result' in AllTables[alt]:
                for j in AllTables[alt]['result']:
                    if j == 0:
                        expression = transforme_binary_to_expression(letters,values[position])
                        final_table[expression] = str(AllTables[alt]['index'][position])
                    position+=1    
            else:

                position = 0
                for y in values:
                    expression = transforme_binary_to_expression(letters,y)

                    final_table[expression] = AllTables[alt]['index'][position]  
                    position +=1

                return final_table




        return expression[:-1]


    def generate_final_expression(self,final_table):

        
        def get_other_terms(last_list, index):
            delta_final_table = last_list

            all_index = []
            expression  =''
            remove_in_Index = []
            dict = list(last_list.keys())
            values = list(last_list.values())
            for i in index:
                for k,v in delta_final_table.items():     
                    
                    if v.split(',').count(str(i))>0:
  
                        all_index.append(v)
            
            counter = collections.Counter(all_index)
            
            keys_counter = list(counter.keys())
            values_counter = list(counter.values())
            get_max_terms = keys_counter[values_counter.index(max(values_counter))]
            for k2,v2 in zip(dict,values):
                if v2 ==get_max_terms:
                    expression += k2
                    remove_in_Index += v2.split(',')
                    del last_list[k2]
                    remove_in_Index = sorted(set(remove_in_Index))
            
            for r in remove_in_Index:

                if r in index:
                    index.remove(r)
            if index != []:
                return expression+'+'+get_other_terms(delta_final_table,index)
            else:
                return expression

        expression_reduced = ''
        values = list(final_table.values())

        index = []
        current_index =''
        remove_in_Index = []
        delta_final_table = final_table
        for v in values:
            
            index+= v.split(',')
            index = sorted(set(index)) #agrupa elemento repetitivos e coloca em ordem
        
        for i in index:
            current_dict = ''
            counter = 0
            for k,v in delta_final_table.items(): 
   
                if i in v:
                    counter += 1
                    current_index = v
                    current_dict = k
            if counter == 1: 
                remove_in_Index+=current_index.split(',')
                remove_in_Index = sorted(set(remove_in_Index))
                
                expression_reduced += current_dict+'+'
                del delta_final_table[current_dict]

        for r in remove_in_Index:
            if r in index:
                index.remove(r)

        if index !=[]:
            expression_reduced += get_other_terms(delta_final_table, index)
        else:
            expression_reduced = expression_reduced[:-1]
        
        return expression_reduced

expression = "a*b'*c*d+a*b*c'*d" 
simplificador = Simplicador(expression)
lista_linhas,letters = simplificador.transforme_in_linhas()
lista_decimals = simplificador.binary_to_decimal(lista_linhas)


table_Quine = []

table_Quine.append(simplificador.first_group(lista_linhas))

table_Quine.extend(x for x in simplificador.news_groups(table_Quine[0]))


table_Quine.append(simplificador.generate_final_table(table_Quine,  letters))
# print(table_Quine[-1])
expression_reduced = simplificador.generate_final_expression(table_Quine[-1])
print('expressão a ser reduzida: '+expression)
print('\n')
print(f'decimals: ({",".join(lista_decimals)})')
print(f'letras: ({",".join(letters)})')
print(f'expressão minima: {expression_reduced}')

