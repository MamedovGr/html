const colors = require('tailwindcss/colors')

module.exports = {
	content: [
		'*/templates/*.html',
		'*/templates/*/*.html',
		'*/templates/*/*/*.html',
	],
	important: true,
	theme: {
		extend: {
			screens: {
				'xs': '425px',
				'sm': '640px',
				'md': '768px',
				'lg': '1024px',
				'xl': '1280px',
				'2xl': '1536px',
			},
			colors: {
				transparent: 'transparent',
				current: 'currentColor',
				'primary-light': '#147BE3',
				'primary-dark': '#114BB2',
				'secondary-light': '#424656',
				'secondary-dark': '#202533',
				'disable-gray': '#e9ecef'
			},
			fontSize: {
				'xsm': '.813rem',
			},
			spacing: {
				'128': '32rem',
				'256': '64rem',
			},
		},
	},
	plugins: [
		require('tailwindcss'),
		require('autoprefixer'),
	],
}
