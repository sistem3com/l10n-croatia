# -*- coding: utf-8 -*-
{
    "name": """Account reference: Poziv na broj""",
    "summary": """Add reference type: Poziv na broj""",
    "category": "Accounting",
    "images": [],
    "version": "10.0.1.0.0",
    "application": False,

    "author": "Slobodni programi d.o.o.",
    "support": "support@odoo-hrvatska.org",
    "website": "http://odoo-hrvatska.org",
    "licence": "LGPL-3",
    #"price" : 20.00,   #-> only if module if sold!
    #"currency": "EUR",

    "depends": [
        'account'
    ],
    "external_dependencies": {
        "python": [],
        "bin": []
    },
    "data": [
        "views/account_journal_view.xml",
        "views/account_invoice_view.xml",
        "views/report_invoice.xml"
    ],
    "qweb": [],
    "demo": [],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
