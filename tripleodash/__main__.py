from tripleodash import clients
from tripleodash import dash


def main():

    UPDATE_INTERVAL = 2

    try:
        dash.Dashboard(clients.ClientManager(), UPDATE_INTERVAL).run()
    except KeyboardInterrupt:
        print("Exited at users request.")

if __name__ == '__main__':
    main()
