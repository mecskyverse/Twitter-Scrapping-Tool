import xlwt
import os

def Excel(
    username,
    data: list,
    output_headers: list,
    output_directory="Excel",  # Default directory to save files
):
    """Writes data to an Excel file with improved formatting and error handling."""

    try:
        wb = xlwt.Workbook()
        sheet1 = wb.add_sheet('Sheet 1')

        # Apply bold formatting to headers
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font

        # Write headers with bold formatting
        for i, header in enumerate(output_headers):
            sheet1.write(0, i, header, style=style)

        # Write data, handling potential index errors
        for i, row in enumerate(data):
            for j, cell in enumerate(output_headers):
                try:
                    sheet1.write(i+1, j, row[cell])
                except IndexError:
                    sheet1.write(i+1, j, "")  # Handle missing data gracefully

        os.makedirs(output_directory, exist_ok=True)  # Create directory if needed
        file_path = os.path.join(output_directory, f"{username}.xls")
        wb.save(file_path)

    except Exception as e:
        print(f"Error writing Excel file: {e}")  # Log any errors

