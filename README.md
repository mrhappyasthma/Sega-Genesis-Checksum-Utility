# Sega Genesis Checksum Utility
A simple command line utility to verify (or correct) Sega Genesis ROM checksums.

# Background

The intent of this script is to be used alongside the [Retrode 2](http://www.retrode.org/), which can be purchased [here](https://www.dragonbox.de/en/71-retrode-2-cart-reader-4260416650091.html?search_query=retrode&results=7), for extracting Sega Genesis saves.

According to this [2013 article](https://web.stanford.edu/group/htgg/cgi-bin/drupal/?q=node/1179) posted on Stanford 's website, the Retrode can be unreliable and occasionally read a ROM with a bad checksum. It's unclear if this is the fault of the device, or an issue with the ROM data itself for certain cartridges. Regardless, I decided to put the info in this document into a self-sufficient tool.

(Note: Existing tools for this exist, such as this nifty interactive tool called [E.S.E by Kuwabara](https://www.romhacking.net/utilities/342/). However, as far as I can tell, it is not open sourced.)

# ROM Layout

All of this information is borrowed from [THE COMPLETE DOCUMENTATION ABOUT GENESIS ROM FORMAT](http://www.emulatronia.com/doctec/consolas/megadrive/genesis_rom.txt). (Note: A backed up copy of this text file can be found in the [Resources/](https://github.com/mrhappyasthma/Sega-Genesis-Checksum-Utility/tree/master/Resources) folder.)

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

All of this information is borrowed from [THE COMPLETE DOCUMENTATION ABOUT GENESIS ROM FORMAT](http://www.emulatronia.com/doctec/consolas/megadrive/genesis_rom.txt). (Note: A backed up copy of this text file can be found in the [Resources/](https://github.com/mrhappyasthma/Sega-Genesis-Checksum-Utility/tree/master/Resources) folder.)


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
