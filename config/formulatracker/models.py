from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

# Unit of Measurement Choices For User To Choose From
UNIT_CHOICE = (
    ('METRIC', 'Metric'),
    ('IMPERIAL', 'Imperial'),
)

'''
User Database 

- Extended the generic User class from Django to include a few custom fields 
'''
class User(AbstractUser):
    feed_goal = models.SmallIntegerField(default=0,null=True)
    child_name = models.CharField(max_length=50, default='Child', null=True)
    units = models.CharField(max_length=8,choices=UNIT_CHOICE,default='Metric')
    
    # Initialize default of child's name field
    def __getattribute__(self, name):
        attr = models.Model.__getattribute__(self, name)
        if name == 'child_name' and not attr:
            return 'Child'
        return attr

    def __str__(self):
        return f'{self.username}'


'''
Main Dashboard for User feedings 
- Allows for user entries
- Log with all user entries for day, includes a filter to allow user to filter by date
- Feed Log Visualization via Graphs.js
- Feed Conversion Rate: gives users (who are using feeding pumps) and a quick and easy way to get the feeding rate based on feed amount and duration of feed
'''
class FormulaLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time_of_feed = models.TimeField(null=True)
    feed_amount = models.PositiveSmallIntegerField(null=True)
    date = models.DateField(null=True)
    date_created = models.DateField(auto_now_add=True,null=True)

    @property
    def current_date(self):
        return date.today()
    
    def __str__(self):
        return f'{self.feed_amount} - {self.date_created}'

"""
User Weight Dashboard

- Allows user to enter weight of child

- Log that shows date of entry and weight 

- Graph for visual representaion of logged entries
"""
class Weight(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    weight = models.FloatField(null=True)
    date = models.DateField(null=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.weight} - {self.date}'





