# Ejecución rápida

1. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
   (o `conda env create -f environment.yml`).

2. Ejecuta el pipeline completo que genera los modelos, métricas, intervalos bootstrap y gráficas en `results/`:
   ```bash
   python -m src.run_all
   ```

3. Consulta las salidas en `results/` (paridad, residuales, métricas y modelos guardados en formato `joblib`).
