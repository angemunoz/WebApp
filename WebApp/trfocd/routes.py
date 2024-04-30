from flask import render_template, url_for, request, redirect
from trfocd import app, db
from trfocd.models import User, ThoughtRecord, SafetyBehaviour
from trfocd.forms import SignInForm, SignUpForm, ThoughtRecordForm, SafetyBehaviourForm, SelectDateForm
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import desc
import pandas as pd
from trfocd.graphs import generateDailyScatter, generateDonutPlots, generateWeeklyDailyAggAreaPlot, generateMonthlyDailyAggAreaPlot, generateYearMonthlyAggAreaPlot, generateDonutPlotsWeekly, generateDonutPlotsMonthly, generateDonutPlotsYearly
from datetime import datetime

# Flask from Flask (https://flask.palletsprojects.com/en/2.3.x/quickstart/).
# Flask log in  from Flask-login (https://flask-login.readthedocs.io/en/stable/)
# SQLALchemy from SQLAlchemy SQL Element (https://docs.sqlalchemy.org/en/14/core/sqlelement.html)
# SQLAlchemy queries from SQLAlchemy Query (https://docs.sqlalchemy.org/en/14/orm/query.html)
# Flask WTForms from Flask-WTF (https://flask-wtf.readthedocs.io/en/1.1.x/quickstart/)
# Pandas "DataFrame" from Pandas DataFrame (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
    # "astype", "to_datetime", "to_numeric" from Pandas Dataframe astype (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.astype.html)
    # "fillna" from Pandas Dataframe fillna (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html)
    # "drop" from Pandas Dataframe drop (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html)
    # "sort_values" from Pandas DataFrame sort_values (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html)
    # "rename" from Pandas DataFrame rename (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html)
    # "apply" from Pandas DataFrame apply (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.apply.html)
    # "to_html" from Pandas DataFrame to_html (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_html.html)
    # "groupby" from Pandas DataFrame groupby (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)
    # "agg" from Pandas DataFrame agg (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.agg.html)
    # "reset_index" from Pandas DataFrame reset_index (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.reset_index.html)
    # "sum" from Pandas DataFrame sum (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sum.html)


# Set the base url to home.
@app.route("/")


# Set the route to navigate to home.
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


# Set customized error page for 401, Unauthorized.
@app.errorhandler(401)
def unauthorized_error(error):
    return render_template("notAuthorized.html"), 401


# Set customized error page for 404, Not Found.
@app.errorhandler(404)
def notFound_error(error):
    return render_template("notFound.html"), 404


# Set Not Authorized page to be accesed by current user id verification fails.
@app.route("/notAuthorized")
def notAuthorized():
    return render_template("notAuthorized.html")


# Set route for the sign up page.
@app.route("/signUp", methods=["GET", "POST"])
def signUp():
    
    # Instatiate form.
    form = SignUpForm()

    # Validation set on forms.py.
    # If validation fails it will not submit to database.
    if form.validate_on_submit():

        # Code to parametrize queries to protect against SQL Injection
        # adapted from "Protecting Your Code from SQL Injection Attacks When Using Raw SQL in Python" by Amezola, M.
        # accessed 05-07-23
        # https://medium.com/@miguel.amezola/protecting-your-code-from-sql-injection-attacks-when-using-raw-sql-in-python-916466961c97
        #[[with mysql.connector.connect(user="user", password="password", host="host", database="database") as conn:]]
        user = User(username=form.username.data, name=form.name.data, email=form.email.data, password=form.password.data, 
                    disclaimer=form.disclaimer.data)
        # end of referenced code
        db.session.add(user)
        db.session.commit()

        # Redirect to sign in page
        return redirect(url_for("signIn"))
    return render_template("signUp.html", title="Sign Up", form=form)


