import random
import re
import json
import itemreader
import sys
import os
import argparse

def parse_args():
    args = argparse.ArgumentParser(description='Item Randomizer')
    args.add_argument('-output_dir', default='generated_maps', help='Output directory for generated maps')
    args.add_argument('-config_file', default='config.txt', help='Config file to use')
    args.add_argument('-seed', default=None, type=int, help='Random seed')
    args.add_argument('--no-write', dest='write', default=True, action='store_false', help='Flag to disable map generation, and do only map analysis')
    args.add_argument('--reset', action='store_true', help='Reset maps by copying the original maps to the output directory.')
    args.add_argument('--shuffle-music', action='store_true', help='Experimental: Shuffles the music in the map.')

    return args.parse_args(sys.argv[1:])

#   _____________________________
#  / :: ~~~~~~~~~~~~~~~~~~~~~ :: \
# | :: KEY DEFINITIONS - START :: |
# '''''''''''''''''''''''''''''''''

def define_variables(item_names):
    variables = {
        "TRUE": True,
        "FALSE": False,
        "ZIP_REQUIRED": False,
        "ADVANCED_TRICKS_REQUIRED": True,
        "BLOCK_CLIPS_REQUIRED": True,
        "POST_GAME_ALLOWED": True,
        "POST_IRISU_ALLOWED": True,
        "STUPID_HARD_TRICKS": False,
        "HALLOWEEN_REACHABLE": False,
        "WARP_DESTINATION_REACHABLE": False,
    }
    for item_name in item_names:
        variables[item_name] = False
    return variables

def define_custom_items():
    # Generally used for items that require you to exit to the shop before you can fully utilize it
    return {
        "WALL_JUMP_LV2": {
            "entry_prereq": "WALL_JUMP",
            "exit_prereq": "NONE",
        },
        "HAMMER_ROLL_LV3": {
            "entry_prereq": "HAMMER_ROLL",
            "exit_prereq": "NONE",
        },
        "BUNNY_STRIKE": {
            "entry_prereq": "SLIDING_POWDER",
            "exit_prereq": "NONE",
        },
        "AIR_DASH_LV3": {
            "entry_prereq": "AIR_DASH",
            "exit_prereq": "NONE",
        },
        "SPEED_BOOST": {
            "entry_prereq": "NONE",
            "exit_prereq": "NONE",
        },
    }

def define_default_expressions(variables):
    # Default expressions take priority over actual variables.
    # so if we parse an expression that has AIR_DASH, the default expression AIR_DASH will be used instead of the variable AIR_DASH.
    # however, the expressions parsed in define_default_expressions (just below) cannot use default expressions in their expressions.
    return {
        "ZIP": parse_expression("ZIP_REQUIRED", variables),
        "BLOCK_CLIP": parse_expression("BLOCK_CLIPS_REQUIRED", variables),
        "POST_GAME": parse_expression("POST_GAME_ALLOWED", variables),
        "STUPID": parse_expression("STUPID_HARD_TRICKS", variables),
        "ADVANCED": parse_expression("ADVANCED_TRICKS_REQUIRED", variables),
        "POST_IRISU": parse_expression("POST_IRISU_ALLOWED", variables),
        "HALLOWEEN": parse_expression("HALLOWEEN_REACHABLE", variables),
        "WARP_DESTINATION": parse_expression("WARP_DESTINATION_REACHABLE", variables),
        "BUNNY_STRIKE": parse_expression("BUNNY_STRIKE & PIKO_HAMMER", variables),
        "BUNNY_WHIRL": parse_expression("BUNNY_WHIRL & PIKO_HAMMER", variables),
        "AIR_DASH": parse_expression("AIR_DASH & PIKO_HAMMER", variables),
        "HAMMER_ROLL_LV3": parse_expression("HAMMER_ROLL_LV3 & BUNNY_WHIRL & PIKO_HAMMER", variables),
        "BOOST": parse_expression("TRUE", variables),
        #"RIBBON": parse_expression("TRUE", variables),
        #"WARP": parse_expression("TRUE", variables),
        #"EXIT_PROLOGUE": parse_expression("TRUE", variables),
        "TRUE": parse_expression("TRUE", variables),
        "FALSE": parse_expression("FALSE", variables),
        "NONE": parse_expression("TRUE", variables),
        "IMPOSSIBLE": parse_expression("FALSE", variables),
    }

