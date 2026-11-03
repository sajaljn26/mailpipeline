from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env into the environment, so Pydantic AI also finds GROQ_API_KEY.
load_dotenv()


class Settings(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_refresh_token: str
    database_url: str
    groq_api_key: str
    classifier_model: str = "llama-3.1-8b-instant"
    agent_model: str = "llama-3.3-70b-versatile"
    poll_interval_seconds: int = 30
    dashboard_username: str = "admin"
    dashboard_password: str = ""

    def __init__(self, **values):
        super().__init__(**values)
        # Strip 'groq:' prefix if present, as Groq API expects only the model ID
        if self.classifier_model.startswith("groq:"):
            self.classifier_model = self.classifier_model[5:]
        if self.agent_model.startswith("groq:"):
            self.agent_model = self.agent_model[5:]



settings = Settings()
