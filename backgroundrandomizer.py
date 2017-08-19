import random
import time

def shuffle_backgrounds(stored_datas):
    #start_time = time.time()
    shuffler = Shuffler(stored_datas, lambda data : data.tiledata_roombg, filter_roombg)
    shuffler.shuffle()
    print('Backgrounds shuffled')

    shuffler = Shuffler(stored_datas, lambda data : data.tiledata_roomcolor, filter_roomcolor)
    shuffler.shuffle()
    print('Tile colors shuffled')
    #print('Backgrounds shuffled in %f seconds' % (time.time()-start_time))

def filter_roombg(val):
    return val <= 118 and val not in (0,23,17,104)

def filter_roomcolor(val):
    return val <= 31 and val not in (0,5,6,30) # DLC: (0,5,32,34,55)

class Shuffler(object):

    def __init__(self, stored_datas, data_select, filter_function):
        self.data_select = data_select
        self.stored_datas = stored_datas
        original_locations = []

        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data_select(data)) if filter_function(val))

        self.original_locations = original_locations

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        new_backgrounds = list(backgrounds)
        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        data_select = self.data_select
        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            data_select(stored_datas[areaid])[posindex] = allocation[val]
