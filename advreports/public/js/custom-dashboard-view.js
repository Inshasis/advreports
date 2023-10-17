// frappe.pages["dashboard-view"].on_page_load = function (wrapper) {
// 	frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: __("Dashboard"),
// 		single_column: true,
// 	});

// 	frappe.dashboard = new Dashboard(wrapper);
// 	$(wrapper).bind("show", function () {
// 		frappe.dashboard.show();
// 	});
//     //     frappe.dashboard.refresh(function(){
// //             // frappe.run_serially([() => this.render_cards(), () => this.render_charts()]);
// //             frappe.run_serially([() => this.render_charts(), () => this.render_cards()]);
// //     });
// };
console.log("custom dashboard js");
console.log(frappe.dashboard);