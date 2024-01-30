frappe.pages['food-menu'].on_page_load = function(wrapper) {
	var me = this
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __('Food Menu')
	});
	let food_menu = new FoodMenu(wrapper);
	$(wrapper).bind('show', ()=> {
		food_menu.show_side_bar()
		food_menu.show_food_items() //remove after designing completed
	});
	


};
class FoodMenu {

	constructor(wrapper) {
		this.wrapper = $(wrapper);
		this.page = wrapper.page;
		this.sidebar = this.wrapper.find('.layout-side-section');
		this.main_section = this.wrapper.find('.layout-main-section');
	// page.main.html(frappe.("food_menu", {}));

	}
	show_side_bar(){
		this.sidebar.empty();
		let me = this;
		let card_no = frappe.ui.form.make_control({
			parent: me.sidebar,
			df: {
				fieldtype: 'Data',
				options: 'Phone',
				fieldname: 'card_no',
				placeholder: __('Show Card'),
				only_select: true,
				change: () => {
					this.get_employee_details(card_no)
					// this.get_food_items()
		this.show_food_items();
		}
			}
			
		});
		card_no.refresh();
		$("input[data-fieldname='card_no']").focus()
		this.sidebar.find('[data-fieldname="card_no"]').append('<div class="employee-details"></div>');
		this.sidebar.find('[data-fieldname="card_no"]').append('<div class="show-bill-amount"></div>');
		var bill_table = []

	}
	show_food_items(){
		this.main_section.empty();

		let me = this;
		frappe.ui.form.make_control({
			parent: me.main_section,
			df: {
				fieldtype: 'HTML',
				fieldname: 'items',
				// change: () => {
				// 	// this.get_employee_details(card_no)
				// 	this.get_food_items()
					
					
					
				// }
			}
			
		});
		this.get_food_items()
		// card_no.refresh();
		this.main_section.find('[data-fieldname=items]').append('<div class="food-items"></div>');


	}

	get_employee_details(card_no) {
		frappe.db.get_value("Employee",{ "proximity_card_no": card_no.get_value() },["name","employee_name","department","designation"])
					.then(r=>{
						$('.employee-details').empty().append(frappe.render_template('employee_details', {
							employee_name: r.message.employee_name,
							employee: r.message.name,
							department: r.message.department,
							designation: r.message.designation
						}));
					})
	}
	get_food_items(){
		frappe.db.get_list("Food Item", {
			fields: ["item","subsidy_rate","original_rate","item_image","limit"]
		}).then((items) => {
			$('.food-items').empty().append(frappe.render_template('food_menu', {
				items: items,
				// employee: r.message.name,
				// department: r.message.department,
				// designation: r.message.designation
			}));
		})
		// this.page.main.on("click", ".food-item", function(r) {
		// 	// var c = items.get_value()
		// 	// var c = this.page.main.find('items').parent().find('.food-item')
		// 	// var c = $(this).attr("food-item");
		// 	var c = document.getElementById("samosa")
		// 	console.log(r)
		// 	// var c = this.find('[data-fieldname=items]').get_value()
		// 	console.log(c)
		// })
		
	}
	
}
async function get_selected_item(id){
	frappe.call({
		method:"cms.cms.page.food_menu.food_menu.add_bill_amount",
		args:{
			item : id
		},
		callback(r){
			bill_table.push(r.message[0])
			// console.log(bill_table)
		$('.show-bill-amount').empty().append(frappe.render_template('bill_amount', {
			
			item:  r.message[0]
			// employee: r.message.name,
			// department: r.message.department,
			// designation: r.message.designation
		}));
		}
	})
}