import time
from locust import HttpUser, task
import random

MESAS = {
    1: 1,
    2: 5,
    3: 9,
    4: 7,
    5: 8,
    6: 2,
    7: 3,
    8: 4,
    9: 11,
    10: 12,
    11: 13
}

CODIGOS_SERVICIO = [2831, 2480, 8774]
IDPRODUCTOS = [1, 2, 3, 4]


class DemoUser(HttpUser):

    @task
    def mesas(self):
        self.client.get("/Mesas")


    @task(3)
    def ver_pedido(self):
        self.client.get(f"/Pedidos/5925")

    @task(4)
    def flujo_completo_mesa(self):

        self.client.get("/Categorias")
        self.client.get("/Productos")

        # Elegir mesa, código de servicio y productos aleatorios
        id_mesa, numero_mesa = random.choice(list(MESAS.items()))
        codigo_mozo = random.choice(CODIGOS_SERVICIO)
        productos_a_pedir = random.sample(IDPRODUCTOS, k=random.randint(1, len(IDPRODUCTOS)))

        # 1. Abrir la mesa
        with self.client.put(f"/Mesas/{id_mesa}/Abrir?codigoMozo={codigo_mozo}", name="Abrir Mesa", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Fallo al abrir mesa {id_mesa}")
                return

       # 2. Hacer pedidos (cantidad aleatoria de ítems, posibles repetidos)
        cantidad_items = random.randint(1, 4)
        productos_a_pedir = random.choices(IDPRODUCTOS, k=cantidad_items)

        for id_producto in productos_a_pedir:
            item_data = {
                "id": id_producto,
                "indicaciones": ""
            }
            with self.client.post(f"/Items/{numero_mesa}", json=[item_data], name="Agregar Item", catch_response=True) as response:
                if response.status_code != 200:
                    response.failure(f"Fallo al agregar item {id_producto} en mesa {numero_mesa}")

        # 3. Cerrar la mesa
        with self.client.put(f"/Mesas/{id_mesa}/Cerrar?codigoMozo=asd", name="Cerrar Mesa", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Fallo al cerrar mesa {id_mesa}")
        
        # Dormir 5 segundos

        time.sleep(5)