# Copyright (c) 2011-2013 Kunal Mehta. All rights reserved.
# Use of this source code is governed by a BSD License found in README.md.

from django import forms

from huxley.accounts.models import HuxleyUser
from huxley.core.models import *

import re

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class':'text empty'}), required=False)
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'text empty'}), required=False)

    def get_user(self):
        """ Note: Remember to validate first! """
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")

        if username and email:
            return HuxleyUser.objects.get(username=username, email=email)
        elif username:
            return HuxleyUser.objects.get(username=username)
        else:
            return HuxleyUser.objects.get(email=email)


    def reset_pass(self, user):
        """ Note: Remember to validate first! """
        new_pass = HuxleyUser.objects.make_random_password(length=10)
        user.set_password(new_pass)
        user.save()
        return new_pass


    # ===== VALIDATION =================================================
    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        # First check if at least one of the fields is provided
        if not (username or email):
            message = "You must fill at least one of the fields."
            if "all" in self._errors:
                self._errors["all"].append(message)
            else:
                self._errors["all"] = self.error_class([message])

        # Make sure user exists
        try:
            if username and email:
                HuxleyUser.objects.get(username=username, email=email)
            elif username:
                HuxleyUser.objects.get(username=username)
            else:
                HuxleyUser.objects.get(email=email)
        except:
            message = "Invalid username and/or email. Please try again."
            if "all" in self._errors:
                self._errors["all"].append(message)
            else:
                self._errors["all"] = self.error_class([message])
            if username in cleaned_data:
                del cleaned_data["username"]
            if email in cleaned_data:
                del cleaned_data["email"]

        # Always return cleaned_data
        return cleaned_data