# Set route for the sign in page
@app.route("/signIn",methods=["GET","POST"])
def signIn():
    
    form = SignInForm()
    # Set error to empty string as it has to be instantiated.
    error = ""

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        # Check the user exist and the password is correct.
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("dailyPage"))
        
        else:
            # Display error message if validation fails, without informing which part failed.
            error = "Incorrect email or password."

    return render_template("signIn.html",title="Sign In",form=form, error=error)


# Route for logging the user out.
@app.route("/signOut",methods=["GET","POST"])
def logOut():
    logout_user()

    return redirect(url_for("home"))


# Route for adding a new thought record.
@app.route("/addThoughtRecord", methods=["GET", "POST"])
# Only registered users can access.
@login_required
def addThoughtRecord():

    form = ThoughtRecordForm()
    
    # Instantiate current user id and thought record id.
    createdby_id = current_user.id
    thoughtRecordInput = ThoughtRecord(id=0)
    
    if form.validate_on_submit():
        thoughtRecordInput = ThoughtRecord(userIdforTR=current_user.id, dateTR=form.dateTR.data, timeTR=form.timeTR.data, 
                                           situation=form.situation.data, thought=form.thought.data, feelings=form.feelings.data, 
                                           feelingsStrength=form.feelingsStrength.data, forEvidence=form.forEvidence.data, 
                                           forEvidenceStrength=form.forEvidenceStrength.data, againstEvidence=form.againstEvidence.data, 
                                           againstEvidenceStrength=form.againstEvidenceStrength.data, 
                                           altThought=form.altThought.data, altFeelings=form.altFeelings.data, 
                                           altFeelingsStrength=form.altFeelingsStrength.data)
        db.session.add(thoughtRecordInput)
        db.session.commit()

        # If save clicked, redirect to daily page.
        if "save" in request.form:
            return redirect(url_for("dailyPage"))
        
        # Else if saveContinue clicked redired to "addSafetyBehaviour", passing the user id and thought id.
        elif "saveContinue" in request.form:
            #print(thoughtRecordInput.id)
            return redirect (url_for("addSafetyBehaviour", createdby_id=createdby_id, thought_id=thoughtRecordInput.id))
        
    return render_template("addThoughtRecord.html", title="Add New Thought Record", form=form, thoughtRecordInput=thoughtRecordInput, createdby_id=createdby_id)


# Route for selecting a thought record to link to new safety behaviours
@app.route("/selectThoughtRecord", methods=["GET", "POST"])
@login_required
def selectThoughtRecord():

    form=SelectDateForm()

    if form.validate_on_submit:
        # Get the selected date from the form data
        selectDate= form.selectDate.data

    # Query the ThoughtRecord table by current user id and selected date and order by date (descending), return all data.
    thoughtRecordList = ThoughtRecord.query.filter_by(userIdforTR=current_user.id, dateTR=selectDate).order_by(desc(ThoughtRecord.dateTR)).all()
    #Instantiate dictionary for safety behaviour data.
    safetyBehaviourDict = {}

    # Loop the thoughtRecordList and query the safetyBehaviour table by thoughtId from ThoughtRecord matching thoughtByU in SafetyBehaviour.
    # Update the dictionary.
    for thoughtByU in thoughtRecordList:
        checkIds = SafetyBehaviour.query.filter_by(thoughtId=thoughtByU.id)
        safetyBehaviourDict [thoughtByU.id] = checkIds

    return render_template("selectThoughtRecord.html", form=form, thoughtRecordList=thoughtRecordList, safetyBehaviourDict=safetyBehaviourDict) 


