#this.max_upload_size = 64 * 1024 * 1024; // 64Mo
#this.max_upload_size = session.max_file_upload_size || 1024 * 1024 * 1024; // 1024Mo
# -*- coding:utf-8 -*-

from odoo import fields, models, api


class SizeLimit(models.Model):
    _name = "size_binary_alter"
    name = fields.Char(string='Name')


    def change_size_binary(self):
        # Read in the file
        print('xxxx')
        with open("C:/Users/Technologies Area/Desktop/odoo14/odoo/addons/web/static/src/js/fields/basic_fields.js",
                  'r') as file:
            filedata = file.read()
            print(filedata)
            filedata = filedata.replace('64 * 1024 * 1024; // 64Mo',
                                        'session.max_file_upload_size || 1024 * 1024 * 1024; // 1024Mo')
            with open('C:/Users/Technologies Area/Desktop/odoo14/odoo/addons/web/static/src/js/fields/basic_fields.js',
                      'w') as file:
                file.write(filedata)