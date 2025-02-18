import json
import os
import Levenshtein
from typing import Dict, List, Tuple, Set
from glob import glob

def evaluate_extraction(gold_path: str, predicted_path: str) -> Dict:
    """
    Evaluates metadata extraction performance using Levenshtein similarity
    
    Args:
        gold_path: Path to gold standard annotations JSON file
        predicted_path: Path to predicted annotations JSON file
        
    Returns:
        Dictionary containing evaluation metrics
    """
    # Load annotations
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold = json.load(f)
    
    with open(predicted_path, 'r', encoding='utf-8') as f:
        predicted = json.load(f)
    
    # Fields to evaluate
    fields = [
        'title', 'abstract', 'author', 'authoraffiliation', 
        'venue', 'doi', 'email', 'date', 'link'
    ]
    
    # Initialize results
    results = {
        'field_metrics': {},
        'overall': {
            'true_positives': 0,
            'false_positives': 0,
            'false_negatives': 0
        }
    }
    
    for field in fields:
        field_results = evaluate_field(gold.get(field, []), predicted.get(field, []))
        results['field_metrics'][field] = field_results
        
        # Accumulate overall metrics
        results['overall']['true_positives'] += field_results['true_positives']
        results['overall']['false_positives'] += field_results['false_positives']
        results['overall']['false_negatives'] += field_results['false_negatives']
    
    # Calculate overall precision, recall, F1
    overall = results['overall']
    if (overall['true_positives'] + overall['false_positives']) > 0:
        overall['precision'] = overall['true_positives'] / (overall['true_positives'] + overall['false_positives'])
    else:
        overall['precision'] = 0
        
    if (overall['true_positives'] + overall['false_negatives']) > 0:
        overall['recall'] = overall['true_positives'] / (overall['true_positives'] + overall['false_negatives'])
    else:
        overall['recall'] = 0
    
    if (overall['precision'] + overall['recall']) > 0:
        overall['f1'] = 2 * overall['precision'] * overall['recall'] / (overall['precision'] + overall['recall'])
    else:
        overall['f1'] = 0
    
    return results

def evaluate_field(gold_items: List[Dict], predicted_items: List[Dict]) -> Dict:
    """
    Evaluates a single metadata field using Levenshtein similarity
    
    Args:
        gold_items: List of gold standard items for the field
        predicted_items: List of predicted items for the field
        
    Returns:
        Dictionary containing field-specific metrics
    """
    # Get text values from annotations
    gold_values = [item['text'] for item in gold_items]
    pred_values = [item['text'] for item in predicted_items]
    
    # Remove duplicates
    gold_values = list(set(gold_values))
    pred_values = list(set(pred_values))
    
    # Match predictions to gold standard using Levenshtein similarity
    matches = []
    for gold_val in gold_values:
        best_match = None
        best_similarity = 0
        
        for pred_val in pred_values:
            # Calculate Levenshtein similarity (0-100%)
            max_len = max(len(gold_val), len(pred_val))
            if max_len == 0:
                similarity = 100  # Both empty strings
            else:
                distance = Levenshtein.distance(gold_val, pred_val)
                similarity = 100 * (1 - distance / max_len)
            
            # Check if similarity meets threshold
            if similarity >= 85 and similarity > best_similarity:
                best_match = pred_val
                best_similarity = similarity
        
        if best_match:
            matches.append((gold_val, best_match, best_similarity))
            # Remove matched prediction to prevent double counting
            pred_values.remove(best_match)
    
    # Calculate metrics
    true_positives = len(matches)
    false_positives = len(pred_values)  # Remaining unmatched predictions
    false_negatives = len(gold_values) - true_positives
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'matches': matches  # Detailed match information for debugging
    }

def print_evaluation_summary(results: Dict, title: str = "") -> None:
    """
    Prints a human-readable summary of evaluation results
    
    Args:
        results: Results dictionary from evaluate_extraction
        title: Optional title for the summary
    """
    if title:
        print(f"\n===== {title} =====\n")
    else:
        print("\n===== METADATA EXTRACTION EVALUATION SUMMARY =====\n")
    
    print("Field-Level Metrics:")
    print("-------------------")
    for field, metrics in results['field_metrics'].items():
        print(f"{field.capitalize()}:")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall: {metrics['recall']:.4f}")
        print(f"  F1 Score: {metrics['f1']:.4f}")
        print(f"  True Positives: {metrics['true_positives']}")
        print(f"  False Positives: {metrics['false_positives']}")
        print(f"  False Negatives: {metrics['false_negatives']}")
        print()
    
    print("Overall Metrics:")
    print("---------------")
    overall = results['overall']
    print(f"Precision: {overall['precision']:.4f}")
    print(f"Recall: {overall['recall']:.4f}")
    print(f"F1 Score: {overall['f1']:.4f}")
    print(f"True Positives: {overall['true_positives']}")
    print(f"False Positives: {overall['false_positives']}")
    print(f"False Negatives: {overall['false_negatives']}")

