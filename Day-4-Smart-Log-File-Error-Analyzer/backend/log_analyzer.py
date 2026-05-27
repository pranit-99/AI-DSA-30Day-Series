from ml_predictor import predict_severity

def read_log_file(file_path):
    with open(file_path,"r") as file:
        logs = file.readlines()

    return logs

def extract_error_logs(logs):
    error_logs = []

    for log in logs:
        if 'ERROR' in log:
            error_logs.append(log.strip())

    return error_logs

def count_error_frequency(error_logs):
    error_count = {}

    for error in error_logs:

        error_message = error.replace("ERROR ", "")

        if error_message in error_count:
            error_count[error_message] += 1
        else:
            error_count[error_message] = 1

    return error_count

def get_top_errors(error_frequency, top_n = 3):
    sorted_errors = sorted(
        error_frequency.items(),
        key=lambda item: item[1],
        reverse=True
    )

    return sorted_errors[:top_n]


#file_path = "../sample_logs/app.log"

def classify_error_category(error_message):
    message = error_message.lower()

    if "database" in message:
        return "Database Error"
    elif "api" in message or "timeout" in message:
        return "API / Network Error"
    elif "authentication" in message or "login" in message:
        return "Authentication Error"
    elif "memory" in message or "cpu" in message:
        return "Performance Error"
    else:
        return "General Error"

def analyze_logs(file_path):
    logs = read_log_file(file_path)
    error_logs = extract_error_logs(logs)
    error_frequency = count_error_frequency(error_logs)
    top_errors = get_top_errors(error_frequency)

    categorized_errors = []

    for error, count in top_errors:
        category = classify_error_category(error)
        severity = predict_severity(error)

        categorized_errors.append({
            "error": error,
            "count": count,
            "category": category,
            "severity" : severity
        })

    result = {
        "total_logs": len(logs),
        "total_errors": len(error_logs),
        "error_frequency": error_frequency,
        "top_errors": categorized_errors
    }

    return result

