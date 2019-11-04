# Reproducing high memory usage in Waitress

For https://github.com/Pylons/waitress/issues/265

This creates a Falcon web app with a 11 KB JSON response. It demonstrates an issue where Waitress uses too much memory.

## How to reproduce

1. Set up Python environment.
    * Direnv can automate this.
    * Otherwise install packages listed in `requirements.txt`.
2. Open 3 terminals.
3. Run `make serve` in the 1st terminal and leave it running.
4. Run `make load` in the 2nd terminal and leave it running.
5. Occasionally run `make check` in the 3rd terminal to see how much memory it is using.

## Results

After only a few seconds, `make check` returns something like this:

```
Top 5 lines
#1: waitress/buffers.py:55: 132145.2 KiB
    file.write(s)
#2: urllib/parse.py:131: 172.2 KiB
    return self._encoded_counterpart(*(x.encode(encoding, errors) for x in self))
#3: urllib/parse.py:107: 63.5 KiB
    return tuple(x.decode(encoding, errors) if x else '' for x in args)
#4: json/encoder.py:257: 62.4 KiB
    return _iterencode(o, 0)
#5: waitress-memory/app.py:10: 56.3 KiB
    junk = {i:i for i in range(1000)} # about 11kb of JSON
350 other: 442.6 KiB
Total allocated size: 132942.4 KiB
```

The top line shows Waitress using over 100 MB of memory.
