import struct

MAP_SIZE = 100000
MAP_ITEMS_OFFSET = 402700

class Item(object):
    def __init__(self, position, areaid, itemid):
        self.areaid = areaid
        self.position = position
        self.itemid = itemid
        self.name = None

    def copy(self):
        item = Item(self.position, self.areaid, self.itemid)
        item.name = self.name
        return item

    def set_location(self, item):
        self.areaid = item.areaid
        self.position = item.position

    def __str__(self):
        x, y = self.position
        return '(%d,%d) : %d : %d : %s' % (x, y, self.areaid, self.itemid, self.name)

def parse_item_from_string(line):
    pos, areaid, itemid, name = (s.strip() for s in line.split(':', 3))
    import ast
    item = Item(ast.literal_eval(pos), int(areaid), int(itemid))
    if len(name) > 0 and name != 'None':
        item.name = name
    return item

def to_position(index):
    y = index%200
    x = index//200
    return x,y

def to_index(position):
    x, y = position
    return x*200 + y

def load_items(areaid):
    f = open(map_filename(areaid), 'rb')
    f.seek(MAP_ITEMS_OFFSET)
    
    tiledata = (struct.unpack('h', f.read(2))[0] for i in range(MAP_SIZE))
    items = list(Item(to_position(pos), areaid, itemid) for pos, itemid in enumerate(tiledata) if itemid != 0)
    f.close()
    return list(items)

def write_items(areaid, items):
    tiledata = [b'\x00\x00' for i in range(MAP_SIZE)]
    for item in items:
        if item.areaid != areaid: continue
        index = to_index(item.position)
        tiledata[index] = struct.pack('h', item.itemid)

    f = open(map_filename(areaid), 'r+b')
    f.seek(MAP_ITEMS_OFFSET)
    f.write(b''.join(tiledata))
    f.close()

def map_filename(areaid):
    return 'area%d.map' % areaid

def print_all_items():
    sb = []
    for areaid in range(0,10):
        items = load_items(areaid)
        sb.append('Area %d: NAME' % areaid)
        for item in items:
            sb.append(str(item))
    print('\n'.join(sb))


class ItemModifier(object):
    def __init__(self, areaids):
        self.areaids = list(areaids)
        self.items = dict((areaid, {}) for areaid in areaids)
        for areaid in areaids:
            for item in load_items(areaid):
                self.items[item.areaid][item.position] = item

        self._set_all_dirty_flags(False)

    def _set_all_dirty_flags(self, value):
        self.modified = dict((areaid, value) for areaid in self.areaids)

    def _dirty(self, areaid):
        self.modified[areaid] = True

    def clear_items(self):
        self.items = dict((areaid, {}) for areaid in self.areaids)
        self._set_all_dirty_flags(True)

    def add_item(self, item):
        self.items[item.areaid][item.position] = item
        self._dirty(item.areaid)

    def delete_item(self, item):
        try: del self.items[item.areaid][item.position]
        except KeyError:
            print('item [%s] does not exist!' % item)
        self._dirty(item.areaid)

    def delete_position(self, areaid, position):
        try: del self.items[areaid][position]
        except KeyError:
            print('position [%d, %s] does not exist!' % areaid, position)
        self._dirty(item.areaid)

    def save(self):
        for areaid, modified in self.modified.items():
            if not modified: continue
            write_items(areaid, self.items[areaid].values())

        # Reset dirty flags
        self._set_all_dirty_flags(False)

def grab_original_maps():
    areaids = list(range(10))
    import shutil
    import os
    BACKUP_DIR = 'original_maps/'
    for f in filter(lambda s : s.endswith('.map'), os.listdir(BACKUP_DIR)):
        shutil.copyfile(BACKUP_DIR+f, f)

def item_modification():
    areaids = list(range(10))
    mod = ItemModifier(areaids)

    mod.add_item(Item(
        position=(140,99),
        areaid=0,
        itemid=28,
    ))

    mod.add_item(Item(
        position=(141,99),
        areaid=0,
        itemid=28,
    ))

    mod.save()



if __name__ == '__main__':
    #grab_original_maps()
    print_all_items()
    #item_modification()