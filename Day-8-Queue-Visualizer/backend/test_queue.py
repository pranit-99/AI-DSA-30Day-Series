# Testing Simple Queue locally
# Real-life example: Bank Token Counter System

from simple_queue import SimpleQueue

# Creating queue object
bank_queue = SimpleQueue()

print("Initial Queue:")
print(bank_queue.get_queue())

print("\nAdding customers...")
print(bank_queue.enqueue("Amit"))
print(bank_queue.enqueue("Priya"))
print(bank_queue.enqueue("Rahul"))

print("\nChecking who is next:")
print(bank_queue.peek())

print("\nServing one customer...")
print(bank_queue.dequeue())

print("\nFinal Queue:")
print(bank_queue.get_queue())