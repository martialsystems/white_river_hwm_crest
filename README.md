# White River HWM vs Nora crest

Do August 2026 high-water marks land on the Nora HAND wet mask at 21.18 ft?

Official points are not scored yet. Probe 2026-09-05 (`99c76a2`): USGS STN Indiana and Marion County returned `[]`; ScienceBase total 0. Empty APIs are a wait. The fixture is not the result.

When USGS STN or ScienceBase publishes points with locations, this tree scores them on the frozen Nora crest wet mask from [Nora wet cells at two stages](https://github.com/martialsystems/white_river_stage_inundation) (`wet_crest_2026-08-15.tif`, 1,876 wet cells, Δ = 4.19 m). Hit: wet cell. Miss: dry in the drain-to-reach window. Out: outside that window. Two figures. Then stop. If they never publish, the parked row is the terminal state.

The schedule in [CADENCE.md](CADENCE.md) exists only so that question can close when the official layer appears. Do not grow a fifth figure, a new model, or a lab around the wait.

Sibling Nora v1 `three_wet.png` stays frozen.

| Official probe (2026-09-05) | Result |
|---|---|
| USGS STN `States=IN` | HTTP 200, empty list |
| USGS STN `States=IN&Counties=Marion` | HTTP 200, empty list |
| ScienceBase "high-water mark Indiana 2026" | total 0 |

![Figure 1. Fixture path: four synthetic points on a tiny crest mask](logs/stage0_fixture/hwm_on_crest.png)

Figure 1. Fixture path only (four synthetic points: two hit, one miss, one out). Not the August 2026 result.

![Figure 2. Fixture path counts](logs/stage0_fixture/hwm_counts.png)

Figure 2. Fixture hit / miss / out. Second figure for the fixture path. Live paint waits on an official layer.

## Stage 0

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src:. python3 scripts/run_fixture.py logs/stage0_fixture
.venv/bin/python -m pytest tests -q
PYTHONPATH=src:. python3 scripts/run_live.py logs/nora_live
```

Live `run_live.py` exits 2 when the official layer is empty or 404. That is not scored yet, not a crash.

[Nora wet cells at two stages](https://github.com/martialsystems/white_river_stage_inundation)

Research index: https://gist.github.com/martialsystems/66b896b0a4a0b8cba2b478aef64312f3
