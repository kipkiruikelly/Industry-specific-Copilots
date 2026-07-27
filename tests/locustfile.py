from locust import HttpUser, task, between

class MediCopilotLoadTestUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def query_clinical_endpoint(self):
        payload = {
            "query": "What is the recommended dosage of Metformin for Patient John Doe DOB 05/12/1980?",
            "patient_id": "P-1001",
            "user_id": "load_test_doc",
            "user_role": "physician",
            "departments": ["cardiology", "endocrinology"],
        }
        self.client.post("/api/v1/clinical/query", json=payload)

    @task(1)
    def check_health(self):
        self.client.get("/api/v1/health/")
