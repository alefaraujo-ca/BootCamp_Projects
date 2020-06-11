'Create a script that will loop through all the stocks for one year for each run and take the
'following information.
''
'The ticker symbol.
'Yearly change from opening price at the beginning of a given year to the closing price at the end of that year.
'The percent change from opening price at the beginning of a given year to the closing price at the end of
'that year.
'The total stock volume of the stock.


'You should also have conditional formatting that will highlight positive change in green and negative change
'in red.

Option Explicit

'Create constants to hold the columns numbers
Const col_Source_Ticker = 1
Const col_Source_Open = 3
Const col_Source_Close = 6
Const col_Source_Vol = 7
Const col_Response_Ticker = 9
Const col_Response_YChange = 10
Const col_Response_PChange = 11
Const col_Response_TStockVol = 12
Const col_Grestest_Labels = 15
Const col_Grestest_Ticker = 16
Const col_Grestest_Value = 17


Sub GetVBAStocksInfo()
    'Set variables to control rows contains data and rows to write the results
    Dim nRowSource, nRowResponse As Integer
    
    'Set variable to hold the ticker grouping data
    Dim sTicker As String
    
    'Set variables do hold the values
    Dim valOpen, valClose, YChange As Double
    
    'Set variable to control each worksheet
    Dim ws As Worksheet
    
    'Set variable do hold the Total Stock Volume
    Dim valTStockVol As Double
    
    
    ' --------------------------------------------
    'Loop through all the worksheets part of the Workbook
    ' --------------------------------------------
    For Each ws In Worksheets
        
        'Write the title for the grouped information
        Call WriteTitles(ws)
        
        'Iniciate the rows containing data
        nRowSource = 2
        nRowResponse = 2
        
        
        ' --------------------------------------------
        ' Loop through all given rows
        ' --------------------------------------------
        Do While ws.Cells(nRowSource, col_Source_Ticker).Value <> ""

            'Inicialize the Total Stock Volume variable, for every new ticker
            valTStockVol = 0
            
            'Set the variable with the ticker the loop will went through
            sTicker = ws.Cells(nRowSource, col_Source_Ticker).Value
            
            'Set the Open Value for the ticker
            valOpen = ws.Cells(nRowSource, col_Source_Open).Value
            
            ' --------------------------------------------
            ' Loop through all rows containing the same ticker
            ' --------------------------------------------
            Do While ws.Cells(nRowSource, col_Source_Ticker).Value = sTicker
            
                If valOpen <= 0 Then
                    'Set the Open Value for the ticker
                    valOpen = ws.Cells(nRowSource, col_Source_Open).Value
                End If
            
                'Sum the current volume to Total Stock Volume
                valTStockVol = valTStockVol + ws.Cells(nRowSource, col_Source_Vol)
                
                'Increment the row so the loop gets the next value
                nRowSource = nRowSource + 1
            
            Loop
            
            'Set the Close Value for the Ticker
            valClose = ws.Cells(nRowSource - 1, col_Source_Close)
            
            
            ' --------------------------------------------
            ' Write grouped information by Ticker
            ' --------------------------------------------
        
            ws.Cells(nRowResponse, col_Response_Ticker).Value = sTicker
            
            YChange = valClose - valOpen
            ws.Cells(nRowResponse, col_Response_YChange).Value = YChange
            
            'Mark Green for positive and Red for negative values
            If YChange >= 0 Then
                ws.Cells(nRowResponse, col_Response_YChange).Interior.ColorIndex = 4 'Green
            Else
                ws.Cells(nRowResponse, col_Response_YChange).Interior.ColorIndex = 3 'Red
            End If
            
            ' Avoid division by zero
            If valOpen = 0 Then
                valOpen = 1
            End If
            
            ws.Cells(nRowResponse, col_Response_PChange).Value = YChange / valOpen
            ws.Cells(nRowResponse, col_Response_PChange).NumberFormat = "0.00%"
            
            ws.Cells(nRowResponse, col_Response_TStockVol).Value = valTStockVol
        
            'Increment the response row
            nRowResponse = nRowResponse + 1
        
        Loop
        
        ' --------------------------------------------
        ' Greatest values - CHALLENGES
        ' --------------------------------------------
        Call GreatestValues(ws, nRowResponse)
        
        ' --------------------------------------------
        ' Arrange Columns
        ' --------------------------------------------
        ws.Columns("A:Q").AutoFit
    
        
    Next ws
    

