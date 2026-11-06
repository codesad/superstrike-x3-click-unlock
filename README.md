# Superstrike X3 Click Unlock

A script that removes the software-imposed CPS limit of the Superstrike X3.
Especially useful for Minecraft and drag clicking in general.

| | Minimum time between clicks | Maximum CPS |
|---|---|---:|
| Before | 50 ms | 20 |
| After | ~10 ms | ~100 |

## Requirements

- Superstrike X3 running firmware `AM 1.2.0015`
- Python 3
- [`hidapi`](https://pypi.org/project/hidapi/)

```bash
python -m pip install hidapi
python main.py
```

> [!WARNING]
> This has only been tested on firmware version `AM 1.2.0015` for the Superstrike X3.
> It is also 101% not going to work on any other combination without targeted changes.

> [!NOTE]
> Device discovery on Windows is currently untested, but it should work.
> If discovery fails, the script exits before touching the mouse, so you
> don't have to worry about things breaking.

## How it works

The mouse has its own firmware updater, and that updater has an integer overflow
in the type-2 record parser's 32-bit `offset + length` calculation. Normally,
that parser only accepts a relative write inside its intended RAM object. With
the overflow, both the bounds-check sum and destination address wrap around, so
we can write to RAM anywhere (albeit sequentially) and point the record at the TCM
where the active mouse handling is running.

Since we only get one continuous write, we put a 32-byte wrapper over the
beginning of the HITS host-command handler at `0x22005b2c`, copy the original
bytes between that address and the normal sensor callback, and install the
callback hook that triggers our wrapper at `0x22005ea4` in the final packet.

## Changes

1. Point Quiver (logitech's button transition logic) at the config where all 
   timing values are `0`, getting rid of the ~50 ms Quiver timing cycle.
2. Clear the two flags that make HITS ignore the sensor for 10 ms after the
   haptic driver changes state (which apparently happens even with haptics off).

These are the only software-imposed delays to my knowledge.

## Reverting

Since the patch only lives in RAM, doing a cold reboot of the mouse will
drop these changes. On the upside, this also means that any permanent damage
is very unlikely to happen due to these changes.

happy gaming
