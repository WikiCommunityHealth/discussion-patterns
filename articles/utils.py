import datetime
from typing import Any, Dict


def date_hook(json_dict: Dict[str, Any]) -> Dict[str, Any]:
    # this hook is also executed in nested json objects
    if "timestamp" in json_dict:
        try:
            json_dict["timestamp"] = datetime.datetime.strptime(
                str(json_dict["timestamp"]), "%Y-%m-%dT%H:%M:%SZ"
            )
        except Exception:
            print("Error parsing datetime in input file")
    return json_dict


def get_year_month_from_timestamp(timestamp: datetime.datetime) -> str:
    return f"{timestamp.year}-{timestamp.month}"


def get_username(record: Any) -> str:
    username: str = ""
    if "user" in record and "text" in record["user"]:
        username = record["user"]["text"]
    elif "user" in record and "ip" in record["user"]:
        username = record["user"]["ip"]
    else:
        username = "??unknown??"

    return username