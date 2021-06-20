from src.transport.cache_server import start_server, CacheService


def _wait_enter(server):
    input('Press enter to exit')
    server.stop(grace=None).wait()
    exit(0)


def main():
    service = CacheService(max_size=5, cleaning_frequency_s=15)
    server = start_server(service, port=8080)
    return server


if __name__ == '__main__':
    started_server = main()
    _wait_enter(started_server)
