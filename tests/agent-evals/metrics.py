from typing import List, Set, Tuple

def extract_entities_from_tags(tokens: List[str], tags: List[int]) -> Set[Tuple[str, int, int]]:
    entities = set()
    current_entity = []
    start_idx = None

    for idx, tag in enumerate(tags):
        if tag != 0:
            if start_idx is None:
                start_idx = idx
            current_entity.append(tokens[idx])
        else:
            if current_entity:
                entity_text = " ".join(current_entity)
                entities.add((entity_text, start_idx, idx - 1))
                current_entity = []
                start_idx = None

    if current_entity:
        entity_text = " ".join(current_entity)
        entities.add((entity_text, start_idx, len(tokens) - 1))

    return entities

def calculate_f1(predicted_entities: Set[Tuple[str, int, int]],
                 ground_truth_entities: Set[Tuple[str, int, int]]) -> dict:

    true_positives = len(predicted_entities & ground_truth_entities)
    false_positives = len(predicted_entities - ground_truth_entities)
    false_negatives = len(ground_truth_entities - predicted_entities)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }
