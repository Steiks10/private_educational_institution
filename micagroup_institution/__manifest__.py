# -*- coding: utf-8 -*-
{
    "name": "Private Institution",
    "version": "1.1",
    'author': "Micagroup",
    "license": "OPL-1",
    "website": "",
    'contributors': [
        'Steiker Mieles <steiker.m2002@gmail.com>',
    ],
    "category": 'Generic Modules/Institution',
    "depends": ['calendar'],
    'data': [
        "security/ir.model.access.csv",
        "views/subject_views.xml",
        "views/student_views.xml",
        "views/teacher_views.xml",
        "views/course_views.xml",
        "views/contract_views.xml",
        "views/career_views.xml",
        "views/menu_items.xml",
        "views/calendar_inherit_view_form.xml",
    ],
    'installable': True,
}
