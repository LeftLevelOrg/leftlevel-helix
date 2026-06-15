# Documentation Standards

LeftLevel Helix is a public open-source repository. Documentation, code comments, examples, and roadmap notes should be written for external readers.

## Tone

Use a professional, neutral, project-focused tone.

Preferred wording:

- "The project supports..."
- "This prototype currently implements..."
- "Future work includes..."
- "Contributors should..."

Avoid personal or private-context wording:

- "I added..."
- "we did this tonight..."
- "for Danielle..."
- "my plan..."
- informal status notes that only make sense inside a private conversation.

## Public roadmap language

Roadmap documents should describe project phases, scope, current limitations, and next milestones. They should not include private scheduling references or conversational context.

Use versioned headings such as:

- v0.7 UI slice
- v0.8 attachment model
- v0.9 send and receive bridge
- v1.0 app shell preparation

## Security language

Until reviewed, documentation should describe LeftLevel Helix as a prototype, reference implementation, or review candidate.

Do not claim that the project is:

- production-ready;
- independently audited;
- metadata-free;
- anonymous by default;
- impossible to trace;
- equivalent to mature secure messengers.

Use precise language such as:

- server-blind relay design;
- sealed message metadata;
- local encrypted storage;
- pairwise pseudonymous identity;
- review-ready prototype.

## Examples and fixtures

Examples and fixtures must be clearly marked when they are test-only. Do not include real user data, private conversation details, personal account information, or private deployment secrets.

## Formatting

Documentation should use clear headings, concise paragraphs, and stable terms. Prefer lists only when they improve scanning. Avoid jokes, private notes, and overly casual language in committed files.