# Route for adding safety behaviours, linked to thought records and user
# Code to link safety behaviours to userID and thoughtRecord
# adapted from "How to Use Flask-SQLAlchemy to Interact with Databases in a Flask Application" by Dyouri, A.
# accessed 07-08-23
# https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application
# [[@app.route("/<int:student_id>/")]]
@app.route("/addSafetyBehaviour/<int:thought_id>/<int:createdby_id>", methods=["GET", "POST"])
# end of referenced code
@login_required
def addSafetyBehaviour(thought_id, createdby_id):

    # If the current user did not create the thought do not allow them to load page.
    if createdby_id != current_user.id:
        return redirect(url_for("notAuthorized"))
    
    # Get the information from the thought record that this entry will be linked to for displaying.
    recogThought=ThoughtRecord.query.get(thought_id)

    form=SafetyBehaviourForm()

    if form.validate_on_submit():
        safetyBehaviourInput = SafetyBehaviour(userIdforSB=current_user.id, thoughtId=thought_id, dateSB=form.dateSB.data, 
                                                timeSB=form.timeSB.data, safetyBehaviour=form.safetyBehaviour.data, 
                                                durationSafetyBhr=form.durationSafetyBhr.data,  
                                                durationSafetyBmin=form. durationSafetyBmin.data, 
                                                durationSafetyBOPhr=form.durationSafetyBOPhr.data, 
                                                durationSafetyBOPmin=form.durationSafetyBOPmin.data, 
                                                thoughtAfterSB=form.thoughtAfterSB.data, feelingsAfterSB=form.feelingsAfterSB.data, 
                                                feelingsAfterSBStrength=form.feelingsAfterSBStrength.data)
        db.session.add(safetyBehaviourInput)
        db.session.commit()

        return redirect(url_for("dailyPage"))
    
    return render_template("addSafetyBehaviour.html", title="Add New Safety Behaviour", form=form, recogThought=recogThought)


