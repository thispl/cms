// Copyright (c) 2021, TeamPRO and contributors
// For license information, please see license.txt


frappe.ui.form.on('Food Menu', {
	refresh: function (frm) {
		hide_field(["i1","i2","i3","i4","i5","i6","i7","i8","i9","i10","i11","i12"])
		frappe.meta.get_label(frm.doc.doctype, "i1", frm.doc.name)
		// $(cur_frm.fields_dict.test.input).html(`<p>hello</p>`);
		frm.disable_save()
		$("input[data-fieldname='card_no']").focus()
		$(cur_frm.fields_dict.submit.input).css({ 'width': '100px', 'height': '50px', 'font-size':'20px','font-weight':'bold' })
		frm.fields_dict['food_child'].grid.wrapper.find('.grid-add-row').hide();
		// frm.fields_dict.menu.$wrapper.append(frappe.render_template("food_menu"));
		frm.call('get_food_items')
		// frappe.db.get_list("Food Item", {
		// 	fields: ["item", "subsidy_rate", "original_rate", "item_image", "limit"]
		// })
		.then((items) => {
			items.message.forEach((i, v) => {
				let d = 'i' + (v + 1).toString()
				unhide_field([d])
				$(cur_frm.fields_dict[d].input).css({ 'width': '150px', 'height': '150px' })
				frm.set_df_property(d, "label", i.item)
				$(cur_frm.fields_dict[d].input).empty().html(`
				  <img src="${i.item_image}" alt="Avatar" style="width:100%">
				  <h4>${i.item}</h4>
				`);
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
		if(frm.doc.employee){
		frappe.call({
			method: "cms.cms.doctype.food_menu.food_menu.calculate_amount",
			args: {
				"item": item_name,
				"employee": frm.doc.employee,
				"food_child": frm.doc.food_child
			},
			callback(r) {
				frm.add_child("food_child", {
					food_item: r.message[0][0],
					qty:1,
					price: r.message[0][1],
					subsidy:r.message[1]
				})
				frm.refresh_field("food_child")
			}
		})
	}
	},
	card_no(frm) {
		frappe.db.get_value("Employee", { "rfid": frm.doc.card_no }, ["employee_name", "name", "department", "designation"],
			(r) => {
				if(r.name){
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
				}
				else{
				var dialog = frappe.warn('Notification',
				'<h1>Authentication Failed</h1>',
				() => {
					frm.reload_doc()
				},
				'Try Again',
				 // Sets dialog as minimizable
			)
			dialog.$wrapper.find('.modal-dialog').css({"width": "400px"});
			}
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