def calculate_micro_average(all_results: List[Dict]) -> Dict:
    """
    Calculate micro-average metrics across all documents
    
    Args:
        all_results: List of evaluation result dictionaries
        
    Returns:
        Dictionary with micro-averaged metrics
    """
    micro_avg = {
        'true_positives': 0,
        'false_positives': 0,
        'false_negatives': 0
    }
    
    # Sum up all TP, FP, FN across all documents
    for result in all_results:
        micro_avg['true_positives'] += result['overall']['true_positives']
        micro_avg['false_positives'] += result['overall']['false_positives']
        micro_avg['false_negatives'] += result['overall']['false_negatives']
    
    # Calculate precision, recall, F1
    if (micro_avg['true_positives'] + micro_avg['false_positives']) > 0:
        micro_avg['precision'] = micro_avg['true_positives'] / (micro_avg['true_positives'] + micro_avg['false_positives'])
    else:
        micro_avg['precision'] = 0
        
    if (micro_avg['true_positives'] + micro_avg['false_negatives']) > 0:
        micro_avg['recall'] = micro_avg['true_positives'] / (micro_avg['true_positives'] + micro_avg['false_negatives'])
    else:
        micro_avg['recall'] = 0
    
    if (micro_avg['precision'] + micro_avg['recall']) > 0:
        micro_avg['f1'] = 2 * micro_avg['precision'] * micro_avg['recall'] / (micro_avg['precision'] + micro_avg['recall'])
    else:
        micro_avg['f1'] = 0
    
    return micro_avg

def calculate_macro_average(all_results: List[Dict]) -> Dict:
    """
    Calculate macro-average metrics across all documents
    
    Args:
        all_results: List of evaluation result dictionaries
        
    Returns:
        Dictionary with macro-averaged metrics
    """
    macro_avg = {
        'precision': 0,
        'recall': 0,
        'f1': 0
    }
    
    # Average precision, recall, F1 across all documents
    n_docs = len(all_results)
    if n_docs == 0:
        return macro_avg
    
    for result in all_results:
        macro_avg['precision'] += result['overall']['precision']
        macro_avg['recall'] += result['overall']['recall']
        macro_avg['f1'] += result['overall']['f1']
    
    macro_avg['precision'] /= n_docs
    macro_avg['recall'] /= n_docs
    macro_avg['f1'] /= n_docs
    
    return macro_avg

def print_average_metrics(micro_avg: Dict, macro_avg: Dict) -> None:
    """
    Print micro and macro average metrics
    
    Args:
        micro_avg: Dictionary with micro-averaged metrics
        macro_avg: Dictionary with macro-averaged metrics
    """
    print("\n===== OVERALL EVALUATION METRICS =====\n")
    
    print("Micro Average (weighted by instances):")
    print("-------------------------------------")
    print(f"Precision: {micro_avg['precision']:.4f}")
    print(f"Recall: {micro_avg['recall']:.4f}")
    print(f"F1 Score: {micro_avg['f1']:.4f}")
    print(f"Total True Positives: {micro_avg['true_positives']}")
    print(f"Total False Positives: {micro_avg['false_positives']}")
    print(f"Total False Negatives: {micro_avg['false_negatives']}")
    print()
    
    print("Macro Average (document-level average):")
    print("--------------------------------------")
    print(f"Precision: {macro_avg['precision']:.4f}")
    print(f"Recall: {macro_avg['recall']:.4f}")
    print(f"F1 Score: {macro_avg['f1']:.4f}")

def get_file_pairs(gold_dir: str, pred_dir: str) -> List[Tuple[str, str]]:
    """
    Find matching gold standard and prediction file pairs
    
    Args:
        gold_dir: Directory containing gold standard files
        pred_dir: Directory containing prediction files
        
    Returns:
        List of tuples with matching (gold_path, pred_path)
    """
    pairs = []
    gold_files = glob(os.path.join(gold_dir, "*.json"))
    
    for gold_file in gold_files:
        basename = os.path.basename(gold_file)
        pred_file = os.path.join(pred_dir, basename)
        
        if os.path.exists(pred_file):
            pairs.append((gold_file, pred_file))
    
    return pairs

# Example usage
if __name__ == "__main__":
    # Directories containing gold standard and prediction files
    gold_dir = "_Data/Annotations/gold"
    pred_dir = "_Data/Annotations/predicted"
    
    # Check if evaluating individual files or directories
    if os.path.isdir(gold_dir) and os.path.isdir(pred_dir):
        # Find matching file pairs
        file_pairs = get_file_pairs(gold_dir, pred_dir)
        
        if not file_pairs:
            print(f"No matching files found in {gold_dir} and {pred_dir}")
            exit(1)
            
        print(f"Found {len(file_pairs)} document pairs to evaluate")
        
        # Evaluate each pair
        all_results = []
        for gold_path, pred_path in file_pairs:
            doc_id = os.path.basename(gold_path)
            try:
                result = evaluate_extraction(gold_path, pred_path)
                all_results.append(result)
                print(f"Successfully evaluated {doc_id}")
            except Exception as e:
                print(f"Error evaluating {doc_id}: {e}")
        
        # Calculate micro and macro averages
        micro_avg = calculate_micro_average(all_results)
        macro_avg = calculate_macro_average(all_results)
        
        # Print averages
        print_average_metrics(micro_avg, macro_avg)
        
    else:
        # Evaluate single file pair
        gold_path = "gold_standard.json"
        predicted_path = "predicted.json" 
        results = evaluate_extraction(gold_path, predicted_path)
        print_evaluation_summary(results)