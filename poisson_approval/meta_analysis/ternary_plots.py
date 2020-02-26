import numpy as np
import ternary
from collections import Counter
from ternary.helpers import simplex_iterator
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from poisson_approval.meta_analysis.ternary_condorcet import draw_condorcet_zones


_WHITE = np.array([1., 1., 1.])
_BRIGHTNESS = 0.5


def _abc_to_rgb(abc):
    """Conversion from candidates to RGB color

    Parameters
    ----------
    abc : tuple, list or ndarray
        Array of size 3. Each coefficient is associated to a candidate a, b, c. Typically the coefficients sum to 1
        or less than 1.

    Returns
    -------
    ndarray
        Array of size 3. RGB color. Roughly speaking, candidate `a` is associated to red, `b` to green and `c` to blue,
        but we try to mix colors more reasonably than just an average in RGB space.

    Examples
    --------
        >>> _abc_to_rgb([1, 0, 0])
        array([1. , 0.5, 0.5])
        >>> _abc_to_rgb([.5, .5, 0])
        array([1. , 1. , 0.5])
        >>> _abc_to_rgb([0., 0., 0])
        array([0.5, 0.5, 0.5])
    """
    norm_inf = np.max(abc)
    if norm_inf == 0:
        rgb = np.zeros(3)
    else:
        norm_1 = np.sum(abc)
        rgb = np.array(abc) * np.min([norm_1, 1]) / norm_inf
    return rgb * (1 - _BRIGHTNESS) + _WHITE * _BRIGHTNESS


_COLOR_NO_ONE = _abc_to_rgb([0, 0, 0])
_COLOR_A = _abc_to_rgb([1, 0, 0])
_COLOR_B = _abc_to_rgb([0, 1, 0])
_COLOR_C = _abc_to_rgb([0, 0, 1])
_COLOR_AB = _abc_to_rgb([1, 1, 0])
_COLOR_AC = _abc_to_rgb([1, 0, 1])
_COLOR_BC = _abc_to_rgb([0, 1, 1])
_COLOR_ABC = _abc_to_rgb([1, 1, 1])


def _uni_mix(color_1, color_2, weight_1, weight_2):
    """Mix two colors, with a fade that emphasizes the two base colors.

    Parameters
    ----------
    color_1, color_2 : tuple, list or ndarray
        Arrays of size 3 in format RGB.
    weight_1, weight_2 : Number
        Respective weights of the two colors.

    Returns
    -------
    ndarray
        Array of size 3 in format RGB. The mix is not linear. Currently, the resulting color is a barycenter
        with respective weights ``weight_1**n`` and ``weight_2**n``, with ``n = 2.5``. This makes a "sharper"
        transition, so that we see more of the base colors and less of the mixes.

    Examples
    --------
        >>> import numpy as np
        >>> _uni_mix(color_1=[1, 0, 0], color_2=[0, 1, 0], weight_1=1, weight_2=0)
        array([1., 0., 0.])
        >>> _uni_mix(color_1=[1, 0, 0], color_2=[0, 1, 0], weight_1=.5, weight_2=.5)
        array([0.5, 0.5, 0. ])
        >>> _uni_mix(color_1=[1, 0, 0], color_2=[0, 1, 0], weight_1=0, weight_2=1)
        array([0., 1., 0.])
    """
    n = 2.5
    return (np.array(color_1) * weight_1 ** n + np.array(color_2) * weight_2 ** n) / (weight_1 ** n + weight_2 ** n)