End Sub

Sub WriteTitles(ws As Worksheet)

    ' --------------------------------------------
    ' Write titles for each expected column
    ' --------------------------------------------
    
    With ws
    
        .Cells(1, col_Response_Ticker).Value = "Ticker"
        .Cells(1, col_Response_YChange).Value = "Yearly Change"
        .Cells(1, col_Response_PChange).Value = "Percentage Change"
        .Cells(1, col_Response_TStockVol).Value = "Total Stock Volume"
        
        .Cells(2, col_Grestest_Labels).Value = "Greatest % Increase"
        .Cells(3, col_Grestest_Labels).Value = "Greatest % Decrease"
        .Cells(4, col_Grestest_Labels).Value = "Greatest Total Volume"

        .Cells(1, col_Grestest_Ticker).Value = "Ticker"
        .Cells(1, col_Grestest_Value).Value = "Value"
        
    End With
    
End Sub

Sub GreatestValues(ws As Worksheet, nRows As Integer)

    Dim i As Integer
    Dim NewPerVal, NewStVolume As Double
    
    'Set array variable to hold the Grestest values for Percent Change (Increase and Decrease) and Total Stock Volume
    'First position will hold the Greatest Increase
    'Second position will hold the Greatest Descrease
    'Third position will hol the Greatest Total Stock Volume
    Dim GtValues(3) As Double
    
    'Set array variable to hold the tickers for the Grestest values
    Dim GtTickers(3) As String
    
    'Set the first value Percent Change as the Greatest Increase
    GtValues(1) = ws.Cells(2, col_Response_PChange).Value
    
    'Set the first value Percent Change as the Greatest Decrease
    GtValues(2) = ws.Cells(2, col_Response_PChange).Value
    
    'Set the first value Percent Change as the first two positions of the array
    GtValues(3) = ws.Cells(2, col_Response_TStockVol).Value
    
    'Set the first ticker for all the three positions
    GtTickers(1) = ws.Cells(2, col_Response_Ticker).Value
    GtTickers(2) = ws.Cells(2, col_Response_Ticker).Value
    GtTickers(3) = ws.Cells(2, col_Response_Ticker).Value
    
    ' --------------------------------------------
    ' Loop through all calculated values for each ticker
    ' --------------------------------------------
    ' Loop must start from the third value, as the second was already stored
    ' Number of rows is comming as a parameter from the function that calculated all the values
    For i = 3 To (nRows - 2)
        
        ' Set the actual value of Percent Change to a variable in order to compare
        '  with the one already stored at our array
        NewPerVal = ws.Cells(i, col_Response_PChange).Value
        
        ' If the actual value is greater then the one stored at our first position of the array
        '   change it
        If NewPerVal > GtValues(1) Then
            GtValues(1) = NewPerVal
            GtTickers(1) = ws.Cells(i, col_Response_Ticker).Value
            
        End If
    
        ' If the actual value is smaller then the one stored at our second position of the array
        '   change it
        If NewPerVal < GtValues(2) Then
            GtValues(2) = NewPerVal
            GtTickers(2) = ws.Cells(i, col_Response_Ticker).Value
            
        End If
        
        ' Set the actual value of Total Stock Volume to a variable in order to compare
        '   with the one already stored at our array
        NewStVolume = ws.Cells(i, col_Response_TStockVol).Value
        
        ' If the actual value is greater then the one stored at our thrid position of the array
        '   change it
        If NewStVolume > GtValues(3) Then
            GtValues(3) = NewStVolume
            GtTickers(3) = ws.Cells(i, col_Response_Ticker).Value
            
        End If
    
    Next i
    
    ' --------------------------------------------
    ' Write the results
    ' --------------------------------------------
    
    ws.Cells(2, col_Grestest_Ticker).Value = GtTickers(1)
    ws.Cells(2, col_Grestest_Value).Value = GtValues(1)
    ws.Cells(2, col_Grestest_Value).NumberFormat = "0.00%"
    
    ws.Cells(3, col_Grestest_Ticker).Value = GtTickers(2)
    ws.Cells(3, col_Grestest_Value).Value = GtValues(2)
    ws.Cells(3, col_Grestest_Value).NumberFormat = "0.00%"
    
    ws.Cells(4, col_Grestest_Ticker).Value = GtTickers(3)
    ws.Cells(4, col_Grestest_Value).Value = GtValues(3)
    
End Sub


