from app.core.config import settings

def main():
    # Print all settings
    print("Settings loaded from .env:")
    for key, value in settings.model_dump().items():
        if "SECRET_KEY" in key:
            value = "*****"  # mask secrets
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
