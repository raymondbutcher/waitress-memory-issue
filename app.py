import falcon
import linecache
import os
import tracemalloc


tracemalloc.start()


junk = {i:i for i in range(1000)} # about 11kb of JSON


class BigResponse:
    def on_get(self, req, resp):
        resp.media = junk


class CheckMemoryUsage:
    def on_get(self, req, resp, limit=5):
        # Mostly copied from https://stackoverflow.com/a/45679009

        output = []

        snapshot = tracemalloc.take_snapshot()
        snapshot = snapshot.filter_traces((
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        ))
        top_stats = snapshot.statistics('lineno')

        output.append("Top %s lines" % limit)
        for index, stat in enumerate(top_stats[:limit], 1):
            frame = stat.traceback[0]
            # replace "/path/to/module/file.py" with "module/file.py"
            filename = os.sep.join(frame.filename.split(os.sep)[-2:])
            output.append("#%s: %s:%s: %.1f KiB" % (index, filename, frame.lineno, stat.size / 1024))
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                output.append('    %s' % line)

        other = top_stats[limit:]
        if other:
            size = sum(stat.size for stat in other)
            output.append("%s other: %.1f KiB" % (len(other), size / 1024))
        total = sum(stat.size for stat in top_stats)
        output.append("Total allocated size: %.1f KiB" % (total / 1024))

        resp.body = "\n".join(output)


api = falcon.API()
api.add_route("/", BigResponse())
api.add_route("/check", CheckMemoryUsage())
