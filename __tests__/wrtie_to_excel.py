import xlsxwriter
import xlsxwriter.format

if __name__ == "__main__":
    workbook = xlsxwriter.Workbook('test.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})

    list_of_details = [
        {
            "title": "Familiarize with the FE Stack used",
            "days":"1"
        },
        {
            "title": "Review the structure of the FE",
            "days":"2"
        },
        {
            "title": "Familiarize with the BE Stack used",
            "days":"3"
        },
        {
            "title": "Review the structure of the BE",
            "days":"2"
        },
        {
            "title": "Identify the configuration files & environment variable used",
            "days":"2"
        },
        {
            "title": "Identify and Backup database",
            "days":"Simultaneous with the items below"
        },
        {
            "title": "Identify the Cloud hosting platform Stork used and find cost-free alternative for deployment testing",
            "days":"1"
        },
        {
            "title": "Mock test deployment of FE and BE from Stork project to the alternative Cloud hosting platform",
            "days":"2"
        },
        {
            "title": "Start migration of Stork's FE and BE to Local Server",
            "days":"2"
        },
    ]

    def write_in_worksheet(column:str, value, *args) -> None:
        if (len(args) > 0):
            return worksheet.write(column, value, *args)
        worksheet.write(column, value)

    write_in_worksheet('A1', 'Items', bold)
    write_in_worksheet('B1', 'Days', bold)

    for index in range(len(list_of_details)):
        column_number = index + 2
        info = list_of_details[index]
        title = info["title"]
        days = info["days"]
        write_in_worksheet(f"A{column_number}", title)
        write_in_worksheet(f"B{column_number}", days)

    workbook.close()

