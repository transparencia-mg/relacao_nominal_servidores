name: Publicar dataset no CKAN (dados.mg.gov.br)

on:
  push:
    branches: [main]
    paths:
      - "data/**"
      - "datapackage/**"
      - "scripts/**"
      - "requirements.txt"
  workflow_dispatch:

jobs:
  publish_ckan:
    runs-on: ubuntu-22.04

    steps:
      - name: 📥 Checkout do repositório
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: 🐍 Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: 📦 Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # (Opcional, mas recomendado)
      - name: 🧪 Verificar versões críticas
        run: |
          python - << 'EOF'
          import dpckan
          import frictionless
          print("dpckan:", dpckan.__version__)
          print("frictionless:", frictionless.__version__)
          EOF

      - name: 📦 Publicar datapackage no CKAN
        env:
          CKAN_HOST: ${{ secrets.CKAN_HOST }}
          CKAN_KEY: ${{ secrets.CKAN_KEY }}
        run: |
          dpckan \
            --datastore \
            --ckan-host "$CKAN_HOST" \
            --ckan-key "$CKAN_KEY" \
            --datapackage datapackage/datapackage.json \
            dataset create || \
          dpckan \
            --datastore \
            --ckan-host "$CKAN_HOST" \
            --ckan-key "$CKAN_KEY" \
            --datapackage datapackage/datapackage.json \
            dataset update


