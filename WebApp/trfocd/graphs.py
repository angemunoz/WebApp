import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
# Scatterplot from Plotly Express (https://plotly.com/python/line-and-scatter/)
# Pie charts from Plotly Express(https://plotly.com/python/pie-charts/)
# Area chart from Plotly plotly.graph_objects (https://plotly.com/python/filled-area-plots/)
# Pandas to_date from Pandas Dataframe astype (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html)

def generateDailyScatter(dailyDF):

    # Create the scatter plot
    dailyScatter = px.scatter(
        dailyDF,
        x="datetimeTR",
        # Treat id as a string or y axis passes the numeric id positions
        y=dailyDF["id"].astype(str), 
        text="thought",
        title="Daily Thought and Safety Behaviour Scatter Plot"
    )

    # Set Behaviours to be distinct with a blue cross marker
    dailyScatter.update_traces(
        marker=dict(
            size=15,
            color="#0072B2",
            symbol="x"),
        showlegend=False,
        hovertemplate=None,
        # Set the text to rgb 0 meaning the text print wont be visible of the 
        # thought but is still available in the mouse over overlay.
        textfont=dict(color="rgba(0, 0, 0, 0)") 
    )

    # The overlay scatterplot for safety behaviour
    dailyScatter.add_scatter(
        x=dailyDF["datetimeSB"],
        y=dailyDF["id"],
        text=dailyDF["safetyBehaviour"],
        mode="markers",
        marker=dict(size=15, 
                    color="#D55E00"),
        showlegend=False
    )

    # Update the layout so nticks sets the breakpoints to 24
    dailyScatter.update_layout(
        xaxis=dict(
            title="DateTime",
            nticks=24
        ),
        yaxis=dict(
            title="Thought",
            # Remove labels since these could be very long
            showticklabels=False 
        )
    )

    # Code to format Plotly axis to show HH:MM
    # adapted from “How to format Plotly xaxis to be shown in H:M:S format” by Raymond, R.
    # accessed 15-09-23
    # https://stackoverflow.com/questions/71772450/how-to-format-plotly-xaxis-to-be-shown-in-hms-format
    #[[px.scatter(
        # table,
        # x=pd.to_datetime(table["time_seconds"],unit="s"),]]
    start_date = datetime.combine(dailyDF["datetimeTR"].max(), datetime.min.time()).date()
    # end of referenced code

    #setting the date range of the x axis. I take the "start date" which sets a min range of the date at 
    # midnight, and adds a day for the max of the range
    dailyScatter.update_xaxes(
        range=[datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S"), \
               datetime.strptime(f"{start_date} 00:00:00", "%Y-%m-%d %H:%M:%S") + timedelta(days=1)],
        tickformat="%H:%M" 
    )

    #scatter plot to html
    scatterHtml = dailyScatter.to_html()
    return scatterHtml



# Donut Plots

def generateDonutPlots(dailyDF):

    # Sum the duration
    addSafetyBU = dailyDF["durationSafetyB"].sum()

    # Check if the duration exceeds 24 hours
    if addSafetyBU > 24:
        # If duration is greater than 24, set addSafetyBUChecker to 1
        addSafetyBUChecker = 1
        # Set addSafetyBU to 24, the visual will not show the true number exceeding 24 hours
        addSafetyBU = 24

    else:
        # If duration is less than or equal to 24, set the addSafetyBUChecker to 0
        addSafetyBUChecker = 0
        # Repeat for all

    addSafetyBOP = dailyDF["durationSafetyBOP"].sum()
    if addSafetyBOP > 24:
        addSafetyBOPChecker = 1
        addSafetyBOP = 24
    else:
        addSafetyBOPChecker = 0

    combinedBUbop = addSafetyBU + addSafetyBOP
    if combinedBUbop > 24:
        combinedBUbopChecker = 1
        combinedBUbop = 24
    else:
        combinedBUbopChecker = 0

    # Convert the annotation of donuts to HH:MM format as a function
    # Repeat to all
    def convertToHHmm(hourDecimal):
        hours = int(hourDecimal)
        minutes = int((hourDecimal - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"


# B Donut Plot

    # Set the colours to be colour-blind friendly
    colours = ["#0072B2", "#D55E00"]

    # Create the Donut plot
    donutBU = px.pie(
        # Print the text in "" and then the remaining hours of the day which are not SB
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBU, 24 - addSafetyBU], 
        # This value turns it from a pie into a Donut
        hole=0.8, 
        title="My Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    # Annotate the Donut plot with overlay text
    donutBU.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBU)}",
        x=0.5,
        # Set the height of the "Other Hours" text which gets printed inside the Donut
        y=0.45,
        showarrow=False
    )

    # Annotate the Donut plot with overlay text
    donutBU.add_annotation(
        # Check if checker set to 1 previously
        # Change annotation to a warning
        # else shows the duration hours as HH:MM
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBUChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBU)}",
        x=0.5,
        # Set the height of the "Safety Behaviour Hours" text which gets printed inside the Donut
        y=0.55,
        showarrow=False
    )

    # Removes the hover over box
    donutBU.update_traces(hovertemplate = None,
                          hoverinfo = "skip") 

    donutBUHtml = donutBU.to_html() 
    # Repeat for all

