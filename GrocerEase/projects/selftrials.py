def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('project')
    context = {'object':project}
    return render(request, 'projects/deletetemplate.html', context)


