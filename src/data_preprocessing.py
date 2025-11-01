import pandas as pd
import numpy as np
from astropy.cosmology import FlatLambdaCDM
from astropy import constants as const

# Define cosmological model
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

# Generate synthetic redshift dataset
z_values = np.linspace(0.01, 5, 50)
distance = cosmo.comoving_distance(z_values).value  # in Mpc
luminosity_distance = cosmo.luminosity_distance(z_values).value  # in Mpc
age = cosmo.age(z_values).value  # in Gyr

# Create dataframe
df = pd.DataFrame({
    "redshift_z": z_values,
    "comoving_distance_Mpc": distance,
    "luminosity_distance_Mpc": luminosity_distance,
    "universe_age_Gyr": age
})

# Add universal constants
constants_data = {
    "G_gravitational": const.G.value,
    "c_speed_of_light": const.c.value,
    "H0_current": cosmo.H0.value,
    "Omega_matter": cosmo.Om0,
    "Omega_lambda": cosmo.Ode0
}

# Save files
df.to_csv("data/processed/cosmology_data.csv", index=False)
pd.DataFrame([constants_data]).to_csv("data/processed/constants.csv", index=False)

print("\n✅ Data preprocessing complete.")
print("Saved files:")
print("→ data/processed/cosmology_data.csv")
print("→ data/processed/constants.csv")
