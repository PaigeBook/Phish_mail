@REM Install pre-commit hooks (Windows)
@REM Run this after cloning

python -m pip install pre-commit
pre-commit install

echo ✓ Pre-commit hooks installed
echo Hooks will run automatically on 'git commit'
echo.
echo To run hooks manually:
echo   pre-commit run --all-files
