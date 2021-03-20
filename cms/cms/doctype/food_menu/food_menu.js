// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt


frappe.ui.form.on('Food Menu', {
	refresh: function (frm) {
		frappe.meta.get_label(frm.doc.doctype, "i1", frm.doc.name)
		// $(cur_frm.fields_dict.test.input).html(`<p>hello</p>`);
		frm.disable_save()
		$("input[data-fieldname='card_no']").focus()
		$(cur_frm.fields_dict.submit.input).css({ 'width': '100px', 'height': '50px', 'font-size':'20px','font-weight':'bold' })
		frm.fields_dict['food_child'].grid.wrapper.find('.grid-add-row').hide();
		// frm.fields_dict.menu.$wrapper.append(frappe.render_template("food_menu"));
		frappe.db.get_list("Food Item", {
			fields: ["item", "subsidy_rate", "original_rate", "item_image", "limit"]
		}).then((items) => {
			items.forEach((i, v) => {
				let d = 'i' + (v + 1).toString()
				$(cur_frm.fields_dict[d].input).css({ 'width': '150px', 'height': '150px' })
				frm.set_df_property(d, "label", i.item)
				$(cur_frm.fields_dict[d].input).empty().html(`
				  <img src="${i.item_image}" alt="Avatar" style="width:100%">
				  <h4>${i.item}</h4>
				`);
				// 			frm.fields_dict[d].$wrapper.append(`
				// 		<html>
				// <head>
				// <meta name="viewport" content="width=device-width, initial-scale=1">
				// <style>
				// .card {
				//   box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
				//   transition: 0.3s;
				//   width: 80%;
				// }

				// .card:hover {
				//   box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
				// }

				// .container {
				//   padding: 2px 16px;
				// }
				// </style>
				// </head>
				// <body>
				// <p>${frm.doc.doctype}</p>
				// <div class="card" id=${frm} onclick="get_selected_item(id)">
				//   <img src="${i.item_image}" alt="Avatar" style="width:100%">
				//   <div class="container">
				// 	<h4><b>${i.item}</b></h4> 
				// 	<p></p> 
				//   </div>
				// </div>
				// <br>

				// </body>
				// </html> 
				// <script>
				// function get_selected_item(id){
				// 	var d = JSON.parse("hii")
				// 	console.log(typeof(d))
				// }
				// </script>

				// 		`)
			})
		})
	},
	i1(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i1", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i2(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i2", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i3(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i3", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i4(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i4", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i5(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i5", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i6(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i6", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i7(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i7", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i8(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i8", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	i9(frm) {
		var item_name = frappe.meta.get_label(frm.doc.doctype, "i9", frm.doc.name)
		frm.events.add_item(frm, item_name)
	},
	add_item(frm, item_name) {
		frappe.call({
			method: "cms.cms.doctype.food_menu.food_menu.calculate_amount",
			args: {
				"item": item_name,
				"employee": frm.doc.employee,
				"food_child": frm.doc.food_child
			},
			callback(r) {
				// console.log(r.message)
				frm.add_child("food_child", {
					food_item: r.message[0],
					qty:1,
					price: r.message[1]
				})
				frm.refresh_field("food_child")
			}
		})
	},
	// add_item:function(frm,item_name){
	// 	frm.add_child("food_child", {
	// 		food_item: item_name
	// 	})
	// 	frm.refresh_field("food_child")
	// },
		// frappe.call({
		// 		method:"cms.cms.doctype.food_menu.food_menu.calculate_amount",
		// 		args:{
		// 			"item": item_name,
		// 			"employee": frm.doc.employee
		// 		},
		// 		callback(r){
		// 			console.log(r.message)
		// 			frm.add_child("food_child",{
		// 				food_item:r.message[0],
		// 				price:r.message[1]
		// 			})
		// 			frm.refresh_field("food_child")
		// 		}
		// 	})
	// let dialog = new frappe.ui.Dialog({
	// 	title: 'Confirm Quantity',
	// 	fields: [
	// 		{
	// 			label: 'Item Name',
	// 			fieldname: 'item_name',
	// 			fieldtype: 'Data',
	// 			default: item_name,
	// 			read_only:1
	// 		},
	// 		{fieldtype: "Section Break"},
	// 		{
	// 			label: '1',
	// 			fieldname: 'add',
	// 			fieldtype: 'Button',
	// 			default: 'add()'
	// 		},
	// 		{fieldtype: "Column Break"},
	// 		{
	// 			label: '2',
	// 			fieldname: '2',
	// 			fieldtype: 'Button'
	// 		},
	// 		{fieldtype: "Column Break"},
	// 		{
	// 			label: '3',
	// 			fieldname: '3',
	// 			fieldtype: 'Button'
	// 		},
	// 		{fieldtype: "Column Break"},
	// 		{
	// 			label: '4',
	// 			fieldname: '4',
	// 			fieldtype: 'Button'
	// 		},
	// 		{fieldtype: "Column Break"},
	// 		{
	// 			label: '5',
	// 			fieldname: '5',
	// 			fieldtype: 'Button'
	// 		},
	// 	],
	// 	// primary_action_label: 'Confirm',
	// 	// add(values) {
	// 	// 	console.log(values);
	// 	// 	dialog.hide();
	// 	// },
	// 	// add(frm) {
	// 	// 	console.log("hiii")
	// 	// },

	// });
	// dialog.$wrapper.find('.add')
	// .on("click", function() {
	// 	console.log("hiii")
	// })
	// dialog.show();

	// dialog.$wrapper.find('.modal-dialog').css("width", "300px");

	// 



	// 	setup: function(element) {
	// 		$input.on("awesomplete-select", function(e) {
	// 			i1.onlick(id){
	// console
	// 			}}
	// 			)
	// 	},
	card_no(frm) {
		frappe.db.get_value("Employee", { "proximity_card_no": frm.doc.card_no }, ["employee_name", "name", "department", "designation"],
			(r) => {
				frm.set_value("employee", r.name)
				frm.fields_dict.employee_details.$wrapper.empty().append(` <table class='table table-bordered'>
		<tr>
		<th>Employee Code</th>
		<td>${r.name}</td>
		<th>Department</th>
		<td>${r.department}</td>
		</tr>
		<tr>
		<th>Employee Name</th>
		<td>${r.employee_name}</td>
		<th>Designation</th>
		<td>${r.designation}</td>
		</tr>
		</table>
		`)
			})
	},
	submit(frm) {
		if((frm.doc.food_child).length != 0){
			frappe.call({
				method: "cms.cms.doctype.food_menu.food_menu.daily_food_entry",
				args: {
					"food_child": frm.doc.food_child,
					"employee":frm.doc.employee
				},
				freeze: true,
        		freeze_message: 'Submitting....',
				callback(r) {
					if(r){
						frappe.show_alert({
							message:__('Thankyou for your order'),
							indicator:'green'
						}, 5);
						frm.reload_doc();
					}
				}
			})
		}
		else{
			frappe.throw(__('Please choose atleast one item'))
		}
		
	}
});