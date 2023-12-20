"""
Day 20: Pulse Propagation
https://adventofcode.com/2023/day/20

The code is mainly for part 1, using several classes to organize things:
- Scheduler: the main brain, which keeps track of the modules and manages the queue of signals
- Module: generic module, with basic fields for name/inputs/outputs and a method for sending a signal which passes it to the scheduler 
- Broadcast: for the broadcaster module, nothing fancy (when it gets a signal, it passes it on to its outputs)
- FlipFlop: implements flip flop module logic for when the module receives a signal
- Conjunction: implements conjunction module logic for when the module receives a signal
- Null: module without any specific logic (this is what rx is)

The function set_up_modules creates the modules and scheduler: it's a bit of a mess, since I have to make the module objects and then go about linking their inputs/outputs

Part 1 solution: the scheduler keeps count of low and high signals, so just run 1,000 button presses and read off those numbers

Part 2 solution: I did this in a notebook, with the help of a SmartScheduler class which tracks when a few key modules send high signals
I did the following in the notebook:
- Print out some info of the modules that feed into rx: it's a few layers of conjunction modules, and you can check that when modules dj, rr, pb, nl give high signals we'll get a low signal from rx
- Ran the SmartScheduler for 100_000 button presses just to be sure I have enough data on dj, rr, pb, nl to find out when they give high signals
- For each of those modules, determine the period between high signals and when it first gives a high signal
- Since the periods match the times of the first high signals, an lcm of the periods gives the solution
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 20

from collections import deque 

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

def create_module_basic(line):
    """Parse a line of input into a "basic" module: just the name and the names of its outputs"""
    aux1, aux2 = tuple(line.replace(' ', '').split('->'))

    # which type of module, and the name
    match aux1[0]:
        case 'b':
            cls = Broadcast
            name = 'broadcaster'
        case '%':
            cls = FlipFlop
            name = aux1[1:]
        case '&':
            cls = Conjunction
            name = aux1[1:]
        case _:
            assert False

    # outputs
    outputs_names = aux2.split(',')

    # form the module
    module = cls(name)
    module.outputs_names = outputs_names

    return module

def set_up_modules(s):
    """Return a Scheduler object (holding all the module objects) for the problem"""
    # create the "basic" modules with outputs set by name
    modules = {}
    names = set()
    for line in split(s):
        module = create_module_basic(line)
        modules[module.name] = module
        for _name in module.outputs_names:
            names.add(_name)

    # set up any unmade modules
    unmade = names - set(modules.keys())
    if unmade:
        #print(f'Modules {unmade} were not made yet, making Null modules')
        for name in unmade:
            modules[name] = Null(name)

    # set the inputs by name
    for name in modules.keys():
        for _name in modules[name].outputs_names:
            modules[_name].inputs_names.append(name)

    # set the inputs and outputs by reference to the objects
    for name in modules.keys():
        module = modules[name]
        module.inputs = [modules[_name] for _name in module.inputs_names]
        module.outputs = [modules[_name] for _name in module.outputs_names]

    # set the states for any conjunction modules: the Conjunction class needed its inputs to be set first
    for module in modules.values():
        try:
            module.set_states()
        except:
            pass

    # set up the scheduler
    scheduler = Scheduler(modules)
    for module in modules.values():
        module.scheduler = scheduler
    
    return scheduler

class Scheduler:
    """The main brains, handling the queue of signals; keeps a dictionary of all the modules so it knows where to send signals"""
    
    def __init__(self, modules):
        self.modules = modules
        self.names = list(modules.keys())
        self.queue = deque()
        self.low_count = 0
        self.high_count = 0
        self.button_pushes = 0
        self.debug = False

    def button_push(self):
        """Push the button once"""
        assert len(self.queue) == 0
        self.button_pushes += 1
        self.low_count += 1
        self.queue.append((Null('button'), 0, self.modules['broadcaster']))
        self.process()

    def process(self):
        """Process the queue of signals"""
        while self.queue:
            module_from, pulse, module_to = self.queue.popleft()
            if self.debug:
                print(f'{module_from.name} sends {pulse} to {module_to.name}')
            module_to.receive(pulse, module_from)

    def send(self, module_from, pulse, module_to):
        """Send a signal, i.e. tack it onto the end of the queue"""
        assert pulse in (0, 1)

        # record low or high pulse
        if pulse == 0:
            self.low_count += 1
        else:
            self.high_count += 1

        # add it to the queue
        self.queue.append((module_from, pulse, module_to))

class SmartScheduler(Scheduler):
    """A scheduler that tracks when the key modules for part 2 give high signals"""

    TRACK = ['dj', 'rr', 'pb', 'nl']

    def __init__(self, scheduler):
        super().__init__(scheduler.modules)
        self.histories = {name : [] for name in self.TRACK}

    def send(self, module_from, pulse, module_to):
        name = module_from.name
        if name in self.TRACK and pulse == 0:
            self.histories[name].append(self.button_pushes)
        super().send(module_from, pulse, module_to)

class Module:
    """Generic module"""
    
    def __init__(self, name):
        self.name = name
        self.inputs_names = []
        self.outputs_names = []
        self.inputs = []
        self.outputs = []
        self.scheduler = None

    def receive(self, pulse, module):
        """Receive a pulse from a module: set this in subclasses"""
        assert False
        
    def send(self, pulse):
        """Send a pulse to all its outputs: just passes things to the scheduler"""
        for module in self.outputs:
            self.scheduler.send(self, pulse, module)

class Broadcast(Module):
    """Broadcast module"""
    
    def receive(self, pulse, module):
        self.send(pulse)

class FlipFlop(Module):
    """FlipFlop module"""
    
    def __init__(self, name):
        """Internal state for the flip flop logic"""
        super().__init__(name)
        self.state = False # False for 'off', True for 'on'

    def receive(self, pulse, module):
        """Flip flop logic when it receives a signal"""
        # do something only if it was a low pulse
        if pulse == 0:
            # update state
            self.state = not self.state

            # send pulses according to the state we ended up in
            self.send(int(self.state))

class Conjunction(Module):
    """Conjunction module"""
    
    def __init__(self, name):
        super().__init__(name)
        self.states = None

    def set_states(self):
        """Internal states for the conjunction logic"""
        self.states = {module.name : 0 for module in self.inputs}
        
    def receive(self, pulse, module):
        """Conjunction logic when it receives a signal"""
        # update memory for this module
        self.states[module.name] = pulse

        # decide which pulse to send: 0 only if every input is in state 1
        pulse_send = 0
        for state in self.states.values():
            if state == 0:
                pulse_send = 1
                break

        # send the pulse
        self.send(pulse_send)

class Null(Module):
    """Null module"""
    
    def receive(self, pulse, module):
        pass

def part1(s):
    """Solve part 1"""
    scheduler = set_up_modules(s)
    [scheduler.button_push() for _ in range(1000)]
    low = scheduler.low_count
    high = scheduler.high_count
    return low * high
    
def part2(s):
    """Solve part 2"""
    # the print outs that tell me to focus on when dj, rr, pb, nl give high signals
    # note how after these nodes things get complicated, so I just focused on them and hoped that this would be enough
    print()
    print('-' * 50)
    print('Understanding the modules that feed into rx')
    scheduler = set_up_modules(s)
    layers = [
        ['rx'],
        ['ns'],
        ['dc', 'rv', 'vp', 'cq'],
        ['dj', 'rr', 'pb', 'nl']
    ]
    for layer in layers:
        for name in layer:
            module = scheduler.modules[name]
            print(name, module.__class__, 'has inputs', module.inputs_names)
        print()

    # use the SmartScheduler to run 100_000 button presses and track when dj, rr, pb, nl give high signals
    scheduler = SmartScheduler(set_up_modules(s))
    for module in scheduler.modules.values():
        module.scheduler = scheduler
    [scheduler.button_push() for _ in range(100_000)]

    # checking the spacing between the low signals, they're consistent
    print()
    print('-' * 50)
    print('Checking periods')
    import numpy as np
    for name in scheduler.TRACK:
        history = scheduler.histories[name]
        print(np.diff(sorted(set(history))))

    # and we can verify those periods are also the first button press that these modules got low signals
    print()
    print('-' * 50)
    print('Checking first high signal times')
    for name in scheduler.TRACK:
        history = scheduler.histories[name]
        print(history[0])

    # so a simple lcm gives the answer
    print()
    print('-' * 50)
    print('Solution:')
    from math import lcm
    return lcm(3797, 4051, 3847, 3877)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
