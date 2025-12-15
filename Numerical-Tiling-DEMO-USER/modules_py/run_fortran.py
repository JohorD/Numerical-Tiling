# modules_py/run_fortran.py
import os
import glob
import subprocess
import time
from modules_py.architecture import MODE_FOLDERS

def run_simulation(mode, param_sets):
    """
    Compile and execute the Fortran (.f90) codes generated for the selected mode,
    using parallel executions via `screen`.

    For each parallelization block:
      - Compile the .f90 file using the Intel `ifx` compiler.
      - Run each binary in a separate `screen` session.

    The status of the simulations is monitored every 15 seconds until
    all sessions are complete. Once completed, the partial
    power spectrum files are concatenated into a single final file within the
    corresponding evolution directory.

    Note:
    - By default, `ifx` (Intel oneAPI) is used on Linux.
    - It can be easily adapted to other compilers (gfortran, ifort)
      or other systems (e.g., macOS).
    """

    # Extract from param_sets
    mod_pref = param_sets[0]["fortran_mod_pref"]
    parallel_sets = param_sets


    # Build paths
    root_folder = MODE_FOLDERS[mode]
    mod_tag = f"{mod_pref:03d}"
    mod_tag_bash = f"{mod_pref}"
    folder_tag = f"Data_&_Codes_{mod_tag}"
    target_dir = os.path.join(root_folder, folder_tag)
    
    # Change to the directory where the .f90 files are located
    original_dir = os.getcwd()
    os.chdir(target_dir)
    
    try:
        # List of .f90 files according to mode
        if mode == "single":
            sources = sorted(glob.glob(f"Tiling_Single_Field_Case_{mod_tag_bash}_Part_*.f90"))
        if mode == "two_field":
            sources = sorted(glob.glob(f"Tiling_Two_Field_Case_{mod_tag_bash}_Part_*.f90"))

        # Compile and run with screen
        for src in sources:
            exe = src.replace(".f90", ".out")
            session = src.replace(".f90", "")
            print(f"🧩 Compiling and executing: {src} → {exe} (screen: {session})")
            subprocess.run(
                ["screen", "-dmS", session, "bash", "-c", f"source /opt/intel/oneapi/setvars.sh && ifx -r8 -O3 {src} -o {exe} && ./{exe}"],
                check=True
            )

        # Wait until they finish
        print("⏳ Waiting for the simulations to finish...")
        while True:
            output = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
            if "No Sockets found" in output.stdout:
                print("✅ All simulations are complete.")
                break
            else:
                print("💡 Still running screens...")
                time.sleep(15)

        # Collect data
        parts = [
            f"Power_Spectrum_PS_{p['fortran_part_iter_parallel']}_{mod_tag}.dat"
            for p in parallel_sets
            if p["fortran_part_iter_parallel"] != "Complete"
        ]

        # The combined file goes in the Evolution folder (which Fortran already created).
        folder_Evolution = f"Evolution_{mod_tag}"
        output_file = os.path.join(folder_Evolution, f"Power_Spectrum_PS_{mod_tag}.dat")

        with open(output_file, "w") as outfile:
            for fname in parts:
                with open(os.path.join(folder_Evolution, fname)) as infile:
                    outfile.write(infile.read())

        print(f"✅ Combined file created: {output_file}")
        return output_file

    finally:
        # Return to the original directory
        os.chdir(original_dir)
