import time
from locust import HttpUser, task

class DemoUser(HttpUser):
    @task
    def mesas(self):
        self.client.get("Mesas")

    @task(4)
    def menu(self):
        self.client.get("Categorias")
        self.client.get("Productos")


    @task(2)
    def ver_pedido(self):
        for id in range(2, 7):
            self.client.get(f"Pedidos/{id}")
            time.sleep(0.3)