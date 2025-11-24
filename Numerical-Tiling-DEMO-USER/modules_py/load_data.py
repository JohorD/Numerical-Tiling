# modules_py/load_data.py
import os
import numpy as np
from modules_py.architecture import MODE_FOLDERS

def load_data(filename, mode):
    """
    Loads the Evolution file and returns a dictionary according to the mode.
    """
    data = np.loadtxt(filename)
    
    if mode == "single":
        dic = {
            'phi': data[:,0], 'phi_dot': data[:,1], 'Hubble': data[:,2], 'N': data[:,3],
            'L': data[:,4], 'Lp': data[:,5], 'Tp': data[:,6], 'epsilon': data[:,7],
            'zpp_z': data[:,8], 'Vphi': data[:,9], 'Vdphi': data[:,10], 'Vddphi': data[:,11],
            'kcom': data[:,12], 'kphys': data[:,13], 'z': data[:,14],
            'Source': data[:,15], 'logL': data[:,16]
        }
        dic['kvar'] = dic['kcom'] / (np.exp(dic['N']) * dic['Hubble'])
        dic['zeta'] = dic['kcom']**3 * dic['L']**2 / (2*np.pi**2 * dic['z']**2)
        dic['gammavv'] = 2.0 * dic['kcom'] * dic['L']**2
        dic['gammavp'] = 2.0 * dic['L'] * dic['Lp']
        dic['gammapp'] = 2.0 * (dic['Lp']**2 + dic['L']**2 * dic['Tp']**2) / dic['kcom']
        dic['Determinant'] = 4.0 * dic['L']**4 * dic['Tp']**2
        dic['r'] = 0.5 * np.arccosh(0.5*(dic['kcom']**2 + dic['Tp']**2 + (dic['Lp']/dic['L'])**2)/(dic['kcom']*dic['Tp']))
        dic['varphi'] = 0.5*np.arctan2(2.0*dic['kcom']*(dic['Lp']/dic['L']), dic['kcom']**2 - dic['Tp']**2 - (dic['Lp']/dic['L'])**2) - np.pi/2
        dic['Omega'] = dic['kcom']**2 - dic['zpp_z']
        
    elif mode == "two_field":
        dic = {
            'phi_1': data[:,0], 'phi_2': data[:,1], 'phi_1_dot': data[:,2], 'phi_2_dot': data[:,3], 
            'Hubble': data[:,4], 'N': data[:,5],
            'L_11': data[:,6], 'L_12': data[:,7], 'L_21': data[:,8], 'L_22': data[:,9],
            'Lp_11': data[:,10], 'Lp_12': data[:,11], 'Lp_21': data[:,12], 'Lp_22': data[:,13],
            'Y_11': data[:,14], 'Y_12': data[:,15], 'Y_21': data[:,16], 'Y_22': data[:,17],
            'Z_11': data[:,18], 'Z_12': data[:,19], 'Z_21': data[:,20], 'Z_22': data[:,21],
            'epsilon': data[:,22], 'eta': data[:,23], 'Hf': data[:,24], 'kcom': data[:,25], 'kphys': data[:,26], 
            'Vphi': data[:,27], 'Vdphi1': data[:,28], 'Vdphi2': data[:,29],
            'Vdphi1dphi1': data[:,30], 'Vdphi1dphi2': data[:,31], 'Vdphi2dphi1': data[:,32], 'Vdphi2dphi2': data[:,33], 
            'M_11': data[:,34], 'M_12': data[:,35], 'M_21': data[:,36], 'M_22': data[:,37], 
            'Omega_11': data[:,38], 'Omega_12': data[:,39], 'Omega_21': data[:,40], 'Omega_22': data[:,41], 
            'A_11': data[:,42], 'A_12': data[:,43], 'A_21': data[:,44], 'A_22': data[:,45],
            'Decoherence_11': data[:,46], 'Decoherence_12': data[:,47], 'Decoherence_21': data[:,48], 'Decoherence_22': data[:,49], 
            'logL': data[:,50], 'F': data[:,51],
        }
        dic['kvar'] = dic['kcom'] / (np.exp(dic['N']) * dic['Hubble'])
        dic['zeta'] = (dic['kcom']**3 / (4*np.pi**2)) * (dic['Hubble']**2 / (np.exp(2.0*dic['N']) * (dic['phi_1_dot']**2 + dic['phi_2_dot']**2)**2)) * (
            dic['phi_1_dot']**2 * dic['L_11']**2 + dic['phi_2_dot']**2 * (dic['L_21']**2 + dic['L_22']**2) + 
            2.0 * dic['phi_1_dot'] * dic['phi_2_dot'] * dic['L_11'] * dic['L_21']
        )
        dic['gammavv_11'] = 2.0 * dic['kcom'] * dic['L_11']**2
        dic['gammavv_12'] = 2.0 * dic['kcom'] * dic['L_11'] * dic['L_21']
        dic['gammavv_22'] = 2.0 * dic['kcom'] * (dic['L_21']**2 + dic['L_22']**2)
        dic['gammavp_11'] = 2.0 * dic['L_11'] * dic['Lp_11']
        dic['gammavp_12'] = 2.0 * dic['L_11'] * (dic['Lp_21'] - dic['L_22'] * dic['Y_12'])
        dic['gammavp_21'] = 2.0 * dic['Lp_11'] * dic['L_21'] + 2.0 * dic['L_11'] * dic['L_22'] * dic['Y_12']
        dic['gammavp_22'] = 2.0 * dic['L_21'] * dic['Lp_21'] + 2.0 * dic['L_22'] * dic['Lp_22']
        dic['gammapp_11'] = 2.0 * (dic['Lp_11']**2 + dic['L_11']**2 * (dic['Y_12']**2 + dic['Z_11'])) / dic['kcom']
        dic['gammapp_12'] = 2.0 * (dic['Lp_11'] * dic['Lp_21'] + dic['L_11'] * dic['L_21'] * (dic['Y_12']**2 + dic['Z_11']) + 
                                  dic['L_11'] * dic['L_22'] * dic['Z_12'] + dic['Y_12'] * (dic['L_11'] * dic['Lp_22'] - dic['Lp_11'] * dic['L_22'])) / dic['kcom']
        dic['gammapp_22'] = 2.0 * (dic['Lp_21']**2 + dic['Lp_22']**2 + dic['L_21']**2 * (dic['Y_12']**2 + dic['Z_11']) + 
                                  dic['L_22']**2 * (dic['Y_12']**2 + dic['Z_22']) + 2.0 * dic['L_21'] * dic['L_22'] * dic['Z_12'] + 
                                  2.0 * dic['Y_12'] * (dic['L_21'] * dic['Lp_22'] - dic['L_22'] * dic['Lp_21'])) / dic['kcom']
        dic['Determinant'] = 16.0 * dic['L_11']**4 * dic['L_22']**4 * (dic['Z_11'] * dic['Z_22'] - dic['Z_12']**2)
    
    return dic

