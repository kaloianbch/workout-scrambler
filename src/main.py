import os
from Sesh import Sesh

def positive_reinforcment_phrase():
    return 'uh'

def data_input_jogging(sesh):
    next_ex = False
    ex = sesh.ex_list[0]

    while not next_ex:
            ex['distance(km)'] = input('\nHow long a distance did you run on route ' + ex['ex'] + '(km)? ')
            ex['time'] = input('And how long did you run for(m:ss)? ')
            
            next_ex = True if input("So you ran a distance of[" + ex['distance(km)'] + 'km]on route[' + ex['ex'] +
            ']for[' + ex['time'] + '].\nAll correct?(Y/N) ').capitalize() == 'Y' else False
    

    print('\nGood run!\n' + positive_reinforcment_phrase() + '\n')


def data_input(sesh):
    if sesh.area == 'jogging':
        data_input_jogging(sesh)
    else:
        for ex in sesh.ex_list:
            next_ex = False
            while not next_ex:
                skip_ex = False
                ex['rep'] = []

                while int(ex['rep_qty']) < 1:
                    ex['rep_qty'] = input('\nHow many reps of ' + ex['ex'] + ' did you do? ')
                    
                    if not ex['rep_qty'].isnumeric():
                        ex['rep_qty'] = 0
                        print('That\'s not a whole positive number bud, try again.')

                    elif int(ex['rep_qty']) < 1 and input('Skip this exersice?(Y/N) ').capitalize() == 'Y' :
                        ex['rep_qty'] = 0
                        skip_ex = True
                        next_ex = True
                        break

                if not skip_ex:
                    ex['weight(kg)'] = input('At what weight(kg)? ')
                    
                    for i in range(int(ex['rep_qty'])):
                        ex['rep'].append(input('How many did you do in rep ' + str(i + 1) + '? '))
                    
                    next_ex = True if input("So you did[" + str(ex['rep_qty']) + "]reps of[" + ex['ex'] + 
                    ']at[' + str(ex['weight(kg)']) + 'kg].\nYour reps were ' + str(ex['rep']) + '.\nAll correct?(Y/N) ').capitalize() == 'Y' else False
        
        print('\nThat\'s all!\n' + positive_reinforcment_phrase() + '\n')
    sesh.complete_sesh()
    

#################### MAIN ####################
start = Sesh()

start.print()

data_input(start)