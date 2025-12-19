set -e  # Exit on error

cd "$(dirname "$0")"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv first."
    exit 1
fi

uv sync
uv run python ./data_questionnaire_agent/server/questionnaire_server_main.py

