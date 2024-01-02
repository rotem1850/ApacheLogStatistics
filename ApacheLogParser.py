import re

from ApacheLog import ApacheLine, ApacheLog

_apache_log_line_parts_format = [
    r'(?P<host>\S+)',
    r'\S+',
    r'(?P<user>\S+)',
    r'\[(?P<time>.+)\]',
    r'"(?P<request>.*)"',
    r'(?P<status>[0-9]+)',
    r'(?P<size>\S+)',  # Notice: can be '-'
    r'"(?P<referrer>.*)"',
    r'"(?P<agent>.*)"',
]

_apache_log_line_format = re.compile(r'\s+'.join(_apache_log_line_parts_format)+r'\s*\Z')


class ApacheLineParser:
    @staticmethod
    def parse(apache_raw_line: str) -> ApacheLine:
        line_match = _apache_log_line_format.match(apache_raw_line)
        if not line_match:
            raise ValueError("Line is not a valid apache log line")

        return ApacheLine(*line_match.groups())


class ApacheLogParser:
    @staticmethod
    def parse(apache_log_file_path: str) -> ApacheLog:
        parsed_lines = []
        with open(apache_log_file_path, 'r') as apache_log_file:
            for apache_line in apache_log_file:
                try:
                    parsed_line = ApacheLineParser.parse(apache_line)
                    parsed_lines.append(parsed_line)
                except ValueError:
                    pass

            return ApacheLog(parsed_lines)