# Label dictionaries
ylabel_dict_single = {
    'phi': '$\\displaystyle{\\phi}$',
    'phi_dot': '$\\displaystyle{\\dot{\\phi}}$',
    'Hubble': 'H',
    'N': '$\\displaystyle{N}$',
    'L': '$\\displaystyle{L}$',
    'Lp': '$\\displaystyle{ L^{\\prime} }$',
    'Tp': '$\\displaystyle{ \\theta^{\\prime} }$',
    'epsilon': '$\\displaystyle{ \\epsilon }$',
    'zpp_z': '$\\displaystyle{ \\frac{z^{\\prime \\prime}  }{z} }$',
    'Vphi': '$\\displaystyle{ V(\\phi)  }$',
    'Vdphi': '$\\displaystyle{ \\partial V(\\phi)   }$',
    'Vddphi': '$\\displaystyle{ \\partial \\partial V(\\phi)   }$',
    'kcom': '$\\displaystyle{ \\text{k} }$',
    'kphys': '$\\displaystyle{ \\text{k}_{\\text{phys}} }$',
    'z': '$\\displaystyle{ z }$',
    'Source': '$\\mathcal{F}$',
    'logL': '$\\displaystyle{ \\ln{\\ell} }$',
    'kvar': '$\\displaystyle{ \\ln\\left(\\frac{k}{aH}\\right) }$',
    'zeta': '$\\displaystyle{ \\mathcal{P}_{\\zeta} }$',
    'gammavv': '$\\displaystyle{\\gamma_{ v v}}$',
    'gammavp': '$\\displaystyle{\\gamma_{ v \\pi }}$',
    'gammapp': '$\\displaystyle{\\gamma_{ \\pi \\pi }}$',
    'Determinant': '$\\displaystyle{ \\mathcal{S} }$',
    'r': '$\\displaystyle{r_{k}}$',
    'varphi': '$\\displaystyle{\\varphi_{k}}$',
    'Omega': '$\\displaystyle{ \\omega }$' 
}

