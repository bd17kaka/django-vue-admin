from django.urls import path, include
from .views import UserViewSet, OrganizationViewSet, PermissionViewSet, RoleViewSet, PositionViewSet, TestView, DictTypeViewSet, DictViewSet, TaskViewSet, MeasurementViewSet, DatasetViewSet, SolutionViewSet, TasktypeViewSet, Download, task_type_measurementViewSet, task_dataset_measurementViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('user', UserViewSet, basename="user")
router.register('organization', OrganizationViewSet, basename="organization")
router.register('permission', PermissionViewSet, basename="permission")
router.register('role', RoleViewSet, basename="role")
router.register('position', PositionViewSet, basename="position")
router.register('dicttype', DictTypeViewSet, basename="dicttype")
router.register('dict', DictViewSet, basename="dict")
router.register('task', TaskViewSet, basename="task")
router.register('measurement',MeasurementViewSet, basename="measurement")
router.register('dataset', DatasetViewSet, basename="dataset")
router.register('solution',SolutionViewSet,basename="solution")
router.register('tasktype', TasktypeViewSet, basename="tasktype")
router.register('task_type_measurement', task_type_measurementViewSet, basename="task_type_measurement")
router.register('task_dataset_measurement', task_dataset_measurementViewSet, basename="task_dataset_measurement")
urlpatterns = [
    path('', include(router.urls)),
    path('test/', TestView.as_view()),
    path('download/<filename>', Download)
]
