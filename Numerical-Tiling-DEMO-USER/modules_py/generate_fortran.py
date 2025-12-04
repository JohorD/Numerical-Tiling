# modules_py/generate_fortran.py
import os
from modules_py.architecture import MODE_FOLDERS

"""
Module responsible for automatically building and generating the Fortran files needed
for each simulation mode. It defines default profiles (`DEFAULT_PROFILES`) for each
mode—for example, `single` or `two_field`—and allows the user to overwrite any parameter
of interest (already defined or to be defined), provided that said parameter exists in the template used.

From a template located in `templates_fortran/`, the module assembles
the configuration values—global, case, and parallel iteration—and
generates the `.f90` files within the corresponding
folder defined in `MODE_FOLDERS`. Each set of parameters produces a separate
Fortran file, organized by mode and iteration block according to the `parallel` configuration.
"""

# -------------------------
# Default profiles
# -------------------------
DEFAULT_PROFILES = {
    "single": {
        # settings_case
        "case": {
            # Case identifier. 0 is reserved for the case without incoherence;
            # values 1, 2, 3, ... are used for the other scenarios.
            "fortran_mod_pref": 0,
            # Parameterization selector for “accidents.” Accepts 0 or 1:
            #   0 → parameterization in (logL–k) (parallelograms).
            #   1 → parameterization in (logL–N) (rectangles) DEFAULT.
            # The possibility of adding more options in the future is left open (2, 3, ...).
            "fortran_mod_accident": 1,
        },
        # settings_global
        "global": {
            # settings_perturbations
            # Total number of modes to inject.
            "fortran_N_mod": 365,
            # Separation between successive modes.
            # Each new mode is injected every N_step efolds.
            "fortran_N_step": 0.2,
            # Efold value where the firts mode is injected.
            "fortran_N_initial_inj": 0.0,
            # Controls whether the temporal evolution of the injected modes is printed.
            # .true. → the evolution of each mode + the final state of all modes is printed.
            # .false. → only the final state of all modes is printed.
            "fortran_ellipse": ".true.",
            # Frequency (in iterations) with which the evolution data is saved
            # for each mode (only if fortran_ellipse = .true.).
            "fortran_time_resolution": 500,
            # Frequency with which ellipse files are printed between modes.
            # If it is 10, an ellipse is printed every 10 injected modes
            # (only if fortran_ellipse = .true.).
            "fortran_ellipse_resolution": 10,
            # settings_background_and_kphys
            # Initial conditions for the inflaton field
            "initial_phi": 25.0,
            "initial_phi_dot": 0.0,
            # Initial value of ln(a). The evolution of the background starts here,
            # typically several e-folds before the injection of modes to
            # ensure that the system reaches the attractor.
            "initial_ln_a": -5.0,
            # Factor that determines the physical value of the mode at the moment of its injection.
            # Once the evolution reaches N_initial_inj, the following is calculated:
            #     k_phys = fortran_kphys * H
            # where H is the value of the Hubble parameter at that instant.
            "fortran_kphys": 1000.0,
            # settings_potential
            # Inflation potential displayed in a user-readable format.
            "fortran_potential": "V(φ) = λ φ⁴ / 4",
            # Expression of the potential used in the Fortran code.
            "fortran_Vphi": "1.0d-14 * phi*phi*phi*phi / 4.0",
            # First derivative of the potential with respect to the φ field.
            "fortran_Vprime": "1.0d-14 * phi*phi*phi",
            # Second derivative of the potential with respect to φ.
            "fortran_Vprimeprime": "3.0 * 1.0d-14 * phi*phi",
            # settings_window
            "fortran_transition": 0.5,
        },
        # settings_iter_parallel
        "parallel": [
            {"fortran_part_iter_parallel": "Complete", "fortran_iter_initial": 1, "fortran_iter_final": 365},
            {"fortran_part_iter_parallel": "Part_1",   "fortran_iter_initial": 1,   "fortran_iter_final": 50},
            {"fortran_part_iter_parallel": "Part_2",   "fortran_iter_initial": 51,  "fortran_iter_final": 100},
            {"fortran_part_iter_parallel": "Part_3",   "fortran_iter_initial": 101, "fortran_iter_final": 150},
            {"fortran_part_iter_parallel": "Part_4",   "fortran_iter_initial": 151, "fortran_iter_final": 200},
            {"fortran_part_iter_parallel": "Part_5",   "fortran_iter_initial": 201, "fortran_iter_final": 250},
            {"fortran_part_iter_parallel": "Part_6",   "fortran_iter_initial": 251, "fortran_iter_final": 300},
            {"fortran_part_iter_parallel": "Part_7",   "fortran_iter_initial": 301, "fortran_iter_final": 365},
        ],
    },

    "two_field": {
        # settings_case
        "case": {
            # Case identifier. 0 is reserved for the case without incoherence;
            # values 1, 2, 3, ... are used for the other scenarios.
            "fortran_mod_pref": 0,
            # Parameterization selector for “accidents.” Accepts 0 or 1:
            #   0 → parameterization in (logL–k) (parallelograms).
            #   1 → parameterization in (logL–N) (rectangles) DEFAULT.
            # The possibility of adding more options in the future is left open (2, 3, ...).
            "fortran_mod_accident": 1,
        },
        # settings_global
        "global": {
            # settings_perturbations
            # Total number of modes to inject.
            "fortran_N_mod": 415,
            # Separation between successive modes.
            # Each new mode is injected every N_step efolds.
            "fortran_N_step": 0.2,
            # Efold value where the firts mode is injected.
            "fortran_N_initial_inj": 0.0,
            # Controls whether the temporal evolution of the injected modes is printed.
            # .true. → the evolution of each mode + the final state of all modes is printed.
            # .false. → only the final state of all modes is printed.
            "fortran_ellipse": ".true.",
            # Frequency (in iterations) with which the evolution data is saved
            # for each mode (only if fortran_ellipse = .true.).
            "fortran_time_resolution": 500,
            # Frequency with which ellipse files are printed between modes.
            # If it is 10, an ellipse is printed every 10 injected modes
            # (only if fortran_ellipse = .true.).
            "fortran_ellipse_resolution": 10,
            # settings_background_and_kphys
            # Initial conditions for the fields
            "initial_phi_1_two_field": 20.0,
            "initial_phi_dot_1_two_field": 0.0,
            "initial_phi_2_two_field": 20.0,
            "initial_phi_dot_2_two_field": 0.0,
            # Initial value of ln(a). The evolution of the background starts here,
            # typically several e-folds before the injection of modes to
            # ensure that the system reaches the attractor.
            "initial_ln_a": -5.0,
            # Factor that determines the physical value of the mode at the moment of its injection.
            # Once the evolution reaches N_initial_inj, the following is calculated:
            #     k_phys = fortran_kphys * H
            # where H is the value of the Hubble parameter at that instant.
            "fortran_kphys": 1000.0,
            # settings_potential
            # Inflation potential displayed in a user-readable format.
            "fortran_potential_two_field": "V(φ₁, φ₂) = λ φ₁⁴ / 4 + 1/2 g φ₁² φ₂²",
            # Expression of the potential used in the Fortran code.
            "fortran_Vphi_two_field": "1.0d-14 * phi(1)*phi(1)*phi(1)*phi(1)*0.25 + 0.5*(2.0*(1.0d-14))*phi(1)*phi(1)*phi(2)*phi(2)",
            # First derivative of the potential with respect to the φ₁ field.
            "fortran_Vprime_1_two_field": "1.0d-14 * phi(1)*phi(1)*phi(1) + (2.0*(1.0d-14))*phi(1)*phi(2)*phi(2)",
            # First derivative of the potential with respect to the φ₂ field.
            "fortran_Vprime_2_two_field": "(2.0*(1.0d-14))*phi(1)*phi(1)*phi(2)",
            # Second derivative of the potential with respect to φ₁φ₁
            "fortran_Vprimeprime_11_two_field": "3.0 * 1.0d-14 * phi(1)*phi(1) + (2.0*(1.0d-14))*phi(2)*phi(2)",
            # Second derivative of the potential with respect to φ₁φ₂
            "fortran_Vprimeprime_12_two_field": "2.0*(2.0*(1.0d-14))*phi(1)*phi(2)",
            # Second derivative of the potential with respect to φ₂φ₂
            "fortran_Vprimeprime_22_two_field": "(2.0*(1.0d-14))*phi(1)*phi(1)",
            # settings_window
            "fortran_transition": 0.5,
            # settings_environment / interactions
            #Generic
            "fortran_interaction_two_field": "I = α₁ v₁ + α₂ v₂",
            "fortran_alpha_1_two_field": 1.0,
            "fortran_alpha_2_two_field": 1.0,
            "fortran_interaction_1_two_field": "alpha(1)",
            "fortran_interaction_2_two_field": "alpha(2)",            
            #Isentropic
            #fortran_interaction_two_field="I∥ = α₁ v∥₁ + α₂ v∥₂",
            #fortran_alpha_1_two_field=1.0,
            #fortran_alpha_2_two_field=1.0,
            #fortran_interaction_1_two_field= "( alpha(1)*phi_dot(1)*phi_dot(1) + alpha(2)*phi_dot(1)*phi_dot(2) )/( phi_dot(1)*phi_dot(1) + phi_dot(2)*phi_dot(2) )",
            #fortran_interaction_2_two_field= "( alpha(1)*phi_dot(1)*phi_dot(2) + alpha(2)*phi_dot(2)*phi_dot(2) )/( phi_dot(1)*phi_dot(1) + phi_dot(2)*phi_dot(2) )",
            #Isocurvature
            #fortran_interaction_two_field="I⊥ = α₁ v⊥₁ + α₂ v⊥₂",
            #fortran_alpha_1_two_field=1.0,
            #fortran_alpha_2_two_field=1.0,
            #fortran_interaction_1_two_field= "alpha(1) - ( alpha(1)*phi_dot(1)*phi_dot(1) + alpha(2)*phi_dot(1)*phi_dot(2) )/( phi_dot(1)*phi_dot(1) + phi_dot(2)*phi_dot(2) )",
            #fortran_interaction_2_two_field= "alpha(2) - ( alpha(1)*phi_dot(1)*phi_dot(2) + alpha(2)*phi_dot(2)*phi_dot(2) )/( phi_dot(1)*phi_dot(1) + phi_dot(2)*phi_dot(2) )",
        },
        # settings_iter_parallel
        "parallel": [
            {"fortran_part_iter_parallel": "Complete", "fortran_iter_initial": 1, "fortran_iter_final": 415},
            {"fortran_part_iter_parallel": "Part_1",   "fortran_iter_initial": 1,   "fortran_iter_final": 60},
            {"fortran_part_iter_parallel": "Part_2",   "fortran_iter_initial": 61,  "fortran_iter_final": 120},
            {"fortran_part_iter_parallel": "Part_3",   "fortran_iter_initial": 121, "fortran_iter_final": 180},
            {"fortran_part_iter_parallel": "Part_4",   "fortran_iter_initial": 181, "fortran_iter_final": 240},
            {"fortran_part_iter_parallel": "Part_5",   "fortran_iter_initial": 241, "fortran_iter_final": 300},
            {"fortran_part_iter_parallel": "Part_6",   "fortran_iter_initial": 301, "fortran_iter_final": 360},
            {"fortran_part_iter_parallel": "Part_7",   "fortran_iter_initial": 361, "fortran_iter_final": 415},
        ],
    },
}

