// Copyright (c) 2021, Teampro and contributors
// For license information, please see license.txt

frappe.ui.form.on('Zecons File Upload', {
	// refresh: function(frm) {

	// },
	file: function(frm) {
		frappe.call({
			"method":"cms.cms.doctype.zecons_file_upload.zecons_file_upload.upload",
			args:{
				"file":frm.doc.file,
			},
			callback(r){
				if (r){
					frm.save()
				}
				// console.log(r.message)
			}
		})
	}
});
