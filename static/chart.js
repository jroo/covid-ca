const gw = Math.min(900, window.innerWidth)
const gh = 200
const marginBottom = 10
const marginDefault = 40
const barColor = 'lightcoral'

// select svg container first
function drawGraph(div, dataField, title) {

	const svg = d3.select('#canvas-' + div)
		.append('svg')
	   .classed("canvas", true)
	   .attr("width", gw)
	   .attr("height", gh);

	const t = svg.append("text")
        .text(title)
        .attr('y', 25)
        .attr('font-size', '12px');


	const margin = {'top': marginDefault, 'right': marginDefault, 'bottom': marginBottom, 'left': marginDefault};
	const graphWidth = gw - margin.left - margin.right;
	const graphHeight = gh - margin.top - margin.bottom;

	const graph = svg.append('g')
		.attr('width', graphWidth)
		.attr('height', graphHeight)
		.attr('transform', `translate(${margin.left}, ${margin.top})`);


	const xAxisGroup = graph.append('g')
		.attr('transform', `translate(0, ${graphHeight})`)
	const yAxisGroup = graph.append('g');

	d3.json('daily.json').then( data => {

		const y = d3.scaleLinear()
			.domain([0, d3.max(data, d => _.get(d, dataField))])
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
			.attr('height', d => graphHeight - y(_.get(d, dataField)))
			.attr('fill', barColor)
			.attr('x', d => x(d.report_date))
			.attr('y', d => y(_.get(d, dataField)));


		// append enter selection to the dom
		rects.enter()
			.append('rect')
				.attr('width', x.bandwidth)
				.attr('height', d => graphHeight - y(_.get(d, dataField)))
				.attr('fill', barColor)
				.attr('x', d => x(d.report_date))
				.attr('y', d => y(_.get(d, dataField)));

		// create axis
		const xAxis = d3.axisBottom(x)
			.tickFormat('')

		const yAxis = d3.axisLeft(y)
			.ticks(5)
		xAxisGroup.call(xAxis);
		yAxisGroup.call(yAxis);
		xAxisGroup.selectAll('text')
			.attr('transform', 'rotate(-48)')
			.attr('text-anchor', 'end')
			.attr('fill', 'grey');
	})
}


window.onload = function() {
	drawGraph('cases', 'cases_past_day', 'Daily New Cases');
	drawGraph('deaths', 'deaths_past_day', 'Daily New Deaths');
	drawGraph('hospital', 'hospitalizations', 'Hospitalizations');
	drawGraph('testing', 'tests_past_day_per_100k', 'Daily Tests (per 100k people)');
}




