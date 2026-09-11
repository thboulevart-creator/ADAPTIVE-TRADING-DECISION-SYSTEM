# Instrument Contracts

This directory is the normative source for source/instrument-specific decoding semantics used by research qualification and compatibility tooling.

## Minimum contract

- `asset_id`
- `source`
- `format`
- `record_size`
- `record_struct`
- `timestamp_unit`
- `price_scale`

The contract is deliberately limited to decoding semantics. Market behaviour, execution specifications, risk parameters, and dynamic statistics remain outside this layer.

A decoder must consume these values from the resolved contract. It must not duplicate instrument-specific decoding constants.

## Current contract

`USATECHIDXUSD / Dukascopy / BI5` is the first concrete contract because it is the dataset currently under V4.3 qualification.

Its `price_scale` is `1000`.

This is not a universal Dukascopy BI5 rule. Price scale is an explicit property of the instrument/source/format contract.

## Change rule

Any new instrument/source/format combination must add or update its contract and adversarial tests before being accepted by a decoder.
