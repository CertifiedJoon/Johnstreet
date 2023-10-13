from market_maker import MarketMaker
from jane_street import Exchange
import multiprocessing

# ~~~~~============== CONFIGURATION  ==============~~~~~
team_name = "JohnStreet"

# ~~~~~============== MAIN LOOP      ==============~~~~~


def market_maker_loop(exchange: Exchange):
    mm = MarketMaker(exchange, logging=True)

    while True:
        message = exchange.read_message()
        mm.listen(message)

        if message["type"] == "close":
            print("the round has ended")
            break


def main():
    args = parse_arguments()

    exchange = Exchange(args=args)

    mm_loop = multiprocessing.Process(target=market_maker_loop, args=(exchange,))

    # starting process 1
    mm_loop.start()

    # wait until process 1 is finished
    mm_loop.join()

    # both processes finished
    print("Done!")


def parse_arguments():
    pass


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert team_name != "PLACEHOLDer"
    main()
