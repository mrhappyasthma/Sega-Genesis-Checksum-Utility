# Sega Genesis Checksum Utility
A simple command line utility to verify (or correct) Sega Genesis ROM checksums.

# Example Usage

Simply execute the script with a single argument: the relative path to a Sega Genesis or Sega Mega Drive binary ROM file.

```
python sega_genesis_checksum_utility.py <path_to_file>
```

Or on Linux, you can simply execute the file as an executable:

```
./sega_genesis_checksum_utility.py <path_to_file>
```

The script will then execute and verify the checksums match. If they match successfully, you will see a success message like so:

![Successful script execution output example.](https://i.imgur.com/XjasEpn.jpg)

If the checksums do not match, you will be prompted with a y/n (yes or no) option to decide if you want the script to update the header checksum to match the computed checksum -- this should "fix" any issue for ROMs that have had their data manipulated:

![Script execution example where the checksums do not match.](https://i.imgur.com/i4DaYzD.jpg)

*Note: Some games, such as [Sonic & Knuckles](https://en.wikipedia.org/wiki/Sonic_%26_Knuckles), lack checksum checks, possibly because of the time required to check the entire ROM. [[Source](https://segaretro.org/Checksum)]*

# Background

Sega Genesis / Sega Mega Drive games have a source of "tamper protection", which compares [checksum](https://en.wikipedia.org/wiki/Checksum) to ensure the ROM on the cartridge matches the intended checksum value. If someone attempted to manipulate the code on the cart, the checksum calculation would no longer match and the system would not load the game.

> The most important data stored in the metadata, at least when determining if the ROM is good, is the "checksum." A checksum is used by companies like Nintendo and Sega to fight game piracy. The checksum is calculated through each company’s unique algorithm. At first, the ROMs were tested in emulators to see if they would run. If they passed the company’s checksum algorithm, they were considered good ROMs of the game. If a single byte in the ROM was different, the checksum wouldn’t calculate properly and thus, not run.
*([Source](https://web.stanford.edu/group/htgg/cgi-bin/drupal/?q=node/1179))*

The intent of this script is to be used alongside the [Retrode 2](http://www.retrode.org/), which can be purchased [here](https://www.dragonbox.de/en/71-retrode-2-cart-reader-4260416650091.html?search_query=retrode&results=7), for extracting Sega Genesis saves.

According to this [2013 article](https://web.stanford.edu/group/htgg/cgi-bin/drupal/?q=node/1179) posted on Stanford 's website, the Retrode can be unreliable and occasionally read a ROM with a bad checksum. It's unclear if this is the fault of the device, or an issue with the ROM data itself for certain cartridges. Regardless, I decided to put together a simple tool, based off of this article, to detect and correct any invalid ROM checksums.

*(Note: Existing tools already exist, such as this nifty interactive tool called [E.S.E by Kuwabara](https://www.romhacking.net/utilities/342/). However, as far as I can tell, it is not open-source.)*

# ROM Layout

All of this information is borrowed from [THE COMPLETE DOCUMENTATION ABOUT GENESIS ROM FORMAT](http://www.emulatronia.com/doctec/consolas/megadrive/genesis_rom.txt). (Note: A backed up copy of this text file can be found in the [Resources/Backup/](https://github.com/mrhappyasthma/Sega-Genesis-Checksum-Utility/blob/master/Resources/Backup/) folder.)

```

  THE BASIC INFORMATION:
  ^^^^^^^^^^^^^^^^^^^^^

H100:    'SEGA MEGA DRIVE'                                   1
H110:    '(C)SEGA 1988.JUL'                                  2
H120:    GAME NAME (DOMESTIC)                                3
H150:    GAME NAME (OVERSEAS)                                4
H180:    'XX'                                                5
H182:    'XXXXXXX-XX'                                        6
H18E:    XXXX                                                7
H190:    'XXXXXXXXXXXXXXXX'                                  8
H1A0:    00000000, XXXXXXXX                                  9
H1A8:    RAM                                                10
H1BC:    MODEM DATA                                         11
H1C8:    MEMO                                               12
H1F0:    Country in which the product                       13
         can be released.
         
...

7:  Check sum, a two-bytes value (see "Calculating the Checksum")
```

All of this information is borrowed from [THE COMPLETE DOCUMENTATION ABOUT GENESIS ROM FORMAT](http://www.emulatronia.com/doctec/consolas/megadrive/genesis_rom.txt). (Note: A backed up copy of this text file can be found in the [Resources/Backup/](https://github.com/mrhappyasthma/Sega-Genesis-Checksum-Utility/blob/master/Resources/Backup/) folder.)


# Calculating the Checksum (Algorithm)

```
  CALCULATING THE CHECKSUM:
  ^^^^^^^^^^^^^^^^^^^^^^^^

  Genesis checksum is simple enough... All you need to do is:
1) Checksum starts as zero
2) Skip the first 512 bytes of the ROM
3) Read a byte from the rom and multiply its ascii value by 256, then sum
  it to the checksum
4) Read the next byte from the rom and just sum it to the checksum
5) If you're not in the end of file, goto step 3
6) Get the first 16 bits from the resulting checksum and discard the higher
  bits
7) That's your checksum!
```
