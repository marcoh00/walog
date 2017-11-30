# -*- coding: utf-8 -*-

import datetime
import json
import logging
import os

from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity


log = logging.getLogger(__name__)


class LogLayer(YowInterfaceLayer):

    PROP_TARGET = "de.wuthoehle.walog.target"

    @ProtocolEntityCallback("message")
    def on_message(self, message: MessageProtocolEntity):
        receipt = OutgoingReceiptProtocolEntity(
            messageIds=message.getId(),
            to=message.getFrom(),
            read=True,
            participant=message.getParticipant()
        )

        today = datetime.datetime.now().isocalendar()

        target_dir = self.getProp(self.__class__.PROP_TARGET)
        target_file = f'{today[0]}-{today[1]}-{today[2]}.json'
        try:
            nice_message = self._jsonify(message)
            if nice_message:
                with open(os.path.join(target_dir, target_file), 'a', encoding='utf-8') as file:
                    file.write(nice_message)
                    file.write(os.linesep)
            else:
                log.info(f'Did not write non-text message with ID {message.getId()}')
        except Exception as e:
            log.warning(f'Unable to write message: {str(e)}')

        self.toLower(receipt)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    @staticmethod
    def _jsonify(message):
        def add_if_not_none(dictionary: dict, key: str, value):
            if value is not None:
                dictionary[key] = value
        if message.getType() == 'text':
            nice_message = dict()
            add_if_not_none(nice_message, 'id', message.getId())
            add_if_not_none(nice_message, 'body', message.getBody())
            add_if_not_none(nice_message, 'from', message.getFrom())
            add_if_not_none(nice_message, 'to', message.getTo())
            add_if_not_none(nice_message, 'participant', message.getParticipant())
            add_if_not_none(nice_message, 'author', message.getAuthor())

            iso_timestamp = None
            try:
                iso_timestamp = datetime.datetime.fromtimestamp(message.getTimestamp()).isoformat()
            except (TypeError, OverflowError) as e:
                log.warning(f'Malformed timestamp: {str(e)}')

            add_if_not_none(nice_message, 'timestamp', iso_timestamp)
            return json.dumps(nice_message)
