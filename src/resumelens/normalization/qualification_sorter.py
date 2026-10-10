from resumelens.models import Profile


def sort_qualifications(qualifications: list[str], profile: Profile) -> list[str]:
    sorted_qualifications = []
    for category in profile.categories:
        for qualification in category.qualifications:
            if qualification in qualifications:
                sorted_qualifications.append(qualification)
                break
    return sorted_qualifications
