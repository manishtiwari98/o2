from django.db import models


class user_auth(models.Model):
	user_name=models.CharField(max_length=20,primary_key=True)
	user_pwd=models.CharField(max_length=100)
	full_name=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	points=models.IntegerField(default=0)
	age=models.IntegerField()
	user_loc_lat=models.CharField(max_length=15)	
	user_loc_long=models.CharField(max_length=15)	
	def __str__(self):
                return self.user_name
class tree_data(models.Model):
	user=models.ForeignKey(user_auth, on_delete=models.CASCADE)
	tree_id=models.CharField(max_length=30,primary_key=True)
	tree_type=models.CharField(max_length=30)
	tree_plant_time=models.DateTimeField(auto_now=True)	
	tree_loc_lat=models.CharField(max_length=15)
	tree_loc_long=models.CharField(max_length=15)
	def __str__(self):
		return self.tree_id

	
