## Testing

### Run Behave API Integration Tests

```bash
# Install dev dependencies (includes behave)
pip install -e ".[dev]"

# Ensure services are running
docker-compose up -d

# Run all Behave tests
python -m behave tests/bdd-features

```