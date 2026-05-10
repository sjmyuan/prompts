# Writing Style Guide

Adapt writing style to the documentation type:

**Requirements & Specifications:**
- Be precise and unambiguous
- Use "must," "should," "may" consistently (RFC 2119 style)
- Focus on what, not how
- Include acceptance criteria

**Architecture Documentation:**
- Use diagrams where helpful (describe them in text)
- Explain the "why" behind architectural decisions
- Document constraints and trade-offs
- Keep high-level; avoid implementation minutiae

**README:**
- Start with a brief, compelling overview
- Prioritize getting started quickly
- Use bullet points and short paragraphs
- Include badges, screenshots, or demos where relevant

**API Documentation:**
- Document all parameters, return values, and exceptions
- Provide type signatures (TypeScript, JSDoc)
- Include usage examples for each method
- Note deprecations and version compatibility

**Usage Examples:**
- Show realistic, practical scenarios
- Include necessary imports and setup
- Comment complex or non-obvious code
- Demonstrate both common and advanced usage

**Troubleshooting Guides:**
- Use problem-solution format
- Include error messages users actually see
- Provide step-by-step debugging instructions
- Link to related issues or discussions

**Changelog:**
- Group by version, newest first
- Categorize: Added, Changed, Deprecated, Removed, Fixed, Security
- Be concise but specific
- Reference issues/PRs when helpful
