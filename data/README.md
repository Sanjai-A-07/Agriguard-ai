# Data

Training data is not committed. Download PlantVillage and build the splits:

    git clone --depth 1 https://github.com/spMohanty/PlantVillage-Dataset data/PlantVillage-Dataset
    python ml/prepare_dataset.py --source data/PlantVillage-Dataset/raw/color --out data/tomato_split

The script lists the tomato folders it finds and stops if any expected class is missing.
