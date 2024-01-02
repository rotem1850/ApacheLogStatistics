from ApacheLogParser import ApacheLogParser


def main():
    #pass # print(get_country("8.8.8.8"))
    apache_log = ApacheLogParser.parse("apache_log.txt")
    #print(apache_log.group_by("country"))
    print("Statistics:")
    apache_log.print_statistics("country")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    apache_log.print_statistics("os")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    apache_log.print_statistics("browser")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