# -------------------------
# Load template from folder
# -------------------------
def load_template(filename):
    path = os.path.join("templates_fortran", filename)
    with open(path, "r") as f:
        return f.read()


# -------------------------
# Build parameter sets
# -------------------------
def build_parameter_sets(mode, case_overrides=None, global_overrides=None, parallel_overrides=None):

    if mode not in DEFAULT_PROFILES:
        raise ValueError("Unknown mode.")

    profile = DEFAULT_PROFILES[mode]

    case = {**profile["case"], **(case_overrides or {})}
    global_p = {**profile["global"], **(global_overrides or {})}
    parallel_list = parallel_overrides if parallel_overrides else profile["parallel"]

    return [
        {**case, **global_p, **p}
        for p in parallel_list
    ]


# -------------------------
# Generate .f90 files into the proper folder
# -------------------------
def generate_fortran_files(template_text, mode, param_sets, output_root=None):
    """
    Generates:
      MODE_FOLDERS[mode] / Data_&_Codes_xxx / Tiling_...f90
    """
    if mode not in MODE_FOLDERS:
        raise ValueError(f"Unknown mode '{mode}'.")

    output_root = output_root or MODE_FOLDERS[mode]

    # All param_sets share same fortran_mod_pref
    mod_pref = param_sets[0]["fortran_mod_pref"]
    folder_tag = f"Data_&_Codes_{mod_pref:03d}"
    target_dir = os.path.join(output_root, folder_tag)
    os.makedirs(target_dir, exist_ok=True)

    generated = []

    for params in param_sets:

        if mode == "single":
            fname = f"Tiling_Single_Field_Case_{params['fortran_mod_pref']}_{params['fortran_part_iter_parallel']}.f90"
        elif mode == "two_field":
            fname = f"Tiling_Two_Field_Case_{params['fortran_mod_pref']}_{params['fortran_part_iter_parallel']}.f90"

        out_path = os.path.join(target_dir, fname)

        with open(out_path, "w") as f:
            f.write(template_text.format(**params))

        generated.append(out_path)
        print(f"[OK] Generated: {out_path}")

    return generated

