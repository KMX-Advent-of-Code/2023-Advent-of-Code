"""
Day 5: If You Give A Seed A Fertilizer
https://adventofcode.com/2023/day/5
"""
import logging
from utilities import run_aoc
from dataclasses import dataclass


def run_part1(input_text: str) -> int:
    """
    Map the seeds to locations according to the chain of maps, and return
    the smallest location.
    """
    seeds, maps = parse_input(input_text)
    # Loop through each of the seeds.
    locations = []
    for num in seeds:
        logging.debug("Starting with seed: %s", num)
        # Apply each map.
        for m in maps:
            num = map_int(num, m)
            logging.debug("Mapped to: %s", num)
        logging.debug("Ended at location: %s", num)
        # Keep track of the final location.
        locations.append(num)
    # Return the smallest location.
    return min(locations)


def run_part2(input_text: str) -> int:
    """
    This is a more efficient version of part 1, which maps intervals of seeds
    instead of individual seeds.
    """
    seeds, maps = parse_input(input_text)
    # Convert pairs of numbers to interval objects.
    intervals = [
        Interval(start, start + len) for start, len in zip(seeds[::2], seeds[1::2])
    ]
    logging.debug("Starting intervals: %s", intervals)

    # Apply each map in sequence to the list of intervals.
    for m in maps:
        logging.debug("Applying map: %s", m)
        intervals = map_intervals(intervals, m)
    # Return the smallest location.
    return min([i.start for i in intervals])


def parse_input(input_text: str):
    """
    Parse the input text into a list of seeds and a list of maps.
    """
    lines = input_text.split("\n")

    # Parse the seeds.
    seeds = [int(s) for s in lines[0].split(": ")[1].split()]
    logging.debug("Seeds: %s", seeds)

    # Parse the maps.
    maps = []
    current_map = None
    for line in lines[1:]:
        if line.endswith("map:"):
            # Start a new map section.
            current_map = []
            maps.append(current_map)
        elif line.strip():
            # Add a row to the current map.
            current_map.append(MapRow.from_line(line))

    # Log the maps for debugging.
    for m in maps:
        logging.debug("Parsed map with %s rows", len(m))

    return seeds, maps


@dataclass
class Interval:
    """Helper class for representing a range of consecutive integers."""

    start: int
    end: int

    def __add__(self, num):
        """Shift both endpoints of the interval."""
        return Interval(self.start + num, self.end + num)

    def __contains__(self, num):
        """Check if a number is in the interval."""
        return self.start <= num <= self.end

    def intersection(self, other):
        """Return the intersection of two intervals, or None if they don't overlap."""
        start = max(self.start, other.start)
        end = min(self.end, other.end)
        if start <= end:
            return Interval(start, end)

    def __lt__(self, other):
        """Define a total order on intervals, for sorting."""
        if self.start == other.start:
            return self.end < other.end
        else:
            return self.start < other.start


@dataclass
class MapRow:
    """Helper class for representing a row of a map."""

    interval: Interval
    offset: int

    @classmethod
    def from_line(cls, line: str):
        """Parse a line of the input into a MapRow."""
        dest_start, source_start, length = map(int, line.strip().split())
        return cls(
            interval=Interval(source_start, source_start + length - 1),
            offset=dest_start - source_start,
        )

    def split_interval(self, source: Interval) -> tuple[list[Interval], list[Interval]]:
        """
        Split an interval into the part that maps and the part that doesn't.
        This is the core logic for applying a map to an interval.
        """
        if source.intersection(self.interval) is None:
            return [source], []
        unmapped = []
        mapped = []
        if source.start < self.interval.start:
            unmapped.append(Interval(source.start, self.interval.start - 1))
        if source.end > self.interval.end:
            unmapped.append(Interval(self.interval.end + 1, source.end))
        intersection = source.intersection(self.interval)
        if intersection:
            mapped.append(intersection + self.offset)
        return unmapped, mapped


def map_int(num: int, rows: list[MapRow]) -> int:
    """Map a single integer according to a list of map rows."""
    for row in rows:
        if num in row.interval:
            return num + row.offset
    return num


def map_intervals(intervals: list[Interval], rows: list[MapRow]) -> list[Interval]:
    """Map a list of intervals according to a list of map rows."""
    # Copy to avoid modifying the input.
    unmapped_intervals = intervals.copy()
    # Array to store the mapped output.
    mapped_intervals = []
    for row in rows:
        # Copy to avoid modifying while iterating through the array.
        to_map = unmapped_intervals
        unmapped_intervals = []
        # Apply the map to each interval.
        for interval in to_map:
            new_unmapped, new_mapped = row.split_interval(interval)
            # Unmapped intervals are added back to the list to be
            # processed by subsequent map rows.
            unmapped_intervals.extend(new_unmapped)
            # Map intervals are added to the output. They won't be
            # processed by subsequent map rows, since only the
            # first row that they intersect with should map them.
            mapped_intervals.extend(new_mapped)
            # Log for debugging.
            if new_mapped:
                logging.debug(
                    "Split %s into %s and %s",
                    interval,
                    new_unmapped,
                    new_mapped,
                )
            else:
                logging.debug("No change to %s", interval)
    # Return both the mapped and unmapped intervals, sorted lexographically.
    return sorted(unmapped_intervals + mapped_intervals)


if __name__ == "__main__":
    run_aoc(run_part1, run_part2)