# Route for daily page. Includes daily views
@app.route("/dailyPage",methods=["GET","POST"])
@login_required
def dailyPage():
    form = SelectDateForm()
    # Instantiate a list for joined thought records and safety behaviours.
    recordBehavioursList = []
    # Instantiate a list for processing data from the database.
    recordBehaviours = []  
    # Specify the selected date as today.
    selectDate = datetime.now().date()

    # Query ThoughtRecord table and Safety Behaviour table and join them by matching ids, then filter by user and date.
    recordBehaviours = db.session.query(ThoughtRecord, SafetyBehaviour).outerjoin(SafetyBehaviour, ThoughtRecord.id == SafetyBehaviour.thoughtId). \
    filter(ThoughtRecord.userIdforTR == current_user.id, ThoughtRecord.dateTR == selectDate).all()

    if form.validate_on_submit():
        # Get the selected date from the form data
        selectDate = form.selectDate.data

        # Filter ThoughtRecord objects by user ID and date
        recordBehaviours = db.session.query(ThoughtRecord, SafetyBehaviour).outerjoin(SafetyBehaviour, ThoughtRecord.id == SafetyBehaviour.thoughtId). \
            filter(ThoughtRecord.userIdforTR == current_user.id, ThoughtRecord.dateTR == selectDate).all()

    # Create joined data for further processing by pandas as dailyDF, either from default or from SelectDateForm.
    # If there are thought records but not safety behaviours then leave as None.
    for thought, behaviour in recordBehaviours:
        recordBehavioursJoined = {
            "id": thought.id, "thought": thought.thought, "dateTR": thought.dateTR, "timeTR": thought.timeTR,
            "safetyBehaviour": behaviour.safetyBehaviour if behaviour else None, "dateSB": behaviour.dateSB if behaviour else None,
            "timeSB": behaviour.timeSB if behaviour else None, "durationSafetyBhr": behaviour.durationSafetyBhr if behaviour else None,
            "durationSafetyBmin": behaviour.durationSafetyBmin if behaviour else None, "durationSafetyBOPhr": behaviour.durationSafetyBOPhr if behaviour else None,
            "durationSafetyBOPmin": behaviour.durationSafetyBOPmin if behaviour else None
        }

        # Add the result of the for loop to the list for joined data.
        recordBehavioursList.append(recordBehavioursJoined)

    # check if there is any data in recordBehavioursList.
    if len(recordBehavioursList) > 0:

        # Converting the joined list to a pandas DataFrame.
        dailyDF = pd.DataFrame(recordBehavioursList)

        # Code to combine date and time into datetime
        # adapted from “Combine Date and Time columns using pandas” by McKinney, T. and Hayden, A.
        # accessed 30-08-23
        # https://stackoverflow.com/questions/17978092/combine-date-and-time-columns-using-pandas
        #[[ In [12]: pd.to_datetime(df["Date"] + " " + df["Time"]) ]]

        # Concatenating thought records and safety behaviours time and date columns into two datetime columns of data.
        # Must be turned into a string for editing before it becomes a datetime type.
        dailyDF["datetimeTR"] = pd.to_datetime(dailyDF["dateTR"].astype(str) + " " + dailyDF["timeTR"].astype(str), format="%Y-%m-%d %H:%M:%S")
        dailyDF["datetimeSB"] = pd.to_datetime(dailyDF["dateSB"].astype(str) + " " + dailyDF["timeSB"].astype(str), errors="coerce", format="%Y-%m-%d %H:%M:%S")
        # end of referenced code

        # Adding durations by users and by other people hours and minutes together.
        # Convert minutes to a fraction of hours (not minutes).
        dailyDF["durationSafetyB"] = dailyDF["durationSafetyBhr"] + dailyDF["durationSafetyBmin"] / 60
        dailyDF["durationSafetyBOP"] = dailyDF["durationSafetyBOPhr"] + dailyDF["durationSafetyBOPmin"] / 60
        
        # Code to replace NaN with 0
        # adapted from “How to replace NaN values by Zeroes in a column of a Pandas Dataframe?” by johnDanger and Aman
        # accessed 20-09-23
        # https://stackoverflow.com/questions/13295735/how-to-replace-nan-values-by-zeroes-in-a-column-of-a-pandas-dataframe
        #[[ In [12]: df[1].fillna(0, inplace=True) ]]
        # Handling NaNs to 0 where there are thoughts with no safety behaviours
        dailyDF["durationSafetyB"].fillna(0, inplace=True)  
        dailyDF["durationSafetyBOP"].fillna(0, inplace=True) 
        # end of referenced code

        # Ensure duration is integer.
        dailyDF["durationSafetyB"] = pd.to_numeric(dailyDF["durationSafetyB"], errors="coerce")
        dailyDF["durationSafetyBOP"] = pd.to_numeric(dailyDF["durationSafetyBOP"], errors="coerce")

        # Drop columns not needed anymore
        dailyDF = dailyDF.drop(columns=["dateTR", "timeTR", "dateSB", "timeSB", "durationSafetyBhr", "durationSafetyBmin", "durationSafetyBOPhr", "durationSafetyBOPmin"])

        # Sort the dailyDF by datetime first for Thought and then Behaviour
        # Printed table is ordered by datetime.
        dailyDF = dailyDF.sort_values(by=["datetimeTR", "datetimeSB"])

        # Retrieve generateDailyScatter and generateDonutPlots using dailyDF as the parameter.
        # Assign result to variable.
        scatterHtml = generateDailyScatter(dailyDF)
        donutBUHtml, donutBOPHtml, donutCombinedHtml = generateDonutPlots(dailyDF)
        
        dailyTableDF = dailyDF.drop(columns=["id"])

        # Add the values by users and by other people.
        dailyTableDF["Duration Combined"] = dailyTableDF["durationSafetyB"] + dailyTableDF["durationSafetyBOP"]

        # Columns to print in the table.
        dailyTableDF = dailyTableDF.rename(columns={"datetimeTR": "Thought date and time", "thought": "Intrusive Thought", "datetimeSB": "Behaviour date and time", 
                                                    "safetyBehaviour": "Safety Behaviour", "durationSafetyB": "Duration by User (HH:MM)",
                                                    "durationSafetyBOP": "Duration by Other (HH:MM)", "Duration Combined": "Duration Combined (HH:MM)"})


        # Code to convert integers to hours and minutes
        # adapted from “How do I convert seconds to hours, minutes and seconds?” by JayRizzo and naïve decoder
        # accessed 13-09-23
        # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
        #[[ def sec_to_hours(seconds):
            # a=str(seconds//3600)
            # b=str((seconds%3600)//60)
            # c=str((seconds%3600)%60)
            # d=["{} hours {} mins {} seconds".format(a, b, c)]
            # return d ]]
        # Convert hour decimals to HH:MM
        def convertToHHmm(hh_decimal):
            hours = int(hh_decimal)
            minutes = int((hh_decimal - hours) * 60)
            return f"{hours:02d}:{minutes:02d}"
        # end of referenced code

        # Use convertToHHmm on the information on the table.
        dailyTableDF["Duration by User (HH:MM)"] = dailyTableDF["Duration by User (HH:MM)"].apply(convertToHHmm)
        dailyTableDF["Duration by Other (HH:MM)"] = dailyTableDF["Duration by Other (HH:MM)"].apply(convertToHHmm)
        dailyTableDF["Duration Combined (HH:MM)"] = dailyTableDF["Duration Combined (HH:MM)"].apply(convertToHHmm)

        # Reorder columns so they print in order.
        dailyTableDF = dailyTableDF[["Thought date and time", "Intrusive Thought", "Behaviour date and time", "Safety Behaviour", "Duration by User (HH:MM)",
                                     "Duration by Other (HH:MM)", "Duration Combined (HH:MM)"]]


        # dailyDF to html for the thought-behaviour table
        tableHtml = dailyTableDF.to_html()


        thoughtRecordList = ThoughtRecord.query.filter_by(userIdforTR=current_user.id, dateTR=selectDate).order_by(desc(ThoughtRecord.dateTR)).all()
        safetyBehaviourList = {}

        for thoughtByU in thoughtRecordList:
            checkIds = SafetyBehaviour.query.filter_by(thoughtId=thoughtByU.id)
            safetyBehaviourList [thoughtByU.id] = checkIds
        
        return render_template("dailyPage.html", title="Daily Page", form=form, thoughtRecordList=thoughtRecordList, safetyBehaviourList=safetyBehaviourList, scatterHtml=scatterHtml, donutBUHtml=donutBUHtml, donutBOPHtml=donutBOPHtml, donutCombinedHtml=donutCombinedHtml, tableHtml=tableHtml)
    else:
        return render_template("dailyPage.html", title="Daily Page", form=form)


