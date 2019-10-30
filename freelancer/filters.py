from freelancer.models import Project
from freelancer.models import Freelancer
import django_filters

class JobsFilter(django_filters.FilterSet):
    
    class Meta:
        service = django_filters.BooleanFilter(field_name='category', lookup_expr='isnull')
        model = Project
        fields = ['service', 'name', ]


class FreelancersFilter(django_filters.FilterSet):
    class Meta:
        model = Freelancer
        fields = ['skills', 'title', ]