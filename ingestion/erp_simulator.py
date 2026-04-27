from faker import Faker
import pandas as pd
import numpy as np
import random
from pathlib import Path

# Seed for reproducibility
fake = Faker(seed=42)
random.seed(42)
np.random.seed(42)

# Risk levels par pays 
Risk_Base = {
    "Turkey":  0.75,
    "China":   0.55,
    "India":   0.50,
    "Brazil":  0.60,
    "Morocco": 0.35,
    "Germany": 0.10,
    "France":  0.12,
}

# Proba d'avoir un fournisseur par pays
Country_Weights = {
    "Turkey":  0.20,
    "China":   0.20,
    "Germany": 0.10,
    "Morocco": 0.15,
    "India":   0.15,
    "France":  0.10,
    "Brazil":  0.10,
}

Categories = [
    "Electronics", "Raw Materials",
    "Logistics", "Packaging",
    "Chemicals", "Automotive Parts"
]

def generate_supplier_data(supplier_id):
    country = random.choices(
        list(Country_Weights.keys()), 
        weights=list(Country_Weights.values())
    )[0]

    base_risk = Risk_Base[country]
    return {
        "SupplierID": f"SUP_{supplier_id:03d}",
        "Name": fake.company(),
        "Country": country,
        "Category": random.choice(Categories),
        "avg_delay_days": float(np.random.normal(loc=base_risk * 12,scale =2).clip(0, 20)),
        "defect_rate": float(np.random.beta(a=base_risk * 2, b=5)),
        "on_time_delivery": float(np.clip(1-base_risk * 0.4 + np.random.normal(0, 0.05), 0.5, 0.99)),
        "annual_volume_usd": random.randint(100_000, 5_000_000),
    }
def main():
    # generate 50 suppliers
    suppliers = pd.DataFrame([generate_supplier_data(i) for i in range(1, 51)])
    # create folder if not exists
    path("data/raw").mkdir(parents=True, exist_ok=True)

    # save to Parquet
    suppliers.to_parquet("data/raw/suppliers.parquet", index=False)

    # afficher 
    print(f"{len(suppliers)} suppliers generated")
    print(f"\nAprecus")
    print(suppliers[["supplier_id", "country", "avg_delay_days", "defect_rate"]].head(10).to_string(index=False))

    # Statistiques rapides
    print(f"\nDistribution par pays :")
    print(suppliers["country"].value_counts().to_string())

if __name__ == "__main__":
    main()