# BOP Donut Plot

    #creating the Donut plot (same as before)
    donutBOP = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBOP, 24 - addSafetyBOP], 
        hole=0.8, 
        title="Their Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBOP.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBOP)}",
        x=0.5,
        y=0.45, 
        showarrow=False
    )

    donutBOP.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBOPChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBOP)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutBOP.update_traces(hovertemplate = None,
                           hoverinfo = "skip")

    donutBOPHtml = donutBOP.to_html() 

# Combined Donut Plot

    # Create the Donut plot (same as before)
    donutCombined = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[combinedBUbop, 24 - combinedBUbop],
        hole=0.8, 
        title="Our Combined Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutCombined.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - combinedBUbop)}",
        x=0.5, 
        y=0.45,
        showarrow=False
    )

    donutCombined.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if combinedBUbopChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(combinedBUbop)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutCombined.update_traces(hovertemplate = None,
                                hoverinfo = "skip")

    
    donutCombinedHtml = donutCombined.to_html()


    return donutBUHtml, donutBOPHtml, donutCombinedHtml


# Daily aggregate plot
def generateWeeklyDailyAggAreaPlot(WeekDailyAggDF):

    # Create a figure
    WeekArea = go.Figure()

    # Add lines for thought and safety behaviour
    WeekArea.add_trace(go.Scatter(x=WeekDailyAggDF["dateTR"], y=WeekDailyAggDF["id"], mode="none", name="id"))
    WeekArea.add_trace(go.Scatter(x=WeekDailyAggDF["dateTR"], y=WeekDailyAggDF["sb.id"], mode="none", name="sb.id"))

    # Set fill colours
    WeekArea.update_traces(fill="tozeroy", fillcolor="#0072B2", selector=dict(name="id"))
    WeekArea.update_traces(fill="tonexty", fillcolor="#D55E00", selector=dict(name="sb.id"))

    # Customize the plot layout
    WeekArea.update_layout(
        title="Weekly Area Chart",
        xaxis_title="Day",
        yaxis_title="Count",
        showlegend=False,
        autosize=True    
    )

    WeekAreaHtml = WeekArea.to_html()

    return WeekAreaHtml

