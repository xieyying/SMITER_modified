# import sys
# sys.path.append(r'C:\Users\xyy\Desktop\python\SMITER')

from pprint import pprint
import matplotlib.pyplot as plt
import pyteomics.mzml as mzml
import smiter
from smiter import synthetic_metabolite_mzml
import warnings
warnings.simplefilter("ignore")

# @click.command()
# @click.argument("input_csv")
# @click.argument("output_mzml")
def main(input_csv, output_mzml):
    peak_properties = smiter.lib.csv_to_peak_properties(input_csv)
    
    fragmentor = smiter.fragmentation_functions.NucleosideFragmentor()

    noise_injector = smiter.noise_functions.GaussNoiseInjector(
        dropout=0.0, ppm_var=1)
   
    # noise_injector = smiter.noise_functions.UniformNoiseInjector(
    #     dropout=0.0, ppm_noise=0, intensity_noise=0) # dropout只在ms2中生效
    
    # mzml_params
    mzml_params = {"gradient_length": 400,"ms_rt_diff": 0.3,"max_intensity":0.97e7}
    synthetic_metabolite_mzml.write_mzml(
        output_mzml, peak_properties, fragmentor, noise_injector, mzml_params
    )

    # plot the total ion chromatogram
    rt = []
    i  = []
    spectra = mzml.read(output_mzml)
    for s in spectra:
        rt.append(s["scanList"]["scan"][0]["scan start time"])
        i.append(s["intensity array"].sum())
    plt.plot(rt, i)
    plt.show()

if __name__ == "__main__":
    input_csv = r'D:\workissues\manuscript\halo_mining\HaloAnalyzer\Simulated_LC_MS\test_molecules1448.csv'
    output_mzml = r'D:\workissues\manuscript\halo_mining\HaloAnalyzer\Simulated_LC_MS\test_molecules1448.mzML'
    main(input_csv, output_mzml)
 
