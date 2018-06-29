#!/usr/bin/env python

import http_main


def main():
    s = http_main.TCP_HTTP("0.0.0.0", 80)


if __name__ == "__main__":
    main()