ylabel_dict_two_field = {
    'phi_1': '$\\displaystyle{\\phi_{1}  }$',
    'phi_2': '$\\displaystyle{\\phi_{2}  }$',
    'phi_1_dot': '$\\displaystyle{\\dot{\\phi}_{1} }$',
    'phi_2_dot': '$\\displaystyle{\\dot{\\phi}_{2}  }$',
    'Hubble': 'H',
    'N': '$\\displaystyle{N}$',
    'L_11': '$\\displaystyle{L_{11}  }$',
    'L_12': '$\\displaystyle{L_{12}  }$',
    'L_21': '$\\displaystyle{L_{21}  }$',
    'L_22': '$\\displaystyle{L_{22}  }$',
    'Lp_11': '$\\displaystyle{L^{\\prime_{11}  }$',
    'Lp_12': '$\\displaystyle{L^{\\prime_{12}  }$',
    'Lp_21': '$\\displaystyle{L^{\\prime_{21}  }$',
    'Lp_22': '$\\displaystyle{L^{\\prime_{22}  }$',
    'Y_11': '$\\displaystyle{Y_{11}  }$',
    'Y_12': '$\\displaystyle{Y_{12}  }$',
    'Y_21': '$\\displaystyle{Y_{21}  }$',
    'Y_22': '$\\displaystyle{Y_{22}  }$',
    'Z_11': '$\\displaystyle{Z_{11}  }$',
    'Z_12': '$\\displaystyle{Z_{12}  }$',
    'Z_21': '$\\displaystyle{Z_{21}  }$',
    'Z_22': '$\\displaystyle{Z_{22}  }$',
    'epsilon': '$\\displaystyle{ \\epsilon }$',
    'eta': '$\\displaystyle{ \\eta }$',
    'Hf': 'Hf',
    'kcom': '$\\displaystyle{ \\text{k} }$',
    'kphys': '$\\displaystyle{ \\text{k}_{\\text{phys}} }$',
    'Vphi': '$\\displaystyle{ V(\\phi)  }$',
    'Vdphi1': '$\\displaystyle{ \\partial_{1} V(\\phi)   }$',
    'Vdphi2': '$\\displaystyle{ \\partial_{2} V(\\phi)   }$',
    'Vdphi1dphi1': '$\\displaystyle{ \\partial_{11} V(\\phi)   }$',
    'Vdphi1dphi2': '$\\displaystyle{ \\partial_{12} V(\\phi)   }$',
    'Vdphi2dphi1': '$\\displaystyle{ \\partial_{21} V(\\phi)   }$',
    'Vdphi2dphi2': '$\\displaystyle{ \\partial_{22} V(\\phi)   }$',
    'M_11': '$\\displaystyle{M_{11}  }$',
    'M_12': '$\\displaystyle{M_{12}  }$',
    'M_21': '$\\displaystyle{M_{21}  }$',
    'M_22': '$\\displaystyle{M_{22}  }$',
    'Omega_11': '$\\displaystyle{\\Omega_{11}  }$',
    'Omega_12': '$\\displaystyle{\\Omega_{12}  }$',
    'Omega_21': '$\\displaystyle{\\Omega_{21}  }$',
    'Omega_22': '$\\displaystyle{\\Omega_{22}  }$',
    'A_11': '$\\displaystyle{A_{11}  }$',
    'A_12': '$\\displaystyle{A_{12}  }$',
    'A_21': '$\\displaystyle{A_{21}  }$',
    'A_22': '$\\displaystyle{A_{22}  }$',
    'Decoherence_11': '$\\displaystyle{D_{11}  }$',
    'Decoherence_12': '$\\displaystyle{D_{12}  }$',
    'Decoherence_21': '$\\displaystyle{D_{21}  }$',
    'Decoherence_22': '$\\displaystyle{D_{22}  }$',    
    'F': '$\\mathcal{F}$',
    'logL': '$\\displaystyle{ \\ln{\\ell} }$',
    'kvar': '$\\displaystyle{ \\ln\\left(\\frac{k}{aH}\\right) }$',
    'zeta': '$\\displaystyle{ \\mathcal{P}_{\\zeta} }$',
    'gammavv_11': '$\\displaystyle{\\gamma^{11}_{ v v}  }$',
    'gammavv_12': '$\\displaystyle{\\gamma^{12}_{ v v}  }$',
    'gammavv_22': '$\\displaystyle{\\gamma^{22}_{ v v}  }$',
    'gammavp_11': '$\\displaystyle{\\gamma^{11}_{ v \\pi }  }$',
    'gammavp_12': '$\\displaystyle{\\gamma^{12}_{ v \\pi }  }$',
    'gammavp_21': '$\\displaystyle{\\gamma^{21}_{ v \\pi }  }$',
    'gammavp_22': '$\\displaystyle{\\gamma^{22}_{ v \\pi }  }$',
    'gammapp_11': '$\\displaystyle{\\gamma^{11}_{ \\pi \\pi }}$',
    'gammapp_12': '$\\displaystyle{\\gamma^{12}_{ \\pi \\pi }}$',
    'gammapp_22': '$\\displaystyle{\\gamma^{22}_{ \\pi \\pi }}$',
    'Determinant': '$\\displaystyle{ \\mathcal{S} }$', 
}

