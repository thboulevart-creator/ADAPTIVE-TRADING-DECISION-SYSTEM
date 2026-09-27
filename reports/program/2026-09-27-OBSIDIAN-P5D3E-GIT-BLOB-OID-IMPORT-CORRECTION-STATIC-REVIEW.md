# OBSIDIAN P5-D3E — GIT BLOB OID IMPORT CORRECTION STATIC REVIEW

Date: 2026-09-27

## Review status

Same-assistant static correction review.

Not independent execution evidence.
Does not qualify P5-D3E implementation.

## Failed tested candidate

    d403482b222b8bcfa4b0befa7684eda4b9d662fc

User-reported targeted result:

    Ran 134 tests in 2.672s
    FAILED (errors=2)

Both errors occurred while importing:

    tools.obsidian_projection.p5d3e_verify

Exact failure:

    ImportError:
    cannot import name 'git_blob_oid'
    from tools.obsidian_projection.git_source

## Root cause

At the tested candidate, git_source.py contains:

    normalize_origin
    FrozenGitSource
    sha256_bytes

but no:

    git_blob_oid

The canonical Git blob object-id algorithm already exists elsewhere in the repository as the private helper:

    dynamic_inventory._git_blob_oid

Its algorithm is:

    SHA1(
        ASCII("blob " + byte_length + NUL)
        + raw_bytes
    )

P5-D3E incorrectly attempted to import a non-existent public symbol.

## Corrected functional candidate

    a0478167404a53aed94a3f3404addb4e7cc23e6a

## Runtime correction

P5-D3E harness blob changed from:

    2380cddc3e15caf1b3f4d1b7942f064c179389ee

to:

    bd7f63b08432a53eaff5deeb2147396eb60d723f

Correction:

- remove git_blob_oid from git_source import;
- define local _git_blob_oid(raw);
- use the canonical Git blob SHA-1 formula;
- use it only for P5-D3E contract blob verification.

No evaluator, builder, bridge, breaker, package or publication semantics were changed.

## Unit breaker

P5-D3E harness test blob changed from:

    a1ae77ae7bfe768d1152885a2cfa154695c47bf0

to:

    fe47910cf7f10a09021d958d7ae60693d0def4bf

Added canonical known-vector assertion:

    _git_blob_oid(b"hello\n")
    ==
    ce013625030ba8dba906f756967f9e9ca394464a

This is the canonical Git blob OID for those exact bytes.

## Unchanged authorities

P5-D3E contract blob remains:

    ae4b1691fae16fcd1616e265a089670b9654db4a

Qualified P5-D3D evaluator blob remains:

    bff5f51abbb344c1ccc5e9c669a11cf0e26c2562

P5-D3E adversarial-test blob remains:

    6af423b77b4ad78a833f7f4e3dedc53f5f23cead

## Evidence-only files between candidates

The following are evidence-only:

- P5-D3E implementation preflight;
- P5-D3E implementation static review;
- user-reported targeted import failure report.

They do not alter runtime semantics.

## Qualification status

P5-D3E implementation remains unqualified.

The corrected candidate must restart the governed implementation qualification from py_compile.

The real integration/system-v1 candidate remains unauthorized.

## Verdict

**STATIC CORRECTION REVIEW PASS — FULL GOVERNED IMPLEMENTATION RE-BREAK REQUIRED**

Exact corrected candidate:

    a0478167404a53aed94a3f3404addb4e7cc23e6a
