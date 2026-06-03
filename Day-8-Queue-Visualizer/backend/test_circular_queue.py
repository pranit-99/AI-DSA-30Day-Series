from circular_queue import CircularQueue

cpu_queue = CircularQueue(capacity=5)

print("Initial Queue:")
print(cpu_queue.get_status("Initial status", "status"))

print("\nAdding CPU tasks...")
print(cpu_queue.enqueue("Task A"))
print(cpu_queue.enqueue("Task B"))
print(cpu_queue.enqueue("Task C"))
print(cpu_queue.enqueue("Task D"))
print(cpu_queue.enqueue("Task E"))

print("\nTrying to add Task F when full...")
print(cpu_queue.enqueue("Task F"))

print("\nProcessing two tasks...")
print(cpu_queue.dequeue())
print(cpu_queue.dequeue())

print("\nAdding Task F and Task G after space is available...")
print(cpu_queue.enqueue("Task F"))
print(cpu_queue.enqueue("Task G"))

print("\nFinal Queue:")
print(cpu_queue.get_status("Final status", "status"))