import argparse
import asyncio
import logging
import redis
import sys
import signal
import sys
from pydoc import locate
import toml

from presso.core import util
from presso.core.eventqueue import EventQueue
from presso.core.util.constants import EVENT


def run(args):
    manifest = toml.load(args.manifest)
    # Setup logger
    log_format = '[%(levelname)s|%(module)s|%(asctime)s] %(message)s'
    log_level = getattr(logging, manifest['log']['level'].upper(), None)
    logging.basicConfig(
        filename=manifest['log']['file'], format=log_format, level=log_level)
    # Set portfolio type
    util.IS_REALTIME = manifest['realtime']
    # Set connection to redis
    util.REDIS_DB = redis.StrictRedis(
        host=manifest["redis"]["url"], port=manifest["redis"]["port"],
        db=manifest["redis"]["db"], decode_responses=True)

    base = manifest["config"]["base"]
    quote = manifest["config"]["quote"]

    # Load dataevents
    dataevents = {}
    for dataevent in manifest['dataevents']:
        module = locate(dataevent['module'])
        dataevent['config'].update({"base": base, "quote": quote})
        dataevents[dataevent['name']] = module(
            dataevent['data_path'],
            dataevent['history_file'],
            dataevent['config']
        )

    # Load connectors
    conn = manifest['connector']
    module = locate(conn['module'])(conn['name'], conn['config'])
    connector = module

    # Load statistics
    statistics = {}
    for stat in manifest['statistics']:
        module = locate(stat['module'])(stat['config'])
        statistics[stat['name']] = module

    # Load reports
    reports = {}
    for report in manifest['reports']:
        module = locate(report['module'])(report['config'])
        reports[report['name']] = module

    # Load portfolio
    portfolio = locate(manifest['module'])(
        connector, reports, statistics, manifest['config'])

    # Load alphas
    for alpha in manifest['alphas']:
        module = locate(alpha['module'])(
            alpha['name'],
            portfolio,
            [EVENT[e] for e in alpha['events']],
            alpha['config']
        )
        # Add all alpha's to the dataevent - the filter is done on dataevent abstract level
        for datevt in dataevents:
            dataevents[datevt].addAlpha(module)

    # Start portfolio
    loop = asyncio.get_event_loop()
    event_queue = EventQueue.getInstance()

    async def main():
        # Let DataEvents to run first
        await asyncio.sleep(2)
        await event_queue.consume()

    def stop():
        for dataevent in dataevents.values():
            dataevent.shutdown()
        asyncio.wait(asyncio.sleep(1))
        loop.stop()
    # Press ENTER to stop eventloop and run statistics
    loop.add_reader(sys.stdin, stop)

    def signal_handler(sig, frame):
            stop()
            sys.exit(0)
    # Or press CTRL+C to stop eventloop and run statistics
    signal.signal(signal.SIGINT, signal_handler)

    try:
        loop.run_until_complete(main())
    except RuntimeError as error:
        if str(error) == 'Event loop stopped before Future completed.':
            print('Event Loop Stopped')
            util.LOG.info('Event Loop Stopped')
        else:
            util.LOG.exception(error)
    portfolio.runStatistics()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    run_parser = subparsers.add_parser('run', help='run a portfolio')
    run_parser.add_argument('manifest', type=open, help='TOML manifest file')
    run_parser.set_defaults(func=run)

    create_parser = subparsers.add_parser(
        'create', help='TODO: create components')
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
