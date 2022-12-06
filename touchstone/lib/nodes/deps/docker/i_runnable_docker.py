from abc import ABC

from touchstone.lib.health_checks.i_health_checkable import IHealthCheckable
from touchstone.lib.nodes.i_networkable import INetworkable
from touchstone.lib.nodes.deps.behaviors.i_behavior import IBehavior
from touchstone.lib.nodes.deps.i_runnable import IRunnable


class IRunnableDocker(ABC, IRunnable, INetworkable, IHealthCheckable):
    def get_behavior(self) -> IBehavior:
        pass
