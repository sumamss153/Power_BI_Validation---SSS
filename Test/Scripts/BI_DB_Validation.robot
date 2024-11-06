*** Settings ***

Resource    ../resourcefile/web.robot
Library    ../resourcefile/Validate.py 

*** Variables ***

*** Test Cases ***

#Forecast of iOS Devices by Date
#    web.Open URL    https://app.powerbi.com/groups/me/reports/414cd51e-932c-4d76-855d-d1af415bea10/ReportSectionfe07d9e3c3e6aa7b9e98?ctid=5b973f99-77df-4beb-b27d-aa0c70b8482c    Forecast of iOS Devices by Date
#    web.Navigate to the Chart    Forecast of iOS Devices by Date
#    web.Export Data from the Chart(Csv/XL)    XL#
#    Validate.Comparison_PowerBI_with_DB    SELECT to_char(datum ,'YYYY-MM-DD 00:00:00') as datum, iphone_8, iphone_8_forecast , iphone_xr, iphone_xr_forecast , iphone_x, iphone_x_forecast FROM public.FORECAST_TMP    Forecast of iOS Devices by Date.xlsx


Top 3 iOS Devices
    web.Open URL   https://app.powerbi.com/groups/me/reports/414cd51e-932c-4d76-855d-d1af415bea10/ReportSectionfe07d9e3c3e6aa7b9e98?ctid=5b973f99-77df-4beb-b27d-aa0c70b8482c    Top 3 iOS Devices
    web.Navigate to the Chart    Top 3 iOS Devices
    web.Export Data from the Chart(Csv/XL)    XL
    Validate.Comparison_PowerBI_with_DB    select "Devices", "Sum_of_iOS" from top_ios_device   Top 3 iOS Devices.xlsx









