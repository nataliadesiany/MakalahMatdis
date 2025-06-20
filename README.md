# 👕 Smart Outfit Planner

## 📌 Overview
Smart Outfit Planner is a Python-based combinatorial outfit recommendation system that suggests clothing combinations based on weather, occasion, and user preferences. It uses a rule-based constraint engine and mathematical combinatorics to generate, filter, and rank potential outfits.

## 🎯 Features
- Constraint-based outfit validation (availability, weather rules, occasion suitability, color harmony)
- Combinatorial generation of outfit combinations using the Rule of Product and Combinations theory
- Dynamic wardrobe management (includes unavailable items simulation)
- Interactive command-line interface (CLI)
- Weighted soft scoring system: 70% color harmony + 30% user preferences

## 🚀 How to Run
Make sure you have Python installed, then simply run:

python Planner.py


## 🧩 Parameters (in Interactive Mode)
- **Weather**: `hot`, `warm`, `cool`, `cold`
- **Occasion**: `formal`, `business`, `casual`, `sporty`, `party`
- **Preferred Colors**: Optional, e.g., `red, navy`
- **Number of Recommendations**: Optional (default: 5, max: 20)

## 📦 System Components
- `ClothingItem`: Object representing an item of clothing
- `Wardrobe`: Manages all clothing items and their availability
- `ConstraintEngine`: Validates constraints for each outfit
- `CombinorialGenerator`: Generates and scores outfit combinations
- `SmartOutfitPlanner`: Main controller class, connects all modules and manages user interaction

## 🛠 CLI Commands
- `recommend` – Generate outfit suggestions
- `status` – Show wardrobe statistics and availability
- `help` – View help guide
- `quit` – Exit the program

---
