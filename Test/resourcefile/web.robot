*** Settings ***
Library    SeleniumLibrary
Library    BuiltIn
Library    String
Library    OperatingSystem
Library    Collections

*** Variables ***

${Download_Path}    C:\\Users\\Sumam.Selvin\\Downloads

*** Keywords ***

Web Input
    [Arguments]    ${path}    ${input_file_name}
#    Log To Console      ${path}\\${input_file_name}
    File Should Exist    ${path}\\${input_file_name}

    ${Test}    Get File    ${path}\\${input_file_name}   encoding=UTF-8    encoding_errors=strict
    @{list}    String.split to lines    ${Test}
    ## To receive the URL
    ${url}   set variable    ${list}[0]
    ${url}    convert to string    ${url}
    ${str}    set variable    url =
    ${url}      fetch from right    ${url}    ${str}
    ${url}    strip string    ${SPACE}${url}${SPACE}

    ## To Receive the chart name to validate
    ${Chart_Element}    set variable    ${list}[1]
    ${Chart_Element}    convert to string    ${Chart_Element}
    ${str}    set variable    Chart_Name =
    ${Chart_Element}      fetch from right    ${Chart_Element}    ${str}
    ${Chart_Element}    strip string    ${SPACE}${Chart_Element}${SPACE}
    set global variable    ${Chart_Element}
    set global variable    ${url}

Open URL
    [Documentation]    This test case is to locate the chart element
    [Arguments]    ${url}    ${Chart_Element}
#    [Tags]    Smoke
    ${Chart_Element}    convert to string    ${Chart_Element}
    ${BI_File_Name}    catenate    ${Chart_Element}.xlsx
    log to console     ${BI_File_Name}
    ${File_Path}    catenate    ${Download_Path}\\${BI_File_Name}
    ${Cnt_File_Bkup}    Count Files In Directory	${Download_Path}\\Backup	${BI_File_Name}
    sleep    2s
    log to console     ${Cnt_File_Bkup}
    run keyword if    ${Cnt_File_Bkup} == 1    remove file    ${Download_Path}\\Backup\\${BI_File_Name}
    sleep    2s
    ${File_Exist}    Count Files In Directory	${Download_Path}	${BI_File_Name}
    sleep    2s
    run keyword if    ${File_Exist} == 1    move file    ${File_Path}    ${Download_Path}\\Backup    ELSE    no operation


    Open Browser   ${url}     edge

Navigate to the Chart
    [Arguments]    ${Chart_Element}
    Wait Until Page Contains    ${Chart_Element}    50
    Click Element    //div[@title='${Chart_Element}']

Export Data from the Chart(Csv/Xl)
    [Arguments]    ${Chart_Format_Type}
    ${Chart_Format_Type1} =	Set Variable If	'${Chart_Format_Type}' == 'XL'	.xlsx (Excel 150,000-row max)	.csv (30,000-row max)
    log to console    ${Chart_Format_Type1}
    Click Element    //button[@aria-label='More options']
    Click Element    //button[@title='Export data']
    #Click Element    //h6[text()='Export data']
    Sleep    10s
    Click Element    //button[@class="popout-button themeableElement ng-star-inserted"]
    sleep    10s
    #Click Element    //span[text()='${Chart_Format_Type1} ']
    Click Element    xpath: //*[contains(., "${Chart_Format_Type1}")]
    sleep    10s
    ${ele}    Get WebElement    //button[@localize="ModalDialogButtonText_Export"]
    Execute Javascript    arguments[0].click();     ARGUMENTS    ${ele}
    sleep    10s
    Close Browser



















#Cleanup
#    [Arguments]    ${BI_File_Name}    ${Download_Path}
#    ${BI_File_Name}    convert to string    ${BI_File_Name}
#    ${Download_Path}    convert to string    ${Download_Path}
#    ${File_Path}    catenate    ${Download_Path}${BI_File_Name}
#    ${Cnt_File_Bkup}    Count Files In Directory	${Download_Path}\\Backup	${BI_File_Name}
#    sleep    2s
#    run keyword if    ${Cnt_File_Bkup} == 1    remove file    ${Download_Path}\\Backup\\${BI_File_Name}
#    sleep    2s
#    ${File_Exist}    Count Files In Directory	${Download_Path}	${BI_File_Name}
#    sleep    2s
##    log to console     ${File_Exist}
#    run keyword if    ${File_Exist} == 1    move file    ${File_Path}    ${Download_Path}\\Backup    ELSE    no operation