#  _____________________________
# | :: KEY DEFINITIONS - END :: |
#  \ :: ~~~~~~~~~~~~~~~~~~~ :: /
#   '''''''''''''''''''''''''''

#   _________________________________
#  / :: ~~~~~~~~~~~~~~~~~~~~~~~~~ :: \
# | :: CONFIG FILE PARSING - START :: |
# '''''''''''''''''''''''''''''''''''''

def fail(message):
    print(message)
    sys.exit(1)

# Used in string parsing. We only have either strings or expressions
isExpr = lambda s : not type(s) is str

# & - and
# | - or
# !/~ - not
# ( ) - parentheses
# throws errors if parsing fails
def parse_expression(line, variables, default_expressions={}):
    try:
        # the str(line) cast is used because sometimes <line> is a u'unicode string' on unix machines.
        return parse_expression_logic(str(line), variables, default_expressions)
    except Exception as e:
        print('Error parsing expression:')
        print(line)
        raise e

def parse_expression_logic(line, variables, default_expressions):
    pat = re.compile('[()&|~!]')
    line = line.replace('&&', '&').replace('||', '|')
    tokens = (s.strip() for s in re.split('([()&|!~])', line))
    tokens = [s for s in tokens if s]
    # Stack-based parsing. pop from [tokens], push into [stack]
    # We push an expression into [tokens] if we want to process it next iteration.
    tokens.reverse()
    stack = []
    while len(tokens) > 0:
        next = tokens.pop()
        if isExpr(next):
            if len(stack) == 0:
                stack.append(next)
                continue
            head = stack[-1]
            if head == '&':
                stack.pop()
                exp = stack.pop()
                assert isExpr(exp)
                tokens.append(OpAnd(exp, next))
            elif head == '|':
                stack.pop()
                exp = stack.pop()
                assert isExpr(exp)
                tokens.append(OpOr(exp, next))
            elif head in '!~':
                stack.pop()
                tokens.append(OpNot(next))
            else:
                stack.append(next)
        elif next in '(&|!~':
            stack.append(next)
        elif next == ')':
            exp = stack.pop()
            assert isExpr(exp)
            assert stack.pop() == '('
            tokens.append(exp)
        else: # string literal
            if next in default_expressions:
                tokens.append(default_expressions[next])
            elif next not in variables:
                fail('Unknown variable %s in expression: %s' % (next, line))
            else:
                tokens.append(OpLit(next))
    assert len(stack) == 1
    return stack[0]


class OpLit(object):
    def __init__(self, name):
        self.name = name
    def evaluate(self, variables):
        return variables[self.name]
    def __str__(self):
        return self.name
    __repr__ = __str__

class OpNot(object):
    def __init__(self, expr):
        self.expr = expr
    def evaluate(self, variables):
        return not self.expr.evaluate(variables)
    def __str__(self):
        return '(NOT %s)' % self.expr
    __repr__ = __str__

class OpOr(object):
    def __init__(self, exprL, exprR):
        self.exprL = exprL
        self.exprR = exprR
    def evaluate(self, variables):
        return self.exprL.evaluate(variables) or self.exprR.evaluate(variables)
    def __str__(self):
        return '(%s OR %s)' % (self.exprL, self.exprR)
    __repr__ = __str__

