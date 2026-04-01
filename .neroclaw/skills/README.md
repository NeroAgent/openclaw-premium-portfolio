# Nero Skill Registry

Skills are stored here as JSON manifests. Each skill captures domain knowledge for a novel problem area.

## Manifest Format

```json
{
  "skill_id": "unique_id",
  "domain": ["category1", "category2"],
  "trigger_phrases": ["phrase1", "phrase2"],
  "tools_required": ["tool1"],
  "validation_check": "command to verify readiness",
  "knowledge_graph": {
    "common_failures": [],
    "quick_fix": ""
  }
}
```

Skills are auto-generated when Nero encounters and solves a new problem domain.
