from market_maker import MarketMaker
from jane_street import ExchangeConnection as Exchange
from jane_street import parse_arguments
from supporter import Supporter
from arbitrage import Arbitrage
import multiprocessing
from bond_buyer import BondBuyer
from min_buyer import MinBuyer
from trend_follower import TrendFollower

# ~~~~~============== CONFIGURATION  ==============~~~~~
team_name = "JohnStreet"

# ~~~~~============== MAIN LOOP      ==============~~~~~


def market_maker_loop(exchange: Exchange, delta):
    mm = MarketMaker(exchange, delta)

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


def arbitrage_loop(exchange: Exchange):
    arb = Arbitrage(exchange)

    while True:
        message = exchange.read_message()
        arb.listen(message)

        if message["type"] == "close":
            print("the round has ended, market maker stop.")
            break


def min_buyer_loop(exchange: Exchange):
    mb = MinBuyer(exchange)

    while True:
        message = exchange.read_message()
        mb.listen(message)

        if message["type"] == "close":
            print("the round has ended, market maker stop.")
            break


def bond_buyer_loop(exchange: Exchange, delta):
    bb = BondBuyer(exchange, delta)

    while True:
        message = exchange.read_message()
        bb.listen(message)

        if message["type"] == "close":
            print("the round has ended, market maker stop.")
            break


def trend_follower_loop(exchange):
    tf = TrendFollower(exchange)

    while True:
        message = exchange.read_message()
        tf.listen(message)

        if message["type"] == "close":
            break


def main():
    args = parse_arguments()

    exchange = Exchange(args=args)

    mm_thread_cnt = 5
    mm_loops = []

    for i in range(0, mm_thread_cnt):
        mm_loops.append(
            multiprocessing.Process(target=market_maker_loop, args=(exchange, 1))
        )

    ml_loop = multiprocessing.Process(target=market_logger_loop, args=(exchange,))
    arb_loop = multiprocessing.Process(target=arbitrage_loop, args=(exchange,))
    bond_loop = multiprocessing.Process(
        target=bond_buyer_loop,
        args=(
            exchange,
            1,
        ),
    )
    min_loop = multiprocessing.Process(target=min_buyer_loop, args=(exchange,))
    tf_loop = multiprocessing.Process(target=trend_follower_loop, args=(exchange,))

    # starting process 1
    for i in range(mm_thread_cnt):
        mm_loops[i].start()
    ml_loop.start()
    arb_loop.start()
    bond_loop.start()
    min_loop.start()
    tf_loop.start()

    # wait until process 1 is finished
    for i in range(mm_thread_cnt):
        mm_loops[i].join()
    ml_loop.join()
    arb_loop.join()
    bond_loop.join()
    min_loop.join()
    tf_loop.join()
    # both processes finished
    print("Round Finished!")


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (
        team_name != "REPLAC" + "EME"
    ), "Please put your team name in the variable [team_name]."

    main()
