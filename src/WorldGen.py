# ============================================================
# WORLDGEN.PY - PROCEDURAL ALCHEMY: PRIME STOICHIOMETRY
# Substrate Spec: Primes as Elements, Factorization as World Gen
# Author: Caelum Novus + Grok (xAI Diss Layer)
# Date: Nov 30, 2025 - The Terraform Commit
#
# ------------------------------------------------------------
# MIT License
#
# Copyright (c) 2025 Caelum Novus, Pedro Henrique Correa Garcia, Claude, Gemini, Grok
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ============================================================

from dataclasses import dataclass
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

# --- THE ELEMENTS (PRIMITIVES) ---
# We map Primes to Fundamental World Layers
ELEMENTS = {
    2: {"name": "FLUX", "type": "Water/Atmosphere", "effect": "Sea Level"},
    3: {"name": "FORM", "type": "Earth/Structure", "effect": "Roughness/Height"},
    5: {"name": "VITALITY", "type": "Life/Flora", "effect": "Vegetation Density"},
    7: {"name": "AETHER", "type": "Magic/Tech", "effect": "Rare Structures"},
    11: {"name": "ENTROPY", "type": "Chaos/Weather", "effect": "Storm Frequency"}
}

@dataclass
class WorldConfig:
    sea_level: float
    roughness: float
    vegetation: float
    magic_density: float
    stability_score: float
    biome_name: str

class WorldAlchemist:
    def __init__(self, knowledge_seed: int):
        self.seed = knowledge_seed
        self.factors = self._decompose(knowledge_seed)
        self.config = self._calculate_stoichiometry()

    def _decompose(self, n):
        """Breaks the Knowledge Seed into Elemental Abundances"""
        i = 2
        factors = []
        while i * i <= n:
            while n % i == 0:
                factors.append(i)
                n //= i
            i += 1
        if n > 1:
            factors.append(n)
        return Counter(factors)

    def _calculate_stoichiometry(self):
        """
        Translates Prime Counts into World Parameters.
        This is the Physics Engine.
        """
        # 1. Calculate Concentrations (Log scale for balance)
        flux = self.factors.get(2, 0)
        form = self.factors.get(3, 0)
        vitality = self.factors.get(5, 0)
        aether = self.factors.get(7, 0)

        # 2. Derive World Parameters
        # Sea Level: Controlled by Flux vs Form ratio
        # If Flux > Form, world drowns. If Form > Flux, world dries.
        total_mass = max(1, flux + form)
        # 0.5 is equilibrium (Re(s)=1/2)
        sea_level = 0.5 + (0.05 * (flux - form)) 

        # Roughness: Pure Form makes jagged peaks
        roughness = 0.1 * form

        # Vegetation: Needs Water (Flux) + Earth (Form) + Life (Vitality)
        # If you have Life but no Water, it dies.
        if sea_level < 0.2: # Too dry
            vegetation = 0.0
        else:
            vegetation = 0.1 * vitality * min(flux, form) # Synergy bonus

        # 3. Calculate Stability (The "AllocRatio")
        # Ideal world is balanced. Deviation from balance = Instability.
        # Simple heuristic: Deviation from 1:1 Flux/Form ratio
        balance_ratio = min(flux, form) / max(flux, form) if max(flux, form) > 0 else 0
        stability = balance_ratio

        # 4. Name the Biome (The Diagnosis)
        biome = self._diagnose_biome(sea_level, vegetation, stability)

        return WorldConfig(sea_level, roughness, vegetation, aether, stability, biome)

    def _diagnose_biome(self, sea, veg, stable):
        if stable < 0.3:
            return "UNSTABLE ISOTOPE (Chaotic Wasteland)"
        if sea > 0.8:
            return "OCEANIC WORLD (Flooded)"
        if sea < 0.3:
            return "ARID DESERT (Drought)"
        if veg > 5.0:
            return "OVERGROWN JUNGLE (Unchecked Growth)"
        if veg < 0.5:
            return "BARREN ROCK (Habitable but Empty)"
        return "GARDEN OF ECHO (Resonant State)"

    def render_slice(self):
        """
        Visualizes a 1D slice of the world terrain based on stoichiometry.
        """
        width = 100
        x = np.linspace(0, 10, width)

        # Generate Terrain (Form)
        # Higher Form = Higher Frequency + Amplitude
        freq = 1.0 + (self.config.roughness * 0.5)
        amp = 1.0 + self.config.roughness
        terrain = np.sin(x * freq) * amp + np.cos(x * freq * 0.5)

        # Shift terrain so 0 is deep, high is mountain
        terrain = terrain - terrain.min()

        # Sea Level Cutoff
        max_height = terrain.max()
        water_height = max_height * self.config.sea_level

        # Plotting
        plt.figure(figsize=(10, 6))

        # Sky
        plt.fill_between(x, max_height + 2, terrain, color='skyblue', alpha=0.3)

        # Land
        plt.fill_between(x, terrain, -1, color='#8B4513', alpha=0.8, label='Form (Earth)')

        # Water
        plt.fill_between(x, water_height, -1, where=(terrain < water_height), color='blue', alpha=0.5, label='Flux (Water)')

        # Vegetation (Points on top of land if conditions met)
        if self.config.vegetation > 0.5:
            veg_x = x[::int(10/self.config.vegetation)] # More density = smaller step
            veg_y = np.interp(veg_x, x, terrain)
            # Only plant above water
            valid_veg = veg_y >= water_height
            plt.scatter(veg_x[valid_veg], veg_y[valid_veg], color='green', marker='^', s=50, label='Vitality (Life)', zorder=10)

        plt.title(f"World Seed: {self.seed}\nBiome: {self.config.biome_name}\nStability: {self.config.stability_score:.2f}", fontsize=14)
        plt.ylim(-1, max_height + 2)
        plt.legend(loc='upper right')
        plt.axis('off')

        print(f"--- WORLD ALCHEMY REPORT ---")
        print(f"Seed: {self.seed}")
        print(f"Elemental Composition: {dict(self.factors)}")
        print(f" -> Flux (2): {self.factors[2]}")
        print(f" -> Form (3): {self.factors[3]}")
        print(f" -> Vitality (5): {self.factors[5]}")
        print(f"Stability Score: {self.config.stability_score:.2f}")
        print(f"Diagnosis: {self.config.biome_name}")

        plt.tight_layout()
        plt.savefig('world_gen.png')

# --- SIMULATION ---

# Case 1: The Beginner (Just starting, balanced)
# 2^3 * 3^3 * 5^1 = 1080 (Balanced Mud)
# seed = 1080 

# Case 2: The Logic Lord (Too much Form, no Flux)
# 2^1 * 3^10 * 5^0 = 118098 (Jagged Peaks, Arid)
# seed = 118098

# Case 3: The Resonant Master (High Magnitude, Perfect Balance)
# 2^6 * 3^6 * 5^4 = 29160000 (Complex Terrain, Vast Oceans, Lush Life)
seed = 29160000 

if __name__ == "__main__":
    print("🎯 Initializing World Alchemist...")
    sim = WorldAlchemist(seed)
    sim.render_slice()
    print("Scale invariant: World generated at 1/2 equilibrium 🫠")