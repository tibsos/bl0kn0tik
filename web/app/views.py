from django.shortcuts import render, get_object_or_404, HttpResponse
import json

from django.contrib.auth.decorators import login_required

from .models import *

@login_required
def home(request):

    user = request.user
    profile = request.user.profile

    c = {}
    
    c['profile'] = profile

    c['active_notepad'] = profile.active_notepad
    
    if profile.active_notepad:
        
        notepads = Notepad.objects.filter(creator = user).exclude(uid = profile.active_notepad.uid)
        notes = profile.active_notepad.notes.all()
        
        if not profile.premium:
            
            if len(notepads) > 0:
                            
                c['notepads'] = notepads[0]
            
            c['notes'] = notes[0:5]
            c['locked_notes'] = notes[5:]
        
        else: 
            
            c['notepads'] = notepads
            c['notes'] = notes

    if profile.active_note:
        
        c['active_note'] = profile.active_note
    
    return render(request, 'home.html', c)


@login_required
def search_note(request):
    
    q = request.POST.get('query', None)
    
    notes_title = Note.objects.filter(title__contains = q)
    notes_content = Note.objects.filter(content__contains = q)
    
    notes = set(list(notes_title) + list(notes_content))
    
    return render(request, 'components/search-results.html', {'search_results': notes})

@login_required
def create_notepad(request):

    user = request.user
    profile = request.user.profile

    rp = request.POST

    notepad = Notepad.objects.create(creator = user, title = rp.get('title'), color = rp.get('color'))
    note = Note.objects.create(creator = user, title = '', content = '')
    notepad.notes.add(note)

    profile.active_notepad = notepad
    profile.active_note = note
    profile.save()

    notepads = Notepad.objects.filter(creator = user)
    
    c = {}
    
    if not profile.premium:
        
        if len(notepads)>1:
            
            c['max_notepads'] = True

    c['active_notepad'] = notepad
    c['notepads'] = notepads.exclude(uid = notepad.uid)
    c['notes'] = notepad.notes.all()
    c['active_note'] = profile.active_note

    return render(request, 'components/notepad.html', c)

@login_required
def get_notepad(request, uid):

    user = request.user
    profile = request.user.profile

    notepad = get_object_or_404(Notepad, uid = uid)
    profile.active_notepad = notepad

    notes = notepad.notes.all()

    if len(notes)>0:

        profile.active_note = notes[0]
    
    else: 

        profile.active_note = None

    profile.save()

    c = {}

    c['active_notepad'] = notepad
    c['notepads'] = Notepad.objects.filter(creator = user).exclude(uid = notepad.uid)
    c['notes'] = notes
    c['active_note'] = profile.active_note

    return render(request, 'components/notepad.html', c)

@login_required
def edit_notepad(request):
    
    user = request.user 
    profile = user.profile
    
    rp = request.POST
    
    title = rp.get('title')
    color = rp.get('color')
    
    notepad = profile.active_notepad
    notepad.title = title
    notepad.color = color
    notepad.save()
    
    c = {}
    
    c['active_notepad'] = notepad
    c['notepads'] = Notepad.objects.filter(creator = user).exclude(uid = notepad.uid)

    return render(request, 'components/notepads.html', c)

@login_required
def delete_notepad(request):

    user = request.user
    profile = user.profile
    
    notepad = profile.active_notepad
    
    profile.active_notepad = None
    profile.save()
    
    notepad.delete()
    
    notepads = Notepad.objects.filter(creator = user)
    
    if len(notepads) > 0:
        
        profile.active_notepad = notepads[0]
        
        notes = notepads[0].notes.all()
        
        notepads = notepads.exclude(uid = notepads[0].uid)
        
        if len(notes) > 0:
            
            profile.active_note = notes[0]
        
        else:
            
            profile.active_note = None

    else:
        
        notepads = []
        notes = []
        profile.active_notepad = None
        profile.active_note = None
    
    profile.save()

    c = {}
    c['active_notepad'] = profile.active_notepad
    c['notepads'] = notepads
    c['notes'] = notes
    c['active_note'] = profile.active_note

    return render(request, 'components/notepad.html', c)

