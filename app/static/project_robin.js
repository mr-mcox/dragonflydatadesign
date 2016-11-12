var boxGridPlot, sortCMs;

sortCMs = function(i) {
  var button_height, button_margin, cm_row_height, legend_height, legend_spacing, level_count, sortOrder, top_axis_height;
  console.log("Sorting CMs using index " + i);
  cm_row_height = 25;
  top_axis_height = 50;
  level_count = 7;
  legend_spacing = 14;
  button_height = 30;
  button_margin = 10;
  legend_height = legend_spacing * (level_count + 1) + button_height + (button_margin * 2);
  sortOrder = function(a, b) {
    return b.sort_orders[i].cm_order_by_field_level - a.sort_orders[i].cm_order_by_field_level;
  };
  return d3.selectAll('.cm_row').sort(sortOrder).transition().delay(function(d, i) {
    return i * 10;
  }).duration(1000).attr("transform", function(d, i) {
    return "translate(0," + (i * cm_row_height + top_axis_height + legend_height) + ")";
  });
};

boxGridPlot = function(data) {
  var button_height, button_margin, button_width, center_color, cm_area_height, cm_name_width, cm_row_height, cm_rows, cms, color_scales, dist_to_center_color, end_date, field_area_margin, field_area_width, field_label_bottom_margin, field_label_height, field_samples, i, j, k, l, legend_data, legend_groups, legend_height, legend_item_start, legend_items, legend_spacing, len, level_count, ref, ref1, sort_buttons, start_colors, start_date, svg, svg_height, svg_width, time_scale, time_scales, top_axis_height, x_axis;
  cms = data.cms;
  legend_data = data.legend;
  cm_row_height = 25;
  top_axis_height = 50;
  level_count = 7;
  legend_spacing = 14;
  button_height = 30;
  button_width = 100;
  button_margin = 10;
  legend_height = legend_spacing * (level_count + 1) + button_height + (button_margin * 2);
  field_label_height = 15;
  field_label_bottom_margin = 5;
  cm_name_width = 120;
  field_area_width = 200;
  field_area_margin = 30;
  cm_area_height = cms.length * cm_row_height;
  svg_height = cm_area_height + top_axis_height + legend_height;
  svg_width = (field_area_width + field_area_margin) * legend_data.length + cm_name_width;
  svg = d3.select("#chart").append('svg').attr('height', svg_height).attr('width', svg_width);
  start_date = new Date(2014, 8, 1);
  end_date = new Date(2015, 4, 1);
  time_scales = [];
  for (i = j = 0, ref = legend_data.length - 1; j <= ref; i = j += 1) {
    time_scales.push(d3.time.scale().domain([start_date, end_date]).range([cm_name_width + (i * field_area_width + field_area_margin), ((i + 1) * field_area_width) + cm_name_width]));
  }
  center_color = 'white';
  dist_to_center_color = 0.001;
  start_colors = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a'];
  color_scales = [];
  for (i = k = 0, ref1 = legend_data.length - 1; k <= ref1; i = k += 1) {
    color_scales.push(chroma.scale([chroma.interpolate(center_color, start_colors[i], dist_to_center_color), start_colors[i]]).mode('lch'));
  }
  legend_item_start = 0;
  legend_data = data['legend'];
  legend_groups = svg.selectAll('.legend').data(legend_data).enter().append('g').attr('class', 'legend').attr('transform', function(d, i) {
    return 'translate(' + (cm_name_width + (i * field_area_width + field_area_margin)) + ',0)';
  });
  legend_groups.append('text').text(function(d) {
    return d.field_label;
  }).attr('y', field_label_height).attr('x', field_area_width / 2).style('text-anchor', 'middle').style('font-weight', 'bold').each(function(d, i) {
    return d.index = i;
  });
  legend_items = legend_groups.selectAll('.legend_level').data(function(d) {
    return d.levels;
  }).enter().append('g').attr('class', 'legend_level').attr('transform', function(d, i) {
    return 'translate(' + legend_item_start + "," + (i * legend_spacing + field_label_height + field_label_bottom_margin) + ')';
  }).each(function(d) {
    return d.leg_num = d3.select(this.parentNode).datum().index;
  });
  legend_items.append('rect').attr('height', 10).attr('width', 10).style('fill', function(d, i) {
    var p_i;
    p_i = d3.select(this.parentNode).datum().leg_num;
    return color_scales[p_i](d.level_value);
  });
  legend_items.append('text').text(function(d) {
    return d.truncated_field_value;
  }).style('text-anchor', 'start').attr('dx', 13).attr('dy', 10);
  for (l = 0, len = time_scales.length; l < len; l++) {
    time_scale = time_scales[l];
    x_axis = d3.svg.axis().scale(time_scale).orient('top').innerTickSize(-cm_area_height).outerTickSize(0).tickFormat(d3.time.format("%b"));
    d3.select('svg').append('g').attr('class', 'x axis').attr('transform', function() {
      return 'translate(0,' + ((top_axis_height * 0.75) + legend_height) + ')';
    }).call(x_axis).selectAll('text').style('text-anchor', 'start').attr('dx', '0.5em').attr('dy', '0.7em').attr('transform', 'rotate(-90)');
  }
  cm_rows = svg.selectAll('.cm_row').data(cms, function(cm) {
    return cm.person_id;
  }).enter().append('g').attr('class', 'cm_row').attr("transform", function(d, i) {
    return "translate(0," + (i * cm_row_height + top_axis_height + legend_height) + ")";
  });
  cm_rows.append('text').text(function(d) {
    return d.cm_full_name;
  }).attr('alignment-baseline', 'hanging');
  field_samples = cm_rows.selectAll('.field_samples').data(function(d) {
    return d.fields;
  }).enter().append('g').attr('class', 'field_samples').each(function(d, i) {
    return d.index = i;
  });
  field_samples.selectAll('rect').data(function(d) {
    return d.samples;
  }).enter().append('rect').attr('height', 10).attr('width', 5).attr('x', function(d, i) {
    var p_i;
    p_i = d3.select(this.parentNode).datum().index;
    return time_scales[p_i](new Date(d.iso_date));
  }).attr('y', 2.5).style('fill', function(d, i) {
    var p_i;
    p_i = d3.select(this.parentNode).datum().index;
    return color_scales[p_i](d.level_value);
  });
  sort_buttons = legend_groups.append('g').attr('transform', function(d, i) {
    return 'translate(' + (field_area_width - button_width) / 2 + ',' + ((7 * legend_spacing) + field_label_height + field_label_bottom_margin + button_margin) + ')';
  }).on("click", function(d, i) {
    return sortCMs(i);
  }).attr('cursor', 'pointer');
  sort_buttons.on('mouseover', function(d){
    d3.select(this).style('opacity', 0.75);
  });
  sort_buttons.on('mouseout', function(d){
    d3.select(this).style('opacity', 1);
  });
  // return sort_buttons.append('button').attr('type', 'button').attr('class', 'btn btn-default').text('Sort Field');
  sort_buttons.append('rect').attr('height', button_height).attr('width', button_width).style('fill', '#1a1d75').attr('rx', 5).attr('ry', 5);
  return sort_buttons.append('text').attr('y', button_height / 2).attr('x', button_width / 2).style('text-anchor', 'middle').text('Sort Field').style('fill', 'white');
};

d3.json("/pr_data", boxGridPlot);