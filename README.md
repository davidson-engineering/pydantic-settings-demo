Below is a README file for the Pydantic settings demonstration script, written in Markdown. The README provides an overview of the project, its purpose, setup instructions, usage details, and other relevant information. It assumes the script is part of a small project or repository and incorporates the Pydantic V2 updates from the improved code. If you have specific requirements (e.g., a particular format, additional sections, or a specific audience), please let me know, and I can tailor it further.

---

# Pydantic Settings Demo

This project demonstrates how to use Pydantic V2's `BaseSettings` to load configuration settings from environment variables and `.env` files. It showcases environment variable precedence, multiple environment configurations (default, development, production), and validation of settings using Pydantic's `@field_validator`. The script is designed to be educational, showing best practices for managing application settings in Python.

## Features

- Load configuration from `.env`, `.env.dev`, and `.env.prod` files.
- Demonstrate environment variable precedence over `.env` files.
- Use Pydantic V2 for type-safe configuration with validation.
- Support case-insensitive log levels via an `Enum`.
- Mask sensitive settings (e.g., API keys, database tokens) by default.
- Handle errors gracefully with clear feedback.
- Provide formatted output to compare settings across environments.

## Requirements

- Python 3.8+
- Pydantic V2 (`pydantic` and `pydantic-settings`)

## Installation

1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd pydantic-settings-demo
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install pydantic pydantic-settings
   ```

## Setup

1. Create the following `.env` files in the project root directory with the structure shown below:

   **`.env`** (default settings):
   ```
   MYAPP_DATABASE_URL=sqlite:///default.db
   MYAPP_DATABASE_TOKEN=secret123
   MYAPP_API_KEY=apikey123
   MYAPP_DEBUG_MODE=True
   MYAPP_LOG_LEVEL=INFO
   MYAPP_PORT=8000
   ```

   **`.env.dev`** (development settings):
   ```
   MYAPP_DATABASE_URL=sqlite:///dev.db
   MYAPP_DEBUG_MODE=True
   MYAPP_LOG_LEVEL=DEBUG
   ```

   **`.env.prod`** (production settings):
   ```
   MYAPP_DATABASE_URL=sqlite:///prod.db
   MYAPP_DEBUG_MODE=False
   MYAPP_LOG_LEVEL=INFO
   ```

2. Ensure the `.env` files are correctly formatted and saved in the project root.

## Usage

Run the script to see the settings loaded from `.env` files and how environment variables override them:

```bash
python settings_demo.py
```

### What the Script Does

1. **Loads Environment Variables**: Checks for existing `MYAPP_*` environment variables and prints them.
2. **Initializes Settings**: Creates `DefaultSettings`, `ProdSettings`, and `DevSettings` instances using Pydantic's `BaseSettings`.
3. **Demonstrates Overrides**:
   - Sets `MYAPP_DATABASE_URL` to show environment variable precedence.
   - Sets `MYAPP_DEBUG_MODE` to demonstrate automatic type parsing (e.g., string "FALSE" to boolean `False`).
4. **Prints Settings**: Displays settings for each environment, comparing initial and overridden values.
5. **Handles Secrets**: Masks sensitive fields (e.g., `database_token`, `api_key`) by default and provides an option to unmask them.
6. **Validates Inputs**:
   - Ensures `port` is within the valid range (1–65535).
   - Validates `log_level` against a predefined `LogLevel` enum, supporting case-insensitive input.

### Example Output

```
Starting application...

No MYAPP_ environment variables found.

Setting MYAPP_DATABASE_URL to demonstrate env var precedence...
Setting MYAPP_DEBUG_MODE to demonstrate type parsing...

Settings for DefaultSettings (Default):
-------------------------------
database_url: sqlite:///default.db
database_token: ********
api_key: ********
debug_mode: True
log_level: INFO
port: 8000

Settings for ProdSettings (Production):
--------------------------------
database_url: this.will.always.win.over.files/database_url
database_token: ********
api_key: ********
debug_mode: False
log_level: INFO
port: 8000

Initial ProdSettings settings (before overrides):
--------------------------------
database_url: sqlite:///prod.db
database_token: ********
api_key: ********
debug_mode: False
log_level: INFO
port: 8000

Note: MYAPP_DATABASE_URL was set in the environment and overrides .env file values for both dev and prod.

Settings for DevSettings (Development):
--------------------------------
database_url: this.will.always.win.over.files/database_url
database_token: ********
api_key: ********
debug_mode: False
log_level: DEBUG
port: 8000

Initial DevSettings settings (before overrides):
--------------------------------
database_url: sqlite:///dev.db
database_token: ********
api_key: ********
debug_mode: True
log_level: DEBUG
port: 8000

Note: MYAPP_DEBUG_MODE was set in the environment, parsed as boolean, and only affects dev settings.

Exposing unmasked secrets for all settings:
...
```

## Project Structure

```
pydantic-settings-demo/
├── settings_demo.py    # Main script
├── .env                # Default settings
├── .env.dev            # Development settings
├── .env.prod           # Production settings
├── README.md           # This file
```

## Notes

- **Pydantic V2**: This script uses Pydantic V2, which replaces the deprecated `@validator` with `@field_validator`. See the [Pydantic V2 Migration Guide](https://docs.pydantic.dev/latest/migration/) for details.
- **Environment Variable Precedence**: Environment variables (e.g., `MYAPP_DATABASE_URL`) always take precedence over `.env` file values.
- **Secret Handling**: Sensitive fields like `database_token` and `api_key` are masked by default for security.
- **Error Handling**: The script includes basic error handling for missing or malformed `.env` files.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
