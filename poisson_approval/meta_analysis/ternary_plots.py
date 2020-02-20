import numpy as np
import ternary
from collections import Counter
from ternary.helpers import simplex_iterator
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from poisson_approval.meta_analysis.ternary_condorcet import draw_condorcet_zones
from poisson_approval.utils.Util import candidates_to_probabilities, d_candidate_value_to_array, one_over_log_t_plus_two


def _generate_heatmap_data(f, scale, color_a, color_b, color_c):
    """Generate RGBA data for a ``simplex to 3D'' heatmap plot.

    Parameters
    ----------
    f : callable
        The function to plot. Input: coordinates `right`, `top`, `left` in the simplex, i.e. that sum to 1. Output: a
        list of 3 numbers between 0 and 1.
    scale
        The scale of the ternary plot.
    color_a
        The RGB code representing candidate `a` (the first output). Each element of the tuple must be in [0, 1].
    color_b
        The RGB code representing candidate `b` (the second output). Each element of the tuple must be in [0, 1].
    color_c
        The RGB code representing candidate `c` (the third output). Each element of the tuple must be in [0, 1].

    Returns
    -------
    dict
        Key: a point of the integer simplex defined by `scale`. Value: the RGBA code of the color representing the
        output of `f`.

    Examples
    --------
        >>> def f(right, top, left):
        ...     return [right, 0, 0]
        >>> _generate_heatmap_data(f, scale=2, color_a=(1., 0., 0.), color_b=(0., 1., 0.), color_c=(0., 0., 1.))
        {(0, 0, 2): (0.0, 0.0, 0.0, 1.0), (0, 1, 1): (0.0, 0.0, 0.0, 1.0), (0, 2, 0): (0.0, 0.0, 0.0, 1.0), \
(1, 0, 1): (0.5, 0.0, 0.0, 1.0), (1, 1, 0): (0.5, 0.0, 0.0, 1.0), (2, 0, 0): (1.0, 0.0, 0.0, 1.0)}
    """
    d = dict()
    for (right, top, left) in simplex_iterator(scale):
        values = f(right / scale, top / scale, left / scale)
        color = (values[0] * np.array(color_a)
                 + values[1] * np.array(color_b)
                 + values[2] * np.array(color_c))
        d[(right, top, left)] = (float(color[0]), float(color[1]), float(color[2]), 1.)
    return d