def generateDonutPlotsWeekly(WeekDailyAggDF):

    # Check if the "dateTR" column contains valid date values
    if pd.to_datetime(WeekDailyAggDF["dateTR"], errors="coerce").notnull().any():
        # Calculate the difference in days if there are valid dates
        WeekDailyAggDFDays = (WeekDailyAggDF["dateTR"].max() - WeekDailyAggDF["dateTR"].min()).days
    else:
        # Return 1 if there are no valid dates
        WeekDailyAggDFDays = 1

    addSafetyBU = WeekDailyAggDF["durationSafetyB"].sum()/WeekDailyAggDFDays
    if addSafetyBU > 24:
        addSafetyBUChecker = 1
        addSafetyBU = 24
    else:
        addSafetyBUChecker = 0

    addSafetyBOP = WeekDailyAggDF["durationSafetyBOP"].sum()/WeekDailyAggDFDays
    if addSafetyBOP > 24:
        addSafetyBOPChecker = 1
        addSafetyBOP = 24
    else:
        addSafetyBOPChecker = 0

    combinedBUbop = addSafetyBU + addSafetyBOP
    if combinedBUbop > 24:
        combinedBUbopChecker = 1
        combinedBUbop = 24
    else:
        combinedBUbopChecker = 0

    def convertToHHmm(hourDecimal):
        hours = int(hourDecimal)
        minutes = int((hourDecimal - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"


#B Donut Plot (same as before)

    colours = ["#0072B2", "#D55E00"]

    # Create the Donut plot 
    donutBU = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBU, 24 - addSafetyBU], 
        hole=0.8,
        title="My Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBU.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBU)}",
        x=0.5,
        y=0.45,
        showarrow=False
    )

    donutBU.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBUChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBU)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutBU.update_traces(hovertemplate = None,
                          hoverinfo = "skip")

    
    WeeklydonutBUHtml = donutBU.to_html() 

# BOP Donut Plot

    # Create the donut plot (same as before)
    donutBOP = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBOP, 24 - addSafetyBOP],
        hole=0.8,
        title="Their Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBOP.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBOP)}",
        x=0.5,
        y=0.45,
        showarrow=False
    )

    donutBOP.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBOPChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBOP)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutBOP.update_traces(hovertemplate = None,
                           hoverinfo = "skip")

    
    WeeklydonutBOPHtml = donutBOP.to_html() 

# Combined Donut Plot

    # Create the Donut plot (same as before)
    donutCombined = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[combinedBUbop, 24 - combinedBUbop],
        hole=0.8, 
        title="Our Combined Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutCombined.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - combinedBUbop)}",
        x=0.5, 
        y=0.45, 
        showarrow=False
    )


    donutCombined.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if combinedBUbopChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(combinedBUbop)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutCombined.update_traces(hovertemplate = None,
                                hoverinfo = "skip")

    
    WeeklydonutCombinedHtml = donutCombined.to_html() 


    return WeeklydonutBUHtml, WeeklydonutBOPHtml, WeeklydonutCombinedHtml


def generateMonthlyDailyAggAreaPlot(MonthDailyAggDF):

    # Create a figure (same as before)
    MonthArea = go.Figure()

    MonthArea.add_trace(go.Scatter(x=MonthDailyAggDF["dateTR"], y=MonthDailyAggDF["id"], mode="none", name="id"))
    MonthArea.add_trace(go.Scatter(x=MonthDailyAggDF["dateTR"], y=MonthDailyAggDF["sb.id"], mode="none", name="sb.id"))

    MonthArea.update_traces(fill="tozeroy", fillcolor="#0072B2", selector=dict(name="id"))
    MonthArea.update_traces(fill="tonexty", fillcolor="#D55E00", selector=dict(name="sb.id"))

    MonthArea.update_layout(
        title="Monthly Area Chart",
        xaxis_title="Day",
        yaxis_title="Count",
        showlegend=False,
        autosize=True
    )

    MonthAreaHtml = MonthArea.to_html()

    return MonthAreaHtml

