from heap_similarity import TransactionSimilarity


similarity = TransactionSimilarity("data/transactions.csv")

input_transaction = {
    "amt": 250.75,
    "category": "shopping_net",
    "state": "CA",
    "gender": "M",
    "city_pop": 50000
}

result = similarity.find_similar_transactions(input_transaction, k=5)

for item in result:
    print(item)