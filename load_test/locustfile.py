import time
from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def sign_up_test(self):
        self.client.post(
            "/sign-up",
            json={
                "email": "email@email.com",
                "name": "송은우",
                "password": "Qwerasdf1234!",
                "profile": "안녕하세요 송은우입니다!"
            }
        )

    @task
    def tweet_test(self):
        self.client.post(
            "/tweet",
            json={
                "id": 1,
                "tweet": "트윗 부하테스트"
            }
        )
