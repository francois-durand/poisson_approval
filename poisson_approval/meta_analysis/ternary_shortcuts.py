from poisson_approval.meta_analysis.ternary_plots import ternary_figure
from poisson_approval.utils.Util import candidates_to_probabilities, one_over_log_t_plus_two, d_candidate_value_to_array


def _order_and_label(t):
    r"""Order and label of a discrete type.

    Parameters
    ----------
    t : a type (cf. examples).

    Returns
    -------
    order : str
        The ranking or weak order.
    label : str
        The label to be used for the corner of the triangle.

    Examples
    --------
        >>> _order_and_label('abc')
        ('abc', '$r(abc)$')
        >>> _order_and_label('ab_c')
        ('abc', '$r(ab\\_c)$')
        >>> _order_and_label('a~b>c')
        ('a~b>c', '$r(a\\sim b>c)$')
        >>> _order_and_label(('abc', 0.5))
        ('abc', '$r(abc, u_b = 0.5)$')
        >>> _order_and_label(('abc', 0.5, 0.01))
        ('abc', '$r(abc, u_b = 0.5 ± 0.01)$')
    """
    if isinstance(t, tuple):
        if len(t) == 2:  # ProfileDiscrete
            return t[0], '$r(%s, u_%s = %s)$' % (t[0], t[0][1], t[1])
        else:  # ProfileNoisyDiscrete
            return t[0], '$r(%s, u_%s = %s ± %s)$' % (t[0], t[0][1], t[1], t[2])
    if len(t) == 3:
        return t, '$r(%s)$' % t
    if len(t) == 4:
        return t.replace('_', ''), ('$r(%s)$' % t).replace('_', '\\_')
    else:  # len(type) == 5
        return t, ('$r(%s)$' % t).replace('~', '\\sim ')


def ternary_plot_n_equilibria_ordinal(cls, right_type, top_type, left_type, scale, **kwargs):  # pragma: no cover
    """Shortcut: ternary plot for the number of ordinal equilibria.

    Parameters
    ----------
    cls : class
        ProfileOrdinal, ProfileTwelve or ProfileDiscrete.
    right_type, top_type, left_type : type
        A type that is suitable for the kind of profile used.
    scale : Number
        Scale of the plot (resolution).
    kwargs
        Other keyword arguments are passed to the function `heatmap_intensity`.
    """
    def n_equilibria_ordinal(right, top, left):
        profile = cls({right_type: right, top_type: top, left_type: left})
        return len(profile.analyzed_strategies_ordinal.equilibria)

    figure, tax = ternary_figure(scale=scale)
    order_r, label_r = _order_and_label(right_type)
    order_t, label_t = _order_and_label(top_type)
    order_l, label_l = _order_and_label(left_type)
    tax.heatmap_intensity(n_equilibria_ordinal,
                          right_label=label_r,
                          top_label=label_t,
                          left_label=label_l, **kwargs)
    tax.annotate_condorcet(right_order=order_r, top_order=order_t, left_order=order_l)
    tax.set_title_padded('Number of ordinal equilibria')
    return figure, tax


def ternary_plot_winners_at_equilibrium_ordinal(cls, right_type, top_type, left_type, scale,
                                                **kwargs):  # pragma: no cover
    """Shortcut: ternary plot for the winners at equilibrium.

    Parameters
    ----------
    cls : class
        ProfileOrdinal, ProfileTwelve or ProfileDiscrete.
    right_type, top_type, left_type : type
        A type that is suitable for the kind of profile used.
    scale : Number
        Scale of the plot (resolution).
    kwargs
        Other keyword arguments are passed to the function `heatmap_candidates`.
    """

    def winners_at_equilibrium(right, top, left):
        profile = cls({right_type: right, top_type: top, left_type: left})
        return candidates_to_probabilities(profile.analyzed_strategies_ordinal.winners_at_equilibrium)

    figure, tax = ternary_figure(scale=scale)
    order_r, label_r = _order_and_label(right_type)
    order_t, label_t = _order_and_label(top_type)
    order_l, label_l = _order_and_label(left_type)
    tax.heatmap_candidates(winners_at_equilibrium,
                           right_label=label_r,
                           top_label=label_t,
                           left_label=label_l,
                           legend_style='color_patches',
                           legend_title='Winners',
                           **kwargs)
    tax.annotate_condorcet(right_order=order_r, top_order=order_t, left_order=order_l)
    return figure, tax


def ternary_plot_winning_frequencies(cls, right_type, top_type, left_type, scale, n_max_episodes,
                                     **kwargs):  # pragma: no cover
    """Shortcut: ternary plot for the winning frequencies in fictitious play.

    Parameters
    ----------
    cls : class
        ProfileOrdinal, ProfileTwelve or ProfileDiscrete.
    right_type, top_type, left_type : type
        A type that is suitable for the kind of profile used.
    scale : Number
        Scale of the plot (resolution).
    n_max_episodes : int
        Maximum number of episodes for the fictitious play.
    kwargs
        Other keyword arguments are passed to the function `heatmap_candidates`.

    Notes
    -----
    The fictitious play starts from sincere voting and uses update ratios of :func:`one_over_log_t_plus_two`.
    """
    def winning_frequencies(right, top, left):
        profile = cls({right_type: right, top_type: top, left_type: left})
        results = profile.fictitious_play(init='sincere', n_max_episodes=n_max_episodes,
                                          perception_update_ratio=one_over_log_t_plus_two,
                                          ballot_update_ratio=one_over_log_t_plus_two,
                                          winning_frequency_update_ratio=one_over_log_t_plus_two)
        return d_candidate_value_to_array(results['d_candidate_winning_frequency'])

    figure, tax = ternary_figure(scale=scale)
    order_r, label_r = _order_and_label(right_type)
    order_t, label_t = _order_and_label(top_type)
    order_l, label_l = _order_and_label(left_type)
    tax.heatmap_candidates(winning_frequencies,
                           right_label=label_r,
                           top_label=label_t,
                           left_label=label_l,
                           legend_style='palette',
                           legend_title='Winners',
                           **kwargs)
    tax.annotate_condorcet(right_order=order_r, top_order=order_t, left_order=order_l)
    return figure, tax
