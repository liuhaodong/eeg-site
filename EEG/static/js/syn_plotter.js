LEN_SEGMENT = 60;
NUM_XTICKS = 9;
REFRESH_RATE = 1000;

///////////////////////////////////////////////////////////////////////
///////// METRIC GRAPH ////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////

function updateGraph(divId, content_group_name, content_name, duration, data, mark, callback, onClick) {
    $(document).ready(function() {
        if (duration === null) {
            var requestData = {'content_group_name': content_group_name,
                'content_name': content_name}
            $.get('/EEG/estimate_duration', requestData, function(duration) {
                duration = parseInt(duration);
                updateGraph(divId, content_group_name, content_name, duration, data, mark, callback);
            });
            return;
        }

        var drawChart = function(data) {
            var chart = getChart(divId);
            if (chart) {
                drawGraph(chart, data, 0, duration, ['low', 'high'], mark)
            }
            if (onClick) {
                chart.bind("plotclick", function (event, pos, item) {
                    onClick(pos.x);
                });
            }
            callback(data);
        }

        if (!data) {
            loadInfo(content_group_name, content_name, duration, drawChart);
        } else {
            drawChart(data);
        }
    });
}

function getChart(divId) {
    var chart = $(divId);
    if (chart.length == 0) {
        chart = $("#" + divId);  // incase we forgot the #
    }
    return chart;
}

function loadInfo(content_group, content, duration, callback) {
    // generate segments
	
    var len_segment = LEN_SEGMENT;

    var segments = [[0, 0]]; // a base case segment to be removed later
    for (var i = 0; i * len_segment < duration; i++) {
        segments.push([segments[i][1], i * len_segment]);
    }
    segments.shift(); // remove the base case

    var checkboxes= $('.syn_checkbox');
    
    var querylist = [];
    
    $.each(checkboxes, function( index, checkbox ) {
    	if (checkbox.checked) {
    		querylist.push($(checkbox).val());
    	}
    });

    var requestData = {'content_group_name': content_group,
        'content_name': content,
        'label_type_names': JSON.stringify(querylist),
        'segments': JSON.stringify(segments)}
    
    $.get('/EEG/get_labels', requestData, function(data) {
    	var data_points = [];
    	var all_data = [];
    	$.each(querylist, function(index,name) {
    		var resObj = data[name];
            if (!resObj) {
                return;
            }
    		// create data points
    		var data_points = [];
    		for (var i = 0; i < resObj.length; i++) {
    			var sub_idx = resObj[i][0];
    			var time = (segments[sub_idx][0] + segments[sub_idx][1]) / 2
    			var metric = resObj[i][1];
    			data_points.push([time, metric]);
                console.log('time, metric: ' + time + ',' + metric);
    		}
    		all_data.push({data: data_points, label: name});
            console.log('name: ' + name);
        
    	})

        // TODO: check what if segments.length is 0 and do something sensible
        var full_start_time = segments[0][0]
        var full_end_time = segments[segments.length - 1][1]

        callback(all_data);
    });
}

///////////////////////////////////////////////////////////////////////
///////// GRAPH UTILS /////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////

function drawGraph(div, data, start_time, end_time, ylabels, mark) {
    var duration = end_time - start_time;
    var len_xticks = (duration / NUM_XTICKS) || 15; // default to 15 seconds

    var xticks = [];
    for (var t = 0; t < duration; t += len_xticks) {
        xticks.push([start_time + t, secondsToMinuteString(t)]);
    }
    xticks.push([end_time, secondsToMinuteString(t)]);

    var yticks = [];
    for (var i = 0; i < ylabels.length; i++) {
        yticks.push([i / (ylabels.length - 1), ylabels[i]]);
    }

    var markings = [];
    if (mark) {
        markings = [{ color: '#000', lineWidth: 1, xaxis: { from: mark, to: mark } }];
    }

    // plot
    $.plot(div,
        data, {
            series: {
                lines: { show: true,
                        lineWidth: 1,
                        fill: false, 
                        fillColor: { colors: [ { opacity: 0.1 }, { opacity: 0.13 } ] }
                        },
                points: { show: true, 
                            lineWidth: 2,
                            radius: 3
                        },
                shadowSize: 0,
            },
            grid: { hoverable: true, 
                    clickable: true, 
                    tickColor: "#f9f9f9",
                    borderWidth: 0,
                    markings: markings
                },
            legend: {
                    // show: false
                    labelBoxBorderColor: "#fff"
                },  
            colors: ["#a7b5c5", "#30a0eb"],
            xaxis: {
                ticks: xticks,
                min: xticks[0][0],
                max: xticks[xticks.length-1][0],
                font: {
                    size: 12,
                    family: "Open Sans, Arial",
                    variant: "small-caps",
                    color: "#697695"
                }
            },
            yaxis: {
                ticks:yticks, 
                min:yticks[0][0],
                max:yticks[yticks.length-1][0],
                font: {
                    size: 12,
                    family: "Open Sans, Arial",
                    variant: "small-caps",
                    color: "#697695"
                }
            }
        }
    );
}

///////////////////////////////////////////////////////////////////////
///////// TIME UTILS //////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////

function secondsToMinuteString(duration) {
    var hours = Math.floor(duration / 60 / 60);
    var minutes = Math.floor(duration / 60 - hours * 60);
    var seconds = Math.floor(duration - minutes * 60 - hours * 60 * 60);

    var hour_str = hours.toString();
    var min_str = zeroPad(minutes.toString(), 2);
    var sec_str = zeroPad(seconds.toString(), 2);

    if (hours > 0) {
        return hour_str + ':' + min_str + ':' + sec_str;
    } else {
        return min_str + ':' + sec_str;
    }
}

function zeroPad(num, length) {
    var zeros = length - num.length;
    for (var i = 0; i < zeros; i++) {
        num = '0' + num;
    }
    return num;
}
