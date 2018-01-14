from rec_parse import parse_file
import argparse
import logging
import time
try:
    from numpy.random import gamma
except ImportError:
    logging.warn("numpy could not be imported. random delays not supported.")


def _init_args():
    parser = argparse.ArgumentParser(
            description="Run a macro.")
    parser.add_argument(
        'filename',
        metavar='<path/to/macro>',
        type=str,
        help="Path to macro file."
    )
    parser.add_argument(
        '--duration',
        dest='dur',
        metavar='<max duration>',
        type=float,
        help="Specify maximum runtime duration."
    )
    parser.add_argument(
        '--limit',
        dest='lim',
        metavar='<instruction limit>',
        type=int,
        help="Specify maximum instruction execution count."
    )
    parser.add_argument(
        '--r_delay',
        dest='delay',
        metavar='<random delay>',
        type=float,
        help="Specify random delay between instructions."
    )
    args = parser.parse_args()
    return args


def execute_commands(commands, limit=0, duration=0, delay=0):
    """Create an execution environment and run the command list.
    """
    begin_ts = time.time()
    ip = [0]  # instruction pointer
    count = 0
    while ip[0] >= 0:
        count += 1
        # halting conditions
        if limit and count > limit:
            break
        if duration and time.time() - begin_ts > duration:
            break
        if delay:
            t_delay = min(delay * 3, gamma(3, delay/3))
            time.sleep(t_delay)
            logging.debug("Random delay: {}s".format(t_delay))
        commands[ip[0]].execute(ip)
        # advance instruction pointer
        ip[0] += 1


if __name__ == "__main__":
    ARGS = _init_args()
    logging.basicConfig(
        level='INFO',
        format="%(levelname)s - %(message)s")
    MACRO_FILE = ARGS.filename
    commands = list(parse_file(MACRO_FILE))
    logging.debug("Commands: {}".format(', '.join(str(c) for c in commands)))
    execute_commands(
        commands,
        limit=ARGS.lim,
        duration=ARGS.dur,
        delay=ARGS.delay)
