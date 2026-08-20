"""
@author: KP
Purpose: SA-CCR Prototype - Multi-Netting Set, Multi-Counterparty, All Asset Classes with Hedging Sets
"""

import numpy as np
import pandas as pd

# Comprehensive Portfolio covering multiple Netting Sets, Counterparties, and Hedging Sets
portfolio = [
    # --- Netting Set N1 (Counterparty: Alpha Corp -> 50% RW) ---
    {
        "Product": "IRS_Payer_Swap_1",
        "Counterparty": "Alpha Corp",
        "Nettingset_ID": "N1",
        "Hedgingset_ID": "IR_USD_Bucket_Long",  # Hedging set identifier (e.g. by currency/maturity bucket)
        "Asset_Class": "IR",
        "Direction": "Long",
        "Notional": 10_000_000,  # Contract face value
        "Supervisory Duration": 5.0,  # DERIVED: Formula-based decay factor
        "Maturity Factor": 1.0,  # RULE: 1.0 for standard unmargined > 1 yr
        "Supervisory Delta": 1.0,  # RULE: 1.0 for linear products
        "Supervisory_Factor": 0.005,  # RULE: 0.5% for Interest Rates (Basel table)
        "mtm": 50_000,  # LIVE DATA: Current fair market value
        "collateral": 0,  # LIVE DATA: Current collateral balance
    },
    {
        "Product": "FX_Forward_EURUSD",
        "Counterparty": "Alpha Corp",
        "Nettingset_ID": "N1",
        "Hedgingset_ID": "FX_EUR_USD",  # Hedging set by currency pair
        "Asset_Class": "FX",
        "Direction": "Long",
        "Notional": 2_000_000,
        "Supervisory Duration": 1.0,
        "Maturity Factor": 1.0,
        "Supervisory Delta": 1.0,
        "Supervisory_Factor": 0.040,  # RULE: 4.0% for FX
        "mtm": 20_000,
        "collateral": 0,
    },
    # --- Netting Set N2 (Counterparty: Beta Bank -> 20% RW) ---
    {
        "Product": "Credit_Single_Name_CDS",
        "Counterparty": "Beta Bank",
        "Nettingset_ID": "N2",
        "Hedgingset_ID": "CR_Entity_A",  # Hedging set per single reference entity
        "Asset_Class": "CREDIT",
        "Direction": "Short",
        "Notional": 3_000_000,
        "Supervisory Duration": 1.0,
        "Maturity Factor": 1.0,
        "Supervisory Delta": 1.0,
        "Supervisory_Factor": 0.0038,  # RULE: Supervisory factor for IG corporate credit
        "mtm": -10_000,
        "collateral": 5_000,
    },
    {
        "Product": "Equity_Single_Stock_AAPL",
        "Counterparty": "Beta Bank",
        "Nettingset_ID": "N2",
        "Hedgingset_ID": "EQ_AAPL",  # Hedging set per single equity underlier
        "Asset_Class": "EQUITY",
        "Direction": "Long",
        "Notional": 1_500_000,
        "Supervisory Duration": 1.0,
        "Maturity Factor": 1.0,
        "Supervisory Delta": 1.0,
        "Supervisory_Factor": 0.320,  # RULE: 32% for single stock equities
        "mtm": 25_000,
        "collateral": 5_000,
    },
    # --- Netting Set N3 (Counterparty: Gamma HighRisk -> 100% RW) ---
    {
        "Product": "Commodity_Oil_Swap",
        "Counterparty": "Gamma HighRisk",
        "Nettingset_ID": "N3",
        "Hedgingset_ID": "COM_Energy_Oil",  # Hedging set per commodity type
        "Asset_Class": "COMMODITY",
        "Direction": "Long",
        "Notional": 1_000_000,
        "Supervisory Duration": 1.0,
        "Maturity Factor": 1.0,
        "Supervisory Delta": 1.0,
        "Supervisory_Factor": 0.180,  # RULE: 18% for energy commodities
        "mtm": 5_000,
        "collateral": 0,
    },
]

df_trades = pd.DataFrame(portfolio)

# 1. Handle Long (+1) vs Short (-1) orientation
df_trades["Sign"] = np.where(df_trades["Direction"] == "Short", -1, 1)

# 2. Trade-Level Effective Notional
df_trades["Effective Notional"] = (
    df_trades["Notional"]
    * df_trades["Supervisory Duration"]
    * df_trades["Maturity Factor"]
    * df_trades["Supervisory Delta"]
    * df_trades["Sign"]
)

# 3. Trade-level Add-on contribution
df_trades["Trade_Addon"] = (
    df_trades["Effective Notional"].abs() * df_trades["Supervisory_Factor"]
)

# 4. Netting-Set Level Aggregation
ns_summary = (
    df_trades.groupby("Nettingset_ID")
    .agg(
        {
            "Counterparty": "first",  # Captures counterparty name per netting set
            "mtm": "sum",
            "collateral": "sum",
            "Trade_Addon": "sum",
        }
    )
    .reset_index()
)

ns_summary["Aggregate_Addon"] = ns_summary["Trade_Addon"]

# 5. Replacement Cost (RC) Calculation
ns_summary["RC"] = np.maximum(
    ns_summary["mtm"] - ns_summary["collateral"], 0.0
)

# 6. Dynamic Multiplier Calculation (with 0.05 floor and 1.0 ceiling)
v_minus_c = ns_summary["mtm"] - ns_summary["collateral"]
addon_val = np.where(
    ns_summary["Aggregate_Addon"] == 0, 1e-6, ns_summary["Aggregate_Addon"]
)

ns_summary["Multiplier"] = np.minimum(
    1.0, 0.05 + 0.95 * np.exp(v_minus_c / (2 * 0.95 * addon_val))
)

# 7. PFE and EAD Calculation
ns_summary["PFE"] = ns_summary["Multiplier"] * ns_summary["Aggregate_Addon"]
ns_summary["EAD"] = 1.4 * (ns_summary["RC"] + ns_summary["PFE"])

# 8. Counterparty Risk Weight Mapping Logic
rw_mapping = {
    "Beta Bank": 0.20,  # 20% risk weight for qualifying banks
    "Alpha Corp": 0.50,  # 50% risk weight for standard corporate
    "Gamma HighRisk": 1.00,  # 100% risk weight for unrated/high-risk
}

ns_summary["Risk_Weight"] = (
    ns_summary["Counterparty"].map(rw_mapping).fillna(1.00)
)

# 9. RWA and Regulatory Capital
ns_summary["RWA"] = ns_summary["EAD"] * ns_summary["Risk_Weight"]
ns_summary["Regulatory_Capital"] = (
    ns_summary["RWA"] * 0.08
)  # 8% Basel minimum

# 10. Output Results
print("--- TRADE LEVEL METRICS ---")
print(
    df_trades[
        [
            "Product",
            "Counterparty",
            "Nettingset_ID",
            "Hedgingset_ID",
            "Asset_Class",
            "Effective Notional",
        ]
    ].to_string(index=False)
)
print("\n--- NETTING SET & CAPITAL LEVEL METRICS ---")
print(
    ns_summary[
        [
            "Nettingset_ID",
            "Counterparty",
            "RC",
            "Multiplier",
            "PFE",
            "EAD",
            "Risk_Weight",
            "RWA",
            "Regulatory_Capital",
        ]
    ].to_string(index=False)
)
