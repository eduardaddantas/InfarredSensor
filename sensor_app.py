import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infrared Sensor Data Publisher")
    parser.add_argument("--sensor-type", type=str, choices=["mockup", "real"], default="mockup", help="Tipo de sensor a emplear")
    parser.add_argument("--frequency", type=int, default=2, help="Frecuencia de lectura del sensor en segundos")
    parser.add_argument("--min-value", type=int, default=0, help="Valor mínimo generado por el sensor mockup")
    parser.add_argument("--max-value", type=int, default=65535, help="Valor máximo generado por el sensor mockup")
    
    args = parser.parse_args()

    print(f"Sensor Type: {args.sensor_type}")
    print(f"Frequency: {args.frequency} seconds")
    print(f"Min Value: {args.min_value}")
    print(f"Max Value: {args.max_value}")
