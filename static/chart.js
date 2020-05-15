const gw = Math.min(900, window.innerWidth)
const gh = 200
const marginTop = 45
const marginBottom = 30
const marginDefault = 40
const barColor = 'lightcoral'

// select svg container first
function drawGraph(div, dataField, title, rollingAverage) {

	const svg = d3.select('#canvas-' + div)
		.append('svg')
	   .classed("canvas", true)
	   .attr("width", gw)
	   .attr("height", gh);

	if (!svg.empty()) {
		const barLegend = svg.append('rect')
			.attr('width', 12)
			.attr('height', 12)
			.attr('y', 15)
			.attr('fill', barColor)

		const barLegendText = svg.append("text")
	        .text(title)
	        .attr("class", "chart-title")
	        .attr('x', barLegend.node().getBBox().width + 8)
	        .attr('y', 25);

	    if (rollingAverage) {
		   	const averageLegend = svg.append('line')
			   	.attr('x1', barLegendText.node().getBBox().x + barLegendText.node().getBBox().width + 8)
				.attr('y1', 21)
				.attr('x2', barLegendText.node().getBBox().x + barLegendText.node().getBBox().width + 23)
				.attr('y2', 21)
				.attr('class', 'rolling-average');

			const averageLegendText = svg.append('text')
				.text('7-day rolling average')
				.attr('class', 'chart-title')
				.attr('x', averageLegend.node().getBBox().x + 20)
				.attr('y', 25);
		}

		const margin = {'top': marginTop, 'right': marginDefault, 'bottom': marginBottom, 'left': marginDefault};
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

			const x = d3.scaleTime()
				.domain(d3.extent(data.map(item => new Date(item.report_date))))
				.range([0, graphWidth])

			const xband = d3.scaleBand()
				.domain(data.map(item => item.report_date))
				.range([0, graphWidth])
				.paddingInner(0.1)
				.paddingOuter(0.2);


			// join data to rects
			const rects = graph.selectAll('rect')
				.data(data)
				.attr('width', xband.bandwidth)
				.attr('height', d => graphHeight - y(_.get(d, dataField)))
				.attr('fill', barColor)
				.attr('x', d => xband(d.report_date))
				.attr('y', d => y(_.get(d, dataField)));


			// append enter selection to the dom
			rects.enter()
				.append('rect')
					.attr('width', xband.bandwidth)
					.attr('height', d => graphHeight - y(_.get(d, dataField)))
					.attr('fill', barColor)
					.attr('x', d => xband(d.report_date))
					.attr('y', d => y(_.get(d, dataField)));

			if (rollingAverage) {
				// add lines
			     graph.append('path')
				      .datum(data)
				      .attr('class', 'rolling-average')
				      .attr("d", d3.line()
				        .x(d => xband(d.report_date) + (xband.bandwidth() / 2))
				        .y(d => y(_.get(d, dataField + '_rolling_average')))
				        )
			}


			// create axis
			const xAxis = d3.axisBottom(x)
				.ticks(d3.timeMonth, 1)
				.tickFormat(d3.timeFormat('%b %d'));

			const yAxis = d3.axisLeft(y)
				.ticks(5)

			xAxisGroup.call(xAxis);
			yAxisGroup.call(yAxis);

			xAxisGroup.selectAll('text')
				.attr('text-anchor', 'end')
				.attr('fill', 'grey');
		})

	}
}


window.onload = function() {
	drawGraph('cases', 'cases_past_day', 'Daily New Cases', true);
	drawGraph('deaths', 'deaths_past_day', 'Daily New Deaths', true);
	drawGraph('hospital', 'hospitalizations', 'Hospitalizations', false);
	drawGraph('testing', 'tests_past_day_per_100k', 'Daily Tests (per 100k people)', true);
}




