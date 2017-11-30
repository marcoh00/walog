#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import sys

from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.stacks import YowStackBuilder
from walog.waloglayer import LogLayer

log = logging.getLogger(__name__)


def setup_stack(credentials, target_dir):
    stack_builder = YowStackBuilder()
    stack = stack_builder.pushDefaultLayers(axolotl=True).push(LogLayer).build()
    stack.setCredentials(credentials)
    stack.setProp(LogLayer.PROP_TARGET, target_dir)
    return stack


def run(stack):
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    stack.loop()


def main():
    logging.basicConfig(level=logging.INFO)
    argparser = argparse.ArgumentParser(description='WhatsApp conversation logger')
    argparser.add_argument('--phone', type=str, required=True, help='Registered WhatsApp Phone Number')
    argparser.add_argument('--passkey', type=str, required=True, help='Passkey belonging to given number')
    argparser.add_argument('--output', '-o', type=str, default='.', help='Output directory to write messages to')
    argparser.add_argument('--retry', action='store_true', help='Try again on errors')
    args = argparser.parse_args()

    if args.retry:
        while True:
            try:
                stack = setup_stack((args.phone, args.passkey), args.output)
                run(stack)
                log.info('Restarting walog stack')
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception as e:
                log.error(f'An error occured: {str(e)}')
    else:
        stack = setup_stack((args.phone, args.passkey), args.output)
        run(stack)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