class OpAnd(object):
    def __init__(self, exprL, exprR):
        self.exprL = exprL
        self.exprR = exprR
    def evaluate(self, variables):
        return self.exprL.evaluate(variables) and self.exprR.evaluate(variables)
    def __str__(self):
        return '(%s AND %s)' % (self.exprL, self.exprR)
    __repr__ = __str__


def read_file_and_strip_comments(filename):
    def strip_comments(line):
        if '//' not in line: return line
        return line[:line.find('//')]
    with open(filename) as f:
        lines = [strip_comments(line).strip() for line in f]
    return lines

def print_error(error, jsondata):
    import re
    pos = int(re.findall('char ([\\d]*)', error.__str__())[0])
    VIEW_RANGE = 100
    start = max(pos-VIEW_RANGE, 0)
    end = min(pos+VIEW_RANGE, len(jsondata))
    print('File parsing error')
    print(error)
    print('Error location:')
    print(jsondata[start:pos])
    print(jsondata[pos:end])

def parse_json(jsondata):
    try:
        return json.loads(jsondata)
    except ValueError as e:
        print_error(e, jsondata)
        raise e

# throws errors for invalid formats.
# returns a dict mapping each location to its prereqs.
def read_constraints(locations, variables, default_expressions, custom_items):
    lines = read_file_and_strip_comments('constraints.txt')
    jsondata = ' '.join(lines)
    jsondata = re.sub(',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split('}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'
    cdicts = parse_json(jsondata)

    DEFAULT_CONSTRAINT = Constraint(default_expressions['IMPOSSIBLE'], default_expressions['IMPOSSIBLE'])
    locations_set = set(locations)
    constraints = dict((location, DEFAULT_CONSTRAINT) for location in locations_set)
    for cdict in cdicts:
        assert cdict['location'] in locations_set, 'Unknown location: %s' % cdict['location']
        entry_expression = parse_expression(cdict['entry_prereq'], variables, default_expressions)
        exit_expression = parse_expression(cdict['exit_prereq'], variables, default_expressions)
        constraints[cdict['location']] = Constraint(entry_expression, exit_expression)

    for item_name, cdict in custom_items.items():
        assert item_name in locations_set, 'Unknown custom item: %s' % item_name
        entry_expression = parse_expression(cdict['entry_prereq'], variables, default_expressions)
        exit_expression = parse_expression(cdict['exit_prereq'], variables, default_expressions)
        constraints[item_name] = Constraint(entry_expression, exit_expression)

    return constraints

def read_config(variables, item_names, config_file='config.txt'):
    lines = read_file_and_strip_comments(config_file)
    jsondata = ' '.join(lines)
    jsondata = re.sub(',\s*]', ']', jsondata)
    jsondata = re.sub(',\s*}', '}', jsondata)
    config_dict = parse_json('{' + jsondata + '}')

    to_shuffle = config_dict['to_shuffle']
    must_be_reachable = set(config_dict['must_be_reachable'])
    settings = config_dict['settings']
    for key, value in settings.items():
        if key not in variables:
            fail('Undefined variable: %s' % key)
        if not type(value) is bool:
            fail('Variable %s does not map to a boolean variable in config.txt' % key)
        variables[key] = value

    if set(to_shuffle) - set(item_names):
        fail('\n'.join[
            'Unknown items defined in config:',
            '\n'.join(map(str, set(to_shuffle) - set(item_names))),
        ])

    if set(must_be_reachable) - set(item_names):
        fail('\n'.join[
            'Unknown items defined in config:',
            '\n'.join(map(str, set(must_be_reachable) - set(item_names))),
        ])

    return to_shuffle, must_be_reachable

def read_items():
    lines = read_file_and_strip_comments('all_items.txt')
    items = [itemreader.parse_item_from_string(line)
             for line in lines if line.lstrip().startswith('(')]
    return items
#  _________________________________
# | :: CONFIG FILE PARSING - END :: |
#  \ :: ~~~~~~~~~~~~~~~~~~~~~~~ :: /
#   '''''''''''''''''''''''''''''''

