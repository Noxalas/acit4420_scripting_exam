import os
import json


class RuleSet:
    def __init__(self, rule_dir: str, default_action: str = "unchanged") -> None:
        self.rule_dir = rule_dir
        self.rules = []
        self.default_action = default_action
        self.load_rules()

    def load_rules(self):
        for filename in sorted(os.listdir(self.rule_dir)):
            if filename.endswith(".json"):
                path = os.path.join(self.rule_dir, filename)
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.rules.append(data)

    def evaluate(self, is_alive: bool, neighbors: int) -> str:
        state = "alive" if is_alive else "dead"
        for rule in self.rules:
            condition = rule["conditions"]
            if condition.get("cell_state") != state:
                continue
            if self._matches(condition, neighbors):
                return rule["action"]
        return self.default_action

    def _matches(self, condition: dict, neighbors: int) -> bool:
        value = condition["value"]

        match condition["operator"]:
            case "equals":
                return neighbors == value
            case "less_than":
                return neighbors < value
            case "greater_than":
                return neighbors > value
            case "in":
                return neighbors in value
            case "not_in":
                return neighbors not in value
            case "and":
                return all(self._matches(c, neighbors) for c in condition["conditions"])
            case "or":
                return any(self._matches(c, neighbors) for c in condition["conditions"])
        return False

    def __repr__(self) -> str:
        names = ", ".join([r["id"] for r in self.rules])
        return f"<RuleSet rules=[{names}]>"

