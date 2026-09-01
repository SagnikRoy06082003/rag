def analyze_legal_text(text):
    
    warnings = []

    keywords = {
        "penalty": "This clause includes penalties.",
        "termination": "This clause discusses termination conditions.",
        "liability": "This clause defines liability.",
        "confidential": "This clause refers to confidentiality."
    }

    for k in keywords:

        if k in text.lower():
            warnings.append(keywords[k])

    if not warnings:
        warnings.append("No risky legal clauses detected.")

    return warnings