# Copyright (c) 2026 Martial Systems LLC


class GateError(RuntimeError):
    """Stage hard gate failed."""


class ClaimBanError(GateError):
    """Report text hit a banned claim."""


class SiblingShaError(GateError):
    """Frozen Nora crest wet mask drifted."""


class FetchError(GateError):
    """Official HWM layer 404 or empty. Live paint refuses."""


class FigureCapError(GateError):
    """This tree stops at two figures."""
