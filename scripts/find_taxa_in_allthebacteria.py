import argparse
import sys
import pandas as pd

try:
    from rapidfuzz import process, fuzz
except Exception:
    # fallback to difflib if rapidfuzz not available
    from difflib import get_close_matches
    process = None
    fuzz = None

def read_table(path):
    if str(path).endswith('.tsv'):
        return pd.read_csv(path, sep='\t', dtype=str).fillna('')
    if str(path).endswith('.json'):
        return pd.read_json(path, dtype=False).astype(str).fillna('')
    # try CSV otherwise
    return pd.read_csv(path, dtype=str).fillna('')

def norm(s):
    if pd.isna(s):
        return ''
    return str(s).strip().lower()

def build_name_index(df, name_col):
    idx = {}
    for i, name in enumerate(df[name_col].astype(str)):
        n = norm(name)
        if n:
            idx.setdefault(n, []).append(i)
    return idx

def fuzzy_match_name(name, choices, threshold=90):
    if not name:
        return None, 0
    if process:
        res = process.extractOne(name, choices, scorer=fuzz.token_sort_ratio)
        if res and res[1] >= threshold:
            return res[0], res[1]
        return None, res[1] if res else 0
    else:
        # difflib fallback
        matches = get_close_matches(name, choices, n=1, cutoff=threshold/100.0)
        if matches:
            # approximate score with simple ratio
            return matches[0], int(100 * (len(matches[0]) / max(len(name), 1)))
        return None, 0

def find_matches(df_query, df_all, query_name_col, query_taxid_col,
                 all_name_col, all_taxid_col, threshold):
    all_name_index = build_name_index(df_all, all_name_col)
    all_names = list(all_name_index.keys())
    all_taxid_map = {norm(v): i for i, v in enumerate(df_all[all_taxid_col].astype(str)) if v != ''} if all_taxid_col in df_all.columns else {}
    rows_matched = []
    rows_unmatched = []
    for _, row in df_query.iterrows():
        q_name = norm(row.get(query_name_col, '')) if query_name_col in df_query.columns else ''
        q_taxid = norm(row.get(query_taxid_col, '')) if query_taxid_col and query_taxid_col in df_query.columns else ''
        match_info = None

        # 1) match by taxid if available
        if q_taxid:
            ai = all_taxid_map.get(q_taxid)
            if ai is not None:
                match_info = (ai, 'taxid_exact', 100)

        # 2) exact name match
        if match_info is None and q_name:
            idxs = all_name_index.get(q_name)
            if idxs:
                match_info = (idxs[0], 'name_exact', 100)

        # 3) fuzzy name match
        if match_info is None and q_name and all_names:
            matched_name, score = fuzzy_match_name(q_name, all_names, threshold)
            if matched_name and score >= threshold:
                ai = all_name_index[matched_name][0]
                match_info = (ai, 'name_fuzzy', score)

        if match_info:
            ai, method, score = match_info
            matched_row = df_all.iloc[ai].to_dict()
            out = row.to_dict()
            out.update({'matched_by': method, 'match_score': score})
            # prefix columns from allthebacteria to avoid collisions
            for k, v in matched_row.items():
                out[f'atb__{k}'] = v
            rows_matched.append(out)
        else:
            rows_unmatched.append(row.to_dict())

    return pd.DataFrame(rows_matched), pd.DataFrame(rows_unmatched)

def main(argv):
    p = argparse.ArgumentParser(description='Find taxa from your tables in AllTheBacteria dataset')
    p.add_argument('--taxa', required=True, help='path to your taxa table (CSV/TSV/JSON)')
    p.add_argument('--genomes', required=False, help='path to your genomes table (CSV/TSV/JSON)')
    p.add_argument('--all', required=True, help='AllTheBacteria table file (CSV/TSV/JSON)')
    p.add_argument('--taxa-name-col', default='name', help='column name in taxa file with taxon names')
    p.add_argument('--taxa-taxid-col', default='', help='column name in taxa file with taxid (optional)')
    p.add_argument('--genomes-name-col', default='genome_name', help='column name in genomes file with name')
    p.add_argument('--genomes-taxid-col', default='', help='column name in genomes file with taxid (optional)')
    p.add_argument('--all-name-col', default='name', help='column name in AllTheBacteria file with name')
    p.add_argument('--all-taxid-col', default='taxid', help='column name in AllTheBacteria file with taxid')
    p.add_argument('--threshold', type=int, default=90, help='fuzzy match threshold (0-100)')
    p.add_argument('--out-prefix', default='match_results', help='output CSV prefix')
    args = p.parse_args(argv)

    df_taxa = read_table(args.taxa)
    df_all = read_table(args.all)

    matched_taxa, unmatched_taxa = find_matches(df_taxa, df_all,
                                                args.taxa_name_col, args.taxa_taxid_col,
                                                args.all_name_col, args.all_taxid_col,
                                                args.threshold)
    matched_taxa.to_csv(f'{args.out_prefix}_taxa_matched.csv', index=False)
    unmatched_taxa.to_csv(f'{args.out_prefix}_taxa_unmatched.csv', index=False)

    print(f'Taxa: matched {len(matched_taxa)} rows, unmatched {len(unmatched_taxa)} rows -> {args.out_prefix}_taxa_*.csv')

    if args.genomes:
        df_gen = read_table(args.genomes)
        matched_gen, unmatched_gen = find_matches(df_gen, df_all,
                                                  args.genomes_name_col, args.genomes_taxid_col,
                                                  args.all_name_col, args.all_taxid_col,
                                                  args.threshold)
        matched_gen.to_csv(f'{args.out_prefix}_genomes_matched.csv', index=False)
        unmatched_gen.to_csv(f'{args.out_prefix}_genomes_unmatched.csv', index=False)
        print(f'Genomes: matched {len(matched_gen)} rows, unmatched {len(unmatched_gen)} rows -> {args.out_prefix}_genomes_*.csv')

if __name__ == '__main__':
    main(sys.argv[1:])