from bs4 import BeautifulSoup as bs
import requests
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
from . models import *
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.core import serializers
import json
@csrf_exempt
def dashboard(request):
	user=get_object_or_404(user_auth,pk=request.POST['user_id'])
	if( user.user_pwd== request.POST['user_pwd']):
		data=serializers.serialize("json",user_auth.objects.filter(pk=user))
		
		return JsonResponse(json.loads(data)[0])
	else:
		return JsonResponse({"Error":"Login ERROR"})
@csrf_exempt
def tree_loc(request):
	if request.POST['create']=="No":
		user_name=get_object_or_404(user_auth,pk=request.POST.get("user_id",False))
		if user_name=="__all":
			trees=serializers.serialize("json",tree_data.objects.all())
		else:
			trees=serializers.serialize("json",tree_data.objects.filter(user=user_name))
		return HttpResponse(trees)
	elif request.POST['create']=="Yes":
		user_id=request.POST['user_id']
		tree_num=len(tree_data.objects.filter(user=user_id))+1
		tree_id=str(user_id)+'_'+tree_num
		tree_type=request.POST['tree_type']
		tree_lat=request.POST['tree_loc_lat']
		tree_long=request.POST['tree_loc_long']
		t=tree_data(user_id,tree_id,tree_type,datetime.now(),tree_lat,tree_long)
		t.save()
	else:
		return JsonResponse({"Error":"Create value not set."})
@csrf_exempt
def leaderboard(request):
	user_list=user_auth.objects.all()
	polls={}
	out=[]
	for user in user_list:
		polls[user.user_name]=user.points
	for w in sorted(polls, key=polls.get,reverse=True):
		out.append({w:polls[w]})

	return HttpResponse(out)
@csrf_exempt
def news(request):
	user=get_object_or_404(user_auth,pk=request.POST['user_id'])
	url1='http://www.indiaenvironmentportal.org.in/news/top/'
	url2='https://api.breezometer.com/baqi/?lat={}&lon={}&key=ef90b1d355fd4d05b610c217afbe8fbe'.format(user.user_loc_lat,user.user_loc_long)
	r1=requests.get(url1)
	r2=requests.get(url2).json()
	data={}
	count=1
	soup=bs(r1.content,'html.parser')
	list_news=soup.findAll('div',{'class':'text'})[:3]
	env_data={'aqi':r2['breezometer_aqi'],'description':r2['breezometer_description'],'effects':r2['dominant_pollutant_text']['effects']}
	for feeds in list_news:
		data['Heading'+str(count)]=feeds.h3.a.get_text()
		data['Link'+str(count)]=feeds.h3.a['href']
		count+=1
	data.update(env_data)
	return JsonResponse(data)	
