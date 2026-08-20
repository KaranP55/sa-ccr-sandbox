import numpy as np
import pandas as pd

product1 = {
            "Product" : "IRS",
            "Notional": 1_000_000,
            "Supervisory Duration":1,
            "Maturity Factor":1,
            "Supervisory Delta":1,
            "Margined/Unmargined":"Margined",
            "Nettingset_ID": "N1",
            "Hedgingset_ID": "NH1"
}

df = pd.DataFrame([product1])

df["Effective Notional"]=df["Notional"]*df["Supervisory Duration"]*df["Maturity Factor"]*df["Supervisory Delta"]
df
