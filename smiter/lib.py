"""Core functionality."""
import csv
from io import TextIOWrapper
from tempfile import _TemporaryFileWrapper

from smiter.params.default_params import default_mzml_params, default_peak_properties

PROTON = 1.00727646677


def calc_mz(mass: float, charge: int):
    """Calculate m/z.

    Args:
        mass (TYPE): Description
        charge (TYPE): Description
    """
    mass = float(mass)
    charge = int(charge)
    calc_mz = (mass + (charge * PROTON)) / charge
    return calc_mz


def check_mzml_params(mzml_params: dict) -> dict:
    """Summary.

    Args:
        mzml_params (dict): Description

    Returns:
        dict: Description

    Raises:
        Exception: Description
    """
    for default_param, default_value in default_mzml_params.items():
        # param not set and default param required
        if (mzml_params.get(default_param, None) is None) and (default_value is None):
            raise Exception(f"mzml parameter {default_param} is required by not set!")
        elif mzml_params.get(default_param, None) is None:
            mzml_params[default_param] = default_value
    return mzml_params


def check_peak_properties(peak_properties: dict) -> dict:
    """Summary.

    Args:
        peak_properties (dict): Description

    Returns:
        dict: Description

    Raises:
        Exception: Description
    """
    for mol, properties in peak_properties.items():
        for default_param, default_value in default_peak_properties.items():
            if (properties.get(default_param, None) is None) and (
                default_value is None
            ):
                raise Exception(
                    f"mzml parameter {default_param} is required by not set!"
                )
            elif properties.get(default_param, None) is None:
                properties[default_param] = default_value
    return peak_properties


def csv_to_peak_properties(csv_file):
    peak_properties = {}
    with open(csv_file) as fin:
        reader = csv.DictReader(fin)
        for line_dict in reader:
            cc = line_dict["chemical_formula"]
            peak_properties[cc] = {
                "trivial_name": line_dict["trivial_name"],
                "chemical_formula": cc,
                "charge": line_dict.get("charge", 2),
                "scan_start_time": float(line_dict["scan_start_time"]),
                # currently only gaussian peaks from csv
                "peak_function": "gauss",
                "peak_params": {"sigma": line_dict.get("sigma", 2)},
                "peak_scaling_factor": float(line_dict["peak_scaling_factor"]),
                "peak_width": line_dict.get("peak_width", 30),
            }
    return peak_properties


def peak_properties_to_csv(peak_properties, csv_file):
    if not isinstance(csv_file, TextIOWrapper):
        csv_file = open(csv_file, "w")
    csv_filename = csv_file.name
    fieldnames = [
        "chemical_formula",
        "trivial_name",
        "charge",
        "scan_start_time",
        "peak_width",
        "peak_scaling_factor",
        "peak_function",
        "peak_params",
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for trivial_name, attribs in peak_properties.items():
        line = {
            "chemical_formula": peak_properties[trivial_name].get(
                "chemical_formula", ""
            ),
            # "trivial_name": peak_properties[cc].get("trivial_name", ""),
            "trivial_name": trivial_name,
            "charge": peak_properties[trivial_name].get("charge", 2),
            "scan_start_time": peak_properties[trivial_name]["scan_start_time"],
            "peak_function": peak_properties[trivial_name]["peak_function"],
            "peak_params": ",".join(
                [
                    f"{key}={val}"
                    for key, val in peak_properties[trivial_name]["peak_params"].items()
                ]
            ),
            "peak_scaling_factor": peak_properties[trivial_name].get(
                "peak_scaling_factor", 1e3
            ),
            "peak_width": peak_properties[trivial_name]["peak_width"],
        }
        writer.writerow(line)
    csv_file.close()
    return csv_filename