def generateDonutPlotsMonthly(MonthDailyAggDF):

    # Check if the "dateTR" column contains valid date values
    if pd.to_datetime(MonthDailyAggDF["dateTR"], errors="coerce").notnull().any():
        # Calculate the difference in days if there are valid dates
        MonthDailyAggDFDays = (MonthDailyAggDF["dateTR"].max() - MonthDailyAggDF["dateTR"].min()).days
    else:
        # Return 1 if there are no valid dates
        MonthDailyAggDFDays = 1

    addSafetyBU = MonthDailyAggDF["durationSafetyB"].sum()/MonthDailyAggDFDays
    if addSafetyBU > 24:
        addSafetyBUChecker = 1
        addSafetyBU = 24
    else:
        addSafetyBUChecker = 0

    addSafetyBOP = MonthDailyAggDF["durationSafetyBOP"].sum()/MonthDailyAggDFDays
    if addSafetyBOP > 24:
        addSafetyBOPChecker = 1
        addSafetyBOP = 24
    else:
        addSafetyBOPChecker = 0

    combinedBUbop = addSafetyBU + addSafetyBOP
    if combinedBUbop > 24:
        combinedBUbopChecker = 1
        combinedBUbop = 24
    else:
        combinedBUbopChecker = 0

    # Convert the annotation of donuts to HH:MM format
    def convertToHHmm(hourDecimal):
        hours = int(hourDecimal)
        minutes = int((hourDecimal - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"


# B Donut Plot (same as before)

    # Colours to use
    colours = ["#0072B2", "#D55E00"]

    # Create the Donut plot
    donutBU = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBU, 24 - addSafetyBU], 
        hole=0.8, #this value turns it from a pie into a Donut
        title="My Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBU.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBU)}",
        x=0.5,
        y=0.45, 
        showarrow=False
    )

    donutBU.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBUChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBU)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutBU.update_traces(hovertemplate = None,
                          hoverinfo = "skip")

    
    MonthlydonutBUHtml = donutBU.to_html() 

# BOP Donut Plot##

    # Create the Donut plot (same as before)
    donutBOP = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBOP, 24 - addSafetyBOP], 
        hole=0.8,
        title="Their Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBOP.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBOP)}",
        x=0.5,
        y=0.45,
        showarrow=False
    )

    donutBOP.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBOPChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBOP)}",
        x=0.5,
        y=0.55, 
        showarrow=False
    )

    donutBOP.update_traces(hovertemplate = None,
                           hoverinfo = "skip")

    
    MonthlydonutBOPHtml = donutBOP.to_html() 

# Combined Donut Plot##

    donutCombined = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[combinedBUbop, 24 - combinedBUbop],
        hole=0.8, 
        title="Our Combined Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutCombined.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - combinedBUbop)}",
        x=0.5, 
        y=0.45,
        showarrow=False
    )

    donutCombined.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if combinedBUbopChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(combinedBUbop)}",
        x=0.5,
        y=0.55, 
        showarrow=False
    )

    donutCombined.update_traces(hovertemplate = None,
                                hoverinfo = "skip")

    MonthlydonutCombinedHtml = donutCombined.to_html() 

    return MonthlydonutBUHtml, MonthlydonutBOPHtml, MonthlydonutCombinedHtml



# Yearly plots
def generateYearMonthlyAggAreaPlot(YearMonthAggDF):

    # function to handle converting month number to short text month
    def month_number_to_text(month_number):
        month_text = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return month_text[month_number - 1] if 1 <= month_number <= 12 else ""

    # Create a figure
    YearArea = go.Figure()

    # Add lines for thought and safety behaviour
    YearArea.add_trace(go.Scatter(x=YearMonthAggDF["month_number"].apply(month_number_to_text), \
                                  y=YearMonthAggDF["id"], mode="none", name="id"))
    YearArea.add_trace(go.Scatter(x=YearMonthAggDF["month_number"].apply(month_number_to_text), \
                                  y=YearMonthAggDF["sb.id"], mode="none", name="sb.id"))

    # setting colours
    YearArea.update_traces(fill="tozeroy", fillcolor="#0072B2", selector=dict(name="id"))
    YearArea.update_traces(fill="tonexty", fillcolor="#D55E00", selector=dict(name="sb.id"))

    # Customize the plot layout
    YearArea.update_layout(
        title="Yearly Area Chart",
        xaxis_title="Month",
        yaxis_title="Count",
        showlegend=False,
        autosize=True
    )

    YearAreaHtml = YearArea.to_html()

    return YearAreaHtml