@app.route("/progressPage", methods=["GET","POST"])
@login_required
def progressPage():
    form = SelectDateForm()
    recordBehavioursList = []
    recordBehaviours = []  
    # specify the selected date as today
    selectDate = datetime.now().date()
    
    year_of_selectDate = selectDate.year # for filtering data to year
    month_of_selectDate = selectDate.month # for filtering data to month
    week_of_selected_date = selectDate.isocalendar()[1] # for filtering data to week

    recordBehaviours = db.session.query(ThoughtRecord, SafetyBehaviour).outerjoin(SafetyBehaviour, ThoughtRecord.id == SafetyBehaviour.thoughtId). \
            filter(ThoughtRecord.userIdforTR == current_user.id, ThoughtRecord.dateTR.like(f"%{year_of_selectDate}%")).all()


    if form.validate_on_submit():
        # gather the selected date from the date picker
        selectDate = form.selectDate.data

        year_of_selectDate = selectDate.year # for filtering data to year
        month_of_selectDate = selectDate.month # for filtering data to month
        week_of_selected_date = selectDate.isocalendar()[1] # for filtering data to week

        # filter ThoughtRecord objects by user ID and year using "year_of_selectDate"
        recordBehaviours = db.session.query(ThoughtRecord, SafetyBehaviour).outerjoin(SafetyBehaviour, ThoughtRecord.id == SafetyBehaviour.thoughtId). \
            filter(ThoughtRecord.userIdforTR == current_user.id, ThoughtRecord.dateTR.like(f"%{year_of_selectDate}%")).all()
            
    # create joined data for further processing by pandas as dailyDF, either from default or from SelectDateForm
    for thought, behaviour in recordBehaviours:
        recordBehavioursJoined = {
            "id": thought.id,
            "thought": thought.thought,
            "dateTR": thought.dateTR,
            "week_number": thought.dateTR.isocalendar()[1],
            "month_number": thought.dateTR.month, 
            "sb.id": behaviour.id if behaviour else None,
            "safetyBehaviour": behaviour.safetyBehaviour if behaviour else None,
            "dateSB": behaviour.dateSB if behaviour else None,
            "durationSafetyBhr": behaviour.durationSafetyBhr if behaviour else None,
            "durationSafetyBmin": behaviour.durationSafetyBmin if behaviour else None,
            "durationSafetyBOPhr": behaviour.durationSafetyBOPhr if behaviour else None,
            "durationSafetyBOPmin": behaviour.durationSafetyBOPmin if behaviour else None
        }
    
        recordBehavioursList.append(recordBehavioursJoined)

    # check if any data in recordBehaviourList
    if len(recordBehavioursList) > 0:

        # converting the joined to a pandas ProgressDF
        ProgressDF = pd.DataFrame(recordBehavioursList)
        ProgressDF = ProgressDF.sort_values(by=["dateTR"])

        # performing some transformation operations for the Doughnut plots
        # adding B or BOP hours and minutes together whilst converting minutes to a fraction of hours (not minutes)
        ProgressDF["durationSafetyB"] = ProgressDF["durationSafetyBhr"] + ProgressDF["durationSafetyBmin"] / 60
        ProgressDF["durationSafetyBOP"] = ProgressDF["durationSafetyBOPhr"] + ProgressDF["durationSafetyBOPmin"] / 60

        # Handle NaN errors
        ProgressDF["durationSafetyB"].fillna(0, inplace=True)
        ProgressDF["durationSafetyBOP"].fillna(0, inplace=True)

        # Ensure these values are stored as numeric
        ProgressDF["durationSafetyB"] = pd.to_numeric(ProgressDF["durationSafetyB"], errors="coerce")
        ProgressDF["durationSafetyBOP"] = pd.to_numeric(ProgressDF["durationSafetyBOP"], errors="coerce")

        # Code to perform counts and sums
        # adapted from “Group dataframe and get sum AND count?” by MLAlex
        # accessed 14-09-23
        # https://stackoverflow.com/questions/38174155/group-dataframe-and-get-sum-and-count
        #[[df.groupby(df["L2 Name"])[["Amount arrear","VSU"]].agg(["sum","count"]) ]]
            # Setting up DailyAggDF which can be used directly in the Week and Month Daily Aggregate calculations
        DailyAggDF = ProgressDF.groupby("dateTR").agg({
        "durationSafetyB": "sum", "durationSafetyBOP": "sum",
        # Perform distinct count
        "id": "nunique",
        # Perform row count
        "sb.id": "size",
        # Keep number using "first"
        "week_number": "first", "month_number": "first"
        }).reset_index()
        # end of referenced code

        # Select the currently selected week of data for the Weekly View
        WeekDailyAggDF = DailyAggDF[DailyAggDF["week_number"] == week_of_selected_date][["dateTR", "week_number", "id", "sb.id", "durationSafetyB", "durationSafetyBOP"]]        

        # Select the currently selected month of data for the Monthly View
        MonthDailyAggDF = DailyAggDF[DailyAggDF["month_number"] == month_of_selectDate][["dateTR", "month_number", "id", "sb.id", "durationSafetyB", "durationSafetyBOP"]]

        # Data for year doesnt need selecting by date ranges since the current year was selected above using "ThoughtRecord.dateTR.like(f"%{year_of_selectDate}%")).all()"
        YearMonthAggDF = DailyAggDF[["dateTR", "month_number", "id", "sb.id", "durationSafetyB", "durationSafetyBOP"]]

        # Further aggregating the Yearly data from day to Month using month_number
        # Row counts and distinct counts have been done by day, so only need to sum
        YearMonthAggDF = YearMonthAggDF.groupby("month_number").agg({
        "durationSafetyB": "sum",
        "durationSafetyBOP": "sum",
        "id": "sum",
        "sb.id": "sum",
        "dateTR": "max"
        }).reset_index()

        # DateTR column to datetime
        YearMonthAggDF["dateTR"] = pd.to_datetime(YearMonthAggDF["dateTR"])

        # Year and month from the dateTR column
        YearMonthAggDF["year"] = YearMonthAggDF["dateTR"].dt.year
        YearMonthAggDF["month"] = YearMonthAggDF["dateTR"].dt.month

        # New column for the first day of each month
        YearMonthAggDF["first_day_of_month"] = pd.to_datetime(YearMonthAggDF["year"].astype(str) + "-" + YearMonthAggDF["month"].astype(str) + "-01")

        # Code to calculate dates between the 1st and the last day of the month
        # adapted from “How to calculate number of days between two given dates” by Gupta, A.
        # accessed 14-09-23
        # https://stackoverflow.com/questions/151199/how-to-calculate-number-of-days-between-two-given-dates
        #[[dt = pd.to_datetime("2008/08/18", format="%Y/%m/%d")
        #dt1 = pd.to_datetime("2008/09/26", format="%Y/%m/%d")
        #(dt1-dt).days
        #]]
        YearMonthAggDF["days"] = (YearMonthAggDF["dateTR"] - YearMonthAggDF["first_day_of_month"]).dt.days
        # end of referenced code

        # Dropping columns not used anymore
        YearMonthAggDF = YearMonthAggDF.drop(columns=["year", "month", "first_day_of_month"])
    
        # Data for yearly donut needs to be aggregated again but this time not grouped by after being used in the area plot
        YearMonthAggDFDonut = pd.DataFrame({
            "durationSafetyB": [YearMonthAggDF["durationSafetyB"].sum()],
            "durationSafetyBOP": [YearMonthAggDF["durationSafetyBOP"].sum()],
            "days": [YearMonthAggDF["days"].sum()]
        })

        # Retrieve generators and generateDonutPlots using their brnaches of the dataframe as the parameter.
        WeekAreaHtml = generateWeeklyDailyAggAreaPlot(WeekDailyAggDF)
        MonthAreaHtml = generateMonthlyDailyAggAreaPlot(MonthDailyAggDF)
        YearAreaHtml = generateYearMonthlyAggAreaPlot(YearMonthAggDF)

        # Assign result to variable.
        WeeklydonutBUHtml, WeeklydonutBOPHtml, WeeklydonutCombinedHtml = generateDonutPlotsWeekly(WeekDailyAggDF)
        MonthlydonutBUHtml, MonthlydonutBOPHtml, MonthlydonutCombinedHtml = generateDonutPlotsMonthly(MonthDailyAggDF)
        YearlydonutBUHtml, YearlydonutBOPHtml, YearlydonutCombinedHtml = generateDonutPlotsYearly(YearMonthAggDFDonut)

        return render_template("progressPage.html", title="Progress Page", form=form, WeekAreaHtml = WeekAreaHtml, WeeklydonutBUHtml = WeeklydonutBUHtml, WeeklydonutBOPHtml = WeeklydonutBOPHtml,
                               WeeklydonutCombinedHtml = WeeklydonutCombinedHtml,MonthAreaHtml = MonthAreaHtml, MonthlydonutBUHtml = MonthlydonutBUHtml, MonthlydonutBOPHtml = MonthlydonutBOPHtml,
                                MonthlydonutCombinedHtml = MonthlydonutCombinedHtml, YearAreaHtml = YearAreaHtml, YearlydonutBUHtml = YearlydonutBUHtml,
                                YearlydonutBOPHtml = YearlydonutBOPHtml, YearlydonutCombinedHtml = YearlydonutCombinedHtml)

    else:
        return render_template("progressPage.html", title="Progress Page", form=form)