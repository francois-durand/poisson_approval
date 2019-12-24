class AnalyzedStrategies:
    """A container with all the strategies analyzed for a given profile.

    Parameters
    ----------
    equilibria : list of :class:`Strategy`
        List of the strategies where equilibrium is sure.
    utility_dependent : list of :class:`Strategy`
        List of the strategies where the equilibrium depends on the exact utilities.
    inconclusive : list of :class:`Strategy`
        List of the strategies where we are not able to decide whether it is an equilibrium or not.
    non_equilibria : list of :class:`Strategy`
        List of the strategies where the program certifies there is no equilibrium.
    """

    def __init__(self, equilibria: list, utility_dependent: list, inconclusive: list, non_equilibria: list):
        self.equilibria = equilibria
        self.utility_dependent = utility_dependent
        self.inconclusive = inconclusive
        self.non_equilibria = non_equilibria

    def __repr__(self):
        # Equilibria (print even if there is none).
        if len(self.equilibria) == 1:
            s = 'Equilibrium:'
        else:
            s = 'Equilibria:'
        if not self.equilibria:
            s += '\nNone'
        for sigma_eq in self.equilibria:
            s += '\n' + str(sigma_eq) + ' (' + str(sigma_eq.tau.focus) + ')'
        # Print utility-dependent strategies only if there are some (this restriction is useful for ProfileTwelve).
        if len(self.utility_dependent) == 1:
            s += '\n\nUtility-dependent equilibrium:'
        elif len(self.utility_dependent) > 1:
            s += '\n\nUtility-dependent equilibria:'
        for sigma_eq in self.utility_dependent:
            s += '\n' + str(sigma_eq) + ' (' + str(sigma_eq.tau.focus) + ')'
        # Non-equilibria (print even if there is none).
        if len(self.non_equilibria) == 1:
            s += '\n\nNon-equilibrium:'
        else:
            s += '\n\nNon-equilibria:'
        if not self.non_equilibria:
            s += '\nNone'
        for sigma_eq in self.non_equilibria:
            s += '\n' + str(sigma_eq) + ' (' + str(sigma_eq.tau.focus) + ')'
        # Print inconclusive strategies only if there are some (which should not happen).
        if len(self.inconclusive) == 1:
            s += '\n\nInconclusive strategy profile:'
        elif len(self.inconclusive) > 1:
            s += '\n\nInconclusive strategy profiles:'
        for sigma_eq in self.inconclusive:
            s += '\n' + str(sigma_eq)
        return s
