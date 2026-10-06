from tools.ao_e0_b12_data01_sr01_a_transform import *

def test_identity_exact():
    for x in (-1000001,-1,0,1,1000001):
        assert transform_milli_price(x)==x

def test_metadata_frozen():
    assert TRANSFORMATION_ID=="DUKASCOPY_CANONICAL_DECODE_IDENTITY_V0_1"
    assert TRANSFORMATION_VERSION=="V0.1"
    assert INPUT_UNIT==OUTPUT_UNIT=="0.001 price unit"
    assert ROUNDING_MODE is None
    assert EPSILON==0
    assert ROW_REMOVAL==0

def test_reject_non_integer_milli():
    import pytest
    with pytest.raises(TypeError,match="INTEGER_MILLI_PRICE_REQUIRED"):
        transform_milli_price(1.0)
