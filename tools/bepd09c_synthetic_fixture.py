from __future__ import annotations
from datetime import date,timedelta
from bepd09c_runtime import week_bounds

SCHEMA='ATDS_BEPD_09C_SYNTHETIC_FIXTURE_PACKAGE_V0_1'
EMPTY_INDEXES=(16,33,50,67,84,101,118)

def build_fixture():
    calendar=[];rows=[];start=date(2025,1,6)
    for i in range(120):
        w=(start+timedelta(days=7*i)).isoformat();calendar.append(w)
        if i in EMPTY_INDEXES: continue
        n=5 if i%9==0 else 4
        a,z=week_bounds(w);dur=(z-a).total_seconds()/3600
        for j in range(n):
            take_h=(8,24,40,56,72,88,104,120,136,152)[(i+2*j)%10]
            if take_h>=dur: take_h=dur-4
            t=a+timedelta(hours=take_h);side='HIGH' if (i+j)%2==0 else 'LOW'
            lp=1.05+0.00012*i+0.00002*j;ov=0.00025*(1+((3*i+j)%9));take=lp*(1+ov if side=='HIGH' else 1-ov)
            age=1+((5*i+2*j)%20);active=2+((2*i+3*j)%13)
            y=((7*i+11*j+(2 if side=='HIGH' else 0)+i//4)%17)<9
            rows.append({'event_id':f'SYN-E-{i:03d}-{j}','target_week_id':w,'sweep_cluster_id':f'SYN-C-{i:03d}','side':side,'level_price_mid':lp,'take_h1_close_mid':take,'take_h1_close_utc':t.isoformat().replace('+00:00','Z'),'level_age_weeks':age,'active_level_count_at_target_week_start':active,'same_week_reintegration':bool(y)})
    return {'schema':SCHEMA,'status':'SYNTHETIC_ONLY_NO_REAL_DATA','calendar':calendar,'rows':rows,'special_cases':{'dst_expected_hours':{'2026-03-02':167,'2026-02-23':168,'2026-10-26':169},'basis_points':[0.25,0.50,0.75,1.00],'empty_weeks':[calendar[x] for x in EMPTY_INDEXES]}}
