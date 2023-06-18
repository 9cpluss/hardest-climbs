from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Hardest Climbs"

    # Database
    db_username: str = ""
    db_password: str = ""
    db_hostname: str = ""
    db_port: int = 3306
    db_name: str = ""
    db_schema: str = ""

    ssh_hostname: str = ""
    ssh_username: str = ""
    ssh_password: str = ""

    # Local development
    local: bool = False


settings = Settings()
