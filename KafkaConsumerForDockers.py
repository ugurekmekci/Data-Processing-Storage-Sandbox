def test_kafka_fixture(self):
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers='kafka.docker:9092',
            key_deserializer=lambda item: json.loads(item.decode('utf-8')),
            value_deserializer=lambda item: json.loads(item.decode('utf-8')),
            auto_offset_reset='earliest',
        )

        actual_data = []
        for i in range(5):
            message = next(consumer)
            data = {'key': message.key, 'value': message.value}
            actual_data.append(data)

        expected_data = self.spark.read.json(
            absolute_path(__file__, 'resources', 'test_fixtures', 'kafka.json')
        )
        self.assertDataFrameEqual(expected_data, actual_data) 