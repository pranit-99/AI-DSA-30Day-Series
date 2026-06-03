from priority_queue import PriorityQueue

hospital_queue = PriorityQueue()

print("Initial Priority Queue:")
print(hospital_queue.get_status("Initial status", "status"))

print("\nAdding patients...")
print(hospital_queue.enqueue("Amit", 3))
print(hospital_queue.enqueue("Rahul", 1))
print(hospital_queue.enqueue("Priya", 2))

print("\nChecking next patient:")
print(hospital_queue.peek())

print("\nServing highest priority patient:")
print(hospital_queue.dequeue())

print("\nFinal Queue:")
print(hospital_queue.get_status("Final status", "status"))