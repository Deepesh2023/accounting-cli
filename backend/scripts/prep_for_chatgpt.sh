set -e

# Configuration
AUTHOR_EMAIL=$(git config user.email)
GIT_LOG_FILE="gitlog.txt"
ZIP_NAME="cli.zip"

# Generate git log
git log > "$GIT_LOG_FILE"

# Remove sensitive information
sed -i "s/$AUTHOR_EMAIL/<EMAIL REMOVED>/g" "$GIT_LOG_FILE"

rm -f "$ZIP_NAME"

# Create zip archive
zip -r "$ZIP_NAME" . \
    -x ".git/*" \
    -x "__pycache__/*" \
    -x "*/__pycache__/*" \
    -x ".python_version" \
    -x ".venv/*" \
    -x "*.json" \
    -x "$ZIP_NAME"

echo "Created $ZIP_NAME"
