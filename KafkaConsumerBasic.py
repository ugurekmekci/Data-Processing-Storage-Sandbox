def run_consumer(self):
        '''core consumer code'''
        bootstrap_server = self.config.get('consumer', 'kafka_bootstrap')
        consumer_group = self.config.get('consumer', 'kafka_consumer_group')

        offset_reset = self.config.get(
            'consumer', 'kafka_auto_offset_reset')
        self.consumer = KafkaConsumer(bootstrap_servers=bootstrap_server,\
                                        consumer_timeout_ms=60000,\
                                        group_id=consumer_group,\
                                        auto_offset_reset=offset_reset)
        topic_whitelist = self.config.get(
            'consumer', 'topic_whitelist')
        self.logger.info("Topic list is " + topic_whitelist)

        self.consumer.subscribe(topic_whitelist.split(","), None, self)

        self.logger.info("Consumer " + self.consumer_id +
                         " starting.... " + str(self.consumer.assignment()))

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        while not self.shutting_down:
            for message in self.consumer:

                consumer_message = MessageInfo(message.topic, message.partition, message.key,\
                                               message.value, message.offset)
                self.process_message(consumer_message)
                if self.shutting_down:
                    break
            self.check_for_rotation()

        for part in self.partitions:
            self.partitions[part].writer.close()

        self.logger.info("Graceful shutdown of consumer " +
                         str(self.consumer_id) + " successful") 