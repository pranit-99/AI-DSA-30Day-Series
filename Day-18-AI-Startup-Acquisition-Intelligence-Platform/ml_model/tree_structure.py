class TreeNode:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value


def print_tree(node, depth=0):
    if node is None:
        return

    space = "  " * depth

    if node.value is not None:
        print(space + "Prediction:", node.value)
        return

    print(space + f"{node.feature} <= {node.threshold}")
    print(space + "Left:")
    print_tree(node.left, depth + 1)

    print(space + "Right:")
    print_tree(node.right, depth + 1)

def predict_with_path(node, startup_data, path=None):
    if path is None:
        path = []

    if node.value is not None:
        path.append(f"Final Prediction: {node.value}")
        return node.value, path

    feature_value = startup_data[node.feature]

    if feature_value <= node.threshold:
        path.append(f"{node.feature} = {feature_value} <= {node.threshold} → Left")
        return predict_with_path(node.left, startup_data, path)
    else:
        path.append(f"{node.feature} = {feature_value} > {node.threshold} → Right")
        return predict_with_path(node.right, startup_data, path)