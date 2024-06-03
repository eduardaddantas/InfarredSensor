## Instalación

Para instalar las dependencias, ejecute:

```bash
pip install -r requirements.txt
```

## Cómo Ejecutar

### Parámetros

La aplicación puede configurarse con los siguientes parámetros de línea de comandos:

- `--sensor-type`: Tipo de sensor a utilizar (`mockup` o `real`). Predeterminado: `mockup`
- `--frequency`: Frecuencia de lectura del sensor en segundos. Predeterminado: `2`
- `--min-value`: Valor mínimo generado por el sensor mockup. Predeterminado: `0`
- `--max-value`: Valor máximo generado por el sensor mockup. Predeterminado: `65535`

### Comandos

Para ejecutar la aplicación con los parámetros predeterminados, usa:

```bash
python infrared_sensor.py
```

## Ejecución de Testes

### Comandos

Para ejecutar los testes, usa:

```bash
python -m unittest "test_infrared_sensor.py"
```