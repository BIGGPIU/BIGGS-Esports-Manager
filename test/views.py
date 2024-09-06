from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Users
from .models import History
import os
from natsort import natsorted
from .yandev import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
# Create your views here.

def index(request):

    template = loader.get_template("main.html")
    namelist = GETnamesFROMdb()
    allinfo = GETallinfofromdb()
    spinfo = GETallSPinfofromdb()
    context = {
        "Name":namelist,
        "restartsignal":0,
        "leaderboardfill":allinfo,
        "spleaderboardfill":spinfo
               }

    if "create" in request.GET.keys():
        CREATEuserindb(request.GET)
        context["restartsignal"] = 1
    if "player1" in request.GET.keys():
        ADDgametodb(request.GET)
        context["restartsignal"] = 1
    if "tournament" in request.GET.keys():
        ADDSPtodb(request.GET)
        context["restartsignal"] = 1
    if "CreateNewRatingPeriod" in request.GET.keys():
        UPDATErankperiod()
        context["restartsignal"] = 1

    return HttpResponse(template.render(context,request))
