// select svg container first

const svg = d3.select('.canvas')
	.append('svg')
	.attr('height', 600)
	.attr('width', 600);

const margin = {'top': 20, 'right': 20, 'bottom': 100, 'left': 100};
const graphWidth = 500 - margin.left - margin.right;
const graphHeight = 500 - margin.top - margin.bottom;

const graph = svg.append('g')
	.attr('width', graphWidth)
	.attr('height', graphHeight)
	.attr('transform', `translate(${margin.left}, ${margin.top})`);

const xAxisGroup = graph.append('g')
	.attr('transform', `translate(0, ${graphHeight})`)
const yAxisGroup = graph.append('g');

d3.json('daily.json').then( data => {

	const y = d3.scaleLinear()
		.domain([0, d3.max(data, d => d.tests_past_day)])
		.range([graphHeight, 0]);

	const x = d3.scaleBand()
		.domain(data.map(item => item.report_date))
		.range([0, graphWidth])
		.paddingInner(0.1)
		.paddingOuter(0.2);

	// join data to rects
	const rects = graph.selectAll('rect')
		.data(data)
		.attr('width', x.bandwidth)
		.attr('height', d => graphHeight - y(d.tests_past_day))
		.attr('fill', 'blue')
		.attr('x', d => x(d.report_date))
		.attr('y', d => y(d.tests_past_day));


	// append enter selection to the dom
	rects.enter()
		.append('rect')
			.attr('width', x.bandwidth)
			.attr('height', d => graphHeight - y(d.tests_past_day))
			.attr('fill', 'orange')
			.attr('x', d => x(d.report_date))
			.attr('y', d => y(d.tests_past_day));

	// create axis
	const xAxis = d3.axisBottom(x)
		.ticks(5);
	const yAxis = d3.axisLeft(y)
		.ticks(5)
	xAxisGroup.call(xAxis);
	yAxisGroup.call(yAxis);
	xAxisGroup.selectAll('text')
		.attr('transform', 'rotate(-48)')
		.attr('text-anchor', 'end')
		.attr('fill', 'grey');

})
