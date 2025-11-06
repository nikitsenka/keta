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

# Run bulk test suite

```commandline
python -m behave -f json -o reports/chat.json -f pretty -f progress --stop tests/bdd-features/chat100.feature
```