class RuleSet:
    """
    Represents a Life-like cellular automaton ruleset.

    A RuleSet parses a rule expressed in the standard Life DSL format
    ``Bxxx/Syyy``, where the ``B`` section specifies neighbor counts
    at which new cells are *born*, and the ``S`` section specifies
    neighbor counts at which existing cells *survive*. For example:

        B3/S23 - Conway's Game of Life
        B36/S23 - HighLife
        B34/S34 - 34-Life

    The rule string is compiled into a small Python function.
    That function is then called at runtime
    to determine the state transition for each cell during grid evolution.
    """

    def __init__(self, dsl_rule: str = None) -> None:
        """
        Initialize a RuleSet from a Life-like rule string.

        Parameters
        ----------
        dsl_rule : str
            A rule in the format ``"Bxxx/Syyy"``. Must contain a birth
            clause starting with ``B`` and a survival clause starting with
            ``S``. Digits represent the neighbor counts (0–8) at which
            birth or survival occurs.

        Raises
        ------
        ValueError
            If no rule is provided or the rule is syntactically invalid.
        """

        if dsl_rule is None:
            raise ValueError("Must provide a rule string (e.g. 'B3/S23')")
        self.rule_func = RuleSet.compile_life_rule(dsl_rule)

    def evaluate(self, is_alive: bool, neighbors: int) -> str:
        return self.rule_func(is_alive, neighbors)

    @staticmethod
    def compile_life_rule(rule_str: str):
        """
        Compile a Life-like rule string into a Python function.

        This method performs three steps:

        1. **Parse** the DSL rule string (e.g. ``"B3/S23"``).
        2. **Extract** the sets of neighbor counts that cause birth and
           survival transitions.
        3. **Generate a Python function dynamically** that implements the
           rule. The function is inserted into a temporary scope using
           ``exec`` and returned.

        The resulting function accepts two arguments:

            (is_alive: bool, neighbors: int) → str

        and returns ``"born"``, ``"survive"``, or ``"die"``.

        Parameters
        ----------
        rule_str : str
            A rule in the standard Life-like notation, e.g. ``"B3/S23"``.

        Returns
        -------
        Callable[[bool, int], str]
            A dynamically generated function implementing the rule.

        Raises
        ------
        ValueError
            If the rule does not follow the required ``B.../S...`` format.
        """

        rule_str = rule_str.strip().upper()
        if not rule_str.startswith("B"):
            raise ValueError("Rule must start with a B (Birth).")

        try:
            born_part, survive_part = rule_str.split("/")
        except ValueError:
            raise ValueError("Rule must be in 'B.../S...' format.")

        if not survive_part.startswith("S"):
            raise ValueError("Rule must start with an S (Survive).")

        born = {int(n) for n in born_part[1:]}
        survive = {int(n) for n in survive_part[1:]}

        src = f"""
def rule(is_alive: bool, neighbors: int) -> str:
    if not is_alive and neighbors in {born}:
        return "born"
    if is_alive and neighbors in {survive}:
        return "survive"
    return "die"
"""

        scope = {}
        exec(src, scope)
        return scope["rule"]
