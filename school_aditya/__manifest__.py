{
    "name": "School Management",
    "author": "Aryabhatta",
    "version":"17.0.0.0",
    "license":"LGPL-3",
    "depends" :["sale","mail","account","stock"],
    "data" : [
        "security/ir.model.access.csv",
        "security/security.xml",
        "data/email_templets_views.xml",
        "data/remainder_student_cron.xml",
        "data/fee_due_remainder_email_templete.xml",
        "report/student_model_report.xml",
        "report/student_model_report_templete.xml",
        "report/sale_report.xml",
        "report/sale_report_template.xml",
        "report/invoicing_inherit_report_template.xml",
        "report/inventory_report.xml",
        "report/inventory_report_template.xml",
        "views/student_views.xml",
        "views/teacher.xml",
        "views/fees_structure_views.xml",
        "views/query_views.xml",
        "views/sale_view.xml",
        "views/invoicing_view.xml",
        "wizard/student_suggestion_wizard_views.xml",
         "views/student_suggestion_list_views.xml",
         "views/product_brand_in_product_template_views.xml",
        "views/inventory.xml",
         "views/menu1.xml",
    ],
}