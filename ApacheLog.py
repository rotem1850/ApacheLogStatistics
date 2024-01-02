import dataclasses
from typing import List, Any, Dict
import user_agents

import geoip2.database
from geoip2.errors import AddressNotFoundError


@dataclasses.dataclass
class ApacheLine:
    host: str
    user: str
    time: str
    request: str
    status: str
    size: str
    referrer: str
    agent: str

    def _get_user_agent(self):
        return user_agents.parse(self.agent)

    @property
    def country(self):
        with geoip2.database.Reader('GeoLite2-Country.mmdb') as reader:
            try:
                return reader.country(self.host).country.name
            except AddressNotFoundError:
                return "Unknown"

    @property
    def os(self):
        return self._get_user_agent().os.family

    @property
    def browser(self):
        return self._get_user_agent().browser.family


class ApacheLog:
    def __init__(self, lines: List[ApacheLine]):
        self._lines = lines

    def _append(self, line: ApacheLine):
        self._lines.append(line)

    def size(self) -> int:
        return len(self._lines)

    def group_by(self, field_name: str) -> Dict[Any, 'ApacheLog']:
        groups = dict()
        if not self._lines:
            return groups

        if not hasattr(self._lines[0], field_name):
            raise ValueError(f"Field {field_name} doesnt exists")

        for line in self._lines:
            field_value = getattr(line, field_name)
            if field_value not in groups:
                groups[field_value] = ApacheLog([])

            groups[field_value]._append(line)

        return groups

    def print_statistics(self, field_name: str) -> None:
        groups = self.group_by(field_name)
        statistics = dict()
        print(f"{field_name}:")
        for group_name, apache_log in groups.items():
            statistics[group_name] = apache_log.size() / self.size()

        ordered_statistics = dict(sorted(statistics.items(), key=lambda item: item[1]))
        for group_name, percentage in reversed(ordered_statistics.items()):
            print(f"{group_name}: {percentage*100:.2f}%")