def get_ylabel_dict(mode):
    """Returns the label dictionary according to the mode"""
    if mode == "single":
        return ylabel_dict_single
    elif mode == "two_field":
        return ylabel_dict_two_field
    else:
        raise ValueError(f"Mode '{mode}' not recognized")



def load_structure(mode, param_sets):    
    """
    Load Power Spectrum and ellipse data from an Evolution_XXX folder.
    """
    if mode not in MODE_FOLDERS:
        raise ValueError(f"Unknown mode '{mode}'.")

    # === Main parameters ===
    mod_pref   = param_sets[0]["fortran_mod_pref"]
    N_mod      = param_sets[0]["fortran_N_mod"]
    N_step     = param_sets[0]["fortran_N_step"]
    res_elip   = param_sets[0]["fortran_ellipse_resolution"]
    fortran_ellipse = (param_sets[0]["fortran_ellipse"]) 
    use_ellipse = str(fortran_ellipse).strip().lower() in [".true."]
    
    try:
        # === Paths ===
        root_folder = MODE_FOLDERS[mode]
        mod_tag = f"{mod_pref:03d}"
        folder_tag = f"Data_&_Codes_{mod_tag}"
        base_path = os.path.join(root_folder, folder_tag)
        folder = os.path.join(base_path, f"Evolution_{mod_tag}")

        # ------------------------------------------------------------------
        #  POWER SPECTRUM
        # ------------------------------------------------------------------
        power_filename = f"Power_Spectrum_PS_{mod_tag}.dat"
        power_path = os.path.join(folder, power_filename)

        data_power = load_data(power_path, mode) if os.path.exists(power_path) else None
        if data_power is None:
            print(f"⚠️   Could not load Power Spectrum (file missing or empty): {power_path}")

        # ------------------------------------------------------------------
        #  Ellipse
        # ------------------------------------------------------------------
        ellipse = {}
        
        if use_ellipse:
            for iter_val in range(1, N_mod + 1):
                if iter_val % res_elip == 0:
                    fname = f"Ellipse_P{mod_tag}_Iter_{iter_val:06d}.dat"
                    fpath = os.path.join(folder, fname)
                    ellipse[iter_val] = load_data(fpath, mode) if os.path.exists(fpath) else None

        # Return final dict
        # --------------------
        return {
            "folder": folder,
            "power_spectrum": data_power,
            "ellipse": ellipse
        }

    except Exception as e:
        print(f"❌ Error loading structure for case {mod_pref}: {e}")
        return None


    
