import argparse
import random 
import asyncio
from nats.aio.client import Client as NATS

class InfraredSensor:
    def __init__(self, sensor_type, min_value, max_value):
        self.sensor_type = sensor_type
        self.min_value = min_value
        self.max_value = max_value

    def read_data(self):
        if self.sensor_type == 'mockup':
            return [random.randint(self.min_value, self.max_value) for _ in range(64)]
        else:
            # Aquí se implementaría la lectura de un sensor real
            return [0] * 64  # Simulamos con ceros por ahora
        

    async def start_capture(self, frequency, nats_client, topic):
        """
        Inicia la captura de datos del sensor y publica los datos en un tema NATS.

        Args:
            frequency (int): Frecuencia en segundos para la captura de datos.
            nats_client (NATS): Cliente NATS conectado.
            topic (str): Tema en el cual publicar los datos del sensor.

        Este método inicia un bucle que:
        1. Lee los datos del sensor.
        2. Publica los datos en el servidor NATS.
        3. Espera el tiempo especificado por `frequency` segundos antes de repetir.

        El bucle continúa ejecutándose hasta que `self.running` sea `False`, 
        lo cual se controla mediante la función `stop_capture`.
        """

        self.running = True
        while self.running:
            data = self.read_data()
            await nats_client.publish(topic, str(data).encode())
            await asyncio.sleep(frequency)

    def stop_capture(self):
        """
        Detiene la captura de datos del sensor.

        Este método simplemente establece `self.running` a `False`, 
        lo cual rompe el bucle en `start_capture`.
        """
          
        self.running = False        

async def main(sensor_type, frequency, min_value, max_value):
    nats_client = NATS()
    await nats_client.connect(servers=["nats://localhost:4222"])

    sensor = InfraredSensor(sensor_type, min_value, max_value)
    
    async def start_handler(msg):
        """
        Manejador de mensajes para iniciar la captura de datos del sensor.
        """
        print("Received a start command")
        await sensor.start_capture(frequency, nats_client, "sensor.data")

    async def stop_handler(msg):
        """
        Manejador de mensajes para detener la captura de datos del sensor.
        """
        print("Received a stop command")
        sensor.stop_capture()

    # Suscribirse a los temas para iniciar y detener la captura de datos
    await nats_client.subscribe("sensor.start", cb=start_handler)
    await nats_client.subscribe("sensor.stop", cb=stop_handler)

    print(f"Listening for start and stop commands on NATS server...")
    # Mantener el programa corriendo indefinidamente
    await asyncio.Event().wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infrared Sensor Data Publisher")
    parser.add_argument("--sensor-type", type=str, choices=["mockup", "real"], default="mockup", help="Tipo de sensor a emplear")
    parser.add_argument("--frequency", type=int, default=2, help="Frecuencia de lectura del sensor en segundos")
    parser.add_argument("--min-value", type=int, default=0, help="Valor mínimo generado por el sensor mockup")
    parser.add_argument("--max-value", type=int, default=65535, help="Valor máximo generado por el sensor mockup")
    
    args = parser.parse_args()

    asyncio.run(main(args.sensor_type, args.frequency, args.min_value, args.max_value))

