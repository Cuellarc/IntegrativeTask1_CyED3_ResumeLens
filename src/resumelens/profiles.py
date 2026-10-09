from resumelens.errors import UnknownProfileError
from resumelens.models import Profile, ProfileCategory

FULL_STACK_DEVELOPER = "FULL_STACK_DEVELOPER"
MACHINE_LEARNING_ENGINEER = "MACHINE_LEARNING_ENGINEER"
DEVOPS_ENGINEER = "DEVOPS_ENGINEER"
DATA_ENGINEER = "DATA_ENGINEER"

PROFILES = [
    Profile(
        name=FULL_STACK_DEVELOPER,
        display_name="Full Stack Developer",
        categories=(
            ProfileCategory("LANGUAGE", ("JAVASCRIPT", "TYPESCRIPT")),
            ProfileCategory("FRONTEND", ("REACT", "ANGULAR", "VUE")),
            ProfileCategory("BACKEND", ("NODE_JS", "DJANGO", "SPRING_BOOT", "EXPRESS")),
            ProfileCategory("DATABASE", ("POSTGRESQL", "MYSQL", "MONGODB", "SQL")),
            ProfileCategory("VERSION_CONTROL", ("GIT",)),
        ),
    ),
    Profile(
        name=MACHINE_LEARNING_ENGINEER,
        display_name="Machine Learning Engineer",
        categories=(
            ProfileCategory("LANGUAGE", ("PYTHON",)),
            ProfileCategory("DATA_PROCESSING", ("PANDAS", "NUMPY")),
            ProfileCategory("ML_FRAMEWORK", ("SCIKIT_LEARN", "TENSORFLOW", "PYTORCH")),
            ProfileCategory("DATABASE", ("SQL", "POSTGRESQL", "MYSQL")),
            ProfileCategory("VERSION_CONTROL", ("GIT",)),
        ),
    ),
    Profile(
        name=DEVOPS_ENGINEER,
        display_name="DevOps Engineer",
        categories=(
            ProfileCategory("OPERATING_SYSTEM", ("LINUX",)),
            ProfileCategory("CONTAINER", ("DOCKER", "KUBERNETES", "PODMAN")),
            ProfileCategory("CI_CD", ("JENKINS", "GITHUB_ACTIONS", "GITLAB_CI")),
            ProfileCategory("CLOUD", ("AWS", "AZURE", "GCP")),
            ProfileCategory("INFRASTRUCTURE_AS_CODE", ("TERRAFORM", "ANSIBLE")),
            ProfileCategory("VERSION_CONTROL", ("GIT",)),
        ),
    ),
    Profile(
        name=DATA_ENGINEER,
        display_name="Data Engineer",
        categories=(
            ProfileCategory("LANGUAGE", ("PYTHON", "SCALA")),
            ProfileCategory("DATABASE", ("SQL", "POSTGRESQL", "MYSQL")),
            ProfileCategory("DATA_PROCESSING", ("SPARK", "HADOOP", "PANDAS")),
            ProfileCategory("WORKFLOW", ("AIRFLOW", "DAGSTER", "PREFECT")),
            ProfileCategory("DATA_WAREHOUSE", ("SNOWFLAKE", "BIGQUERY", "REDSHIFT")),
            ProfileCategory("VERSION_CONTROL", ("GIT",)),
        ),
    ),
]


def get_profiles() -> list[Profile]:
    return list(PROFILES)


def get_profile(name: str) -> Profile:
    for profile in PROFILES:
        if profile.name == name:
            return profile
    raise UnknownProfileError(name)
