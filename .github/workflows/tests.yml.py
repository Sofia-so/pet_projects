name: Run Tests

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: my_project_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U postgres"
          --health-interval=10s
          --health-timeout=5s
          --health-retries=5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Create .env
        run: |
          echo "SECRET_KEY=test_secret" > .env
          echo "DATABASE_URI=postgresql://postgres:postgres@localhost:5432/my_project_test" >> .env

      - name: Run migrations
        run: alembic upgrade head

      - name: Run tests
        run: python -m pytest tests
