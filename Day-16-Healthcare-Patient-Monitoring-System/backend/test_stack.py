from stack_manager import Stack

stack = Stack()

stack.push("Heart Rate: 80")
stack.push("Heart Rate: 85")
stack.push("Heart Rate: 90")

print("All readings newest first:")
print(stack.get_all())

print("\nLatest reading:")
print(stack.peek())

print("\nUndo latest reading:")
print(stack.pop())

print("\nAfter undo:")
print(stack.get_all())

print("\nStack size:")
print(stack.size())