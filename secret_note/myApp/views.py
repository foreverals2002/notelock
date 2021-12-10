from django.shortcuts import render, redirect
from .forms import CustomUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.utils.timezone import now
from django.core.files.base import ContentFile
from django.core.files import File


from .models import Folder, Note

def main(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    folder_list = Folder.objects.filter(owner=request.user).order_by('-date_last_used')[:10]
    return render(request=request, template_name="myApp/index.html", context={"folder_list":folder_list})

def create_note_request(request, folder_name):
    if not request.user.is_authenticated:
        return redirect("/login/")
    folder_list = Folder.objects.filter(owner=request.user).order_by('-date_last_used')[:10]
    return render(request=request, template_name="myApp/new_note.html", context={"folder_list":folder_list, "folder_name":folder_name.strip(), "note_title":"note title", "note_content":"note content"})

def list_folders_request(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    folder_list = Folder.objects.filter(owner=request.user).order_by('-date_last_used')[:10]
    return render(request=request, template_name="myApp/folders.html", context={"folder_list":folder_list})


def view_note_content_request(request, folder_name, note_name):
    if not request.user.is_authenticated:
        return redirect("/login/")
    folder_list = Folder.objects.filter(owner=request.user).order_by('-date_last_used')[:10]
    reqNote = Note.objects.get(owner=request.user, folder_name=Folder.objects.get(owner=request.user, folder_name=folder_name), note_name=note_name)
    note_content = reqNote.file.open(mode='r').read()
    return render(request=request, template_name="myApp/index.html", context={"folder_list":folder_list, "folder_name":folder_name.strip(), "note_title":reqNote.note_name.strip(), "note_content":note_content.strip()})

def register_request(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return (redirect("/"))
        messages.error(request, "Unsuccessful registration.")
    form = CustomUserForm()
    return render(request=request, template_name="myApp/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="myApp/login.html", context={"login_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

def create_folder_request(request):
    user = request.user
    newFolder = Folder(folder_name=request.POST.__getitem__("folderName"), owner=user)
    newFolder.save()
    return redirect("/")

def view_folder_content(request, folder_name):
    folder_list = Folder.objects.filter(owner=request.user).order_by('-date_last_used')[:10]
    folder = Folder.objects.get(owner=request.user, folder_name=folder_name)
    note_list = Note.objects.filter(folder_name=folder)
    return render(request=request, template_name="myApp/note_list.html", context={"folder_list":folder_list, "note_list":note_list, "folder_name":folder_name})

def save_new_note_request(request):
    user = request.user
    folder_name_input = request.POST.__getitem__("folder_name_form")
    note_name_input = request.POST.__getitem__("note_title_form")
    note_content = request.POST.__getitem__("note_content_form")

    folder = Folder.objects.get(owner=request.user, folder_name=folder_name_input)

    f = ContentFile(note_content, note_name_input+'.txt')

    newNote = Note(note_name=note_name_input.strip(), owner=user, folder_name=folder, file=f)
    newNote.save()

    return redirect("/")

def note_update_request(request):
    user = request.user
    folder_name_input = request.POST.__getitem__("folder_name_form")
    note_name_input = request.POST.__getitem__("note_title_form")
    note_content = request.POST.__getitem__("note_content_form")

    folder = Folder.objects.get(owner=request.user, folder_name=folder_name_input)

    note = Note.objects.get(owner=user, folder_name=folder, note_name=note_name_input.strip())

    note.file.open(mode="w").write(note_content.strip())
    note.file.close()
    note.save()

    return redirect("/view_folder_content/"+folder_name_input)

def delete_folder_request(request, folder_name):
    Folder.objects.get(owner=request.user, folder_name=folder_name).delete()
    return redirect("/folders")

def delete_note_request(request, folder_name, note_name):
    folder = Folder.objects.get(owner=request.user, folder_name=folder_name)
    Note.objects.get(owner=request.user, folder_name=folder, note_name=note_name).delete()
    return redirect("/view_folder_content/" + folder_name)
