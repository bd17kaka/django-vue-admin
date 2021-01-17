from django.urls import path, include
from .views import UserViewSet, OrganizationViewSet, PermissionViewSet, RoleViewSet, PositionViewSet, TestView, DictTypeViewSet, DictViewSet, TaskViewSet, MeasurementViewSet, DatasetViewSet, SolutionViewSet, TasktypeViewSet, Download, task_type_measurementViewSet, task_dataset_measurementViewSet, solution_resultViewSet, TraceView, RepresentationView, ClassifierView, TrainingView, ResultView, RepResultView
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
router.register('solution_result', solution_resultViewSet, basename="solution_result")
urlpatterns = [
    path('', include(router.urls)),
    path('test/', TestView.as_view()),
    path('download/<filename>', Download),
    path('trace/', TraceView.as_view()),
    path('representation/', RepresentationView.as_view()),
    path('classifier/', ClassifierView.as_view()),
    path('training/', TrainingView.as_view()),
    path('result/', ResultView.as_view()),
    path('represult/', RepResultView.as_view())
]
