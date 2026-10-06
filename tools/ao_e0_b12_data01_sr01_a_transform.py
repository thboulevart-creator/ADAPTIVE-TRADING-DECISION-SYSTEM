from __future__ import annotations

TRANSFORMATION_ID="DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1"
TRANSFORMATION_VERSION="V0.1"
INPUT_UNIT="0.001 price unit"
OUTPUT_UNIT="0.001 price unit"
ROUNDING_MODE=None
PRECISION="exact integer milli-price"
EPSILON=0
ROW_REMOVAL=0

def transform_milli_price(value: int) -> int:
    if type(value) is not int:
        raise TypeError("INTEGER_MILLI_PRICE_REQUIRED")
    return value
