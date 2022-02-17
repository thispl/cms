// Copyright (c) 2021, Teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Food Consumption Annexure', {
	refresh: function(frm) {
		// frm.call('get_consumption')
		frm.add_custom_button(__("Download"), function () {
			var f_name = frm.doc.name
			var print_format = "Food Consumption Annexure";
			window.open(frappe.urllib.get_full_url("/api/method/frappe.utils.print_format.download_pdf?"
				+ "doctype=" + encodeURIComponent("Food Consumption Annexure")
				+ "&name=" + encodeURIComponent(f_name)
				+ "&trigger_print=1"
				+ "&format=" + print_format
				+ "&no_letterhead=0"
			));
		})
	}
});
