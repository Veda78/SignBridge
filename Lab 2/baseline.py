import argparse
import json
import os
import sys

from anthropic import Anthropic

MODEL = os.environ.get("SIGNBRIDGE_MODEL", "claude-sonnet-5")
SYSTEM_PROMPT = """Convert these ASL glosses into an English sentence, reordering words since ASL grammar differs from English, and flag any gloss at or below the given confidence threshold, replying with a JSON object containing a "sentence" field and a "flagged_signs" field listing each flagged gloss with its confidence and a short reason."""


def run(gloss, threshold):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)
 
    client = Anthropic(api_key=api_key)
    prompt = f"Threshold: {threshold}\n\n{json.dumps(gloss, indent=2)}"
 
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
 
    text = "".join(b.text for b in response.content if b.type == "text").strip()
 
   
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.startswith("json"):
            text = text[4:].strip()
 
    return json.loads(text)
 
 
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gloss", required=True)
    parser.add_argument("--threshold", type=float, default=0.7)
    parser.add_argument("--out", default="outputs/result.json")
    args = parser.parse_args()
 
    gloss = json.load(open(args.gloss))
    result = run(gloss, args.threshold)
 
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    json.dump(result, open(args.out, "w"), indent=2)
 
    print(json.dumps(result, indent=2))
    print(f"\nsaved to {args.out}", file=sys.stderr)
 
if __name__ == "__main__":
    main()