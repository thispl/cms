# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "cms"
app_title = "CMS"
app_publisher = "Teampro"
app_description = "Canteen Management System"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "subash.p@groupteampro.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/cms/css/cms.css"
# app_include_js = "/assets/cms/js/cms.js"

# include js, css files in header of web template
# web_include_css = "/assets/cms/css/cms.css"
# web_include_js = "/assets/cms/js/cms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "cms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "cms.install.before_install"
# after_install = "cms.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "cms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"CMS Log": {
# 		"after_insert": "cms.utils.create_dfe_from_cms_log",
# 		# "on_cancel": "method",
# 		# "on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"cms.tasks.all"
# 	],
	"cron": {
		"0 1 * * *": [
           "cms.utils.clean_cms_log",
        ],
		"0 2 * * *": [
		   "cms.utils.create_dfe_from_cms_log_bulk",
        ],
		"0 3 * * *": [
		   "cms.utils.send_fca_test_email",
        ]
	}
# 	"hourly": [
# 		"cms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"cms.tasks.weekly"
# 	]
# 	"monthly": [
# 		"cms.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "cms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "cms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "cms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

fixtures = ["Desk Page"]

jenv = {
	"methods": [
		"get_consumption_data:cms.cms.doctype.food_consumption_annexure.food_consumption_annexure.get_consumption_data"
	]
}