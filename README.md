# Debate Practice MVP

A solo student plays all three speakers on one side against an AI opponent. This is a practice tool, not an official adjudicator or a tool for controlled competition debates.

## Local run

With Python 3.11 or newer, from this folder:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Without an API key the app runs in demo mode: type each student speech and step through six or eight turns. For real transcription, AI opposing speeches, and spoken audio, set `OPENAI_API_KEY` as a shell environment variable. Do not commit the key. `DEBATE_TEXT_MODEL` optionally overrides the default `gpt-4.1-mini` model.

## First deployment and trial

1. Deploy this public repository's `app.py` on Streamlit Community Cloud. In the app's Sharing settings select **Only specific people can view this app** before inviting student testers. Set `OPENAI_API_KEY` in Streamlit's Advanced settings → Secrets as `OPENAI_API_KEY = "..."`. Never commit it or paste it into an issue. An alternative private Python host can run `streamlit run app.py --server.address 0.0.0.0 --server.port $PORT` (substitute its port variable).
2. Test the hosted site over HTTPS on an actual phone. Grant microphone permission. Check a short student recording, edit its transcript, play the AI speech, complete all six turns from each starting side, request feedback, and download the report. Repeat with replies enabled.
3. Try microphone denial, transcription errors, a refresh mid-debate, and a slow or failed API response. Refresh currently loses the session; treat that as a trial limitation.
4. Ask an experienced NZ school debating adjudicator to review several recordings and the AI feedback. Check whether the AI identifies real points of clash, distinguishes student from opponent, and gives useful age-appropriate advice. Revise prompts and rules before inviting a class.
5. Set an API spending limit and tell trial participants what audio/transcripts are sent to the provider and how the host handles logs. Get the appropriate school and family involvement before involving minors.

## Scope

The grade presets follow Auckland Schools Debating's 2026 speech times and order. Other NZ competitions may differ. Advanced-grade live points of information, a real timer, sign-in, durable session storage, and scoring of vocal delivery are not implemented. AI replies are deliberately shorter than official competition speeches to keep first trials practical. The audio transcription API accepts at most 25 MB per speech; the app checks this before upload. Audio remains in the current session and no application database is used. The hosting provider and API provider have their own data handling policies.

## Tests

```bash
python -m unittest discover -s tests
```
