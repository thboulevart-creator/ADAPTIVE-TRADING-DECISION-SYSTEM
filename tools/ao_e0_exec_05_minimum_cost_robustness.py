NODE_ID="F2_S4"
FINANCING_MULTIPLIER=2.0
SLIPPAGE_BPS_PER_EXECUTION_EVENT=4.0
AUTHORITY={"oos_consumption_authorized":False,"performance_observation_authorized":False,"b12":"CLOSED"}

def required_node():
    return NODE_ID, FINANCING_MULTIPLIER, SLIPPAGE_BPS_PER_EXECUTION_EVENT

def evaluate(economic_support_state: str) -> str:
    mapping={"SUPPORTED":"PASS","REFUTED":"FAIL","INCONCLUSIVE":"INCONCLUSIVE"}
    if economic_support_state not in mapping:
        raise ValueError("UNMAPPED_ECONOMIC_SUPPORT_STATE")
    return mapping[economic_support_state]