def _palette(x, y):
    """Compute the data for a nice color palette.

    Parameters
    ----------
    x, y : Number
        Cartesian coordinates of the point.

    Returns
    -------
    ndarray
        Array of size 3 in format RGB. The resulting figure consists of:

        * A nice color palette in the unit disk,
        * A black circle on the unit circle,
        * White background outside.

    Examples
    --------
        >>> _palette(x=0, y=1.5)
        array([1., 1., 1.])
        >>> _palette(x=0, y=0.99)
        array([0., 0., 0.])
        >>> color_almost_a = _palette(x=0, y=0.95)
        >>> np.all(np.isclose(color_almost_a, [1, .5, .5], atol=1E-2))
        True
    """
    z = x + 1j * y
    r = np.abs(z)
    if r > 1:
        return np.array([1., 1., 1.])
    if r > 0.96:
        return np.array([0., 0., 0.])
    theta = (np.angle(z, 'deg') + 30) % 360 - 30
    for theta_sup, color_inf, color_sup in zip([30, 90, 150, 210, 270, 330],
                                               [_COLOR_C, _COLOR_AC, _COLOR_A, _COLOR_AB, _COLOR_B, _COLOR_BC],
                                               [_COLOR_AC, _COLOR_A, _COLOR_AB, _COLOR_B, _COLOR_BC, _COLOR_C]):
        if theta <= theta_sup:
            weight_inf = (theta_sup - theta) / 60
            color = _uni_mix(color_sup, color_inf, 1 - weight_inf, weight_inf)
            return _uni_mix(color, _COLOR_ABC, r ** .8, 1 - r ** .8)


_DATA_PALETTE = np.array([[_palette(x / 100, y / 100) for x in range(-100, 100)] for y in range(-100, 100)])


