from __future__ import annotations
import bepd09c_runtime as _base
from bepd09c_runtime import *

SOURCE_RUNTIME_BLOB = "72645c3201d3d454d4d5402a0e2191e1195c68a6"
R2_REPAIR_CLASS = "R2_SOLVER_OPTIMIZER_BEHAVIOR_CHANGE"
R2_ONLY_FUNCTIONAL_CHANGE = "MAX_ITER_100_TO_5000"

MAX_ITER = 5000
FIT_TOL = _base.FIT_TOL
_ORIGINAL_FIT_LOGISTIC = _base.fit_logistic

_stats = _base._stats
_mats = _base._mats

def fit_logistic(X, y, max_iter=MAX_ITER, tol=FIT_TOL):
    return _ORIGINAL_FIT_LOGISTIC(X, y, max_iter=max_iter, tol=tol)

_base.fit_logistic = fit_logistic
run_protocol = _base.run_protocol