#   _________________________________________
#  / :: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ :: \
# | :: RANDOMIZER / ANALYSIS LOGIC - START :: |
# '''''''''''''''''''''''''''''''''''''''''''''

class Constraint(object):
    def __init__(self, entry_expression, exit_expression):
        self.entry_expression = entry_expression
        self.exit_expression = exit_expression

    def can_enter(self, variables):
        return self.entry_expression.evaluate(variables)

    def can_exit(self, variables, current_item_name):
        temp = variables[current_item_name]
        variables[current_item_name] = True
        result = self.exit_expression.evaluate(variables)
        variables[current_item_name] = temp
        return result

    def can_enter_and_exit(self, variables, current_item_name):
        return self.can_enter(variables) and \
               self.can_exit(variables, current_item_name)

    def __str__(self):
        return '\n'.join([
            'Entry: %s' % self.entry_expression,
            'Exit: %s' % self.exit_expression,
        ])

class LocationMap(object):
    def __init__(self, items, locations, variables, constraints):
        # name -> item mapping
        self.items = dict((item.name, item) for item in items)
        # default assignment assigns every item to its original location.
        self.assigned_locations = dict((location, location) for location in locations)
        self.locations = locations
        self.variables = dict(variables) # copy
        self.constraints = constraints

    def reassign(self, assignments):
        for location, item_name in assignments:
            self.assigned_locations[item_name] = location

    def validate_required_reachables(self, must_be_reachable):
        unreachable = self.compute_unreachable()
        return len(must_be_reachable & unreachable) == 0

    def compute_unreachable(self, analyzer=None):
        unreachable = set(self.locations) # copy
        to_remove = set()
        variables = dict(self.variables) # copy
        has_change = True

        while has_change:
            has_change = False
            for item_name in unreachable:
                location = self.assigned_locations[item_name]
                if self.constraints[location].can_enter_and_exit(variables, item_name):
                    # item can be reached.
                    to_remove.add(item_name)
                    has_change = True
            for item_name in to_remove:
                variables[item_name] = True
            if analyzer != None:
                analyzer.analyze(to_remove)
            unreachable -= to_remove
            to_remove.clear()

        if analyzer != None:
            analyzer.finish(unreachable)
        return unreachable

    # returns (new_items, assigned_locations)
    # new_items: items with newly-assigned locations
    # assigned_locations: item_name -> location map for analysis purposes.
    def compute_item_locations(self):
        new_items = []
        assigned_locations = {}
        for item_name, location in self.assigned_locations.items():
            if item_name not in self.items: continue # custom items are skipped
            new_item = self.items[item_name].copy()
            new_item.set_location(self.items[location])
            new_items.append(new_item)
            assigned_locations[item_name] = location

        analyzer = Analyzer()
        self.compute_unreachable(analyzer)
        return new_items, assigned_locations, analyzer

def mean(values):
    values = tuple(values)
    return float(sum(values))/len(values)

def is_xx_up(item_name):
    return bool(re.match('^[A-Z]*_UP', item_name))

def is_egg(item_name):
    return bool(item_name.startswith('EGG_'))

class Analyzer(object):
    def __init__(self):
        self.step_count = -1
        self.levels = []
        self.unreachable = None
    def analyze(self, to_remove):
        if len(to_remove) == 0: return
        self.step_count += 1
        self.levels.append(list(sorted(to_remove)))
    def finish(self, unreachable):
        self.unreachable = list(sorted(unreachable))
        self._post_process()
    def _post_process(self):
        item_levels = {}
        for level, items in enumerate(self.levels):
            for item_name in items:
                item_levels[item_name] = level
        self.item_levels = item_levels
    def average_hard_to_reach_step_count(self, hard_to_reach_items):
        return mean(self.item_levels[item_name] for item_name in hard_to_reach_items)
    def compute_hard_to_reach_items(self, actual_items):
        accepted_item_pool = set()
        item_pool = set()
        current_level = self.step_count
        while len(item_pool) < 5 and (len(item_pool) < 2 or self.step_count-current_level < 2):
            accepted_item_pool.update(item_pool)
            item_pool.update(item for item in self.levels[current_level]
                             if not is_xx_up(item) and not is_egg(item) and item in actual_items)
            current_level -= 1
        for item_name in item_pool:
            if len(accepted_item_pool) >= 5: break
            accepted_item_pool.add(item_name)
        return accepted_item_pool