class TernaryAxesSubplotPoisson(ternary.TernaryAxesSubplot):  # pragma: no cover
    """Subclass of `TernaryAxesSubplot`, defined in the package python-ternary.

    This class implements some additional methods for Poisson Approval. For some examples, cf. the tutorial
    in section "Meta-Analysis".
    """

    def __init__(self, scale=None, size_inches='auto', **kwargs):
        self.size_inches = size_inches
        super().__init__(scale=scale, **kwargs)

    def _scaled_number(self, x):
        """Scale a number.

        Parameters
        ----------
        x : Number
            A coordinate in [0, 1].

        Returns
        -------
        Number
            A coordinate in [0, ``self.scale``].
        """
        return x * self.get_scale()

    def _scaled_position(self, p):
        """Scale a position.

        Parameters
        ----------
        p : tuple
            Three coordinates in [0, 1] (typically, that sum to 1).

        Returns
        -------
        Tuple
            Three coordinates in [0, ``self.scale``].
        """
        return [self._scaled_number(x) for x in p]

    def set_title_padded(self, title, **kwargs):
        """Adaptation of `set_title`.

        Adjust the position of the title to avoid collision with the label of the top corner.

        Parameters
        ----------
        Cf. `set_title` in python-ternary.
        """
        size_inches = plt.gcf().get_size_inches()
        pad = 6 * size_inches[1]
        pad += kwargs.pop('pad', 0)
        self.set_title(title, pad=pad, **kwargs)

    def annotate_simplex(self, text, position, horizontalalignment='center', verticalalignment='center', **kwargs):
        """Adaptation of `annotate`.

        * The input position is in the simplex (instead of the scaled simplex), i.e. coordinates are in [0, 1].
        * The default horizontal and vertical alignments are centered.

        Parameters
        ----------
        Cf. `annotate` in python-ternary.
        """
        self.annotate(text, position=self._scaled_position(position),
                      horizontalalignment=horizontalalignment, verticalalignment=verticalalignment, **kwargs)

    def gridlines_simplex(self, multiple=None, horizontal_kwargs=None, left_kwargs=None,
                          right_kwargs=None, **kwargs):
        """Adaptation of `gridlines`.

        * The argument `multiple` is a grid step in [0, 1] (instead of [0, scale]).

        Parameters
        ----------
        Cf. `gridlines` in python-ternary.
        """
        self.gridlines(multiple=self._scaled_number(multiple), horizontal_kwargs=horizontal_kwargs,
                       left_kwargs=left_kwargs, right_kwargs=right_kwargs, **kwargs)

    def line_simplex(self, p1, p2, color='black', **kwargs):
        """Adaptation of `line`.

        * The input positions are in the simplex (instead of the scaled simplex), i.e. coordinates are in [0, 1].

        Parameters
        ----------
        Cf. `line` in python-ternary.
        """
        self.line(self._scaled_position(p1), self._scaled_position(p2), color=color, **kwargs)

    def horizontal_line_simplex(self, i, color='black', **kwargs):
        """Adaptation of `horizontal_line`.

        * The argument `i` is in [0, 1] (instead of [0, scale]).

        Parameters
        ----------
        Cf. `horizontal_line` in python-ternary.
        """
        self.horizontal_line(self._scaled_number(i), color=color, **kwargs)

    def left_parallel_line_simplex(self, i, color='black', **kwargs):
        """Adaptation of `left_parallel_line`.

        * The argument `i` is in [0, 1] (instead of [0, scale]).

        Parameters
        ----------
        Cf. `left_parallel_line` in python-ternary.
        """
        self.left_parallel_line(self._scaled_number(i), color=color, **kwargs)

    def right_parallel_line_simplex(self, i, color='black', **kwargs):
        """Adaptation of `right_parallel_line`.

        * The argument `i` is in [0, 1] (instead of [0, scale]).

        Parameters
        ----------
        Cf. `right_parallel_line` in python-ternary.
        """
        self.right_parallel_line(self._scaled_number(i), color=color, **kwargs)

    def heatmap_intensity(self, func, right_label, top_label, left_label,
                          style='hexagonal', cmap='plasma', **kwargs):
        """Adaptation of `heatmapf`.

        Parameters
        ----------
        func : callable
            The function to plot. Input: coordinates `right`, `top`, `left` in the simplex, i.e. that sum to 1.
            Output: a number.
        right_label : str
            Label of the right corner.
        top_label : str
            Label of the top corner.
        left_label : str
            Label of the left corner.
        style : str
            Contrarily to default settings in python-ternary, the default is ``'hexagonal'``.
        cmap : str
            Colormap. Contrarily to default settings in python-ternary, the default is ``'plasma'``.
        kwargs
            All other keywords arguments are passed to method ``heatmapf`` of python-ternary.
        """
        default_pad = 0.15
        if 'cb_kwargs' not in kwargs.keys():
            kwargs['cb_kwargs'] = {'pad': default_pad}
        elif 'pad' not in kwargs['cb_kwargs'].keys():
            kwargs['cb_kwargs']['pad'] = default_pad
        self.heatmapf(lambda p: func(*p), style=style, cmap=cmap, **kwargs)
        self.right_corner_label(right_label)
        self.top_corner_label(top_label)
        self.left_corner_label(left_label)
        if self.size_inches == 'auto':
            plt.gcf().set_size_inches(7, 5)

    def heatmap_candidates(self, func, right_label, top_label, left_label, legend_title='',
                           color_a=(1, 0.5, 0.5), color_b=(0.5, 1, 0.5), color_c=(0.5, 0.5, 1),
                           color_a_edge=(.6, 0, 0), color_b_edge=(0, .6, 0), color_c_edge=(0, 0, .6),
                           style='hexagonal', colorbar=False, **kwargs):
        """Heatmap of a function from the simplex to 3D vectors.

        Parameters
        ----------
        func: callable
            The function to plot. Input: coordinates `right`, `top`, `left` in the simplex, i.e. that sum to 1.
            Output: a list of 3 numbers between 0 and 1.
        right_label : str
            Label of the right corner.
        top_label : str
            Label of the top corner.
        left_label : str
            Label of the left corner.
        legend_title : str
            Title of the legend.
        color_a
            RGB color associated to candidate `a` (i.e. first output of the function). Default: red.
        color_b
            RGB color associated to candidate `b` (i.e. second output of the function). Default: green.
        color_c
            RGB color associated to candidate `c` (i.e. third output of the function). Default: blue.
        color_a_edge
            RGB color used for the edge of the patch for candidate `a` in the legend.
        color_b_edge
            RGB color used for the edge of the patch for candidate `b` in the legend.
        color_c_edge
            RGB color used for the edge of the patch for candidate `c` in the legend.
        style
            Contrarily to default settings in python-ternary, the default is ``'hexagonal'``.
        colorbar
            Contrarily to default settings in python-ternary, the default is False.
        kwargs
            All other keywords arguments are passed to method ``heatmap`` of python-ternary.
        """
        data = _generate_heatmap_data(func, self.get_scale(), color_a, color_b, color_c)
        self.heatmap(data, style=style, colorbar=colorbar, use_rgba=True, **kwargs)
        self.right_corner_label(right_label)
        self.top_corner_label(top_label)
        self.left_corner_label(left_label)
        if self.size_inches == 'auto':
            plt.gcf().set_size_inches(5, 5)
        legend_elements = [Patch(facecolor=color_a, edgecolor=color_a_edge, label='$a$'),
                           Patch(facecolor=color_b, edgecolor=color_b_edge, label='$b$'),
                           Patch(facecolor=color_c, edgecolor=color_c_edge, label='$c$')]
        self.legend(title=legend_title, handles=legend_elements)

    def annotate_condorcet(self, right_order, top_order, left_order):
        """Annotate who is the Condorcet winner depending on the region.

        This method can be used when each point of the simplex represents a profile with only three different types,
        each coordinate representing the share of one type. It annotates the regions according to which candidate
        is the Condorcet winner, and indicates where no one is the Condorcet winner.

        If there are weak orders, the method may not work on all distributions because it relies on an external
        package called `shapely`. If there are rankings only, it is supposed to work on all distributions.

        Parameters
        ----------
        right_order : str
            The order whose share is maximal at the right corner.
        top_order : str
            The order whose share is maximal at the top corner.
        left_order : str
            The order whose share is maximal at the left corner.
        """
        try:
            draw_condorcet_zones(self, right_order, top_order, left_order)
        except NameError:
            self._annotate_condorcet_old(right_order, top_order, left_order)

    def _annotate_condorcet_old(self, right_ranking, top_ranking, left_ranking):
        """Old version, for rankings only"""
        count_candidate_tops = dict(Counter([
            ranking[0] for ranking in [right_ranking, top_ranking, left_ranking]]))
        if len(count_candidate_tops) == 1:
            # All rankings have the same top: 'a..', 'a..', 'a..'
            candidate = right_ranking[0]
            self.annotate_simplex('%s is CW' % candidate, (0.33, 0.33, 0.33))
        elif len(count_candidate_tops) == 2:
            # Two different tops: 'a..', 'a..', 'b..'
            weak_candidate, strong_candidate = sorted(count_candidate_tops.keys(),
                                                      key=count_candidate_tops.get)
            if right_ranking[0] == weak_candidate:
                self.left_parallel_line_simplex(0.5)
                self.annotate_simplex('%s is CW' % weak_candidate, (0.7, 0.15, 0.15))
                self.annotate_simplex('%s is CW' % strong_candidate, (0.25, 0.375, 0.375))
            elif top_ranking[0] == weak_candidate:
                self.horizontal_line_simplex(0.5)
                self.annotate_simplex('%s is CW' % weak_candidate, (0.15, 0.7, 0.15))
                self.annotate_simplex('%s is CW' % strong_candidate, (0.375, 0.25, 0.375))
            else:  # left_ranking[0] == weak_candidate
                self.right_parallel_line_simplex(0.5)
                self.annotate_simplex('%s is CW' % weak_candidate, (0.15, 0.15, 0.7))
                self.annotate_simplex('%s is CW' % strong_candidate, (0.375, 0.375, 0.25))
        else:
            # Three different tops
            count_candidate_bottoms = dict(Counter([
                ranking[2] for ranking in [right_ranking, top_ranking, left_ranking]]))
            if len(count_candidate_bottoms) == 3:
                # Condorcet cycle: 'abc', 'bca', 'cab'
                self.horizontal_line_simplex(0.5)
                self.left_parallel_line_simplex(0.5)
                self.right_parallel_line_simplex(0.5)
                self.annotate_simplex('%s is CW' % right_ranking[0], (0.7, 0.15, 0.15))
                self.annotate_simplex('%s is CW' % top_ranking[0], (0.15, 0.7, 0.15))
                self.annotate_simplex('%s is CW' % left_ranking[0], (0.15, 0.15, 0.7))
                self.annotate_simplex('no CW', (0.33, 0.33, 0.33))
            else:
                # Divided majority: 'abc', 'bac', 'cab'
                middle_candidate, weak_candidate = sorted(count_candidate_bottoms.keys(),
                                                          key=count_candidate_bottoms.get)
                strong_candidate = next(
                    candidate for candidate in {'a', 'b', 'c'} - {middle_candidate, weak_candidate})
                if right_ranking[0] == strong_candidate:
                    self.horizontal_line_simplex(0.5)
                    self.right_parallel_line_simplex(0.5)
                    self.annotate_simplex('%s is CW' % right_ranking[0], (0.5, 0.25, 0.25))
                    self.annotate_simplex('%s is CW' % top_ranking[0], (0.15, 0.7, 0.15))
                    self.annotate_simplex('%s is CW' % left_ranking[0], (0.15, 0.15, 0.7))
                elif top_ranking[0] == strong_candidate:
                    self.left_parallel_line_simplex(0.5)
                    self.right_parallel_line_simplex(0.5)
                    self.annotate_simplex('%s is CW' % right_ranking[0], (0.7, 0.15, 0.15))
                    self.annotate_simplex('%s is CW' % top_ranking[0], (0.25, 0.5, 0.25))
                    self.annotate_simplex('%s is CW' % left_ranking[0], (0.15, 0.15, 0.7))
                else:  # left_ranking[0] == strong_candidate
                    self.horizontal_line_simplex(0.5)
                    self.left_parallel_line_simplex(0.5)
                    self.annotate_simplex('%s is CW' % right_ranking[0], (0.7, 0.15, 0.15))
                    self.annotate_simplex('%s is CW' % top_ranking[0], (0.15, 0.7, 0.15))
                    self.annotate_simplex('%s is CW' % left_ranking[0], (0.25, 0.25, 0.5))


