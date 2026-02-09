from smartmeter.collector.args import arguments

def main():
    parsed_args = arguments().parse_args()

    print("SmartMeter Collector")