def _generate_heatmap_data(f, scale):
    """Generate RGBA data for a ``simplex to 3D'' heatmap plot.

    Parameters
    ----------
    f : callable
        The function to plot. Input: coordinates `right`, `top`, `left` in the simplex, i.e. that sum to 1. Output: a
        list of 3 numbers between 0 and 1.
    scale
        The scale of the ternary plot.

    Returns
    -------
    dict
        Key: a point of the integer simplex defined by `scale`. Value: the RGBA code of the color representing the
        output of `f`.

    Examples
    --------
        >>> def f(right, top, left):
        ...     return [right, 0, 0]
        >>> _generate_heatmap_data(f, scale=2)
        {(0, 0, 2): (0.5, 0.5, 0.5, 1.0), (0, 1, 1): (0.5, 0.5, 0.5, 1.0), (0, 2, 0): (0.5, 0.5, 0.5, 1.0), \
(1, 0, 1): (0.75, 0.5, 0.5, 1.0), (1, 1, 0): (0.75, 0.5, 0.5, 1.0), (2, 0, 0): (1.0, 0.5, 0.5, 1.0)}
    """
    d = dict()
    for (right, top, left) in simplex_iterator(scale):
        values = f(right / scale, top / scale, left / scale)
        color = _abc_to_rgb(values)
        d[(right, top, left)] = (float(color[0]), float(color[1]), float(color[2]), 1.)
    return d


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
                           legend_style='palette', style='hexagonal', colorbar=False, **kwargs):
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
        legend_style : str
            The style of the legend. The two available options are ``'palette'`` and ``'color_patches'``.
            Cf. :meth:`legend_palette` and :meth:`legend_color_patches`.
        style
            Contrarily to default settings in python-ternary, the default is ``'hexagonal'``.
        colorbar
            Contrarily to default settings in python-ternary, the default is False.
        kwargs
            All other keywords arguments are passed to method ``heatmap`` of python-ternary.
        """
        data = _generate_heatmap_data(func, self.get_scale())
        self.heatmap(data, style=style, colorbar=colorbar, use_rgba=True, **kwargs)
        self.right_corner_label(right_label)
        self.top_corner_label(top_label)
        self.left_corner_label(left_label)
        if self.size_inches == 'auto':
            plt.gcf().set_size_inches(5, 5)
        if legend_style == 'palette':
            self.legend_palette(title=legend_title)
        else:
            self.legend_color_patches(title=legend_title, data=data)

    def annotate_condorcet(self, right_order, top_order, left_order, d_order_fixed_share=None):
        """Annotate who is the Condorcet winner depending on the region.

        We consider a simplex where:

        * Fixed shares of voters have preference orders given by `d_order_fixed_share`.
        * The remaining voters are split between `right_order`, `top_order` and `left_order` in proportions that are
          given by the point in the simplex.

        This method annotates the regions according to which candidate is the Condorcet winner, and indicates where no
        one is the Condorcet winner.

        If there are weak orders and/or fixed shares of voters, the method may not work on all distributions because it
        relies on an external package called `shapely`. If there are rankings only and no fixed shares of voters, it is
        supposed to work on all distributions.

        Parameters
        ----------
        right_order : str
            The order whose share is maximal at the right corner.
        top_order : str
            The order whose share is maximal at the top corner.
        left_order : str
            The order whose share is maximal at the left corner.
        d_order_fixed_share : dict, optional
            Key: order. Value: a fixed share of voters in [0, 1].
        """
        try:
            draw_condorcet_zones(self, right_order, top_order, left_order, d_order_fixed_share)
        except NameError:
            self._annotate_condorcet_old(right_order, top_order, left_order, d_order_fixed_share)

    def _annotate_condorcet_old(self, right_ranking, top_ranking, left_ranking, d_order_fixed_share):
        """Old version, for rankings only"""
        if d_order_fixed_share is not None:
            raise NotImplementedError
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

    def legend_color_patches(self, title, all_mixes=False, data=None):
        """Add a "color patches" legend to the current figure (for candidates heat maps).

        Parameters
        ----------
        title : str
            Title of the legend.
        all_mixes : bool
            If True, then all mixes are indicated in the legend: a + b, a + c, b + c and a + b + c.
        data : dict, optional
            Key : anything. Value: a tuple, list, etc giving an RGB or RGBA code. This is used only if `all_mixes`
            is False.

        Notes
        -----
        * The color patches for single candidates a, b, c are in the legend anyway.
        * If `all_mixes` is True, then all mixes are indicated in the legend.
        * If `all_mixes` is False and `data` is given, then if at least a value is close to a perfect mix (like half
          of `a` and half of `b`), then this mix is added to the legend.
        """
        def _edge_color(color):
            return [max(x - .4, 0) for x in color]
        legend_elements = [Patch(facecolor=_COLOR_A, edgecolor=_edge_color(_COLOR_A), label='$a$'),
                           Patch(facecolor=_COLOR_B, edgecolor=_edge_color(_COLOR_B), label='$b$'),
                           Patch(facecolor=_COLOR_C, edgecolor=_edge_color(_COLOR_C), label='$c$')]
        if all_mixes or data is not None:
            def add_optional_patch(color, label, insertion=False):
                if all_mixes or (data is not None
                                 and any(np.all(np.isclose(data_col[0:3], color, atol=1E-1))
                                         for data_col in data.values())):
                    patch = Patch(facecolor=color, edgecolor=_edge_color(color), label=label)
                    if insertion:
                        legend_elements.insert(0, patch)
                    else:
                        legend_elements.append(patch)
            add_optional_patch(_COLOR_NO_ONE, 'No one', insertion=True)
            add_optional_patch(_COLOR_AB, 'a, b')
            add_optional_patch(_COLOR_AC, 'a, c')
            add_optional_patch(_COLOR_BC, 'b, c')
            add_optional_patch(_COLOR_ABC, 'a, b, c')
        self.legend(title=title, handles=legend_elements)

    @staticmethod
    def legend_palette(title):
        """Add a "palette" legend to the current figure (for candidates heat maps).

        Parameters
        ----------
        title : str
            Title of the legend.

        Notes
        -----
        This is rather a hack than a real matplotlib legend. Hence the usual commands to choose the position
        of the legend, for example, are not meant to work here.
        """
        legend_ax = plt.gcf().add_axes([.68, .63, .2, .2], facecolor='k')
        legend_ax.imshow(_DATA_PALETTE, origin='lower', interpolation='gaussian')
        legend_ax.set_xticks([])
        legend_ax.set_yticks([])
        legend_ax.axis('off')
        legend_ax.annotate('a', (100, 169), horizontalalignment='center', verticalalignment='center')
        legend_ax.annotate('b', (35, 63), horizontalalignment='center', verticalalignment='center')
        legend_ax.annotate('c', (165, 63), horizontalalignment='center', verticalalignment='center')
        legend_ax.set_title(title)
