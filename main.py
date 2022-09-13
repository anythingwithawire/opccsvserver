#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Gareth Smith"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os

#from logzero import logger
import logging
import asyncio
import sys

sys.path.insert(0, "..")

from asyncua import ua, Server
from asyncua.common.methods import uamethod


@uamethod
def func(parent, value):
    return value * 2


async def main(args):
    """ Main entry point of the app """
    #logger.info("hello world")
    #logger.info(args)

    #_logger = logging.getLogger('asyncua')
    # setup our server
    print("\nOPC CSV SERVER - serve up OPC based on contents of csv file\n")
    print('run sudo netstat -nutlp | grep "4840" to find pid of port holder 4840\n\n')

    server = Server()
    await server.init()
    server.set_endpoint(f'opc.tcp://{args.ipAddress}:{args.port}/StateSim/server/')

    # setup our own namespace, not really necessary but should as spec
    uri = 'http://gsim.opc.io'
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root

    myobj = await server.nodes.objects.add_object(idx, 'MyObject')
    # myvar = await myobj.add_variable(idx, 'MyVariable', 6.7)

    # Set MyVariable to be writable by clients
    # await myvar.set_writable()
    #await server.nodes.objects.add_method(ua.NodeId('ServerMethod', 2), ua.QualifiedName('ServerMethod', 2), func,
                                          #[ua.VariantType.Int64], [ua.VariantType.Int64])
    #_logger.info('Starting server!')

    async with server:
        while True:
            await asyncio.sleep(1)
            # new_val = await myvar.get_value() + 0.1
            # _logger.info('Set value of %s to %.1f', myvar, new_val)
            # await myvar.write_value(new_val)
            # await myvar2.write_value(789)
            if args.multi:
                if os.path.isfile(args.filename):
                    m = open(args.filename)
                    r = m.readlines()
                    m.close()
                else:
                    print(f'\nError opening {args.filename}\n')
                    sys.exit(-1)
            else:
                r = []
                r.append(str(args.filename))

            for ff in r:
                if os.path.isfile(ff.strip()):
                    f = open(ff.strip())
                    myvars = f.readlines()
                    for v in myvars:
                        x = v.split(',')
                        if len(x) >= 2:
                            vName = x[0].strip()
                            vValue = x[1].strip()
                            vNameObj = vName + 'Ob'
                            try:
                                await myWriteValue(locals()[vNameObj], idx, vName, vValue)
                                #_logger.info('Set value of %s to %s', vName, str(vValue))
                            except:
                                locals()[vNameObj] = await myMakeObject(myobj, idx, vName, vValue)
                                #_logger.info('Set value of %s to %s', vName, str(vValue))
                                # await mySetWriteable(locals()[vNameObj], idx, vName, vValue)
                    f.close()

async def aaa(myobj, idx, vName, vValue):
    return await myobj.add_variable(idx, f'{vName}', vValue)


async def myMakeObject(myobj, idx, vName, vValue):
    return await aaa(myobj, idx, vName, vValue)


async def bbb(myobj, idx, vName, vValue):
    return await myobj.write_value(vValue)


async def myWriteValue(myobj, idx, vName, vValue):
    await bbb(myobj, idx, vName, vValue)


async def ccc(myobj, idx, vName, vValue):
    return await myobj.set_writeable()


async def mySetWriteable(myobj, idx, vName, vValue):
    await ccc(myobj, idx, vName, vValue)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("ipAddress", help="Required - ip address")

    # Required positional argument
    parser.add_argument("port", help="Required - port (4840)")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-f", "--file", action="store", dest="filename")

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-m", "--multiple", action="store_true", dest="multi")

    db = False
    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-d", "--debug", action="store_true", dest="db")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()

    asyncio.run(main(args), debug=db)
