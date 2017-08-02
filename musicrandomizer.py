import random
import time

def shuffle_music(stored_datas):
    shuffler = MusicShuffler(stored_datas)
    shuffler.shuffle()
    print('Music shuffled')

is_bgm = lambda v : 129 <= v and v <= 159

class MusicShuffler(object):

    def __init__(self, stored_datas):
        self.stored_datas = stored_datas
        original_locations = []
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, eventid)
                for posindex, eventid in enumerate(data.tiledata_event) if is_bgm(eventid))

        self.original_locations = original_locations

    def shuffle(self):
        musics = list(set(eventid for areaid, posindex, eventid in self.original_locations))
        new_musics = list(musics)
        random.shuffle(new_musics)
        allocation = dict(zip(musics, new_musics))

        stored_datas = self.stored_datas
        for areaid, posindex, eventid in self.original_locations:
            stored_datas[areaid].tiledata_event[posindex] = allocation[eventid]