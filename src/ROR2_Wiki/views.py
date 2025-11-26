from django.shortcuts import render
from django.views import generic
from .models import Monster, Item, Survivor

# ================================================================= #
#                      Homepage View                                  #
# ================================================================= #

def home(request):
    """
    View function for the home page of the site.
    """
    survivors = Survivor.objects.all()
    monsters = Monster.objects.all()
    items = Item.objects.all()

    context = {
        'survivors': survivors,
        'monsters': monsters,
        'items': items,
    }
    return render(request, 'home.html', context)

# ================================================================= #
#                      Survivor Views                                 #
# ================================================================= #

class SurvivorListView(generic.ListView):
    """
    Generic class-based view for a list of survivors.
    """
    model = Survivor
    template_name = 'survivors/survivor_list.html'
    context_object_name = 'survivors'

class SurvivorDetailView(generic.DetailView):
    """
    Generic class-based view for the details of a single survivor.
    """
    model = Survivor
    template_name = 'survivors/survivor_detail.html'
    context_object_name = 'survivor'

# ================================================================= #
#                       Monster Views                                 #
# ================================================================= #

class MonsterListView(generic.ListView):
    """
    Generic class-based view for a list of monsters.
    """
    model = Monster
    template_name = 'monsters/monster_list.html'
    context_object_name = 'monsters'

class MonsterDetailView(generic.DetailView):
    """
    Generic class-based view for the details of a single monster.
    """
    model = Monster
    template_name = 'monsters/monster_detail.html'
    context_object_name = 'monster'

# ================================================================= #
#                         Item Views                                  #
# ================================================================= #

class ItemListView(generic.ListView):
    """
    Generic class-based view for a list of items.
    """
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'

class ItemDetailView(generic.DetailView):
    """
    Generic class-based view for the details of a single item.
    """
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'

# ================================================================= #
#                      Context Processors                             #
# ================================================================= #

def survivor_classes(request):
    """
    Makes a list of all survivor classes available to all templates.
    """
    return {
        'survivor_classes': Survivor.objects.values_list('Class', flat=True).distinct()
    }