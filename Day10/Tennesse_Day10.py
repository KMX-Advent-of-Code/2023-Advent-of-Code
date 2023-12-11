"""
Day 10: Pipe Maze
https://adventofcode.com/2023/day/10
"""
from utilities import run_aoc
import networkx as nx


def run_part1(input_text: str) -> int:
    """Find the loop which contains the starting position, and return the
    distance to the farther node on that loop.
    """
    G, starting_position = parse_input(input_text)
    shortest_paths = nx.shortest_path(G, starting_position)
    distances = {node: len(path) - 1 for node, path in shortest_paths.items()}
    farthest_node = max(distances, key=distances.get)
    # Display the path discovered for debugging purposes.
    display(input_text, set(shortest_paths[farthest_node]))
    return max(distances.values())


def run_part2(input_text: str) -> int:
    """Count the number of squares enclosed by the loop.

    The main observation is that if you draw a line from any
    given point to the outside, it'll cross the loop an even number
    of times if the point is on the exterior of the loop, and an odd
    number of times if it's on the interior.
    """
    G, starting_position = parse_input(input_text)
    # Find the set of nodes that are part of the loop.
    loop = set(nx.shortest_path(G, starting_position).keys())
    # Process rows one at a time. Move from left to right, and keep track
    # of how many times we've crossed the loop (odd = inside, even = outside).
    interior = set()
    for i, line in enumerate(input_text.splitlines()):
        inside = False
        for j, char in enumerate(line):
            if char == "S":
                char = get_node_type(G, (i, j))
            if (i, j) not in loop:
                if inside:
                    interior.add((i, j))
            elif char in "|LJ":
                inside = not inside
    display(input_text, loop, interior)
    return len(interior)


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse a nx.Graph from the input text."""
    lines = input_text.splitlines()
    num_rows = len(lines)
    num_cols = len(lines[0])
    starting_position = None
    G = nx.grid_2d_graph(num_rows, num_cols)
    # Loop through the characters in the input, and add edges to the
    # graph based on the directionality of the characters.
    #
    # It requires two connections for an edge to count. The edge is
    # created on the first connection, but if the second connection
    # is never made it'll get deleted at the end.
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "|":
                mark_edge(G, ((i, j), (i - 1, j)))
                mark_edge(G, ((i, j), (i + 1, j)))
            elif char == "-":
                mark_edge(G, ((i, j), (i, j - 1)))
                mark_edge(G, ((i, j), (i, j + 1)))
            elif char == "L":
                mark_edge(G, ((i, j), (i - 1, j)))
                mark_edge(G, ((i, j), (i, j + 1)))
            elif char == "J":
                mark_edge(G, ((i, j), (i - 1, j)))
                mark_edge(G, ((i, j), (i, j - 1)))
            elif char == "7":
                mark_edge(G, ((i, j), (i + 1, j)))
                mark_edge(G, ((i, j), (i, j - 1)))
            elif char == "F":
                mark_edge(G, ((i, j), (i + 1, j)))
                mark_edge(G, ((i, j), (i, j + 1)))
            if char == ".":
                continue
            elif char == "S":
                starting_position = (i, j)
                mark_edge(G, ((i, j), (i - 1, j)))
                mark_edge(G, ((i, j), (i, j - 1)))
                mark_edge(G, ((i, j), (i + 1, j)))
                mark_edge(G, ((i, j), (i, j + 1)))
    assert starting_position is not None
    # Remove any edges that were only connected once.
    for e in list(G.edges):
        if "count" not in G.edges[e] or G.edges[e]["count"] < 2:
            G.remove_edge(*e)
    return G, starting_position


def mark_edge(G, e):
    """Increment the count of the edge in the graph, or add it if it doesn't
    exist yet."""
    if e not in G.edges:
        return
    if "count" not in G.edges[e]:
        G.edges[e]["count"] = 1
    else:
        G.edges[e]["count"] += 1


def display(input_text, mask, interior=tuple()):
    """Display the path discovered for debugging purposes."""
    output = ""
    for i, line in enumerate(input_text.splitlines()):
        for j, char in enumerate(line):
            if (i, j) in mask:
                output += char
            elif (i, j) in interior:
                output += "I"
            else:
                output += " "
        output += "\n"
    with open("output.txt", "w") as f:
        f.write(output)


def get_node_type(G, node):
    """Deduce which node type the starting node is, based on the
    neighbors it connects to.
    """
    assert len(G.edges(node)) == 2
    i, j = node
    edges = list(G.neighbors(node))
    if edges == [(i, j - 1), (i, j + 1)]:
        return "-"
    elif edges == [(i - 1, j), (i + 1, j)]:
        return "|"
    elif edges == [(i - 1, j), (i, j + 1)]:
        return "L"
    elif edges == [(i - 1, j), (i, j - 1)]:
        return "J"
    elif edges == [(i + 1, j), (i, j - 1)]:
        return "7"
    elif edges == [(i + 1, j), (i, j + 1)]:
        return "F"
    else:
        raise ValueError(edges)


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
