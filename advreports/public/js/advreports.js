

function get_project_contracts(project, elementObj){ 
    set_active_class(elementObj);
    frappe.call({
        method: "advreports.advanced_reports.custom.custom_dashboard_cards.get_ongoing_project_contacts",
        args: {
            'project':project
        },
        callback: function(r) {
            if(r.message){
                let num_card_obj = frappe.dashboard.number_card_group.widgets_dict['Project Contacts'];                
                num_card_obj.data = r.message.html;
                num_card_obj.settings.get_number(r.message.html);                
                num_card_obj.render_number();
                let new_data = r.message.chart_data;
                if(new_data !== 'undefined'){
                    $('#task_status_chart').html('<canvas id="pieChart" style="min-height: 250px; height: 250px; max-height: 250px; max-width: 100%;"></canvas>');
                
                // load_chart_custom();
                    setTimeout(function(){
                        custom_chart(new_data);
                    })
                }

                if(r.message.activity_html !== 'undefined'){
                    activity_html = r.message.activity_html;
                    new_activity_html = '<ul>'
                    for(key in activity_html){
                        new_activity_html += '<li>'+activity_html[key]['subject']+'</li>';
                    }
                    new_activity_html += '</ul>';

                    let activity_card_obj = frappe.dashboard.number_card_group.widgets_dict['Recent Activity'];                
                    activity_card_obj.data = new_activity_html;
                    activity_card_obj.settings.get_number(new_activity_html);                
                    activity_card_obj.render_number();
                }
                // const new_options = Object.assign({}, {title: 'Project Task Chart', type: 'bar'}, {data: new_data});
                // console.log(new_options);
                // const chart = new frappe.Chart("#task_status_chart", new_options);
                // // add
                // setTimeout(function () {chart.draw(true)}, 1);
				// frappe.query_report.render_chart(new_options);

					// frappe.query_report.raw_chart_data = new_data;
                // load_chart_data(r.message.chart_data);
            }
        }
    })

}

function custom_chart(chart_data){
    $(function () {
        /* ChartJS
         * -------
         * Here we will create a few charts using ChartJS
         */
        // console.log(chart_data);
        if(typeof chart_data !== 'undefined' && chart_data !== 'undefined' && 'labels' in chart_data && chart_data.labels !== 'undefined'){
            var donutData = {
            labels: [],
            datasets: [
                {
                data: [],
                backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de'],
                }
            ]
            }        
            donutData.labels = chart_data.labels;
            donutData.datasets[0].data = chart_data.datasets[0].values;        
            //-------------
            //- PIE CHART -
            //-------------
            // Get context with jQuery - using jQuery's .get() method.
            var pieChartCanvas = $('#pieChart').get(0).getContext('2d')
            var pieData        = donutData;
            var pieOptions     = {
            maintainAspectRatio : false,
            responsive : true,
            }
            //Create pie or douhnut chart
            // You can switch between pie and douhnut using the method below.
            new Chart(pieChartCanvas, {
            type: 'pie',
            data: pieData,
            options: pieOptions
            })

        }
        else{
            $('#task_status_chart').html('Please update the chart data.');
        }
    
    });
}

function load_chart_data(chart_data){
    if(typeof chart_data !== 'undefined' && chart_data !== '' && chart_data !== 'undefined'){
        // console.log(chart_data);
        // console.log(typeof chart_data);
        var donutData = {
            labels: [],
            datasets: [
              {
                data: [],
                backgroundColor : ['#f56954', '#00a65a', '#f39c12', '#00c0ef', '#3c8dbc', '#d2d6de'],
              }
            ]
          }        
          donutData.labels = chart_data.labels;
          donutData.datasets[0].data = chart_data.datasets[0].values; 
        $('#task_status_chart').html('');
        let chart = new frappe.Chart("#task_status_chart", {
            data: donutData,
            title: 'Project Chart',
            type: 'pie',
            height: 250
          });
        //   console.log(chart);
        //   setTimeout(function () {chart.draw();}, 1);
    }
    else{
        $('#task_status_chart').html('Task status or label not found. Please first setup correctly.');
    }
}

function set_active_class(obj) {
    let parentVal = $(obj).parent('div.number');
    
    $(parentVal).children().each(function(index, element) {
        // console.log(element, index);
        if($(element).hasClass('active'))
            $(element).removeClass('active');
    });

    $(obj).addClass('active');
}