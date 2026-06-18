class PortfolioStack:
    def __init__(self):
        self.stack = []

    def push(self, change):
        self.stack.append(change)
        return change
    
    def pop(self):
        if self.is_empty():
            return None
        return self.stack.pop()
    
    def peek(self):
        if self.is_empty():
            return None
        return self.stack[-1]
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def get_all_changes(self):
        return list(reversed(self.stack))


if __name__ == "__main__":
    history = PortfolioStack()

    history.push("Reduce TSLA by 10%")
    history.push("Increase Cash by 5%")
    history.push("Add JPM by 8%")

    print("All Changes:", history.get_all_changes())
    print("Latest Change:", history.peek())
    print("Undo:", history.pop())
    print("After Undo:", history.get_all_changes())
    

        