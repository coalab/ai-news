# .github/workflows/daily-build.yml
name: Daily AI News Build

on:
  schedule:
    - cron: "30 22 * * *"    # 매일 07:30 KST
  workflow_dispatch:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4

      # build.py가 없으면 '건드리지 않고' 종료
      - name: Check script exists
        id: chk
        run: |
          if [ ! -f scripts/build.py ]; then
            echo "has_script=false" >> $GITHUB_OUTPUT
          else
            echo "has_script=true" >> $GITHUB_OUTPUT
          fi

      - name: Set up Python
        if: steps.chk.outputs.has_script == 'true'
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install deps
        if: steps.chk.outputs.has_script == 'true' && hashFiles('requirements.txt') != ''
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build site
        if: steps.chk.outputs.has_script == 'true'
        run: python scripts/build.py

      - name: Commit & Push changes
        if: steps.chk.outputs.has_script == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "Auto update site" || echo "No changes"
          git push
