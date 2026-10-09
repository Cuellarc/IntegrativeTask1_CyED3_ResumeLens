NAME_PATTERN = r"[A-ZÁÉÍÓÚÑ][\w'’-]*(?:\s+(?:(?:de|del|la|las|los|y)\s+)*[A-ZÁÉÍÓÚÑ][\w'’-]*){1,4}"

EMAIL_PATTERN = r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"

PHONE_PATTERN = r"(?<!\d)(?:\+\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}(?!\d)"

LINK_PATTERN = r"(?i)(?:https?://|www\.)[^\s,;<>()\"']+|(?:linkedin\.com|github\.com)/[^\s,;<>()\"']+"

LOCATION_PATTERN = r"(?im)^[ \t]*location[ \t]*:[ \t]*(.+?)[ \t]*$"

CURRENT_ROLE_PATTERN = r"(?im)^[ \t]*(?:current[ \t]+role|role)[ \t]*:[ \t]*(.+?)[ \t]*$"

SUMMARY_PATTERN = r"(?ims)^[ \t]*(?:profile[ \t]+summary|summary|profile)[ \t]*:[ \t]*\n?(.+?)(?:\n[ \t]*\n|\Z)"

EDUCATION_PATTERN = (
    r"(?im)^[ \t]*(?:[-*•][ \t]*)?"
    r"((?:bachelor|master|ph\.?d|doctorate|associate|diploma|b\.?sc|m\.?sc|ingenier[ií]a|licenciatura)"
    r"[^\n]*?)[ \t]*$"
)

EXPERIENCE_HEADER_PATTERN = (
    r"(?i)[ \t]*(?P<role>[^\n(]+?)[ \t]+(?:[-–—@]|at)[ \t]+(?P<organization>[^\n(]+?)"
    r"[ \t]*\([ \t]*(?P<years>\d+)[ \t]+years?[ \t]*\)[ \t]*$"
)

EXPERIENCE_SENTENCE_PATTERN = r"(?i)(?P<years>\d+)[ \t]+years?[ \t]+of[ \t]+experience[ \t]*(?P<description>[^.\n]*)"

HIGHLIGHT_PATTERN = r"[ \t]*[-*•][ \t]+(.+?)[ \t]*$"

SKILL_START = r"(?<![\w.])"
SKILL_END = r"(?![\w+#])"

LANGUAGE_PATTERN = (
    r"(?i)" + SKILL_START
    + r"(?:java[ \t]?script|js|type[ \t]?script|ts|python|scala|java)"
    + SKILL_END
)

FRAMEWORK_PATTERN = (
    r"(?i)" + SKILL_START
    + r"(?:react(?:\.?[ \t]?js)?|angular(?:\.?[ \t]?js)?|vue(?:\.?[ \t]?js)?"
    + r"|node(?:\.?[ \t]?js)?|express\.?js|django|spring[ \t]?boot"
    + r"|pandas|numpy|scikit[-_ \t]?learn|sklearn|tensor[ \t]?flow|py[ \t]?torch"
    + r"|(?:apache[ \t])?spark|pyspark|hadoop|airflow|dagster|prefect)"
    + SKILL_END
)

DATABASE_PATTERN = (
    r"(?i)" + SKILL_START
    + r"(?:postgres(?:ql)?|postgre[ \t]?sql|mysql|my[ \t]sql|mongo[ \t]?db|mongo"
    + r"|sql|snowflake|big[ \t]?query|redshift)"
    + SKILL_END
)

TOOL_PATTERN = (
    r"(?i)" + SKILL_START
    + r"(?:github[ \t]?actions|gitlab[ \t]?ci(?:/cd)?|git|docker|kubernetes|k8s|podman|jenkins"
    + r"|aws|amazon[ \t]+web[ \t]+services|azure|gcp|google[ \t]+cloud(?:[ \t]+platform)?"
    + r"|terraform|ansible|linux)"
    + SKILL_END
)
