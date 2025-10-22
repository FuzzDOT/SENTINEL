from enum import Enum


class ModelStage(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"
