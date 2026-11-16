# Environmental Monitoring Data Science

Repository for coursework in Environmental Monitoring Data Science.

## Block 4: FLUXNET Data Summary Report

### Requirements
- Python 3.12+ with `pandas`, `numpy`, `matplotlib`, `jupyter`, and `nbconvert`:
  ```bash
  pip install pandas numpy matplotlib jupyter nbconvert
  ```

### Reproduce from a fresh clone
1. Download the five FLUXNET towers (`AU-How`, `BE-Lon`, `ID-PaD`, `NL-Vkp`, `US-Vcm`) into `data/raw/` using the FLUXNET Shuttle script:
   ```bash
   python scripts/get_my_towers.py --sites AU-How BE-Lon ID-PaD NL-Vkp US-Vcm
   ```
   *(Or use `--student 22` if `tower_sets_block4.csv` is in the project root.)*
2. Execute the notebook and render the HTML report into `reports/fluxnet_data_summary.html`:
   ```bash
   jupyter nbconvert --to html --execute --ExecutePreprocessor.timeout=300 reports/fluxnet_data_summary.ipynb
   ```

### Key files
- `scripts/read_flux.py`: `read_hh()` helper that reads `_FLUXMET_HH_` CSVs directly from FLUXNET `.zip` archives, parses `-9999` as `NaN`, and converts `TIMESTAMP_START` to `datetime`.
- `reports/fluxnet_data_summary.ipynb`: Source notebook covering sections C1–C6.

---

## Block 2: Cluster Hello

Bootstraps a synthetic Gross Primary Productivity (GPP) series and calculates a 95% confidence interval using Monte Carlo resampling.

```bash
python scripts/cluster_hello.py 200
```

- `scripts/`: analysis and script files (`cluster_hello.py`, `read_flux.py`, `get_my_towers.py`)
- `jobs/`: Slurm cluster job submission scripts
- `docs/`: documentation files (`STORAGE.md`)

**Author:** Sanglap Roy