# returns a LocationMap object
def randomize(items, locations, variables, to_shuffle, must_be_reachable, constraints, seed=None):
    items = list(items) # all actual items
    locations = list(locations) # actual items + custom items
    must_be_reachable = set(must_be_reachable)

    # shuffling
    to_shuffle = list(to_shuffle)
    target_locations = to_shuffle[:]

    if seed != None: random.seed(seed)
    location_map = LocationMap(items, locations, variables, constraints)
    attempts = 0
    while True:
        attempts += 1
        random.shuffle(target_locations)
        location_map.reassign(zip(target_locations, to_shuffle))
        if location_map.validate_required_reachables(must_be_reachable): break

    print('Computed after %d attempts' % attempts)
    return location_map

#  _________________________________________
# | :: RANDOMIZER / ANALYSIS LOGIC - END :: |
#  \ :: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ :: /
#   '''''''''''''''''''''''''''''''''''''''

def decide_difficulty(mean_important_level, true_step_count):
    score = mean_important_level + true_step_count
    if score >= 7:
        return 'V.HARD (%s)' % score
    if score >= 5.5:
        return 'HARD (%s)' % score
    if score >= 3.5:
        return 'MEDIUM (%s)' % score
    else:
        return 'EASY (%s)' % score

def print_allocation(assigned_locations):
    print('Assignment:')
    for item_name, location in assigned_locations.items():
        if item_name != location:
            print(" %s -> %s's location" % (item_name, location))

def print_analysis(analyzer, assigned_locations):
    # Print all item levels
    for index, items in enumerate(analyzer.levels):
        print('Level %d' % index)
        for item in items:
            print('  %s' % item)

    # Print all unreachable items
    print('Unreachable items:')
    print('\n'.join('  %s' % s for s in analyzer.unreachable))

    # Print select item levels
    items_to_check = [
        'PIKO_HAMMER',
        'SLIDING_POWDER',
        'CARROT_BOMB',
        'AIR_JUMP'
    ]
    for item_name in items_to_check:
        print('%s: level %d' % (item_name, analyzer.item_levels[item_name]))
    # Print steps needed to get everything
    print('Steps needed: %d' % analyzer.step_count)

    mean_important_level = mean(analyzer.item_levels[item_name] for item_name in items_to_check)
    print('Mean Important Levels: %f' % mean_important_level)

    actual_items = set(assigned_locations.keys())
    hard_to_reach_items = analyzer.compute_hard_to_reach_items(actual_items)
    print('Hard to reach:')
    print(hard_to_reach_items)

    true_step_count = analyzer.average_hard_to_reach_step_count(hard_to_reach_items)
    print('True Step Count: %f' % true_step_count)

    print('Difficulty: %s' % decide_difficulty(mean_important_level, true_step_count))

