import json
import pandas as pd
with open('data/glossary-export.json', encoding='utf-8-sig') as f:
    data = json.load(f)
df = pd.json_normalize(data['parentTerms'])

filtered_df = df[df['seeAlso'].apply(lambda x: isinstance(x, list) and len(x) > 0)]
print(filtered_df)

def extract_text(lst):
    if isinstance(lst, list) and len(lst) > 0:
        return lst[0].get("text", "")
    return ""

def has_value(x):
    return x is not None and (not (isinstance(x, float) and pd.isna(x))) and (not (isinstance(x, list) and len(x) == 0))

df['definition'] = df.apply(
    lambda row: extract_text(row['definitions']) if has_value(row['definitions']) else extract_text(row['abbrSyn']),
    axis=1
)

term_definition_dict = df.set_index('term').apply(
    lambda row: {"definition": row['definition'], "link": row['link']}, axis=1
).to_dict()


#print(term_definition_dict)

with open('data/rag_dataset_object.json', 'w', encoding='utf-8') as f:
    json.dump(term_definition_dict, f, ensure_ascii=False, indent=2)
