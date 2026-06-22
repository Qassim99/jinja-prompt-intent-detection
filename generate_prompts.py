"""
generate_prompts.py
Loads the Jinja template, fills it with example inputs from examples.json,
and prints several prompt variants for customer-support intent detection.

Run:  python generate_prompts.py
"""

import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

HERE = Path(__file__).parent


def load_data():
    with open(HERE / "examples.json", encoding="utf-8") as f:
        return json.load(f)


def build_env():
    # trim_blocks/lstrip_blocks keep the rendered prompt clean despite the
    # block tags used for loops and conditionals.
    return Environment(
        loader=FileSystemLoader(str(HERE)),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )


def main():
    data = load_data()
    env = build_env()
    template = env.get_template("prompt_template.j2")

    intents = data["intents"]
    examples = data["few_shot_examples"]
    messages = data["messages_to_classify"]

    # Three variants demonstrate why a templating engine beats string formatting:
    # the same template produces structurally different prompts from flags alone.
    variants = [
        {
            "label": "ZERO-SHOT (plain text)",
            "kwargs": dict(
                examples=None,
                want_json=False,
                allow_clarify=False,
                want_confidence=False,
            ),
        },
        {
            "label": "FEW-SHOT + CLARIFY (plain text + confidence)",
            "kwargs": dict(
                examples=examples,
                want_json=False,
                allow_clarify=True,
                want_confidence=True,
            ),
        },
        {
            "label": "FEW-SHOT (JSON output + confidence)",
            "kwargs": dict(
                examples=examples,
                want_json=True,
                allow_clarify=False,
                want_confidence=True,
            ),
        },
    ]

    for msg in messages:
        for v in variants:
            prompt = template.render(intents=intents, message=msg, **v["kwargs"])
            print("=" * 70)
            print(f"VARIANT: {v['label']}")
            print(f"MESSAGE: {msg}")
            print("-" * 70)
            print(prompt.strip())
            print()


if __name__ == "__main__":
    main()
