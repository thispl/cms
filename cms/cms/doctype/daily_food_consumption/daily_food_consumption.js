// Copyright (c) 2021, Teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Food Consumption', {
	refresh: function(frm) {
		frm.disable_save();
		frm.fields_dict['consumption'].grid.wrapper.find('.grid-add-row').hide();
		frm.fields_dict['consumption'].grid.wrapper.find('.grid-remove-rows').hide();
		// var cur_month = frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		frm.set_value("date",frappe.datetime.nowdate())
		
	},
	employee(frm){
		frm.trigger("get_consumption")
		if(frm.doc.employee){
			frm.add_custom_button(__("Exit"), function(){
				frm.reload_doc()
			  }).css({ 'width': '100px', 'height': '50px', 'font-size':'20px','font-weight':'bold','background-color':'#00FF00' });
			}
	},
	date(frm){
		frm.trigger("get_consumption")
	},
	get_consumption(frm){
		if(frm.doc.employee){
			if(frm.doc.date){
			frappe.call({
				method:"cms.cms.doctype.daily_food_consumption.daily_food_consumption.get_food_consumption",
				args:{
					employee:frm.doc.employee,
					date:frm.doc.date
				},
				callback(r){
					frm.clear_table("consumption")
					frm.set_value("subsidy_balance",r.message[1])
					frm.set_value("bill_amount",r.message[2])
					$.each(r.message[0],function(i,v){
						frm.add_child("consumption",{
							"food_item": v.item,
							"qty": v.qty,
							"amount": v.amount
						})
					})
					frm.refresh_field("consumption")
				}
			})
		}
		}
	}
});
