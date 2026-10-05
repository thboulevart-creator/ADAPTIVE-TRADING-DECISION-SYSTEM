from __future__ import annotations
from itertools import product

CONTRACT="ATDS_AO_E0_EXEC_04_PRE_RESULT_CONSERVATIVE_COST_STRESS_POLICY_V0_1"
FINANCING_ANCHOR=6.3665
FINANCING_MULTIPLIERS=[0.0,1.0,2.0,4.0]
SLIPPAGE_BPS=[0.0,0.5,1.0,2.0,4.0,8.0,16.0]
ROLLOVER_MULTIPLIERS={"monday":1,"tuesday":1,"wednesday":1,"thursday":1,"friday":3}
AUTHORITY={"oos_consumption_authorized":False,"performance_observation_authorized":False,"strategy_qualification_authorized":False}
STRESS_NODES=tuple(product(FINANCING_MULTIPLIERS,SLIPPAGE_BPS))

def adverse_slippage_cost(*,reference_price:float,bps:float)->float:
    if reference_price<=0 or bps<0:
        raise ValueError("INVALID_STRESS_INPUT")
    return float(reference_price)*float(bps)/10000.0

def execution_event_slippage_cost(*,reference_prices,bps:float)->float:
    return sum(adverse_slippage_cost(reference_price=float(p),bps=float(bps)) for p in reference_prices)

def rollover_policy_cost(*,direction:str,weekday:str,stress_multiplier:float)->float:
    if direction not in {"LONG","SHORT"}:
        raise ValueError("INVALID_DIRECTION")
    if weekday not in ROLLOVER_MULTIPLIERS:
        raise ValueError("INVALID_WEEKDAY")
    if stress_multiplier not in FINANCING_MULTIPLIERS:
        raise ValueError("UNREGISTERED_FINANCING_STRESS")
    return FINANCING_ANCHOR*float(stress_multiplier)*ROLLOVER_MULTIPLIERS[weekday]

def policy_surface():
    return [
        {"financing_multiplier":f,
         "slippage_bps_per_execution_event":s,
         "epistemic_class":"POLICY_STRESS_NOT_OBSERVED_HISTORICAL_COST"}
        for f,s in STRESS_NODES
    ]
