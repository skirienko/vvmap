const darkModeMql = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)');

const isDark: boolean = darkModeMql && darkModeMql.matches;

type ColorName = 'default' | 'red' | 'blue' | 'green' | 'purple' | 'yellow' | 'peach' | 'neutral';
type ColorScheme = Record<ColorName, string>;

const LIGHT: ColorScheme = {
    default: '#333333',
    red: '#FF3333',
    blue: '#3333FF',
    green: '#33DD33',
    purple: '#CC33CC',
    yellow: '#FFDD66',
    peach: '#FFDAB9',
    neutral: '#99AA99',
};
const DARK: ColorScheme = {
    default: '#808080',
    red: '#cc2929',
    blue: '#3d3dcc',
    green: '#3dBB3d',
    purple: '#992699',
    yellow: '#b39736',
    peach: '#a68769',
    neutral: '#9aab9a',
};

const SCHEME: ColorScheme = isDark ? DARK : LIGHT;

export { isDark, SCHEME, DARK, LIGHT };