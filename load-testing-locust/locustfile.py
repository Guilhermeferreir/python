import random
from locust import HttpUser, TaskSet, task, between, constant


API_KEY = "*:development.038edc4c1a4f6b67ebfb2ed7b4ead102c85afedf22ba5de15514775a"
API_HEADER = {
    "Authorization": API_KEY
}


class UserBehavior(TaskSet):
    GLOBAL_FEATURES = []
    
    @task
    def get_all_flags(self):
        response = self.client.get("/api/client/features",
            headers=API_HEADER,
        )
        all_features_response = response.json()
        features = []
        for feature in all_features_response.get('features', []):
            features.append(feature["name"])
        self.GLOBAL_FEATURES = features

    @task
    def get_unique_flag(self):
        if len(self.GLOBAL_FEATURES) > 0:
            response = self.client.get(f"/api/client/features/{random.choice(self.GLOBAL_FEATURES)}", headers=API_HEADER)            


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = constant(1)
    host = "http://unleash.unleash:4242"
