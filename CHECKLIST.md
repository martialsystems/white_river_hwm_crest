# Operator checklist

1. Fixture Stage 0 green.
2. Nora crest wet sha matches `LOCKED_CREST_WET_SHA256`.
3. Probe only on [CADENCE.md](CADENCE.md) (calendar or off-calendar). Not daily.
4. `scripts/run_live.py`: official HWM layer present, or exit 2.
5. Exit 2: not scored yet. README probe date only. Fixtures frozen (fixture is not the result). Maps/index SHA only if that date-only commit is the parked pin (`99c76a2` pattern). No scoring on empty. Do not grow a fifth figure or a new model.
6. At most two figures.
7. Push public `martialsystems/white_river_hwm_crest`.
