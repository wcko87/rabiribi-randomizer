import random
import time

LAGGY_BACKGROUNDS = set((37, 65, 66, 80, 84, 88, 89, 99))

def to_tile_index(x, y):
    return x*18 + y

def shuffle_backgrounds(stored_datas, no_laggy_backgrounds):
    #start_time = time.time()
    shuffler = BackgroundShuffler(stored_datas, no_laggy_backgrounds)
    shuffler.shuffle()
    print('Backgrounds shuffled')

    shuffler = RoomColorShuffler(stored_datas)
    shuffler.shuffle()
    print('Tile colors shuffled')
    #print('Backgrounds shuffled in %f seconds' % (time.time()-start_time))


class BackgroundShuffler(object):
    def __init__(self, stored_datas, no_laggy_backgrounds):
        self.stored_datas = stored_datas
        original_locations = []

        filter_function = self.filter_function
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data.tiledata_roombg) if filter_function(val))

        self.original_locations = original_locations
        self.no_laggy_backgrounds = no_laggy_backgrounds

    def filter_function(self, val):
        # don't shuffle DLC backgrounds
        # don't shuffle Noah3 background because it does weird things to boss doors
        # don't shuffle library entrance background because it removes springs
        return val <= 118 and val not in (0,23,17,83,104,110)

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        if self.no_laggy_backgrounds:
            new_backgrounds = [b for b in backgrounds if b not in LAGGY_BACKGROUNDS]
            while len(new_backgrounds) < len(backgrounds):
                new_backgrounds += new_backgrounds
        else:
            new_backgrounds = list(backgrounds)

        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            # Fix for pyramid super-trampoline bug
            if areaid == 1 and posindex == to_tile_index(16,11): continue

            # Fix for Alius3 Noah becoming the Noah1 boss fight bug
            if areaid == 8 and posindex == to_tile_index(18,7): continue
            # Fix for Noah1 becoming the Alius3 Noah boss fight bug
            if areaid == 8 and posindex == to_tile_index(18,5) and allocation[val] == 9: continue

            # Fix for early sysint computer bug
            if areaid == 4 and posindex == to_tile_index(17,16): continue

            # Fix for bug where you can't enter warps if it has computer room background.
            if allocation[val] == 64:
                # plurkwood warp from starting forest
                if areaid == 0 and posindex == to_tile_index(8,4): continue
                # warp to exit plurkwood
                if areaid == 6 and posindex == to_tile_index(9,3): continue
                # warp to exit sysint
                if areaid == 9 and posindex == to_tile_index(14,8): continue

            stored_datas[areaid].tiledata_roombg[posindex] = allocation[val]


class RoomColorShuffler(object):
    def __init__(self, stored_datas):
        self.stored_datas = stored_datas
        original_locations = []

        filter_function = self.filter_function
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data.tiledata_roomcolor) if filter_function(val))

        self.original_locations = original_locations

    def filter_function(self, val):
        # don't shuffle DLC colors
        # don't shuffle library color (24) because it deletes trampolines
        # don't shuffle FC2/HoM colors (6,30) because they do weird things to bosses
        return val <= 31 and val not in (0,5,6,24,30) # DLC: (0,5,32,34,55)

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        new_backgrounds = list(backgrounds)
        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            stored_datas[areaid].tiledata_roomcolor[posindex] = allocation[val]
