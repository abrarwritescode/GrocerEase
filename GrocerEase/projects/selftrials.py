def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)  # so that project info contained thake 

    if request.method == 'POST':
        #print(request.POST) #prints in terminal
        form = ProjectForm(request.POST, request.FILES, instance=project) # instantiating PostForm class and passing requested data (request.data). passing instance so that it knows which project we will be updating
        if form.is_valid():
            form.save()
            return redirect('project') # name in url

    context = {'form':form}
    return render(request, 'projects/project_form.html', context)
