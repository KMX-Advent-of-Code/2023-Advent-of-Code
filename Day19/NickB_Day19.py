"""
Day 19: Aplenty
https://adventofcode.com/2023/day/19

Approach:
- Work with "interval pieces" which represent a range of x, m, a, s values
- Use objects for pieces, workflows, and rules to keep things reasonably organized
- Part 1 uses intervals that cover just one element
- Idea: when applying a rule to an interval piece, you split the piece into the part that follows the rule and the part that doesn't
"""

# Make sure to have the input in the file f'input{DAY}.txt'
DAY = 19

def split(s, line_char = '\n', block_char = '\n\n'):
    """Split into lines of input, or possibly into blocks of lines of input"""
    out = [block.split(line_char) for block in s.strip().split(block_char)]
    if len(out) == 1:
        return out[0]
    else:
        return out

class IntervalPiece:
    """Main piece object, holding x, m, a, s intervals"""
    def __init__(self, x_range, m_range, a_range, s_range):
        self.x_range = x_range
        self.m_range = m_range
        self.a_range = a_range
        self.s_range = s_range

    def __repr__(self):
        return f'{self.x_range} {self.m_range} {self.a_range} {self.s_range}'

    def size(self):
        """Product of sizes of the intervals"""
        return (self.x_range[1] - self.x_range[0] + 1) * (self.m_range[1] - self.m_range[0] + 1) * (self.a_range[1] - self.a_range[0] + 1) * (self.s_range[1] - self.s_range[0] + 1)

    def process_workflows(self, workflows):
        """Push ourselves through the workflows (splitting into smaller pieces along the way), and return a list of (piece, target) of the pieces and where they ended up"""
        open = [(self, 'in')]
        closed = []
        while open:
            piece, target = open.pop()
            _open = workflows[target].process_interval_piece(piece)
            for _piece, _target in _open:
                if _target in ('A', 'R'):
                    closed.append((_piece, _target))
                else:
                    open.append((_piece, _target))
        return closed

    def split(self, attribute, comparison, value):
        """Return piece1, piece2 where piece1 satisfies the condition and piece2 doesn't
        ex. variable = x, comparison = <, value = 10: then piece1 is the part that has x < 10 and piece2 has x >= 10
        If either piece has invalid ranges, instead return None for it
        """
        # set up starting point for the pieces, so I can restrict a single range when I apply the condition
        piece1 = IntervalPiece(self.x_range, self.m_range, self.a_range, self.s_range)
        piece2 = IntervalPiece(self.x_range, self.m_range, self.a_range, self.s_range)

        # easiest approach was manually coding all the cases
        match attribute:
            case 'x':
                match comparison:
                    case '>':
                        piece1.x_range = (max(piece1.x_range[0], value+1), piece1.x_range[1])
                        piece2.x_range = (piece2.x_range[0], min(piece2.x_range[1], value))
                    case '<':
                        piece1.x_range = (piece1.x_range[0], min(piece1.x_range[1], value-1))
                        piece2.x_range = (max(piece2.x_range[0], value), piece2.x_range[1])
            case 'm':
                match comparison:
                    case '>':
                        piece1.m_range = (max(piece1.m_range[0], value+1), piece1.m_range[1])
                        piece2.m_range = (piece2.m_range[0], min(piece2.m_range[1], value))
                    case '<':
                        piece1.m_range = (piece1.m_range[0], min(piece1.m_range[1], value-1))
                        piece2.m_range = (max(piece2.m_range[0], value), piece2.m_range[1])
            case 'a':
                match comparison:
                    case '>':
                        piece1.a_range = (max(piece1.a_range[0], value+1), piece1.a_range[1])
                        piece2.a_range = (piece2.a_range[0], min(piece2.a_range[1], value))
                    case '<':
                        piece1.a_range = (piece1.a_range[0], min(piece1.a_range[1], value-1))
                        piece2.a_range = (max(piece2.a_range[0], value), piece2.a_range[1])
            case 's':
                match comparison:
                    case '>':
                        piece1.s_range = (max(piece1.s_range[0], value+1), piece1.s_range[1])
                        piece2.s_range = (piece2.s_range[0], min(piece2.s_range[1], value))
                    case '<':
                        piece1.s_range = (piece1.s_range[0], min(piece1.s_range[1], value-1))
                        piece2.s_range = (max(piece2.s_range[0], value), piece2.s_range[1])

        # check if either piece is trivial
        if (piece1.x_range[0] > piece1.x_range[1]) | (piece1.m_range[0] > piece1.m_range[1]) | (piece1.a_range[0] > piece1.a_range[1]) | (piece1.s_range[0] > piece1.s_range[1]):
            piece1 = None
        if (piece2.x_range[0] > piece2.x_range[1]) | (piece2.m_range[0] > piece2.m_range[1]) | (piece2.a_range[0] > piece2.a_range[1]) | (piece2.s_range[0] > piece2.s_range[1]):
            piece2 = None
        
        return piece1, piece2

