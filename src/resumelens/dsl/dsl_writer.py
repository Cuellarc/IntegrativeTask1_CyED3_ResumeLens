from resumelens.models import CandidateData


def _sanitize_text(value: str) -> str:
    return value.replace('"', "'").replace("\r", " ").replace("\n", " ")


def _format_qualification_list(qualifications: list[str]) -> str:
    return ", ".join(qualifications)


def write_dsl(candidate: CandidateData) -> str:
    lines = [f'candidate "{_sanitize_text(candidate.full_name)}" {{']

    if candidate.email or candidate.phone or candidate.links:
        lines.append("    contact {")

        if candidate.email:
            lines.append(f'        email: "{_sanitize_text(candidate.email)}"')

        if candidate.phone:
            lines.append(f'        phone: "{_sanitize_text(candidate.phone)}"')

        for link in candidate.links:
            lines.append(f'        link: "{_sanitize_text(link)}"')

        lines.append("    }")

    if candidate.location:
        lines.append(
            f'    location: "{_sanitize_text(candidate.location)}"'
        )

    if candidate.current_role:
        lines.append(
            f'    role: "{_sanitize_text(candidate.current_role)}"'
        )

    if candidate.summary:
        lines.append(
            f'    summary: "{_sanitize_text(candidate.summary)}"'
        )

    if candidate.education:
        lines.append("    education {")

        for education in candidate.education:
            lines.append(f'        "{_sanitize_text(education)}"')

        lines.append("    }")

    for experience in candidate.experiences:
        lines.append("    experience {")
        lines.append(
            f'        {experience.years} years '
            f'"{_sanitize_text(experience.description)}"'
        )

        if experience.role:
            lines.append(
                f'        role "{_sanitize_text(experience.role)}"'
            )

        if experience.organization:
            lines.append(
                f'        organization '
                f'"{_sanitize_text(experience.organization)}"'
            )

        if experience.highlights:
            lines.append("        {")

            for highlight in experience.highlights:
                lines.append(
                    f'            "{_sanitize_text(highlight)}"'
                )

            lines.append("        }")

        lines.append("    }")

    lines.append("    skills {")
    lines.append(
        f"        {_format_qualification_list(candidate.skills)}"
    )
    lines.append("    }")

    accepted_classifications = [
        classification
        for classification in candidate.classifications
        if classification.accepted
    ]

    if accepted_classifications:
        lines.append("    classification {")

        for classification in accepted_classifications:
            qualifications = _format_qualification_list(
                classification.qualifications
            )
            lines.append(
                f"        {classification.profile_name}: "
                f"ACCEPTED [{qualifications}]"
            )

        lines.append("    }")

    lines.append("}")

    return "\n".join(lines)