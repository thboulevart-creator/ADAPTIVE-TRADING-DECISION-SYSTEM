import json
from copy import deepcopy
from pathlib import Path

import pytest

from tools.trading_breaks_recovery_batch11_adjudication import adjudicate_runtime

RUNTIME=json.loads(Path('reports/data-qualification/historical_trading_breaks_recovery_batch11_runtime.json').read_text(encoding='utf-8'))


def test_batch11_authoritative_runtime_adjudicates_all_five_pass():
    report=adjudicate_runtime(deepcopy(RUNTIME))
    assert report['verdict']=='PASS'
    assert (report['pass'],report['blocked'],report['fail'])==(5,0,0)
    assert all(x['verdict']=='PASS' for x in report['adjudications'])

@pytest.mark.parametrize('mutation', ['wrong_date','wrong_instrument','missing_dom','cross_date','bad_artifact'])
def test_batch11_adjudication_rejects_tampering(mutation):
    data=deepcopy(RUNTIME)
    if mutation=='wrong_date': data['results'][0]['requested_date']='2025-05-25'
    elif mutation=='wrong_instrument': data['results'][0]['instrument_id_observed']='9999'
    elif mutation=='missing_dom': data['results'][0]['dom_witness_lines']=[]
    elif mutation=='cross_date': data['results'][0]['matching_records'][0]['start']='1748132399000'
    elif mutation=='bad_artifact': data['provenance']['artifact_sha256']='0'*64
    with pytest.raises(ValueError): adjudicate_runtime(data)
