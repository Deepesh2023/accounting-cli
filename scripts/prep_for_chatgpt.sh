set -e

# Configuration
AUTHOR_EMAIL=$(git config user.email)
GIT_LOG_FILE="gitlog.txt"
ZIP_NAME="cli.zip"

# Generate git log
git log > "$GIT_LOG_FILE"

# Remove sensitive information
sed -i "s/$AUTHOR_EMAIL/<EMAIL REMOVED>/g" "$GIT_LOG_FILE"

# Create zip archive
zip -r "$ZIP_NAME" . \
    -x ".git/*" \
    -x "__pycache__\*" \
    -x ".venv/*" \
    -x "$ZIP_NAME"

echo "Created $ZIP_NAME"
