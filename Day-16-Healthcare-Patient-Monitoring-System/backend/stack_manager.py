class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        return item
    
    def pop(self):
        if self.is_empty():
            return None
        
        return self.items.pop()
    
    def peek(self):
        if self.is_empty():
            return None
        
        return self.items[-1]
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)
    
    def get_all(self):
        return self.items[::-1]
    

