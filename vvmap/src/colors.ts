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
    peach: '#cc9c72',
    neutral: '#99AA99',
};
const DARK: ColorScheme = {
    default: '#808080',
    red: '#a82222',
    blue: '#3d3dcc',
    green: '#2a802a',
    purple: '#802080',
    yellow: '#a88f32',
    peach: '#805e40',
    neutral: '#738073',
};

const SCHEME: ColorScheme = isDark ? DARK : LIGHT;

export { isDark, SCHEME, DARK, LIGHT };