class Workflow:
    """Made up of rules"""
    def __init__(self, line):
        self.name, rules = tuple(line.replace(' ', '')[:-1].split('{'))
        self.rules = [Rule(rule) for rule in rules.split(',')]
        self.simplify_rules()

    def simplify_rules(self):
        """Extra step just to remove rules that don't do anything: ex. if the 2nd to last rule matched the final rule (the default case), remove it"""
        rule = self.rules[-1]
        assert rule.comparison is None
        target = rule.target

        while len(self.rules) > 1 and self.rules[-2].target == target:
            self.rules.pop(-2)

    def __repr__(self):
        return f"{self.name}: {', '.join([repr(rule) for rule in self.rules])}"

    def process_interval_piece(self, piece):
        """Return a list of (piece, target) after processing all the rules"""
        out = []
        for rule in self.rules:
            piece1, target, piece = rule.process_interval_piece(piece)
            if not piece1 is None:
                out.append((piece1, target))
            if piece is None:
                return out
        assert False
        
class Rule:
    """A single rule in a workflow
    The "default" rule has attribute, comparison, and value all None
    """
    def __init__(self, rule):
        if ':' in rule:
            condition, self.target = tuple(rule.split(':'))
            if '>' in condition:
                self.attribute, value = condition.split('>')
                self.comparison = '>'
                self.value = int(value)
            elif '<' in condition:
                self.attribute, value = condition.split('<')
                self.comparison = '<'
                self.value = int(value)
            else:
                assert False
        else:
            self.attribute = None
            self.comparison = None
            self.value = None
            self.target = rule

    def __repr__(self):
        if self.comparison is None:
            return f'to {self.target}'
        else:
            return f'{self.attribute} {self.comparison} {self.value} to {self.target}'

    def process_interval_piece(self, piece):
        """Return piece1, target, piece2 where piece1 gets assigned target and piece2 couldn't be assigned by this rule"""
        # trivial case
        if self.comparison is None:
            return piece, self.target, None

        # main case
        piece1, piece2 = piece.split(self.attribute, self.comparison, self.value)
        return piece1, self.target, piece2

def parse_line(line):
    """Parse a "piece" input line into the x, m, a, s for part 1"""
    x, m, a, s = tuple(line.replace(' ', '')[1:-1].split(','))
    x = int(x.split('=')[1])
    m = int(m.split('=')[1])
    a = int(a.split('=')[1])
    s = int(s.split('=')[1])
    return x, m, a, s

def part1(s):
    """Solve part 1"""
    # get pieces and workflows
    block_workflows, block_pieces = tuple(split(s))
    workflows = [Workflow(line) for line in block_workflows]
    workflows = {workflow.name : workflow for workflow in workflows}
    pieces = [IntervalPiece(*[[t, t] for t in parse_line(line)]) for line in block_pieces]

    # apply the workflows to the pieces
    results = [piece.process_workflows(workflows)[0] for piece in pieces]

    # narrow down to the pieces that ended up Accepted
    accepted = [piece for piece, target in results if target == 'A']

    # sum the attributes
    return sum([piece.x_range[0] + piece.m_range[0] + piece.a_range[0] + piece.s_range[0] for piece in accepted])
    
def part2(s):
    """Solve part 2"""
    # get workflows
    block_workflows, _ = tuple(split(s))
    workflows = [Workflow(line) for line in block_workflows]
    workflows = {workflow.name : workflow for workflow in workflows}

    # start with a piece for all the x, m, a, s values
    I = [1, 4000]
    piece = IntervalPiece(I, I, I, I)

    # process into a list of (piece, target)
    results = piece.process_workflows(workflows)

    # get sizes for the Accepted pieces
    sizes = [piece.size() for piece, target in results if target == 'A']
    
    return sum(sizes)
    

if __name__ == "__main__":
    with open(f'input{DAY}.txt', 'r') as f:
        s = f.read()
    print('Part 1 solution:')
    print(part1(s))
    print()
    print('Part 2 solution:')
    print(part2(s))
