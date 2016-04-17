#!/usr/bin/env python
# Copyright (c) 2016 by Ken Guyton.  All Rights Reserved.

"""Flip items in a list until all have the same orientation"""

# coding: utf-8

from __future__ import print_function
from __future__ import absolute_import, division, unicode_literals

import argparse
import re
import sys

FIRST_DOWN_ITEMS = re.compile(r'^(\-+)')
FIRST_UP_ITEMS = re.compile(r'^(\++)')
LEGAL_STACK = re.compile(r'^[\-\+]*$')


class CharacterError(Exception):
  """An illegal character, not + or -, was found."""


def get_args():
  """Parse command line arguments."""

  parser = argparse.ArgumentParser()
  parser.add_argument('--items',
                      help='A str representing a list of items like "--+--+".')
  parser.add_argument('--experiments', default=False, action='store_true',
                      help='Run a set of flipping experiments.')
  parser.add_argument('--verbose', default=False, action='store_true',
                      help='Output the set for each number * i.')
  parser.add_argument('--data', default=False, action='store_true',
                      help='Process a sequence of input sequences.')
  parser.add_argument('--fix',
                      help=('Provide a stack of items like "--+--+" to be '
                            'converted to all "+".'))
  return parser.parse_args()


def split_items(num, items):
  """Split off the first num items in the sequence.

  Args:
    num: int.  Split into a list of num.
    items: str. A str of "+" and "=".

  Returns:
    Two str which are sequences, the first with the first num items
    and the second with the remaining items.
  """

  return items[:num], items[num:]


def flip_char(char):
  """Flip a single character."""

  if char == '+':
    return '-'
  elif char == '-':
    return '+'
  else:
    raise CharacterError(char)


def flip_chars(items):
  """Flip all chars in an input str of items."""

  return ''.join([flip_char(x) for x in items])


def reverse_items(items):
  """Reverse the sequence of items."""

  return ''.join(reversed(items))


def stack_flip(index, items):
  """Take the first index items and flip them over.

  Args:
    index: int. Index of the last item in the part to flip.
    items: list of str.  List of + and - chars.
  Returns:
    A new list with the items up to i flipped and the individual
    states flipped as well.
  """

  part1, part2 = split_items(index, items)
  flipped_part1 = flip_chars(reverse_items(part1))

  return flipped_part1 + part2


def flip_and_print(index, items, verbose=True):
  """Stack_flip and print.

  Args:
    index: int. Flip up to this item.
    items: str. Representation of the stack as + and -.
    verbose: bool. True if the resulting stack of items
  """

  items = stack_flip(index, items)
  if verbose:
    print(items)

  return items


def first_down(items):
  """Return True if the first item is down."""

  return items[0] == '-'


def count_down_items(items):
  """Return the number of items that are down."""

  match = FIRST_DOWN_ITEMS.search(items)
  if match:
    return len(match.group(1))
  else:
    return 0


def count_up_items(items):
  """Return the number of items that are up."""

  match = FIRST_UP_ITEMS.search(items)
  if match:
    return len(match.group(1))
  else:
    return 0


def all_up(up_count, items):
  """Return True if all items are up.

  Args:
    up_count: int. The number of first items that are up. From
      count_up_items().
    items: list of str.  List of + and - chars.
  Returns:
    A bool that is True if all of the items are up, indidicating we are
    finished.
  """

  return len(items) == up_count


def first_experiments():
  """A first set of flipping experiments."""

  items = '--+--+'
  print(items)
  items = flip_and_print(2, items)
  items = flip_and_print(3, items)
  items = flip_and_print(5, items)
  print()

  items = '--++-+'
  print(items)
  items = flip_and_print(2, items)
  items = flip_and_print(4, items)
  items = flip_and_print(5, items)
  print()

  items = '----+-'
  print(items)
  items = flip_and_print(4, items)
  items = flip_and_print(5, items)
  items = flip_and_print(6, items)
  print()

  items = '-+-+-+'
  print(items)
  items = flip_and_print(1, items)
  items = flip_and_print(2, items)
  items = flip_and_print(3, items)
  items = flip_and_print(4, items)
  items = flip_and_print(5, items)
  print()


def fix_stack(items, verbose=True):
  """Flip until all items are up.

  Args:
    items: str. Representation of stack as + and -.
    verbose: bool.  True if printing should be turned off.
  Returns:
    An int which is the flip_count.
  """

  match = LEGAL_STACK.search(items)
  if not match:
    raise CharacterError('Not a legal stack: {0}'.format(items))

  flip_count = 0
  finished = False
  if first_down(items):
    down_count = count_down_items(items)
    if verbose:
      print('{0} '.format(down_count), end='')
    items = flip_and_print(down_count, items, verbose=verbose)
    flip_count += 1

  up_count = count_up_items(items)
  finished = all_up(up_count, items)
  while not finished:
    if verbose:
      print('{0} '.format(up_count), end='')
    items = flip_and_print(up_count, items, verbose=verbose)
    flip_count += 1

    down_count = count_down_items(items)
    if verbose:
      print('{0} '.format(down_count), end='')
    items = flip_and_print(down_count, items, verbose=verbose)
    flip_count += 1

    up_count = count_up_items(items)
    finished = all_up(up_count, items)

  return flip_count


def process_input_data_stream():
  """Read a data stream from stdin of a count and then numbers.

  The first line of the input is a count of the the upcoming input numbers
  then each line is one of those numbers to process.

  Output Case #n: <result>
  """

  count = int(sys.stdin.readline().strip())

  case = 0
  for stack_raw in sys.stdin:
    case += 1
    if case > count:
      sys.exit(0)

    stack = stack_raw.strip()
    flip_count = fix_stack(stack, verbose=False)
    print('Case #{0}: {1}'.format(case, flip_count))


def main():
  """Find the first multiple when all digits have been seen."""

  try:
    opts = get_args()
    if opts.experiments:
      first_experiments()
    elif opts.fix:
      print('  {0}'.format(opts.fix))
      flip_count = fix_stack(opts.fix)
      print('Flips: {0}'.format(flip_count))
    elif opts.data:
      process_input_data_stream()
  except CharacterError as msg:
    sys.stderr.write('\nThere was a character error:\n{0}\n'.format(msg))
    sys.exit(1)


if __name__ == '__main__':
  main()
