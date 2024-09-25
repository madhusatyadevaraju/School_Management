import base64
import tempfile


from odoo import api, fields, models
import re
class InventoryDelivery(models.Model):
    _inherit = "stock.picking"  # Inherit the stock.picking model in this module

    bank_name = fields.Char(string="Bank Name")
    iban_code = fields.Char(string="IBAN No")
    account_name = fields.Char(string="Account Name")
    account_number = fields.Char(string="Account No")
    branch = fields.Char(string="Branch")




# python file for the Xlsx Report
class InventoryXlsx(models.AbstractModel):
    _name = 'report.school_aditya.report_name_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # To create a sheet in workbook.
        sheet = workbook.add_worksheet("DELIVERY")
        # Hide the gridlines
        sheet.hide_gridlines(2)  # Pass 2 to hide both printed and visible gridlines

        # Dynamically insert the company logo if it exists
        if lines.company_id.logo:
            # Assuming logo is in base64 format, decode it
            logo_data = base64.b64decode(lines.company_id.logo)

            # Create a temporary file for the logo
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_logo_file:
                temp_logo_file.write(logo_data)
                temp_logo_path = temp_logo_file.name

            # Insert the logo from the temporary file
            sheet.insert_image('A1:D4',temp_logo_path,{'x_scale': 0.6, 'y_scale': 0.6})
            # Create a format with color
        bold = workbook.add_format({ 'font_size': 10})
        regular_format = workbook.add_format({'font_size': 10})
        bold_format = workbook.add_format({'bold': True, 'font_size': 10 ,'bg_color':'#2645a8','color':'white'})
        table_border=workbook.add_format({'bold':True})
        format= workbook.add_format({'font_color':'#227C7C','bold': True})
        color = workbook.add_format({'bold': True, 'font_size': 15, 'color': '#0E4444'})
        combined_format = workbook.add_format({'bold': True, 'font_size': 10, 'bg_color': '#2645a8', 'color': 'white','align':'center','valign':'vcenter'})
        combined_line = workbook.add_format({'border': 1})
        border_formate=workbook.add_format({'border': 1,'align':'center','valign':'vcenter'})
        # Create a format for wrapping text
        wrap_format = workbook.add_format({
            'border': 1,  # Apply border
            'align': 'left',  # Align text to the left
            'valign': 'top',  # Align text to the top
            'text_wrap': True  # Enable text wrapping
        })



        sheet.merge_range('A6:E6', lines.company_id.name ,format)
        sheet.merge_range('A7:D8', f"{lines.company_id.city}\n{lines.company_id.country_id.name}",bold)
        sheet.merge_range('G2:I3','Delivery Order',color)
        # Shipping Address
        sheet.merge_range('A11:D11', 'Shipping Address:', bold_format)
        if lines.partner_id:
            shipping_address = f"{lines.partner_id.name}\n{lines.partner_id.street}\n{lines.partner_id.city}, \n{lines.partner_id.country_id.name}"
            sheet.merge_range('A12:D15', shipping_address, regular_format)

            # Delivery order details
            sheet.merge_range('G7:H7', 'Order #: ' )
            sheet.merge_range('I7:J7', lines.name,combined_line )
            # Assuming lines.scheduled_date contains both date and time
            scheduled_date = lines.scheduled_date
            # Extract only the date part
            formatted_date = scheduled_date.date()
            sheet.merge_range('G8:H8', 'Scheduled Date:'  )
            sheet.merge_range('I8:J8', str(formatted_date),combined_line)
            sheet.merge_range('E18:F19', str(formatted_date), border_formate)

        sheet.merge_range('G11:J11', 'Invoicing Address:', bold_format)
        if lines.partner_id:
            shipping_address = f"{lines.partner_id.name}\n{lines.partner_id.street}\n{lines.partner_id.city}, \n{lines.partner_id.country_id.name}"
            sheet.merge_range('G12:J15', shipping_address, regular_format)
        # Add details of the sales person

        sheet.merge_range('A17:B17','Sales Person',combined_format)
        sheet.merge_range('A18:B19',lines.user_id.name,border_formate)
        sheet.merge_range('C17:D17', 'Shipping Policy', combined_format)
        sheet.merge_range('C18:D19', lines.move_type, border_formate)
        sheet.merge_range('E17:F17', 'Scheduled Date', combined_format)


        effective_date = lines.date_done
        if effective_date:
             format_date = effective_date.date()
             sheet.merge_range('G18:H19', str(format_date), border_formate)
        else:
            format_date=""
            sheet.merge_range('G18:H19', format_date, border_formate)

        sheet.merge_range('G17:H17', 'Effective Date', combined_format)
        sheet.merge_range('I17:J17', 'Source Document', combined_format)
        sheet.merge_range('I18:J19', lines.origin, border_formate)

        # Add a product details headers
        sheet.merge_range('A21:C21',"Product",combined_format)
        sheet.merge_range('D21:F21', "Description", combined_format)
        sheet.merge_range('G21:H21', "Demand", combined_format)
        sheet.merge_range('I21:J21', "Quantity", combined_format)
        # Start writing product details from row 22 onwards
        row_number = 22  # Start from row 22

        # Loop through each stock move in the picking (move_ids_without_package)
        for line in lines.move_ids_without_package:
            # Fetch the details from each move line
            product_name = line.product_id.name if line.product_id else 'N/A'  # Product Name
            #product_description = line.description_picking if line.product_id else 'N/A'  # Product Description
            product_description=line.description_picking.split('\n')
            product_names=""
            if len(product_description)>1:
                for description_picking in product_description:
                    product_names += "\n"+"*"+description_picking
            else:
                product_names=product_description[0]

            demand = line.product_uom_qty  # Requested demand quantity
            quantity = line.quantity  # Quantity that has been processed (delivered)

            # Write the product details into the Excel sheet
            sheet.merge_range(f'A{row_number}:C{row_number}', product_name, combined_line)  # Product Name
            sheet.merge_range(f'D{row_number}:F{row_number}', product_names,combined_line)  # Description
            sheet.merge_range(f'G{row_number}:H{row_number}', demand, border_formate)  # Demand
            sheet.merge_range(f'I{row_number}:J{row_number}', quantity, border_formate)  # Quantity

            # Move to the next row for the next product
            row_number += 1

        # After all products are listed, add the Special Note and Instructions
        special_note= row_number + 1  # Leave an extra row before Special Note

        # Write the cleaned note into the Excel sheet
        if lines.note:
           sheet.merge_range(f'A{special_note}:J{special_note}', "Special Notes and Instructions", combined_format)
        # Use regex to remove HTML tags

           clean_note = re.sub(r'<.*?>', '', lines.note)
           sheet.merge_range(f'A{special_note + 1}:J{special_note + 2}', clean_note, wrap_format)
        else:
            # If there is no note, do nothing or handle it differently
            print("No special notes available.")

        text_center_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})
        text_center_format2 = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
        dotted_top_format = workbook.add_format({'top': 1, 'top_color': '##2c2e80', 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})
        special_note += 5
        sheet.merge_range(f'A{special_note}:J{special_note}', 'Thank you for your business!', text_center_format)
        sheet.merge_range(f'A{special_note + 1}:J{special_note + 1}',f'Should you have any inquiries concerning this order,contact : {lines.user_id.name} on  {lines.user_id.mobile}.',text_center_format2)
        sheet.merge_range(f'A{special_note + 2}:J{special_note + 3}',f'{lines.company_id.street} , {lines.company_id.city} , {lines.company_id.country_id.name} \n {lines.company_id.mobile}     {lines.company_id.email}     {lines.company_id.website}',dotted_top_format)
