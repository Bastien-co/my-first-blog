from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement

# Create your views here.

def post_list(request):
    animals=Animal.objects.filter()
    equipements=Equipement.objects.filter()
    return render(request, 'blog/post_list.html', {'animals':animals,},{'equipements':equipements,})

def animal_detail(request, id_animal):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    lieu=animal.lieu
    message=''
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
    else:
        form = MoveForm()
    if form.is_valid():
        form.save(commit=False)
        nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
        if  nouveau_lieu.disponibilite=="libre" :
            if lieu.id_equip=="mangeoire":
                if nouveau_lieu.id_equip=="roue" :
                    animal.etat="fatigué"
                else :
                    message=animal.id_animal + " veut courir comme un fou dans son manège !"
            if lieu.id_equip=="roue":
                if nouveau_lieu.id_equip=="nid":
                    animal.etat="endormi"
                else:
                    message=animal.id_animal + " est fatigué !"
            if lieu.id_equip=="nid":
                if nouveau_lieu.id_equip=="litière":
                    animal.etat="affamé"
                else:
                    message=animal.id_animal + " veut faire sa grasse mat !"
            if lieu.id_equip=="litière":
                if nouveau_lieu.id_equip=="mangeoire":
                    animal.etat="repus"
                else : 
                    message=animal.id_animal + " a faim !"
            if message=="":
                ancien_lieu = get_object_or_404(Equipement, id_equip=lieu)
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()
                if nouveau_lieu.id_equip != "litière" :
                    nouveau_lieu.disponibilite="occupé"
                nouveau_lieu.save()
                animal.save()
                lieu=nouveau_lieu
        else : 
            message="Le "+nouveau_lieu.id_equip+" n'est pas disponible !"
        return render(request,'blog/animal_detail.html',{'animal': animal, 'lieu': lieu, 'form': form, 'message': message,'etat':animal.etat, 'photo':animal.photo})
    else:
        form = MoveForm()
        return render(request,'blog/animal_detail.html',{'animal': animal, 'lieu': lieu, 'form': form, 'message': message,'etat':animal.etat, 'photo':animal.photo})