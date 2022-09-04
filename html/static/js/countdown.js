simplyCountdown('#cuenta', {
	year: 2022,
	month: 4,
	day: 20, 
	hours: 0,
	minutes: 0,
	seconds: 0, 
	words: { 
		days: { singular: 'día', plural: 'días' },
		hours: { singular: 'hora', plural: 'horas' },
		minutes: { singular: 'minuto', plural: 'minutos' },
		seconds: { singular: 'segundo', plural: 'segundos' }
	},
	plural: true, 
	inline: false, 
	inlineClass: 'simply-countdown-inline',
	enableUtc: true, //Usar hora UTC
	onEnd: function() { return; }, 
	refresh: 1000,
	sectionClass: 'simply-section',
	amountClass: 'simply-amount', 
	wordClass: 'simply-word',
	zeroPad: true,
	countUp: false
});

let myElement = document.querySelector('.my-countdown');
simplyCountdown(myElement, { /* opciones */ });

let multipleElements = document.querySelectorAll('.my-countdown');
simplyCountdown(multipleElements, { /* opciones */ });