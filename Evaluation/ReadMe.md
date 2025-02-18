# Metadata Extraction Evaluation
A tool for evaluating metadata extraction systems using Levenshtein similarity.

## Installation 
```bash
pip install python-Levenshtein
```


## Usage
```bash
from metadata_eval import evaluate_extraction, print_evaluation_summary

# Single document
results = evaluate_extraction("gold_standard.json", "predicted.json")
print_evaluation_summary(results)

# Multiple documents
file_pairs = get_file_pairs("gold_dir", "pred_dir")
all_results = [evaluate_extraction(g, p) for g, p in file_pairs]
micro_avg = calculate_micro_average(all_results)
macro_avg = calculate_macro_average(all_results)
print_average_metrics(micro_avg, macro_avg)
```
## Input Format
```bash
{
  "title": [{"start": 0, "end": 50, "text": "Document Title"}],
  "abstract": [{"start": 60, "end": 300, "text": "Abstract text..."}],
  ...
}
```



## Metrics
- Similarity Threshold: 85% (configurable)
- Field-level metrics: Precision, Recall, F1 for each metadata field
- Overall metrics: Micro and macro averages across documents

## Error Handling
- Gracefully handles missing files and invalid JSON
- Provides detailed error reporting
