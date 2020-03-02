from poisson_approval.utils.ComputationEngineExact import ComputationEngineExact
from poisson_approval.utils.ComputationEngineApproximate import ComputationEngineApproximate


def computation_engine(exact):
    """Choose the computation engine.

    Parameters
    ----------
    exact : bool

    Returns
    -------
    ComputationEngine
        :class:`ComputationEngineExact` if `exact` is True, :class:`ComputationEngineApproximate` otherwise.
    """
    return ComputationEngineExact if exact else ComputationEngineApproximate
