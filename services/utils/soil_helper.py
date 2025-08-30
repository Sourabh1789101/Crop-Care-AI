from typing import Dict

SOIL_NORM = {
    "ph": (6.0, 7.5),
    "N": (50, 120),
    "P": (30, 60),
    "K": (30, 60),
}

FERTILIZER_GUIDE = {
    # very simplified demo values (kg/acre)
    "rice": {"urea": 50, "dap": 40, "mop": 20},
    "wheat": {"urea": 45, "dap": 35, "mop": 25},
    "maize": {"urea": 55, "dap": 45, "mop": 25},
}

CORRECTION_TIPS = {
    "low_N": "Add urea or FYM; grow legumes in rotation.",
    "high_N": "Reduce urea; split applications.",
    "low_P": "Apply DAP/SSP; avoid waterlogging.",
    "high_P": "Avoid excess P; use organic matter.",
    "low_K": "Apply MOP; incorporate crop residues.",
    "high_K": "Avoid KCl overuse; balance N and P.",
    "low_ph": "Apply agricultural lime as per recommendation.",
    "high_ph": "Add organic manure/gypsum; avoid over-liming.",
}

def analyze_soil(soil: Dict) -> Dict:
    report = {"warnings": [], "status": {}}
    for k, (lo, hi) in SOIL_NORM.items():
        val = soil.get(k)
        if val is None:
            continue
        if val < lo:
            if k == "ph":
                report["warnings"].append(CORRECTION_TIPS["low_ph"])
            else:
                report["warnings"].append(CORRECTION_TIPS[f"low_{k}"])
            report["status"][k] = "low"
        elif val > hi:
            if k == "ph":
                report["warnings"].append(CORRECTION_TIPS["high_ph"])
            else:
                report["warnings"].append(CORRECTION_TIPS[f"high_{k}"])
            report["status"][k] = "high"
        else:
            report["status"][k] = "ok"
    return report


def fertilizer_plan(crop: str, soil: Dict) -> Dict:
    base = FERTILIZER_GUIDE.get(crop.lower())
    if not base:
        base = {"urea": 40, "dap": 30, "mop": 20}
    analysis = analyze_soil(soil)
    adj = base.copy()

    # very simple adjustments (+/- 10%)
    if analysis["status"].get("N") == "low":
        adj["urea"] = round(adj["urea"] * 1.1, 1)
    if analysis["status"].get("N") == "high":
        adj["urea"] = round(adj["urea"] * 0.9, 1)
    if analysis["status"].get("P") == "low":
        adj["dap"] = round(adj["dap"] * 1.1, 1)
    if analysis["status"].get("P") == "high":
        adj["dap"] = round(adj["dap"] * 0.9, 1)
    if analysis["status"].get("K") == "low":
        adj["mop"] = round(adj["mop"] * 1.1, 1)
    if analysis["status"].get("K") == "high":
        adj["mop"] = round(adj["mop"] * 0.9, 1)

    return {"base": base, "adjusted": adj, "notes": analysis["warnings"]}
