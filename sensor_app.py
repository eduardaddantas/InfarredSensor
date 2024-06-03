import argparse
import random 

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infrared Sensor Data Publisher")
    parser.add_argument("--sensor-type", type=str, choices=["mockup", "real"], default="mockup", help="Tipo de sensor a emplear")
    parser.add_argument("--frequency", type=int, default=2, help="Frecuencia de lectura del sensor en segundos")
    parser.add_argument("--min-value", type=int, default=0, help="Valor mínimo generado por el sensor mockup")
    parser.add_argument("--max-value", type=int, default=65535, help="Valor máximo generado por el sensor mockup")
    
    args = parser.parse_args()

    sensor = InfraredSensor(args.sensor_type, args.min_value, args.max_value)
    data = sensor.read_data()
    print(data)
