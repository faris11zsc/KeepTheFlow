# Project Validators

Automated checks that protect critical invariants. Run before every push via pre-push hook.

| Validator | What it checks | Command |
|:----------|:---------------|:--------|
| validate-lessons.js | Every lesson has matching hide/copy-link buttons, JS reveal logic, clipboard handler | `node validate-lessons.js` |

## Adding New Validators

When a bug is fixed that could recur, create a validator:
1. Write the script in the repo root (e.g., `validate-<what>.js`)
2. Add it to this table
3. Add it to `.git/hooks/pre-push`
