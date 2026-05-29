import ast

def estimate_time_complexity(max_loop_depth, recursion_count):
    if recursion_count > 0:
        return "O(2^n) or recursive complexity"

    if max_loop_depth == 0:
        return "O(1)"

    if max_loop_depth == 1:
        return "O(n)"

    if max_loop_depth == 2:
        return "O(n²)"

    return "O(n³) or higher"

def estimate_space_complexity(code):
    memory_patterns = ["[]", "{}", "list(", "dict(", "set(", "tuple("]

    memory_count = 0

    for pattern in memory_patterns:
        memory_count += code.count(pattern)

    if memory_count == 0:
        return "O(1)"

    return "O(n)"

def calculate_performance_score(
    max_loop_depth,
    recursion_count,
    loop_count
):
    score = 100

    score -= (max_loop_depth * 15)
    score -= (recursion_count * 20)
    score -= (loop_count * 5)

    if score < 0:
        score = 0

    return score

def get_risk_level(score):
    if score >= 80:
        return "LOW"

    if score >= 50:
        return "MEDIUM"

    return "HIGH"

def generate_optimization_suggestions(
    max_loop_depth,
    recursion_count,
    loop_count,
    space_complexity
):
    suggestions = []

    if max_loop_depth >= 2:
        suggestions.append(
            "Nested loops detected. Consider using HashMap, Set, or sorting-based logic to reduce time complexity."
        )

    if recursion_count > 0:
        suggestions.append(
            "Recursion detected. Check base condition and consider memoization or dynamic programming if repeated calls exist."
        )

    if loop_count > 2:
        suggestions.append(
            "Multiple loops detected. Check if some loops can be combined or optimized."
        )

    if space_complexity == "O(n)":
        suggestions.append(
            "Extra memory usage detected. Review whether list/dict/set storage is required."
        )

    if not suggestions:
        suggestions.append(
            "Code structure looks efficient for the current static analysis."
        )

    return suggestions

def get_runtime_heaviness(time_complexity):
    if time_complexity == "O(1)":
        return "Very Light"

    if time_complexity in ["O(n)", "O(log n)"]:
        return "Light"

    if time_complexity == "O(n²)":
        return "Heavy"

    return "Very Heavy"


def analyze_code_structure(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return {
            "error": "Invalid Python code",
            "details": str(error)
        }

    total_lines = len(code.split("\n"))

    loop_count = 0
    if_count = 0
    function_count = 0
    recursion_count = 0
    max_loop_depth = 0

    function_names = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_count += 1
            function_names.add(node.name)

        if isinstance(node, (ast.For, ast.While)):
            loop_count += 1

        if isinstance(node, ast.If):
            if_count += 1

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in function_names:
                    recursion_count += 1

    def get_loop_depth(node, current_depth=0):
        max_depth = current_depth

        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While)):
                max_depth = max(
                    max_depth,
                    get_loop_depth(child, current_depth + 1)
                )
            else:
                max_depth = max(
                    max_depth,
                    get_loop_depth(child, current_depth)
                )

        return max_depth

    max_loop_depth = get_loop_depth(tree)
    space_complexity = estimate_space_complexity(code)
    time_complexity = estimate_time_complexity(max_loop_depth, recursion_count)
    performance_score = calculate_performance_score(max_loop_depth,
                                                    recursion_count,
                                                    loop_count)

    return {
    "total_lines": total_lines,
    "loop_count": loop_count,
    "if_count": if_count,
    "function_count": function_count,
    "recursion_count": recursion_count,
    "max_loop_depth": max_loop_depth,
    "estimated_time_complexity": time_complexity,
    "estimated_space_complexity": space_complexity,
    "performance_score": performance_score,
    "risk_level": get_risk_level(performance_score),
    "runtime_heaviness": get_runtime_heaviness(time_complexity),
    "optimization_suggestions": generate_optimization_suggestions(
        max_loop_depth,
        recursion_count,
        loop_count,
        space_complexity
    )
}