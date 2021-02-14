#!/usr/bin/env python

# Reads the checksum from a Sega Genesis binary ROM file
# and compares it to the computed checksum. If there is a
# mismatch, the script will ask the user if they want to
# update the checksum to the "correct" computed value.
#
# Resources:
#   - http://www.emulatronia.com/doctec/consolas/megadrive/genesis_rom.txt
#   - https://web.stanford.edu/group/htgg/cgi-bin/drupal/?q=node/1179
#   - https://segaretro.org/Checksum
import argparse
import os
import struct

# The fixed offset into a Genesis file where the checksum metadata is stored.
CHECKSUM_HEADER_OFFSET = 0x18E


def main():
  parser = argparse.ArgumentParser(description='Compares (and optionally '
                                               'corrects) the checksum for a '
                                               'Sega Genesis ROM.')
  parser.add_argument('path', nargs=1, help='Relative file path to the Sega '
                                            'Genesis ROM binary.')
  args = parser.parse_args()

  print('Reading checksum from file...')
  with open(args.path[0], 'r+b') as genesis_file:
    valid_genesis_file = verify_console_name_from_header(genesis_file)
    if not valid_genesis_file:
      print('\nERROR: File is not a valid Genesis or Mega Drive ROM file.')
      return

    header_checksum = read_checksum_from_header(genesis_file)
    print('Header checksum =',)
    print_word(header_checksum)

    print('Computing checksum...')
    computed_checksum = compute_checksum(genesis_file)
    print('Computed checksum = ',)
    print_word(computed_checksum)

    if header_checksum == computed_checksum:
      print('\nChecksums match. Horray!')
      return

    print('\nWARNING: Checksums do not match!')
    while(1):
      data = input('\nWould you like to update the header checksum to match'
                       'match the computed checksum? (y/n)')
      if data == 'n':
        return
      if data != 'y':
        continue

      print('\nWriting computed checksum to header...')
      write_checksum_to_header(genesis_file, computed_checksum)
      print('Writing complete. The header should now be updated.')
      print('Verifying header checksum...')
      header_checksum = read_checksum_from_header(genesis_file)
      if header_checksum == computed_checksum:
        print('\nChecksums match. Horray!')
        return
      print('\nERROR: Failed to write to file. Are you sure you have '
            'permission?')
      print('Aborting script...')
      return


def print_word(word):
  """Prints a hexidecimal representation of a WORD.

  Args:
    word: A integer containing a WORD value.
  """
  print('0x{0:04X}'.format(word))


def read_byte_as_int(open_file):
  """Read a BYTE from an opened file, as an int.

  Args:
    open_file: An opened file object from `open()`.

  Returns:
    An integer containing the BYTE value.
  """
  return ord(open_file.read(1))


def read_word_as_int(open_file):
  """Read a WORD from an opened file, as an int.

  Args:
    open_file: An opened file object from `open()`.

  Returns:
    An integer containing the WORD value.
  """
  high_bits = read_byte_as_int(open_file) << 8
  low_bits = read_byte_as_int(open_file)
  return high_bits | low_bits


def read_checksum_from_header(open_file):
  """Read the checksum value stored in the header metadata of the file.

  Args:
    open_file: An opened file object referencing the binary ROM for a genesis
               game.

  Returns:
    An integer containing the checksum value.
  """
  open_file.seek(CHECKSUM_HEADER_OFFSET)
  return read_word_as_int(open_file)

def read_checksum_from_header(open_file):
  """Read the checksum value stored in the header metadata of the file.

  Args:
    open_file: An opened file object referencing the binary ROM for a genesis
               game.

  Returns:
    An integer containing the checksum value.
  """
  open_file.seek(CHECKSUM_HEADER_OFFSET)
  return read_word_as_int(open_file)


def verify_console_name_from_header(open_file):
  """Verify an `open_file` is a valid Genesis rom, by reading the console name
  from the file's header.

  Args:
    open_file: An opened file object referencing the binary ROM for a genesis
               game.

  Returns:
    True if the header of `open_file` contains the correct console name in the
    right location.
  """
  memorybuffer = open_file.read()
  console_name = memorybuffer[0x100:0x110].decode('utf-8')
  if console_name == "SEGA MEGA DRIVE":
    return True
  if console_name == "SEGA GENESIS":
    return True
  return False


def compute_checksum(open_file):
  """Computes the checksum manually from a given Sega Genesis file.

  Args:
    open_file: An opened file object referencing the binary ROM for a genesis
               game.

  Returns:
    An interger containing the checksum value.
  """
  CHECKSUM_CALCULATION_START_OFFSET = 0x200
  open_file.seek(CHECKSUM_CALCULATION_START_OFFSET)

  checksum = 0
  file_size = os.path.getsize(open_file.name)
  NUM_BYTES_PER_WORD = 2
  for i in range(open_file.tell(), file_size, NUM_BYTES_PER_WORD):
    word = read_word_as_int(open_file)
    checksum += word

  # Extract the checksum as the lowest 16 bits of the result.
  WORD_MASK = 65535
  return checksum & WORD_MASK


def write_checksum_to_header(open_file, checksum):
  """Writes the computed `checksum` into the header metadata of `open_file`.

  Args:
    open_file: An opened file object referencing the binary ROM for a genesis
               game.
    checksum: An integer representing the computer checksum, as a WORD, to write
              to the `open_file` header metadata.
  """
  open_file.seek(CHECKSUM_HEADER_OFFSET)
  open_file.write(struct.pack('>H', checksum))


main()
