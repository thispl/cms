// Copyright (c) 2021, Teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Food Consumption', {
	refresh: function(frm) {
		frm.disable_save();
		frm.fields_dict['consumption'].grid.wrapper.find('.grid-add-row').hide();
		frm.fields_dict['consumption'].grid.wrapper.find('.grid-remove-rows').hide();
		var cur_month = frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		if(cur_month == 1){
			frm.set_value("month","Jan")
		}
		else if(cur_month == 2){
			frm.set_value("month","Feb")
		}
		else if(cur_month == 3){
			frm.set_value("month","Mar")
		}
		else if(cur_month == 4){
			frm.set_value("month","Apr")
		}
		else if(cur_month == 5){
			frm.set_value("month","May")
		}
		else if(cur_month == 6){
			frm.set_value("month","Jun")
		}
		else if(cur_month == 7){
			frm.set_value("month","Jul")
		}
		else if(cur_month == 8){
			frm.set_value("month","Aug")
		}
		else if(cur_month == 9){
			frm.set_value("month","Sep")
		}
		else if(cur_month == 10){
			frm.set_value("month","Oct")
		}
		else if(cur_month == 11){
			frm.set_value("month","Nov")
		}
		else{
			frm.set_value("month","Dec")
		}
		
	},
	employee(frm){
		frm.trigger("get_consumption")
	},
	month(frm){
		frm.trigger("get_consumption")
	},
	get_consumption(frm){
		if(frm.doc.employee){
			if(frm.doc.month){
			frappe.call({
				method:"cms.cms.doctype.monthly_food_consumption.monthly_food_consumption.get_monthly_food_consumption",
				args:{
					employee:frm.doc.employee,
					month:frm.doc.month
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
