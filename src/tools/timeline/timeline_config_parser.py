import json
import humps
from typing import List
from core.enums import CoordinateSystem, NodeCalc
from tools.timeline.timeline_config import AspectsConfig, TimelineConfig
from events.astro_event import *


def parse_json_to_timeline_configs(json_str: str) -> List[TimelineConfig]:
    try:
        # Convert JSON string to Python dictionary
        data = json.loads(json_str)

        # Convert keys from camelCase to snake_case
        snake_case_data = humps.decamelize(data)

        configs = []
        for config in snake_case_data["configurations"]:
            config["start_date"] = _parse_utc_date(config["start_date"])
            config["end_date"] = _parse_utc_date(config["end_date"])
            # Convert string names in events to class types
            event_classes = [globals().get(event) for event in config["events"]]

            if None in event_classes:
                missing_events = [
                    event
                    for event, cls in zip(config["events"], event_classes)
                    if cls is None
                ]
                raise ValueError(f"Unknown events: {', '.join(missing_events)}")

            config["events"] = event_classes
            config["coordinate_system"] = CoordinateSystem.from_string(
                config["coordinate_system"]
            )
            config["node_calc"] = NodeCalc.from_string(config["node_calc"])

            if "aspects" in config and config["aspects"] is not None:
                aspects = AspectsConfig(**config["aspects"])
                config["aspects"] = aspects
            else:
                config["aspects"] = None

            configs.append(TimelineConfig(**config))
        return configs
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}")
    except KeyError as e:
        raise ValueError(f"Missing required configuration field: {e}")
    except ValueError as e:
        raise ValueError(f"Invalid configuration value: {e}")


def _parse_utc_date(date_str: str) -> datetime:
    try:
        # If the time part is not included, assume midnight
        if "T" not in date_str:
            date_str += "T00:00:00Z"
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")
