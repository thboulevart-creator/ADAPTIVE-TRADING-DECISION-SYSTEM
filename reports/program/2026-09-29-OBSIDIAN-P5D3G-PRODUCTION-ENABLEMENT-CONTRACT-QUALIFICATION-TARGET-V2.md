# OBSIDIAN P5-D3G — PRODUCTION ENABLEMENT CONTRACT QUALIFICATION TARGET V2

Date: 2026-09-29

## Evidence status

Static qualification target only.

## Corrected exact candidate

    47facc362c89728425e134588bfbdb7721ed1e98

Contract blob unchanged:

    5de65f5d13a93d1325d53e1b58536ed0860921f2

Contract tests blob unchanged:

    12873436d6354ffa454253cdf754023378d35076

Corrected governed runner blob:

    aa40a6bdca3e7285c18f1fe1cffc96cff859716a

## Correction

The prior governed re-break passed all targeted and historical tests but left one untracked Python bytecode file in the repository during py_compile.

The corrected runner now redirects Python bytecode cache output to a temporary directory outside the repository by setting PYTHONPYCACHEPREFIX for the governed run and restoring the prior environment afterward.

No contract semantic changed.
No contract-test expectation changed.
No production authority changed.

## Qualification gate

The corrected governed runner must again pass:

1. targeted production-enablement contract tests;
2. complete historical Obsidian suite;
3. final clean-control-clone gate.

Only that complete PASS may qualify the contract.