@login_required
def create_note(request):

    user = request.user
    profile = request.user.profile

    notes = profile.active_notepad.notes.all()
    
    if len(notes)>0:

        note = notes.get(active = True)
        note.active = False
        note.save()

    note = Note.objects.create(creator = user, title = '', content = '', active = True)
    profile.active_notepad.notes.add(note)

    profile.active_note = note
    profile.save()
    
    notes = profile.active_notepad.notes.all()
    
    if len(notes) > 4 and not profile.premium:

        c['max_notes'] = True
        
    c = {}

    c['active_notepad'] = profile.active_notepad
    c['notepads'] = Notepad.objects.filter(creator = user).exclude(uid = profile.active_notepad.uid)
    c['notes'] = notes
    c['active_note'] = note

    return render(request, 'components/notepad.html', c)

@login_required
def get_note(request, uid):

    user = request.user
    profile = request.user.profile

    note = profile.active_note
    note.active = False
    note.save()

    note = get_object_or_404(Note, uid = uid)
    note.active = True
    note.save()

    profile.active_note = note
    profile.save()

    c = {}

    c['active_notepad'] = profile.active_notepad
    c['notepads'] = Notepad.objects.filter(creator = user).exclude(uid = profile.active_notepad.uid)
    c['notes'] = profile.active_notepad.notes.all()
    c['active_note'] = note

    return render(request, 'components/notepad.html', c)

@login_required
def update_note(request):

    note = request.user.profile.active_note
    note.title = request.POST.get('title') 
    note.content = request.POST.get('content')
    note.save()

    return HttpResponse('K')

@login_required
def pin_note(request):

    user = request.user
    profile = user.profile

    note = profile.active_note
    note.pinned = not note.pinned
    note.save()

    c = {}

    c['active_notepad'] = profile.active_notepad
    c['notepads'] = Notepad.objects.filter(creator = user).exclude(uid = profile.active_notepad.uid)
    c['notes'] = profile.active_notepad.notes.all()
    c['active_note'] = profile.active_note

    return render(request, 'components/notepad.html', c)

@login_required
def move_note(request, uid):
    
    user = request.user
    profile = user.profile

    old_notepad = profile.active_notepad
    note = profile.active_note
    new_notepad = get_object_or_404(Notepad, uid = uid)
    
    old_notepad.notes.remove(note)
    new_notepad.notes.add(note)
    
    profile.active_notepad = new_notepad
    profile.save()
    
    c = {}

    c['notepads'] = Notepad.objects.filter(creator = user).exclude(uid = new_notepad.uid)
    c['active_notepad'] = new_notepad
    c['notes'] = new_notepad.notes.all()
    c['active_note'] = note
    
    
    return render(request, 'components/notepad.html', c)

@login_required
def delete_note(request):

    user = request.user
    profile = user.profile

    notepad = profile.active_notepad
    notepad.notes.remove(profile.active_note)
    profile.active_note.active = False
    profile.active_note.save()

    notes = notepad.notes.all()

    if len(notes)>0:

        profile.active_note = notes[0]
        notes[0].active = True
        notes[0].save()

    else:

        profile.active_note = None 

    profile.save()
    
    notepads = Notepad.objects.filter(creator = user).exclude(uid = notepad.uid)
    
    if not profile.premium:
        
        if len(notes) > 4:
            
            c['notes'] = notes[0:5]
            c['locked_notes'] = notes[5:]
        
        else:
            
            c['notes'] = notes
            
            
        if len(notepads) > 0:
                        
            c['notepads'] = notepads[0]
            c['locked_notepads'] = notepads[1:] 
        
    else:
        
        c['notepads'] = notepads
        c['notes'] = notes

    c = {}

    c['active_notepad'] = notepad
    c['active_note'] = profile.active_note

    return render(request, 'components/notepad.html', c)

@login_required
def upload_image(request):

    user = request.user
    profile = user.profile

    file = request.FILES.get('image')
    image = Image.objects.create(file = file)

    profile.active_note.images.add(image)

    notepads = Notepad.objects.filter(creator = user)
    if len(notepads) > 1:

        notepads = True

    else:

        notepads = False

    return render(request, 'components/note.html', {'active_note': profile.active_note, 'notepads': notepads})

@login_required
def delete_image(request, uid):

    user = request.user
    profile = user.profile

    get_object_or_404(Image, uid = uid).delete()

    notepads = Notepad.objects.filter(creator = user)

    if len(notepads) > 1:

        notepads = True
        
    else:

        notepads = False

    return render(request, 'components/note.html', {'active_note': profile.active_note, 'notepads': notepads})