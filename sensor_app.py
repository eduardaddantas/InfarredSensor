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
        
async def main(sensor_type, frequency, min_value, max_value):
    nats_client = NATS()
    await nats_client.connect(servers=["nats://localhost:4222"])

    sensor = InfraredSensor(sensor_type, min_value, max_value)
    
    async def publish_data():
        while True:
            data = sensor.read_data()
            await nats_client.publish("sensor.data", str(data).encode())
            await asyncio.sleep(frequency)

    await publish_data()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infrared Sensor Data Publisher")
    parser.add_argument("--sensor-type", type=str, choices=["mockup", "real"], default="mockup", help="Tipo de sensor a emplear")
    parser.add_argument("--frequency", type=int, default=2, help="Frecuencia de lectura del sensor en segundos")
    parser.add_argument("--min-value", type=int, default=0, help="Valor mínimo generado por el sensor mockup")
    parser.add_argument("--max-value", type=int, default=65535, help="Valor máximo generado por el sensor mockup")
    
    args = parser.parse_args()

    asyncio.run(main(args.sensor_type, args.frequency, args.min_value, args.max_value))

