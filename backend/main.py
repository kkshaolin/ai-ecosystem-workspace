import sys
from core.config import settings
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def run_app():
    print(f"Start: {settings.APP_NAME}")
    print(f"Port: {settings.PORT} (Type: {type(settings.PORT)})")    

if __name__ == "__main__":
    run_app()
