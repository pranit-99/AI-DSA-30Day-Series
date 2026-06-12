class SeverityManager:
    def assign_severity(self, category, description):
        text = description.lower()

        if category == "Security Incident":
            if "malware" in text or "breach" in text or "brute force" in text:
                return "Critical"
            return "High"

        if category == "Database Failure":
            if "crashed" in text or "down" in text or "stopped" in text:
                return "Critical"
            if "timeout" in text or "slow" in text:
                return "High"
            return "Medium"

        if category == "Network Failure":
            if "unreachable" in text or "dropped" in text or "gateway" in text:
                return "High"
            return "Medium"

        if category == "Application Error":
            if "500" in text or "payment" in text or "crashed" in text:
                return "High"
            return "Medium"

        return "Low"