def generateDonutPlotsYearly(YearMonthAggDFDonut):

    # Check duration (same as before)
    addSafetyBU = YearMonthAggDFDonut["durationSafetyB"].sum()/YearMonthAggDFDonut["days"].sum()
    if addSafetyBU > 24:
        addSafetyBUChecker = 1
        addSafetyBU = 24
    else:
        addSafetyBUChecker = 0

    addSafetyBOP = YearMonthAggDFDonut["durationSafetyBOP"].sum()/YearMonthAggDFDonut["days"].sum()
    if addSafetyBOP > 24:
        addSafetyBOPChecker = 1
        addSafetyBOP = 24
    else:
        addSafetyBOPChecker = 0

    combinedBUbop = addSafetyBU + addSafetyBOP
    if combinedBUbop > 24:
        combinedBUbopChecker = 1
        combinedBUbop = 24
    else:
        combinedBUbopChecker = 0

    # Convert the annotation of donuts to HH:MM format
    def convertToHHmm(hourDecimal):
        hours = int(hourDecimal)
        minutes = int((hourDecimal - hours) * 60)
        return f"{hours:02d}:{minutes:02d}"


# B Donut Plot (same as before)

    colours = ["#0072B2", "#D55E00"]

    donutBU = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBU, 24 - addSafetyBU], 
        hole=0.8, 
        title="My Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBU.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBU)}",
        x=0.5,
        y=0.45, 
        showarrow=False
    )

    donutBU.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBUChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBU)}",
        x=0.5,
        y=0.55, 
        showarrow=False
    )

    donutBU.update_traces(hovertemplate = None,
                          hoverinfo = "skip")

    YearlydonutBUHtml = donutBU.to_html() 

# BOP Donut Plot

    # Create the Donut plot (same as before)
    donutBOP = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[addSafetyBOP, 24 - addSafetyBOP], 
        hole=0.8,
        title="Their Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutBOP.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - addSafetyBOP)}",
        x=0.5,
        y=0.45,
        showarrow=False
    )

    donutBOP.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if addSafetyBOPChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(addSafetyBOP)}",
        x=0.5,
        y=0.55, 
        showarrow=False
    )

    donutBOP.update_traces(hovertemplate = None,
                           hoverinfo = "skip")

    
    YearlydonutBOPHtml = donutBOP.to_html() 

# Combined Donut Plot

    # Create the Donut plot (same as before)
    donutCombined = px.pie(
        names=["Safety Behaviour Hours", "Other Hours"],
        values=[combinedBUbop, 24 - combinedBUbop],
        hole=0.8, 
        title="Our Combined Daily Safety Behaviour Hours",
        color_discrete_sequence=colours
    )

    donutCombined.add_annotation(
        text=f"Other Hours: {convertToHHmm(24 - combinedBUbop)}",
        x=0.5, 
        y=0.45,
        showarrow=False
    )

    donutCombined.add_annotation(
        text="Safety Behaviour Hours exceed 24 hours" if combinedBUbopChecker == 1 
            else f"Safety Behaviour Hours: {convertToHHmm(combinedBUbop)}",
        x=0.5,
        y=0.55,
        showarrow=False
    )

    donutCombined.update_traces(hovertemplate = None,
                                hoverinfo = "skip")

    
    YearlydonutCombinedHtml = donutCombined.to_html() 


    return YearlydonutBUHtml, YearlydonutBOPHtml, YearlydonutCombinedHtml