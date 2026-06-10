from ml_model import predict_failure

result = predict_failure(
    equipment_age=10,
    usage_hours=15000,
    previous_breakdowns=6,
    maintenance_frequency=120,
    error_count=50
)

print(result)