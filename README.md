# PyCK-Expense-Tracker

Welcome to our Expense Tracking app!

We have to tried to keep things as simple as possible but you will have to pip install a few libraries in order for the application to work properly.
&nbsp;&nbsp;a) tkinter<br />
&nbsp;&nbsp;b) tkcalendar<br />
&nbsp;&nbsp;c) numpy<br />
&nbsp;&nbsp;d) matplotlib<br />
&nbsp;&nbsp;e) pandas<br />
&nbsp;&nbsp;f) sqlite3<br />

Once you have done that you can simply run the Expense_Tracker.py file

The GUI has been split into 3 tabs : Add Expense, Graph and Calculator.

<b>Expenses :</b><br /><br />
In order to add an expense you need to provide the date of the expense, the amount spent and a title for your own referral. Once you've done that, simply click on the 'Add' button. You can also add multiple expenses on the same day but remember to have different titles for each of them.
Your expense will be added to the database in the backend and you can also see it added to the Tree View just below the button.<br /><br />
The Tree View displays all the entries you've made in one session and will be resetted once you close the application. But the data will be safely stored in a database file in the same directory.<br /><br />
Below the tree lies the Progress Bar and the slider to adjust the Max Funds in the Progress Bar. The Progres Bar shows the percentage of Funds you've used up out of the Max Funds. It is there to give you a visual warning in case your expenses are about to exceed the Max Funds you have available.A label to the right has also been added for user convenience.<br /><br />
We realise that the Max Funds may vary for everyone and it may even vary between months/years. For this, we've added a slider just above the Progress Bar which allows the user to adjust the Max Funds Limit according to their requirements. The Progress Bar automatically adjusts to the new Max Funds that you've selected using the slider.

<b>Graph :</b><br /><br />
The Graph Tab is meant for diplaying a line graph of Expenses VS Date. All expenses added on any given date will be clubbed together and the sum will be plotted on the graph.
Initially, no graph will be displayed in the tab. To fix that, simply click on the 'View Graph' button and the graph will pop up below the button.
In order to refresh the graph after adding a new expense, simply click the 'View Graph' button.<br />

<b>Calculator :</b><br /><br />
We have also added a calculator for the convenience of the user. It can be used for all sorts of basic calculations that the user may require to calculate their expenses.

And yeah that's pretty much it. We tried to keep it as simple as possible but would love to implement some new features, which we couldn't due to the time constraint.<br /><br />
Hope this helps!
