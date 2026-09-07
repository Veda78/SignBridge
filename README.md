# SignBridge

Baseline for my capstone project. Takes a list of ASL glosses with
confidence scores and turns it into an English sentence, flagging any
sign that had low confidence instead of just guessing it.

## Setup

python3 -m pip install -r requirements.txt

Needs an Anthropic API key from console.anthropic.com, either export
it:

export ANTHROPIC_API_KEY=your-key-here

or put it in a .env file copied from .env.example.

## Run

python3 baseline.py --gloss examples/gloss.json

Prints the result and saves it to outputs/result.json.

## Notes

Input is examples/gloss.json. Needs internet access to reach the
Anthropic API. If the model wraps its reply in a code block, the
script strips it before parsing, but it will crash if the reply still
is not valid JSON. Only sees the top guess per sign right now, and is
not connected to the real camera pipeline yet.
