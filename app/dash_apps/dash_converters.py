# Converters to Dash info
import qcelemental as qcel

_atom_color_codes = {
    "H": "#ffffff",
    "He": "#ffbfcb",
    "Li": "#b22221",
    "Be": "#ff1393",
    "B": "#00fb02",
    "C": "#c6c6c6",
    "N": "#8c8efb",
    "O": "#ec0000",
    "F": "#d9a420",
    "Ne": "#fd1492",
    "Na": "#0000fd",
    "Mg": "#1e7c1e",
    "Al": "#808090",
    "Si": "#d39f1f",
    "P": "#f19c00",
    "S": "#fac431",
    "Cl": "#00f100",
    "Ar": "#fb1491",
    "K": "#ffffff",
    "Ca": "#ffbfcb",
    "Sc": "#b22221",
    "Ti": "#ff1393",
    "V": "#00fb02",
    "Cr": "#c6c6c6",
    "Mn": "#8c8efb",
    "Fe": "#ec0000",
    "Co": "#d9a420",
    "Ni": "#fd1492",
    "Cu": "#0000fd",
    "Zn": "#1e7c1e",
    "Ga": "#808090",
    "Ge": "#d39f1f",
    "As": "#f19c00",
    "Se": "#fac431",
    "Br": "#00f100",
    "Kr": "#fb1491",
    "Rb": "#ffffff",
    "Sr": "#ffbfcb",
    "Y": "#b22221",
    "Zr": "#ff1393",
    "Nb": "#00fb02",
    "Mo": "#c6c6c6",
    "Tc": "#8c8efb",
    "Ru": "#ec0000",
    "Rh": "#d9a420",
    "Pd": "#fd1492",
    "Ag": "#0000fd",
    "Cd": "#1e7c1e",
    "In": "#808090",
    "Sn": "#d39f1f",
    "Sb": "#f19c00",
    "Te": "#fac431",
    "I": "#00f100",
    "Xe": "#fb1491",
}


def molecule_to_d3moljs(molecule=None):

    style_data = {}
    model_data = {"atoms": [], "bonds": []}

    if molecule is None:
        return style_data, model_data

    pos = molecule.geometry * qcel.constants.conversion_factor("bohr", "nanometer")
    for i, (sym, xyz) in enumerate(zip(molecule.symbols, molecule.geometry)):
        model_data["atoms"].append(
            {
                "name": sym,
                "chain": f"A{i}",
                "positions": list(xyz),
                "residue_index": i,
                "element": sym,
                # "residue_name": "res",
                "serial": i,
            }
        )
        style_data[i] = {
            "visualization_type": "stick",
            "color": _atom_color_codes.get(sym, "#0000"),
        }

    for idx1, idx2 in qcel.molutil.guess_connectivity(
        molecule.symbols, molecule.geometry
    ):
        model_data["bonds"].append({"atom1_index": idx1, "atom2_index": idx2})

    return model_data, style_data
