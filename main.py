from market_maker import MarketMaker
from jane_street import Exchange
from supporter import Supporter
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
            print("the round has ended, market maker stop.")
            break


def market_logger_loop(exchange: Exchange):
    sup = Supporter(exchange, "history.csv")
    while True:
        message = exchange.read_message()
        sup.listen(message)

        if message["type"] == "close":
            print("the round has finished. logging stop.")


def main():
    args = parse_arguments()

    exchange = Exchange(args=args)

    mm_loop = multiprocessing.Process(target=market_maker_loop, args=(exchange,))
    ml_loop = multiprocessing.Process(target=market_logger_loop, args=(exchange,))

    # starting process 1
    mm_loop.start()
    ml_loop.start()

    # wait until process 1 is finished
    mm_loop.join()
    ml_loop.join()

    # both processes finished
    print("Round Finished!")


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (
        team_name != "REPLAC" + "EME"
    ), "Please put your team name in the variable [team_name]."

    main()
