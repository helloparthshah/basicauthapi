from locust import HttpUser, between, task
import json


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        self.login()

    def login(self):
        self.token = json.loads(self.client.get(
            "/login", auth=('test', 'test')).content.decode())['token']

    @ task
    def users(self):
        self.client.get("/users")

    @ task
    def user(self):
        self.client.get("/user", headers={'token': self.token})
