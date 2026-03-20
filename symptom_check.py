SYMPTOMS = {
    "Do you have redness in your eye?": "redness",
    "Is your eye swollen or puffy?": "swelling",
    "Do you notice yellowing of the white part of your eye?": "jaundice",
    "Does your vision appear cloudy or blurry?": "cataract",
    "Is your eyelid drooping?": "ptosis",
    "Do you have pain inside the eye?": "internal",
    "Do you see flashes or floaters?": "internal",
    "Do you have difficulty seeing at night?": "internal",
}
def triage(answers):
    internal_flags = [
        "Do you have pain inside the eye?",
        "Do you see flashes or floaters?",
        "Do you have difficulty seeing at night?"
    ]
    for q in internal_flags:
        if answers.get(q, False):
            return 'fundus'
    return 'front'
