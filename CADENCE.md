# Probe cadence: official HWM layer

Last empty probe: 2026-09-05 (`99c76a2`). USGS STN Indiana/Marion returned `[]` (2-byte body). ScienceBase total 0. Live `run_live.py` exited 2. Empty APIs are not scored yet. The fixture is not the result.

The schedule exists only so the HWM question can close when USGS or ScienceBase publishes points. If they never do, the parked row is the terminal state. Do not grow a fifth figure, a new model, or a lab around the wait.

Field marks get flagged fast because they perish. Public STN / ScienceBase points come later, after survey and an event record. For a mid-August crest that is still normal at three weeks. The 2008 White River marks showed up in a later report, not in the first fortnight.

Not daily. The gate already proved empty twice in three days (2026-09-02 and 2026-09-05). Another empty `[]` does not move the tree.

## Calendar

| Window | Interval | Why |
|---|---|---|
| Now → 16 Sep 2026 | none | Last probe 5 Sep. |
| 17 Sep 2026 | one run | Same day as the CPC issue. One calendar, two waits. |
| 17 Sep → 31 Oct 2026 | weekly | First window official IN/Marion points usually appear. Thursdays: 17 Sep, 24 Sep, 1 Oct, 8 Oct, 15 Oct, 22 Oct, 29 Oct. |
| Nov 2026 → Feb 2027 | monthly, first Sunday | After field season; ScienceBase items lag STN. 1 Nov 2026, 6 Dec 2026, 3 Jan 2027, 7 Feb 2027. |
| After 7 Feb 2027 if still `[]` | stop the clock | Park until a named publication, not another timer. |

Seventeen days of silence, then weekly through October, is enough. More often is just watching the same two-byte body.

## Off-calendar

Also run if any of these is true. Do not poll daily to watch the same two-byte body.

- USGS Indiana WSC or IDNR posts a 2026 HWM / flood-documentation note
- Flood Event Viewer grows an August 2026 Indiana event
- ScienceBase search total leaves 0 (total is no longer 0)
- STN `States=IN` body is no longer 2 bytes

## How to run

Same command, same stop:

```bash
PYTHONPATH=src:. .venv/bin/python scripts/run_live.py logs/nora_live
```

Exit 2: official layer empty or 404. Fixtures stay frozen. Do not run `scripts/run_fixture.py` against `logs/stage0_fixture`. README probe date only. No scoring on empty.

Do not restamp maps/index unless the SHA of that date-only commit is the parked pin (as with `99c76a2`). Index one-liner stays unless it would be stale.

If the official layer has points: score them on the frozen Nora crest wet mask. That is fetch-or-stop, not a new model and not a new question.

After 7 Feb 2027, if the layer is still empty, stop the clock. The parked row is then the terminal state until a named USGS / IDNR / ScienceBase publication. Do not start another timer. Do not grow a fifth figure, a new model, or a lab around the wait.
