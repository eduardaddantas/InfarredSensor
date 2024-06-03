import unittest
import asyncio
from unittest.mock import MagicMock, patch
from nats.aio.client import Client as NATS
from sensor_app import InfraredSensor

class TestInfraredSensor(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.nats_client = MagicMock(spec=NATS)
        await self.nats_client.connect.return_value

    async def asyncTearDown(self):
        await self.nats_client.close.return_value

    async def test_start_capture_mockup(self):
        sensor = InfraredSensor('mockup', 0, 100)
        frequency = 2
        topic = "sensor.data"

        publish_task = asyncio.create_task(sensor.start_capture(frequency, self.nats_client, topic))
        
        await asyncio.sleep(0.1)  # Espera breve para asegurar que se ejecute el método

        sensor.stop_capture()
        await publish_task  # Espera a que la tarea de publicación termine

        # Verificar que se llamó a publish en nats_client con los datos generados
        self.nats_client.publish.assert_called_once_with(topic, str(sensor.read_data()).encode())

    async def test_main_with_mockup_sensor(self):
        sensor_type = 'mockup'
        frequency = 2
        min_value = 0
        max_value = 100

        with patch('argparse.ArgumentParser.parse_args',
                   return_value=MagicMock(sensor_type=sensor_type, frequency=frequency,
                                          min_value=min_value, max_value=max_value)):
            with patch('nats.aio.client.Client.connect', new_callable=MagicMock) as connect_mock:
                await main(sensor_type, frequency, min_value, max_value)

        connect_mock.assert_called_once()

    async def test_main_with_real_sensor(self):
        sensor_type = 'real'
        frequency = 2
        min_value = 0
        max_value = 100

        with patch('argparse.ArgumentParser.parse_args',
                   return_value=MagicMock(sensor_type=sensor_type, frequency=frequency,
                                          min_value=min_value, max_value=max_value)):
            with patch('nats.aio.client.Client.connect', new_callable=MagicMock) as connect_mock:
                await main(sensor_type, frequency, min_value, max_value)

        connect_mock.assert_called_once()

if __name__ == '__main__':
    unittest.main()

