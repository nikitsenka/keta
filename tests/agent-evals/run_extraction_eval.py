import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from datasets import load_dataset
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

sys.path.insert(0, str(Path(__file__).parent))
from metrics import extract_entities_from_tags, calculate_f1

class ExtractedEntity(BaseModel):
    name: str = Field(description="Entity name")
    type: str = Field(description="Entity type")
    confidence: float = Field(description="Confidence score", ge=0.0, le=1.0)

class EntityExtractionOutput(BaseModel):
    entities: list[ExtractedEntity] = Field(description="List of extracted entities")

async def main():
    print("Loading Few-NERD dataset...")
    dataset = load_dataset("DFKI-SLT/few-nerd", "supervised")
    test_samples = dataset['test'][:10]

    print(f"Loaded {len(test_samples['tokens'])} samples\n")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=api_key)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert at extracting named entities from text.

Extract all named entities from the provided text. Identify:
- PERSON: Names of people
- ORGANIZATION: Companies, institutions, organizations
- LOCATION: Places, cities, countries, addresses
- DATE: Dates, times, periods
- PRODUCT: Products, services, tools
- CONCEPT: Abstract concepts, theories, methods
- EVENT: Named events, meetings, conferences

For each entity, provide:
- name: The exact text as it appears
- type: One of the types above
- confidence: How confident you are (0.0 to 1.0)

Be thorough but precise. Only extract entities that are clearly identifiable."""),
        ("human", "Text to analyze:\n\n{text}"),
    ])

    chain = prompt | llm.with_structured_output(EntityExtractionOutput)

    all_results = []
    total_precision = 0.0
    total_recall = 0.0
    total_f1 = 0.0

    for idx in range(len(test_samples['tokens'])):
        tokens = test_samples['tokens'][idx]
        ner_tags = test_samples['ner_tags'][idx]

        text = " ".join(tokens)
        ground_truth = extract_entities_from_tags(tokens, ner_tags)

        print(f"\n{'='*80}")
        print(f"Sample {idx + 1}")
        print(f"{'='*80}")
        print(f"Text: {text[:150]}{'...' if len(text) > 150 else ''}")
        print(f"\nGround truth entities: {len(ground_truth)}")
        for entity in list(ground_truth)[:5]:
            print(f"  - {entity[0]} (pos: {entity[1]}-{entity[2]})")
        if len(ground_truth) > 5:
            print(f"  ... and {len(ground_truth) - 5} more")

        result = await chain.ainvoke({"text": text})
        extracted = [{"name": e.name, "type": e.type, "confidence": e.confidence} for e in result.entities]

        predicted_entities = set()
        for entity in extracted:
            entity_name = entity['name']
            entity_text_lower = entity_name.lower()
            text_lower = text.lower()

            if entity_text_lower in text_lower:
                start_char = text_lower.index(entity_text_lower)

                start_token_idx = len(text[:start_char].split())
                end_token_idx = start_token_idx + len(entity_name.split()) - 1

                predicted_entities.add((entity_name, start_token_idx, end_token_idx))

        print(f"\nExtracted entities: {len(predicted_entities)}")
        for entity in list(predicted_entities)[:5]:
            print(f"  - {entity[0]} (pos: {entity[1]}-{entity[2]})")
        if len(predicted_entities) > 5:
            print(f"  ... and {len(predicted_entities) - 5} more")

        metrics = calculate_f1(predicted_entities, ground_truth)

        print(f"\nMetrics:")
        print(f"  Precision: {metrics['precision']:.3f}")
        print(f"  Recall:    {metrics['recall']:.3f}")
        print(f"  F1 Score:  {metrics['f1']:.3f}")
        print(f"  TP: {metrics['true_positives']}, FP: {metrics['false_positives']}, FN: {metrics['false_negatives']}")

        all_results.append(metrics)
        total_precision += metrics['precision']
        total_recall += metrics['recall']
        total_f1 += metrics['f1']

    print(f"\n{'='*80}")
    print(f"OVERALL RESULTS (10 samples)")
    print(f"{'='*80}")
    print(f"Average Precision: {total_precision / 10:.3f}")
    print(f"Average Recall:    {total_recall / 10:.3f}")
    print(f"Average F1 Score:  {total_f1 / 10:.3f}")

if __name__ == "__main__":
    asyncio.run(main())
