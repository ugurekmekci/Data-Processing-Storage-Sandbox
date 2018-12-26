def consume():
    """Consumes events from partitionlag topic"""
    LOGGER.setLevel(APPLICATION_LOGGING_LEVEL)
    LOGGER.info("Starting lagreader")
    LOGGER.debug('Set Logging Level to ' + APPLICATION_LOGGING_LEVEL)
    LOGGER.debug('Listening on Kafka at: ' + KAFKA_URI)

    consumer = KafkaConsumer(group_id='lagConsumerGroup', bootstrap_servers=KAFKA_URI)
    consumer.subscribe(topics=['partitionlag'])
    partition_lag_dict = PartitionLagDict()

    last_writetime = datetime.datetime.now()

    for msg in consumer:
        jsonstring = msg.value
        partitionlag = PartitionLag.from_json(jsonstring)
        partition_lag_dict.addPartitionLag(partitionlag)
        LOGGER.debug(str(partitionlag.eventdate) + "  Received partitionlag event: " \
            + "partition: " + str(partitionlag.partition) \
            + " lag: " + str(partitionlag.lag))
        LOGGER.debug(str(datetime.datetime.now()) + ' Received partitionlag: ' \
            + partition_lag_dict.toString())

        last_writetime = _notifylag_conditionally(partition_lag_dict, last_writetime) 