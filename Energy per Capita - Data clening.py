from pickle import TRUE
import pandas as pd


df_energy_data = pd.read_csv(
    "/Users/bzabert/Documents/Portfolio/Python/Data Exploration & Cleaning/per-capita-energy-stacked.csv"
)

df_countries_codes = pd.read_csv(
    "/Users/bzabert/Documents/Portfolio/Python/Data Exploration & Cleaning/country_codes.csv"
)

# Inspecting the data
print(df_energy_data.columns)
print(df_energy_data.isna().sum())
print(df_energy_data.describe())
print(df_energy_data.dtypes)
print(df_energy_data["Entity"].value_counts())


# Continent are in the same column than countries
print(df_energy_data[df_energy_data["Code"].isna()])

# Taking out all of the continent and globaly value in Entity
df_wo_continent = df_energy_data[df_energy_data["Code"].notnull()]
df_final = df_wo_continent.loc[df_wo_continent["Code"] != "OWID_WRL"]

# Creating a clomun with the correct Continent using other Data Frame
continent = []

for country in df_final["Code"]:
    if country in df_countries_codes["alpha-3"].unique():
        s = df_countries_codes.set_index("alpha-3")["region"]
        continent.append(s[country])
    else:
        pass

df_final["Continent"] = continent

# Adding the all generated energy
df_final.rename(
    columns={
        "Coal per capita (kWh)": "Coal",
        "Oil per capita (kWh)": "Oil",
        "Gas per capita (kWh)": "Gas",
        "Nuclear per capita (kWh)": "Nuclear",
        "Hydro per capita (kWh)": "Hydro",
        "Wind per capita (kWh)": "Wind",
        "Solar per capita (kWh)": "Solar",
        "Other renewables per capita (kWh)": "Other",
    },
    inplace=TRUE,
)

df_final = df_final.assign(TotalNoNRew=lambda x: x.Coal + x.Oil + x.Gas + x.Nuclear)
df_final = df_final.assign(TotalRew=lambda x: x.Hydro + x.Wind + x.Solar + x.Other)
df_final = df_final.assign(
    Total=lambda x: x.Coal
    + x.Oil
    + x.Gas
    + x.Nuclear
    + x.Hydro
    + x.Wind
    + x.Solar
    + x.Other
)

# View the Data Frame
print(df_final)

# Create various plot to explore the data
print(
    df_final.groupby("Continent")[
        "Oil", "Gas", "Nuclear", "Coal", "Hydro", "Solar", "Wind", "Other"
    ].sum()
)

print(
    df_final.groupby("Year")["Total", "TotalNoNRew", "TotalRew"]
    .sum()
    .plot.line(title="Type of generation of energy per capital from 1965 to 2020")
)

print(
    df_final.groupby("Year")["Total", "Oil", "Gas", "Nuclear", "Coal"]
    .sum()
    .plot.line(title="Generation of energy per capita by Source from 1965 to 2020")
)

print(
    df_final.groupby("Continent")["Total"]
    .sum()
    .plot(kind="pie", title="Energy Production Distribution from 1965 to 2020")
)


print(
    df_final[df_final["Entity"] == "Argentina"]
    .loc[:, ["Year", "TotalNoNRew", "TotalRew", "Total"]]
    .plot.line(
        x="Year", title="Argentinian Generation of energy per capita from 1965 to 2020"
    )
)
