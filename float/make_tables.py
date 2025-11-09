import re

import pandas as pd

files = {
    'speedup/clang.txt': 'Clang',
    'speedup/clang_plugin.txt': 'Clang_w_plug'
}

def extract_vector_width(info):
    m = re.search(r"VectorizationFactor:\s*(?:vscale x )?(\d+)", info)
    return int(m.group(1)) if m else 1

def parse_vector_file(path):
    d = {}
    try:
        with open(path, 'r') as f:
            for line in f.readlines()[2:]:
                parts = line.strip().split(maxsplit=3)
                if len(parts) < 4:
                    continue
                fn, _, status, info = parts
                d[fn] = extract_vector_width(info) if status == 'Vectorized' else 1
    except:
        pass
    return d

vector_main   = parse_vector_file('out.log')
vector_plugin = parse_vector_file('out_plugin.log')

data_dict = {}
for filename, cname in files.items():
    try:
        df = pd.read_csv(filename, sep='\t').rename(columns={'Speedup': cname})
        data_dict[cname] = df.set_index('Loop')[cname]
    except:
        pass

combined_df = pd.DataFrame(data_dict).reset_index()

combined_df['Theoretical_S'] = combined_df['Loop'].map(vector_main).fillna(1)
combined_df['Theoretical_S_w_plug'] = combined_df['Loop'].map(vector_plugin).fillna(1)

# порядок столбцов
cols = ['Loop', 'Theoretical_S', 'Theoretical_S_w_plug'] \
       + [c for c in combined_df.columns if c not in ['Loop', 'Theoretical_S', 'Theoretical_S_w_plug']]
combined_df = combined_df[cols]

combined_df.to_string('text_table/combined_speedup_table.txt', index=False)
print(combined_df.head())
