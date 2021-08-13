from time import sleep
import PrintTags as pt
import argparse
from os import system
from wakeonlan import send_magic_packet


def _do_bringup_countdown(num_seconds: int) -> None:
    count: int = 0
    while count < num_seconds:
        pt.info(f'Starting bring-up in {num_seconds - count} seconds.', end='\r')
        sleep(1.0)
        count += 1


def _send_packet(mac_address: str) -> None:
    send_magic_packet(mac_address)
    pt.info(f'Packet sent to: {mac_address}')


def _shutdown() -> None:
    sleep(5.0)
    system('systemctl poweroff')
    pt.warn('Shutdown started')


def main(mac_address: str, delay: int, shutdown: bool) -> None:
    _do_bringup_countdown(delay)
    _send_packet(mac_address)
    if shutdown:
        _shutdown()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sends a Wake-on-LAN packet to bring up the network.')
    parser.add_argument('mac_address', nargs=1, type=str,
                        help='The MAC address the packet should be sent to.')
    parser.add_argument('-d', '--delay', metavar='Delay', type=int,
                        help='The time in seconds before the packet is sent.')
    parser.add_argument('-s', '--shutdown', action="store_true",
                        help='Shutdown the device after packet is sent.')
    args = parser.parse_args()
    main(args.mac_address, args.delay, args.shutdown)