def generate_analysis_file(assigned_locations, analyzer, output_dir):
    actual_items = set(assigned_locations.keys())
    hard_to_reach_items = analyzer.compute_hard_to_reach_items(actual_items)
    important_items = ['PIKO_HAMMER', 'SLIDING_POWDER', 'CARROT_BOMB', 'AIR_JUMP']
    mean_important_level = mean(analyzer.item_levels[item_name] for item_name in important_items)
    true_step_count = analyzer.average_hard_to_reach_step_count(hard_to_reach_items)
    difficulty = decide_difficulty(mean_important_level, true_step_count)
    warnings = get_all_warnings(assigned_locations)

    file_lines = []
    def printline(line=''):
        print(line)
        file_lines.append(str(line))

    printline('-- analysis --')
    printline('Difficulty: %s' % difficulty)
    printline()
    printline('Hard to reach items:')
    for item in hard_to_reach_items:
        printline(item)
    printline()
    printline('Unreachable Items:')
    for item in analyzer.unreachable:
        if item.startswith('UNKNOWN'): continue # Skip DLC items
        printline(item)
    printline()
    for warning in warnings:
        printline('WARNING: %s' % warning)

    f = open('%s/%s' % (output_dir, 'analysis.txt'), 'w+')
    f.write('\n'.join(file_lines))
    f.close()


def get_all_warnings(assigned_locations):
    warnings = []
    if assigned_locations['CARROT_BOMB'] != 'CARROT_BOMB':
        warnings.append('Carrot bomb not in carrot bomb original location!')
    if assigned_locations['SLIDING_POWDER'] != 'SLIDING_POWDER':
        warnings.append('Sliding powder not in sliding powder original location!')
    warnings.append("Don't pick up rabi slippers if you see it before ribbon!")
    return warnings

# returns (new_items, assigned_locations)
# new_items: items with newly-assigned locations
# assigned_locations: item_name -> location map for analysis purposes.
def run_item_randomizer(seed=None, config_file='config.txt'):
    items = read_items()
    custom_items = define_custom_items()
    locations = [item.name for item in items] + list(custom_items.keys())
    item_names = locations
    variables = define_variables(item_names)
    default_expressions = define_default_expressions(variables)

    to_shuffle, must_be_reachable = read_config(variables, item_names, config_file=config_file)
    constraints = read_constraints(locations, variables, default_expressions, custom_items)

    location_map = randomize(items, locations, variables, to_shuffle, must_be_reachable, constraints, seed=seed)
    return location_map.compute_item_locations()

def generate_randomized_maps(seed=None, output_dir='.', config_file='config.txt', write_to_map_files=False, shuffle_music=False):
    if write_to_map_files and not os.path.isdir(output_dir):
        fail('Output directory %s does not exist' % output_dir)

    items, assigned_locations, analyzer = run_item_randomizer(seed=seed, config_file=config_file)
    areaids = list(range(10))
    assert len(set(item.areaid for item in items) - set(areaids)) == 0
    
    #print_allocation(assigned_locations)
    #print_analysis(analyzer, assigned_locations)
    #warnings = get_all_warnings(assigned_locations)
    #for warning in warnings:
        #print('WARNING: %s' % warning)

    if not write_to_map_files: return

    generate_analysis_file(assigned_locations, analyzer, output_dir)
    print('Analysis Generated...')

    source_dir = 'original_maps'
    itemreader.grab_original_maps(source_dir, output_dir)
    print('Maps copied...')
    mod = itemreader.ItemModifier(areaids, source_dir=source_dir, no_load=True, shuffle_music=shuffle_music)
    mod.clear_items()
    for item in items:
        mod.add_item(item)
    mod.save(output_dir)
    print('Maps saved successfully to %s.' % output_dir)

def reset_maps(output_dir='.'):
    if not os.path.isdir(output_dir):
        fail('Output directory %s does not exist' % output_dir)
    itemreader.grab_original_maps(output_dir)
    print('Original maps copied to %s.' % output_dir)

if __name__ == '__main__':
    args = parse_args()
    if args.reset:
        # copy over the default maps without randomization.
        reset_maps(
            output_dir=args.output_dir
        )
    else:
        generate_randomized_maps(
            seed=args.seed,
            output_dir=args.output_dir,
            config_file=args.config_file,
            write_to_map_files=args.write,
            shuffle_music=args.shuffle_music,
        )
