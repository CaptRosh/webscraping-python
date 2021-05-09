import xlsxwriter
import bs4
from msedge.selenium_tools import Edge,EdgeOptions

excel = xlsxwriter.Workbook("excel.xlsx")
sheet = excel.add_worksheet()
sheet.set_default_row(30)

row = 0
col = 0
op = EdgeOptions()
op.use_chromium = True
driver = Edge(options = op)

bold = excel.add_format({'bold':True})
sheet.write(row,col,"Sr.No",bold)
sheet.write(row,col+1,"Question",bold)
sheet.write(row,col+2,"Option A",bold)
sheet.write(row,col+3,"Option B",bold)
sheet.write(row,col+4,"Option C",bold)
sheet.write(row,col+5,"Option D",bold)
sheet.write(row,col+6,"Answer",bold)

row+=1

for pageEnd in range(1,10):
    driver.get("""https://ssconlineexam.com/general-science-mcq-questions-and-answers-for-competitive-exams&page="""+ str(pageEnd))
    source = driver.page_source
    
    soup = bs4.BeautifulSoup(source,'lxml')

    for mcqquestions in soup.find_all('div',class_='mcq-question'):
        col = 0
        sheet.write(row,col,row)
        question = mcqquestions.find('div',class_='__question')
        col += 1
        sheet.write(row,col,question.text[5:])
        options = mcqquestions.find_all('div',class_='js-choose-answer')
        for option in options:
            myList = option.find_all('div')
            selectedOption = ''
            for i in myList:
                if i.text in ['a','b','c','d']:
                    selectedOption += '({})'.format(i.text)
                else:
                    selectedOption += i.text
            col += 1
            sheet.write(row,col,selectedOption)
        col += 1
        correct = mcqquestions.find('div',correct='1')
        sheet.write(row,col,"({}){}".format(correct.text[0],correct.text[2:]))
        row += 1
driver.close()
excel.close()