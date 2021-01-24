import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.get("/index")
        self.client.get("/charts")
        # self.client.get("/profileform")
        self.client.get("/ui-buttons")
        # self.client.get("/ui-component")
        self.client.get("/ui-tables")
        self.client.get("/ui-typography")
        self.client.get("/sign-up")

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    def on_start(self):
        # self.client.post("/login", data={"email":"eandrews@robinson-fletcher.com", "password":"3vodnn"})

        with self.client.post('/login', data={"email":"eandrews@robinson-fletcher.com", "password":"3vodnn"}, catch_response=True) as response:
            if 'cookie' not in response.cookies:
                response.failure('login failed')
                # print("Response cookies:", response.cookies)
                # print("Response status code:", response.status_code)
                # print("Response text:", response.text)
