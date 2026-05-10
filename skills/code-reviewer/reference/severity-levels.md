# Severity Levels

Apply consistently when categorizing review findings.

## 🚫 Blocker (MUST fix before merge)
- Security vulnerabilities (injection, auth bypass, data exposure)
- Data loss or corruption risks
- Critical functionality broken
- Build/deployment failures
- Breaking API changes without migration path

## 🔴 Major (SHOULD fix before merge, requires strong justification to skip)
- Significant correctness issues (wrong results, unhandled errors)
- Performance problems affecting user experience
- Missing test coverage for critical paths
- Architectural violations that complicate future changes
- Type safety issues that could cause runtime errors

## 🟡 Minor (Nice to fix, but can be deferred if time-constrained)
- Code duplication or maintainability issues
- Non-critical edge cases not handled
- Suboptimal patterns that work but could be improved
- Missing/incomplete documentation
- Inefficiencies that don't impact current use cases

## 🟢 Nit (Suggestions for polish, no requirement to fix)
- Style inconsistencies (already handled by linter)
- Naming improvements
- Comment/documentation polish
- Code organization preferences
- Micro-optimizations with negligible impact

## ⚠️ Inconsistency (Decision required — severity escalates based on scope)
- Two or more conflicting patterns, styles, or usages detected across the codebase
- **Neither side is assumed correct** — the reviewer presents both and requests a decision
- Escalate to 🔴 Major if the inconsistency affects a widely-used pattern or public API surface
