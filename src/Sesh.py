import json, os, random, copy, datetime


#################### PARAM ####################
EX_PER_GROUP = 2


class Sesh:
    def __init__(self, *args):
        self.res_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'res'))
        self.prog_data = self.get_prog_data()

        if 'current_sesh' not in self.prog_data:
            self.scramble()
        else:
            print("Incomplete session exits, using it.\n")
            self.area = self.prog_data['current_sesh']['area']
            self.ex_list = self.prog_data['current_sesh']['ex_list']


    # Print method
    def print(self):
        print('Today\'s session is ' + self.area.upper() +'.\nHere are your excersises:')
        ex_str = ''
        for ex in self.ex_list:
            ex_str += '- ' + ex['ex'] + '\n'
        print(ex_str)


    # Load or create new program data if not present
    def get_prog_data(self):
            scrambler_data = {}

            if  os.path.isfile(self.res_path + '/scrambler_data.json'):
                print('Reading scrambler data file...\n')

                with open(self.res_path + '/scrambler_data.json', 'r') as file:
                    scrambler_data = json.load(file)
            else:
                print('No scrambler data present, creating new file...\n')

                scrambler_data = self.create_new_prog_data_file()
            return scrambler_data
    

    # Creates program data file
    def create_new_prog_data_file(self):
        ex_list = []
        new_data = {}
        new_data['unused_ex_list'] = []
        new_data['master_ex_list'] = []
        new_data['area_list'] = []

        
        with open(self.res_path + '/ex_list.json', 'r') as file: # ex_list file could be txt in future
            ex_list = json.load(file)
    


        for entry in ex_list:
            new_data['area_list'].append(entry['area'])
            for group in entry['groups']:
                group['area'] = entry['area']
                new_data['master_ex_list'].append(group)

        new_data['unused_ex_list'] = new_data['master_ex_list'].copy() 

        with open(self.res_path + '/scrambler_data.json', 'w') as newfile:
            newfile.write(json.dumps(new_data, indent = 4))   

        return new_data


    # Randomly builds a workout session with some rules:
    # 1. A new session cannot be for the same area as the last one
    # 2. the exersise list exhausts itself before being reset
    def scramble(self):
        sesh_area = ''
        ex_list = []
        unused_list = self.prog_data['unused_ex_list']

        #rule 1 code
        if 'prev_sesh_list' in self.prog_data:
            area_list = self.prog_data['area_list'].copy()
            for i in range(len(area_list) - 1):
                if area_list[i] == self.prog_data['prev_sesh_list'][len(self.prog_data['prev_sesh_list']) - 1]['area']:
                    del area_list[i]
            sesh_area = area_list[random.randrange(len(area_list))]
        else:
            sesh_area = self.prog_data['area_list'][random.randrange(len(self.prog_data['area_list']))]
        
        new_unused_list = []

        #rule 2 code
        for i in range(len(unused_list)):
            if unused_list[i]['area'] == sesh_area:
                ex_set = []

                if sesh_area=='jogging':
                    if len(unused_list[i]['ex']) > 1:
                        ex_set = self.select_ex(unused_list[i]['ex'], 1)
                    else:
                        ex_set = self.reset_and_select_ex(1, self.prog_data, unused_list, i)
                    
                    ex_list.append({'ex': ex_set[0], 'time': '0:00', 'distance(km)': 0 , 'group': unused_list[i]['group']})
                    break

                if len(unused_list[i]['ex']) > EX_PER_GROUP:
                    ex_set = self.select_ex(unused_list[i]['ex'], EX_PER_GROUP)
                else:
                    ex_set = self.reset_and_select_ex(EX_PER_GROUP, self.prog_data, unused_list, i)

                for ex in ex_set:
                    ex_list.append({'ex': ex, 'rep_qty': 0, 'rep': [], 'weight(kg)': 0, 'group': unused_list[i] ['group']})

        #set generated data and save it
        print('New session created!\n')
        self.area = sesh_area
        self.ex_list = ex_list
        self.prog_data['current_sesh'] = {'area': sesh_area, 'ex_list': ex_list}
        self.save()


    def reset_and_select_ex(self, ex_amount, unused_list, i):
        print('Exercise list exhausted for: ' + unused_list[i]['group'] + ', resetting...\n')
        if (len(unused_list[i])) == 1 and ex_amount == 1:
            return [unused_list[i]['ex'][0]]

        unused_list[i]['ex'] = self.prog_data['master_ex_list'][i]['ex'].copy()
        return self.select_ex(unused_list[i]['ex'], ex_amount)


    # return random subset of excerse set and list of entries used
    def select_ex(self, ex_set, ex_amount):
        return_list = []
        for i in range(ex_amount):
            ex_entry = {}

            used_ex = random.randrange(len(ex_set) - i)

            ex_entry['rep'] = 0
            ex_entry['rep_qty'] = []
            ex_entry['name'] = ex_set[used_ex]

            return_list.append(ex_set[used_ex])
            del ex_set[used_ex]


        return return_list
    

    def save(self):
        print('Saving scrambler data...\n')
        with open(self.res_path + '/scrambler_data.json', 'w') as newfile:
            newfile.write(json.dumps(self.prog_data, indent = 4))   
    
    # Move current sesh data to previous sesh list
    def complete_sesh(self):
        if 'prev_sesh_list' not in self.prog_data:
            self.prog_data['prev_sesh_list'] = []

        self.prog_data['current_sesh']['timestamp'] = datetime.datetime.timestamp(datetime.datetime.now())
        print("Session completed on[" + str(datetime.datetime.now()) + '], moving to archive...\n')
        self.prog_data['prev_sesh_list'].append(copy.deepcopy(self.prog_data['current_sesh']))
        del self.prog_data['current_sesh']
        
        self.save()
    
    def delete_curr_sesh(self):
        print('Clearning current session data...\n')
        del self.prog_data['current_sesh']
        self.save()
