const gw = 400
const gh = 200
const marginBottom = 10
const marginDefault = 40

// select svg container first

function drawGraph(div, dataField) {

	const svg = d3.select('#canvas-' + div)
		.append('svg')
		.attr('height', gh)
		.attr('width', gw);

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
			.attr('fill', '#00ccff')
			.attr('x', d => x(d.report_date))
			.attr('y', d => y(_.get(d, dataField)));


		// append enter selection to the dom
		rects.enter()
			.append('rect')
				.attr('width', x.bandwidth)
				.attr('height', d => graphHeight - y(_.get(d, dataField)))
				.attr('fill', '#00ccff')
				.attr('x', d => x(d.report_date))
				.attr('y', d => y(_.get(d, dataField)));

		// create axis
		const xAxis = d3.axisBottom(x)
			.tickFormat('');
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


drawGraph('cases', 'total_cases');
drawGraph('deaths', 'deaths');
drawGraph('hospital', 'hospitalizations');
drawGraph('testing', 'total_tests');