def ternary_figure(size_inches='auto', scale=None, boundary_width=1.0, **kwargs):  # pragma: no cover
    """Create a ternary plot (adaptation of `figure` from the package python-ternary).

    Parameters
    ----------
    size_inches : tuple or str
        The horizontal and vertical sizes of the figure, in inches. If 'auto', we will try to do our best.
    scale : Number
        The scale of the figure. The higher it is, the higher the resolution of the heatmap for example.
    boundary_width
        Width of the line representing the boundary of the triangle.
    kwargs
        Other keyword arguments are passed to the function `figure` of the package python-ternary.

    Returns
    -------
    figure : matplotlib.figure.Figure
    ternary_ax : TernaryAxesSubplotPoisson
    """
    ternary_ax = TernaryAxesSubplotPoisson(scale=scale, size_inches=size_inches, **kwargs)
    figure = ternary_ax.get_figure()
    if size_inches == 'auto':
        figure.set_size_inches(5, 5)
    else:
        figure.set_size_inches(*size_inches)
    plt.axis('off')
    ternary_ax.boundary(linewidth=boundary_width)
    return figure, ternary_ax


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
    """
    if isinstance(t, tuple):
        return t[0], '$r(%s, u_%s = %s)$' % (t[0], t[0][1], t[1])
    if len(t) == 3:
        return t, '$r(%s)$' % t
    if len(t) == 4:
        return t.replace('_', ''), ('$r(%s)$' % t).replace('_', '\\_')
    else:  # len(type) == 5
        return t, ('$r(%s)$' % t).replace('~', '\\sim ')


def ternary_plot_n_bloc_equilibria(cls, right_type, top_type, left_type, scale, **kwargs):  # pragma: no cover
    """Shortcut: ternary plot for the number of bloc equilibria.

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
    def n_bloc_equilibria(right, top, left):
        profile = cls({right_type: right, top_type: top, left_type: left})
        return len(profile.analyzed_strategies.equilibria)

    figure, tax = ternary_figure(scale=scale)
    order_r, label_r = _order_and_label(right_type)
    order_t, label_t = _order_and_label(top_type)
    order_l, label_l = _order_and_label(left_type)
    tax.heatmap_intensity(n_bloc_equilibria,
                          right_label=label_r,
                          top_label=label_t,
                          left_label=label_l, **kwargs)
    tax.annotate_condorcet(right_order=order_r, top_order=order_t, left_order=order_l)
    tax.set_title_padded('Number of bloc equilibria')


