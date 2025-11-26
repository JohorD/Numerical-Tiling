# modules_py/architecture.py

import os

"""
Module responsible for managing the folder structure associated with the different
project integration modes. It defines the mapping between each mode and its base folder
and provides a function to create summary files within the corresponding folder.


It also includes a default reference folder for `int0`, reserved for cases without environmental effects.
"""

# ============================================================
# Mapping of mode → base folder (expandable: three_fields, ...)
# ============================================================

MODE_FOLDERS = {
    "single": "int_blocks_split_mode_single",
    "two_field":  "int_blocks_split_mode_two_field",
    #"three_field":  "int_blocks_split_mode_three_field",
}


# ============================================================
# Universal function
# Create int0 summary file inside the correct split folder
# ============================================================

def create_split_file(mode="single"):
    """
    Create the int0 summary file inside the correct folder
    for the selected mode.

    MODE_FOLDERS[mode] / int0_block_file / int0_summary.inc    
    """
    if mode not in MODE_FOLDERS:
        raise ValueError(f"Unknown mode '{mode}'.")

    root_folder = MODE_FOLDERS[mode]
    subfolder = "int0_block_file"
    include_file = "int0_summary.inc"

    # Construct full paths
    full_path = os.path.join(root_folder, subfolder)
    os.makedirs(full_path, exist_ok=True)

    include_path = os.path.join(full_path, include_file)

    # Write the file content
    with open(include_path, "w") as f:
        f.write("int0 = 0.0\n")

    print(f"✔ Created: {include_path}")
    return include_path
