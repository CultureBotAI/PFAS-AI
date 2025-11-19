# PFAS_Reactions Category Files

This directory contains **static reference data** for PFAS biodegradation reactions organized by functional category.

## Purpose

These files serve as curated seed data derived from the original Excel sheets. They are **NOT extended dynamically** by the pipeline. All new reaction data is added to the main `PFAS_Data_for_AI_reactions_extended.tsv` file in the parent directory.

## Files

### Base Files (from Excel conversion)
- `PFAS_Reactions_dehalogenase.tsv` - C-F and C-X bond cleavage enzymes (16 reactions)
- `PFAS_Reactions_fluoride_resistance.tsv` - Fluoride transport and resistance mechanisms (38 reactions)
- `PFAS_Reactions_hydrocarbon_degradation.tsv` - Alkane/hydrocarbon metabolism (19 reactions)
- `PFAS_Reactions_known_pfas_degraders.tsv` - Validated PFAS-degrading reactions (11 reactions)
- `PFAS_Reactions_oxygenase_cometabolism.tsv` - Oxygenase co-metabolism pathways (29 reactions)
- `PFAS_Reactions_important_genes.tsv` - Non-enzymatic genes (transporters, regulators) (3 entries)

### Extended Files (with gene linking)
- `*_extended.tsv` versions - Include `linked_genes` column cross-referencing genes_and_proteins table

## Data Source

All data originally comes from `data/sheet/PFAS Data for AI.xlsx`:
- Excel sheets: "Reactions - dehalogenase", "Reactions - fluoride", etc.
- Converted via `src/convert_reactions_excel.py`
- Extended with gene linking via `src/extend_reactions_by_category.py` (historical - no longer run)

## Integration with Main Pipeline

The merge script (`scripts/merge_reaction_categories.py`) combines these category files into the unified reactions table:

```bash
make merge-reactions
```

**Output**: `data/txt/sheet/PFAS_Data_for_AI_reactions_extended.tsv` (113 unique reactions)

## Reaction Categories

1. **dehalogenase**: Enzymes that cleave C-F and C-X bonds (RdhA, DehH, DhaA, etc.)
2. **fluoride_resistance**: Fluoride transport, exporters, and homeostasis (CrcB, FEX)
3. **hydrocarbon_degradation**: Alkane and aromatic metabolism for PFAS backbone cleavage
4. **known_pfas_degraders**: Reactions from validated PFAS-degrading organisms
5. **oxygenase_cometabolism**: Oxygenase-mediated co-metabolism pathways (AlkB, NahAc, CatA)
6. **important_genes**: Non-enzymatic genes relevant to PFAS biodegradation

## Key Columns

- **Reaction identifier**: RHEA ID or custom identifier
- **Equation**: Stoichiometric reaction equation
- **Enzyme class**: Functional enzyme classification
- **ec_number**: Enzyme Commission number (EC:X.X.X.X)
- **rhea_id**: RHEA database identifier
- **linked_genes**: Custom gene IDs (e.g., `custom_rdhA;custom_dhaA`)
- **reaction_category**: Category label for ML feature extraction
- **source**: Data provenance (reactions_excel)

## Cross-References

Linked genes in these files reference entries in:
- `PFAS_Data_for_AI_genes_and_proteins_extended.tsv`

Custom gene IDs follow the pattern `custom_{gene_symbol}` (e.g., `custom_rdhA`, `custom_crcB`).

## Important Notes

⚠️ **These files are reference data only** - do not run extension scripts on them.

✅ **To add new reactions**: Extend the main `PFAS_Data_for_AI_reactions_extended.tsv` using `make update-reactions`.

📝 **To regenerate from Excel**: Run `make convert-excel` if the source Excel file is updated.

## Validation

To verify data integrity:
```bash
# Check that all reactions are in main table
wc -l PFAS_Reactions_*_extended.tsv
wc -l ../PFAS_Data_for_AI_reactions_extended.tsv

# Run consistency validation
make validate-consistency
```

---

**Last updated**: November 2024 (reorganization - moved to subdirectory)
**Total unique reactions**: 113 (116 entries with 3 duplicates across categories)