def ternary_plot_winners_at_equilibrium(cls, right_type, top_type, left_type, scale, **kwargs):  # pragma: no cover
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
        return candidates_to_probabilities(profile.winners_at_equilibrium)

    figure, tax = ternary_figure(scale=scale)
    order_r, label_r = _order_and_label(right_type)
    order_t, label_t = _order_and_label(top_type)
    order_l, label_l = _order_and_label(left_type)
    tax.heatmap_candidates(winners_at_equilibrium,
                           right_label=label_r,
                           top_label=label_t,
                           left_label=label_l,
                           legend_title='Winners',
                           **kwargs)
    tax.annotate_condorcet(right_order=order_r, top_order=order_t, left_order=order_l)


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
                                          ballot_update_ratio=one_over_log_t_plus_two)
        return d_candidate_value_to_array(results['d_candidate_winning_frequency'])

    figure, tax = ternary_figure(scale=scale)
    order_r, label_r = _order_and_label(right_type)
    order_t, label_t = _order_and_label(top_type)
    order_l, label_l = _order_and_label(left_type)
    tax.heatmap_candidates(winning_frequencies,
                           right_label=label_r,
                           top_label=label_t,
                           left_label=label_l,
                           legend_title='Winners',
                           **kwargs)
    tax.annotate_condorcet(right_order=order_r, top_order=order_t, left_order=order_l)
