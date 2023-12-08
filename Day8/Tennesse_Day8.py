"""
Day 8: Haunted Wasteland
https://adventofcode.com/2023/day/8
"""
import logging
import math
from utilities import run_aoc
import itertools


def run_part1(input_text: str) -> int:
    """Follow the instructions and find the path from AAA to ZZZ."""
    instructions, network = parse_input(input_text)
    logging.debug(instructions)
    logging.debug(network)
    node = "AAA"
    for i, direction in enumerate(itertools.cycle(instructions)):
        logging.debug(f"{i=}, {node=}, {direction=}")
        if node == "ZZZ":
            break
        node = network[node][direction]
    return i


def run_part2(input_text: str) -> int:
    """Follow the instructions from each starting node, wait for
    it to enter a cycle. Then return the least common multiple,
    which is the number of steps it takes for all ghosts to
    simultaneously reach an ending node.
    """
    instructions, network = parse_input(input_text)
    starting_nodes = [n for n in network if n[-1] == "A"]
    ending_nodes = {n for n in network if n[-1] == "Z"}
    logging.debug("Found %s instructions", len(instructions))
    logging.debug("Found %s nodes", len(network))
    logging.debug("Found %s starting nodes: %s", len(starting_nodes), starting_nodes)
    logging.debug("Found %s ending nodes: %s", len(ending_nodes), ending_nodes)
    cycles = []
    for node in starting_nodes:
        logging.debug("Starting at %s", node)
        previous_states_set = set()
        previous_states_list = []
        ending_node_indices = []
        for i, direction in enumerate(itertools.cycle(instructions)):
            state = (node, i % len(instructions))
            if state in previous_states_set:
                # We've found a cycle! Record where it starts and how long it is.
                cycle_offset = previous_states_list.index(state)
                cycle_length = i - cycle_offset
                ending_nodes_in_cycle = [
                    n for n in ending_node_indices if n >= cycle_offset
                ]
                cycles.append((cycle_offset, cycle_length, ending_nodes_in_cycle))
                break
            previous_states_set.add(state)
            previous_states_list.append(state)
            if node in ending_nodes:
                # This is an ending node. Record the index.
                ending_node_indices.append(i)
            # Move the next node.
            node = network[node][direction]
    for cycle_offset, cycle_length, ending_nodes_in_cycle in cycles:
        logging.debug(
            "Found cycle of length %s starting at %s, ending at %s",
            cycle_length,
            cycle_offset,
            ending_nodes_in_cycle,
        )
    # Turns out the network is structured in a way that makes things
    # easy. Each starting node falls into a cycle fairly quickly
    # (within 10 steps), and each cycle visits only one ending node.
    # Furthermore, the first step when the ending node is visited just
    # happens to coincide with the cycle length.
    #
    # Given all of that, it's sufficient to just find the least common
    # multiple of the cycle lengths. That's not a fully general solution,
    # for an arbitrary network though.
    return math.lcm(*[cycle_length for _, cycle_length, _ in cycles])


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """Parse the instructions and network from the input text."""
    lines = input_text.split("\n")
    instructions = [0 if c == "L" else 1 for c in lines[0]]
    network = {line[:3]: (line[7:10], line[12:15]) for line in lines[2:]}
    return instructions, network


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
