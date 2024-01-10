import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from projects.models import Customer, Seller, Item, Notification, Favorite
from projects.forms import RegistrationCustomerForm, LoginCustomerForm, OTPVerificationCustomerForm, ItemForm, RegistrationSellerForm, LoginSellerForm, OTPVerificationSellerForm, EditSellerForm, ChangeCustomerImageForm, ReviewForm 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import timedelta
import re
from django.core.mail import send_mail
import random
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect

import json
from projects.models import * 
from projects.utils import cookieCart, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from django.template import loader
from datetime import timedelta

